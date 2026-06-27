import { emojis } from "../config/poliConfig.js";

export function renderTicketData(tiket) {
  const kode = tiket.nomor_antrian
    ? tiket.nomor_antrian.split("-")[0]
    : "";

  const elNomor = document.getElementById("nomorAntrian");
  const elPoli = document.getElementById("poliName");
  const elDokter = document.getElementById("dokterName");
  const elNomorRM = document.getElementById("nomorRM");
  const elEstimasi = document.getElementById("estimasi");
  const elPosisi = document.getElementById("posisi");
  const elPosisiLabel = document.getElementById("posisiLabel");

  if (elNomor) {
    elNomor.textContent = tiket.nomor_antrian || "—";
  }

  if (elPoli) {
    elPoli.textContent = `${emojis[kode] || "🏥"} ${tiket.nama_poli || "—"}`;
  }

  if (elDokter) {
    elDokter.textContent = tiket.nama_dokter || "—";
  }

  if (elNomorRM) {
    elNomorRM.textContent = tiket.nomor_rm || "—";
  }

  if (elEstimasi) {
    elEstimasi.textContent = tiket.estimasi_menit
      ? `${tiket.estimasi_menit} menit`
      : "—";
  }

  if (elPosisi) {
    elPosisi.textContent = tiket.posisi
      ? `Ke-${tiket.posisi}`
      : "—";
  }

  if (elPosisiLabel) {
    elPosisiLabel.textContent = tiket.posisi
      ? `${tiket.posisi} / ${tiket.posisi + 2}`
      : "— / —";
  }
}

// Sidebar
export function renderSidebarSummary(pasien, tiket) {
  const sNama = document.getElementById("sNama");
  const sPoli = document.getElementById("sPoli");
  const sDokter = document.getElementById("sDokter");
  const sNomor = document.getElementById("sNomor");
  const sNomorRM = document.getElementById("sNomorRM");
  const sEstimasi = document.getElementById("sEstimasi");

  if (sNama) {
    sNama.textContent = pasien.nama_lengkap || tiket.nama_pasien || "—";
  }

  if (sPoli) {
    sPoli.textContent = tiket.nama_poli || "—";
  }

  if (sDokter) {
    sDokter.textContent = tiket.nama_dokter || "—";
  }

  if (sNomor) {
    sNomor.textContent = tiket.nomor_antrian || "—";
  }

  if (sNomorRM) {
    sNomorRM.textContent = tiket.nomor_rm || pasien.nomor_rm || "—";
  }

  if (sEstimasi) {
    sEstimasi.textContent = tiket.estimasi_menit
      ? `${tiket.estimasi_menit} menit`
      : "—";
  }
}

export function initProgressBar(posisi) {
  if (!posisi) return;

  const fillEl = document.getElementById("posisiFill");
  if (!fillEl) return;

  const pct = Math.max(10, 100 - (posisi - 1) * 20);

  setTimeout(() => {
    fillEl.style.width = `${pct}%`;
  }, 400);
}

export function renderTicketDate(targetId) {
  const el = document.getElementById(targetId);
  if (!el) return;

  const now = new Date();

  const opts = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };

  el.textContent = now.toLocaleDateString("id-ID", opts);
}

export function updateTicketClock(targetId) {
  const el = document.getElementById(targetId);
  if (!el) return;

  el.textContent = new Date().toLocaleTimeString("id-ID", {
    hour: "2-digit",
    minute: "2-digit",
  });
}