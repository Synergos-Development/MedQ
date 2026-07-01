/* ════════════════════════════════════════════
   1. GLOBAL CONFIGURATION & APP STATE
   ════════════════════════════════════════════ */
const API_BASE_URL = "http://localhost:5000/api";

const emojis = {
  UMUM: "🩺",
  GIGI: "🦷",
  JANTUNG: "❤️",
  ANAK: "👶",
  MATA: "👁️",
};

let poliList = [];
let activePoli = null;
let antrianData = [];
let calledHistory = [];
let batalTarget = null;
let refreshTimer = null;

/* ════════════════════════════════════════════
   2. APP INIT LIFECYCLE MANAGEMENT
   ════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setDate();
  loadPoli();
  setupEventListeners();

  // Menerapkan fitur background polling refresh otomatis setiap 10 detik
  refreshTimer = setInterval(() => {
    if (activePoli) loadAntrian();
  }, 10000);
});

/* ════════════════════════════════════════════
   3. BASE LOGIC & APPLICATION UTILITIES
   ════════════════════════════════════════════ */
function setDate() {
  const d = new Date();
  const opts = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  document.getElementById("heroDate").textContent = d.toLocaleDateString("id-ID", opts);
}

function initTheme() {
  const saved = localStorage.getItem("medq-theme");
  const preferDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  if (saved === "dark" || (!saved && preferDark)) {
    document.documentElement.setAttribute("data-theme", "dark");
    document.getElementById("iconSun").style.display = "none";
    document.getElementById("iconMoon").style.display = "";
  }
}

function toggleDark() {
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark";
  html.setAttribute("data-theme", isDark ? "light" : "dark");
  document.getElementById("iconSun").style.display = isDark ? "" : "none";
  document.getElementById("iconMoon").style.display = isDark ? "none" : "";
  localStorage.setItem("medq-theme", isDark ? "light" : "dark");
}

function showToast(msg, type = "") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = `toast show ${type}`;
  setTimeout(() => {
    t.className = "toast";
  }, 2800);
}

/* ════════════════════════════════════════════
   4. API CLIENT METHOD SERVICES
   ════════════════════════════════════════════ */
async function loadPoli() {
  try {
    const res = await fetch(`${API_BASE_URL}/poli/list`);
    const json = await res.json();
    poliList = json.data;
  } catch {
    // Mode demo cadangan otomatis apabila koneksi REST API backend terputus
    poliList = [
      { id_poli: 1, kode_poli: "UMUM", nama_poli: "Poli Umum" },
      { id_poli: 2, kode_poli: "GIGI", nama_poli: "Poli Gigi" },
      { id_poli: 3, kode_poli: "JANTUNG", nama_poli: "Poli Jantung" },
      { id_poli: 4, kode_poli: "ANAK", nama_poli: "Poli Anak" },
      { id_poli: 5, kode_poli: "MATA", nama_poli: "Poli Mata" },
    ];
  }
  renderPoliPills();
}

async function loadAntrian() {
  if (!activePoli) return;
  try {
    const res = await fetch(`${API_BASE_URL}/antrian/aktif/${activePoli}`);
    const json = await res.json();
    if (json.status === "success") {
      antrianData = json.data.antrian.map((item, i) => ({
        id_antrian: item.id_antrian,
        nomor: item.nomor_antrian,
        posisi: i + 1,
        status: item.status,
        nama_pasien: item.nama_pasien || "—",
        nomor_rm: item.nomor_rm || "—",
        nama_dokter: item.nama_dokter || "—",
        nama_poli: item.nama_poli || "—",
      }));
      updateStats(json.data);
      renderQueue(antrianData);
      updateNextNomor(antrianData.filter(a => a.status === "Menunggu"));
    }
  } catch {
    // Demo Mock Fallback Data
    antrianData = [
      { id_antrian: 101, nomor: "UMUM-004", posisi: 1, status: "Menunggu", nama_pasien: "Budi Santoso", nomor_rm: "RM-0912", nama_dokter: "dr. Andi" },
      { id_antrian: 102, nomor: "UMUM-005", posisi: 2, status: "Menunggu", nama_pasien: "Siti Rahayu", nomor_rm: "RM-0834", nama_dokter: "dr. Andi" },
      { id_antrian: 103, nomor: "UMUM-006", posisi: 3, status: "Menunggu", nama_pasien: "Ahmad Fauzi", nomor_rm: "RM-0711", nama_dokter: "dr. Andi" },
      { id_antrian: 104, nomor: "UMUM-003", posisi: 0, status: "Dipanggil", nama_pasien: "Dewi Kusuma", nomor_rm: "RM-0442", nama_dokter: "dr. Andi" },
      { id_antrian: 105, nomor: "UMUM-001", posisi: 0, status: "Selesai", nama_pasien: "Hendra W.", nomor_rm: "RM-0112", nama_dokter: "dr. Andi" },
    ];
    
    const menunggu = antrianData.filter(a => a.status === "Menunggu").length;
    const dilayani = antrianData.filter(a => ["Dipanggil", "Diperiksa"].includes(a.status)).length;
    const selesai = antrianData.filter(a => a.status === "Selesai").length;
    
    document.getElementById("statMenunggu").textContent = menunggu;
    document.getElementById("statDilayani").textContent = dilayani;
    document.getElementById("statSelesai").textContent = selesai;
    
    renderQueue(antrianData);
    updateNextNomor(antrianData.filter(a => a.status === "Menunggu"));
  }
}

async function panggilBerikutnya() {
  if (!activePoli) return;
  const btn = document.getElementById("callBtn");
  btn.classList.add("loading");
  try {
    const res = await fetch(`${API_BASE_URL}/antrian/panggil`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_poli: activePoli }),
    });
    const json = await res.json();
    if (json.status === "success") {
      const d = json.data;
      addCalledHistory(d.nomor_antrian, d.nama_pasien);
      showToast(`✅ ${d.nomor_antrian} — ${d.nama_pasien} dipanggil`, "ok");
      await loadAntrian();
    } else {
      showToast(json.message, "error");
    }
  } catch {
    const menunggu = antrianData.filter(a => a.status === "Menunggu");
    if (menunggu.length > 0) {
      const next = menunggu[0];
      next.status = "Dipanggil";
      addCalledHistory(next.nomor, next.nama_pasien);
      showToast(`✅ ${next.nomor} dipanggil (Demo Mode)`, "ok");
      await loadAntrian();
    } else {
      showToast("Tidak ada antrian menunggu", "error");
    }
  } finally {
    btn.classList.remove("loading");
  }
}

async function mulaiPeriksa(idAntrian) {
  try {
     const res = await fetch(`${API_BASE_URL}/antrian/diperiksa`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_antrian: idAntrian }),
    });
    const json = await res.json();
    showToast(json.status === "success" ? "Pasien mulai diperiksa" : json.message, json.status === "success" ? "ok" : "error");
    await loadAntrian();
  } catch {
    const target = antrianData.find(a => a.id_antrian === idAntrian);
    if (target) target.status = "Diperiksa";
    showToast("Pasien mulai diperiksa (Demo Mode)", "ok");
    await loadAntrian();
  }
}

async function selesaikan(idAntrian) {
  try {
    const res = await fetch(`${API_BASE_URL}/antrian/selesai`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_antrian: idAntrian }),
    });
    const json = await res.json();
    showToast(json.status === "success" ? "Antrian selesai diproses" : json.message, json.status === "success" ? "ok" : "error");
    await loadAntrian();
  } catch {
    const target = antrianData.find(a => a.id_antrian === idAntrian);
    if (target) target.status = "Selesai";
    showToast("Antrian selesai (Demo Mode)", "ok");
    await loadAntrian();
  }
}

async function konfirmasiBatal() {
  if (!batalTarget) return;
  const btn = document.getElementById("batalConfirm");
  btn.classList.add("loading");
  try {
    const item = antrianData.find(a => a.id_antrian === batalTarget);
    if (!item?.id_antrian) {
      showToast("Antrian dibatalkan", "ok");
      closeBatalModal();
      return;
    }
    const res = await fetch(`${API_BASE_URL}/antrian/batal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_antrian: item.id_antrian }),
    });
    const json = await res.json();
    showToast(json.status === "success" ? `Antrian ${item.nomor} dibatalkan` : json.message, json.status === "success" ? "ok" : "error");
  } catch {
    showToast("Gagal membatalkan antrian. Coba lagi nanti.", "error");
  } finally {
    btn.classList.remove("loading");
    closeBatalModal();
    await loadAntrian();
  }
}

/* ════════════════════════════════════════════
   5. INTERFASE DOM VIEW RENDERING ACTIONS
   ════════════════════════════════════════════ */
function renderPoliPills() {
  const container = document.getElementById("poliPills");
  if (!poliList || poliList.length === 0) return;
  container.innerHTML = poliList
    .map(p => `
      <div class="poli-pill ${activePoli === p.id_poli ? 'active' : ''}" data-id="${p.id_poli}">
        ${emojis[p.kode_poli] || "🏥"} ${p.nama_poli}
      </div>
    `).join("");
}

function selectPoli(id) {
  activePoli = parseInt(id);
  const poli = poliList.find(p => p.id_poli === activePoli);
  if (poli) {
    document.getElementById("callingPoliName").textContent = `${emojis[poli.kode_poli] || "🏥"} ${poli.nama_poli}`;
    renderPoliPills();
    loadAntrian();
  }
}

function updateStats(data) {
  document.getElementById("statMenunggu").textContent = data.total_menunggu ?? 0;
  document.getElementById("statDilayani").textContent = (data.total_dipanggil ?? 0) + (data.total_diperiksa ?? 0);
  document.getElementById("statSelesai").textContent = data.total_selesai ?? 0;
}

function updateNextNomor(menunggu) {
  const btn = document.getElementById("callBtn");
  if (menunggu.length > 0) {
    document.getElementById("nextNomor").textContent = menunggu[0].nomor;
    document.getElementById("nextPasien").innerHTML = `<span style="color:var(--text-2)">${menunggu[0].nama_pasien !== "—" ? menunggu[0].nama_pasien : ""}</span>`;
    btn.disabled = false;
  } else {
    document.getElementById("nextNomor").textContent = "—";
    document.getElementById("nextPasien").innerHTML = `<span class="npc-empty">Semua antrian dipanggil</span>`;
    btn.disabled = true;
  }
}

function renderQueue(data) {
  const container = document.getElementById("qTbody");
  const countEl = document.getElementById("queueCount");
  
  if (!data || data.length === 0) {
    container.innerHTML = `
      <div class="q-empty">
        <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" /></svg>
        <div class="q-empty-text">Belum ada data antrian aktif</div>
      </div>`;
    countEl.textContent = "0 antrian";
    return;
  }

  container.innerHTML = data
    .map(a => {
      let rank = a.posisi;
      let rankCls = "";
      if (a.status !== "Menunggu") {
        rank = "—";
        rankCls = "dash";
      }

      let actionBlock = "";
      switch (a.status) {
        case "Menunggu":
          actionBlock = `<button class="q-action-btn row-call-btn" data-id="${a.id_antrian}">Panggil</button>`;
          break;
        case "Dipanggil":
          actionBlock = `<button class="q-action-btn row-start-btn" data-id="${a.id_antrian}">Mulai Periksa</button>`;
          break;
        case "Diperiksa":
          actionBlock = `<button class="q-action-btn row-done-btn" data-id="${a.id_antrian}">Selesai</button>`;
          break;
        case "Selesai":
          actionBlock = `<span class="done-label">✔ Selesai</span>`;
          break;
        case "Batal":
          actionBlock = `<span class="cancel-label">✖ Batal</span>`;
          break;
      }

      const canBatal = ["Menunggu", "Dipanggil"].includes(a.status);
      const statusClass = `s-${a.status.toLowerCase()}`;

      return `
        <div class="q-item">
          <div class="q-rank ${rankCls}">${rank}</div>
          <div class="q-info">
            <div class="q-nomor">${a.nomor}</div>
            <div class="q-name">${a.nama_pasien}</div>
            <div class="q-rm">RM: ${a.nomor_rm}</div>
            <div class="q-dokter">Dokter: ${a.nama_dokter}</div>
          </div>
          <span class="q-status-pill ${statusClass}">${a.status}</span>
          <div class="q-action">
            ${actionBlock}
            ${canBatal ? `<button class="batal-btn row-cancel-btn" data-id="${a.id_antrian}"><svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>` : ""}
          </div>
        </div>
      `;
    }).join("");

  const totalMenunggu = data.filter(a => a.status === "Menunggu").length;
  countEl.textContent = `${data.length} antrian · ${totalMenunggu} menunggu`;
}

function addCalledHistory(nomor, nama) {
  const now = new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });
  const poli = poliList.find(p => p.id_poli === activePoli);
  const poliName = poli ? poli.nama_poli : "";

  calledHistory.unshift({ nomor, nama, time: now, poli: poliName });
  if (calledHistory.length > 8) calledHistory.pop();

  document.getElementById("calledList").innerHTML = `
    <div class="tl-list">
      ${calledHistory.map(c => `
        <div class="tl-item">
          <div class="tl-dot-wrap"><div class="tl-dot"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.79 19.79 0 0 1 11.61 19a19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 3.12 4.18 2 2 0 0 1 5.08 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.1l-1.27 1.27a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7a2 2 0 0 1 1.72 2z"/></svg></div></div>
          <div class="tl-content">
            <div class="tl-nomor">${c.nomor}</div>
            <div class="tl-name">${c.nama}</div>
            <div class="tl-poli">${c.poli}</div>
          </div>
          <div class="tl-time">${c.time}</div>
        </div>
      `).join("")}
    </div>
  `;
}

/* ════════════════════════════════════════════
   6. INTERAKSI DIALOG WINDOWS SYSTEM MODAL
   ════════════════════════════════════════════ */
function showBatalModal(idAntrian) {
  batalTarget = parseInt(idAntrian);
  const item = antrianData.find(a => a.id_antrian === batalTarget);
  if (item) {
    document.getElementById("batalDesc").textContent = `Antrian ${item.nomor} atas nama ${item.nama_pasien} akan dibatalkan permanen dan tidak dapat dikembalikan.`;
  }
  document.getElementById("batalModal").classList.add("show");
}

function closeBatalModal() {
  document.getElementById("batalModal").classList.remove("show");
  batalTarget = null;
}

/* ════════════════════════════════════════════
   7. PRODUCER LISENER EVENT UTAMA DEKLARATIF
   ════════════════════════════════════════════ */
function setupEventListeners() {
  // Pengubah Mode Gelap
  document.getElementById("darkToggle").addEventListener("click", toggleDark);

  // Delegasi Event untuk Pemilihan Poliklinik Pill
  document.getElementById("poliPills").addEventListener("click", (e) => {
    const pill = e.target.closest(".poli-pill");
    if (pill) selectPoli(pill.dataset.id);
  });

  // Pemanggilan Pasien Melalui Tombol Panel Utama
  document.getElementById("callBtn").addEventListener("click", panggilBerikutnya);

  // Tombol Segarkan Data Manual
  document.getElementById("refreshQueueBtn").addEventListener("click", () => {
    if (activePoli) {
      loadAntrian();
      showToast("Data antrian diperbarui", "ok");
    } else {
      showToast("Pilih poli terlebih dahulu", "error");
    }
  });

  // Penutupan Jendela Modal Pembatalan Antrian
  document.getElementById("closeBatalBtn").addEventListener("click", closeBatalModal);
  document.getElementById("batalConfirm").addEventListener("click", konfirmasiBatal);
  document.getElementById("batalModal").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) closeBatalModal();
  });

  // 💡 DELEGASI EVENT MUTAKHIR: Mengendalikan semua baris tombol aksi antrian
  document.getElementById("qTbody").addEventListener("click", (e) => {
    const target = e.target;
    const btnAction = target.closest("button");
    if (!btnAction) return;

    const idAntrian = parseInt(btnAction.dataset.id);
    if (!idAntrian) return;

    if (btnAction.classList.contains("row-call-btn")) {
      panggilBerikutnya();
    } else if (btnAction.classList.contains("row-start-btn")) {
      mulaiPeriksa(idAntrian);
    } else if (btnAction.classList.contains("row-done-btn")) {
      selesaikan(idAntrian);
    } else if (btnAction.classList.contains("row-cancel-btn")) {
      showBatalModal(idAntrian);
    }
  });
}