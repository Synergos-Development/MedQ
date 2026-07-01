import { fallbackPoli } from '../config/poliConfig.js';
import { fetchPoliList, fetchDokterByPoli } from '../api/poliApi.js';
import { registerPasien } from '../api/pasien.api.js';
import { postAmbilAntrian, fetchAntrianAktif } from '../api/antiranApi.js';
import { showToast } from '../ui/notification.js';
import { renderPoliGrid } from '../ui/poliSelection.js';
import { showDokterSkeleton, renderDokterList } from '../ui/dokterSelection.js';
import { updateSidebarSummary } from '../ui/sidebarSummary.js';

// State Management
const params = new URLSearchParams(location.search);
const mode = params.get('mode') || 'baru';

let poliData = [];
let dokterData = [];
let selectedPoli = null;
let selectedDokter = null;

const btnAmbil = document.getElementById('btnAmbil');
const searchInput = document.getElementById('searchInput');

// Load awal data Poli beserta jumlah antreannya
async function initPoliPage() {
  try {
    const json = await fetchPoliList();
    poliData = json;

    // Menembak antrean aktif secara pararel (Promise.all)
    await Promise.all(poliData.map(async p => {
      try {
        const j = await fetchAntrianAktif(p.id_poli);
        if (j.status === 'success') {
          p.antrian = j.data.total_menunggu ?? j.data.antrian_menunggu?.length ?? 0;
        }
      } catch { 
        p.antrian = '-'; 
      }
    }));
  } catch {
    poliData = fallbackPoli;
  }
  executeRenderPoli();
}

// Pembungkus render poli agar sinkron dengan input pencarian
function executeRenderPoli() {
  const query = searchInput ? searchInput.value.toLowerCase() : '';
  const filtered = poliData.filter(p => p.nama_poli.toLowerCase().includes(query));
  renderPoliGrid(filtered, selectedPoli, 'poliGrid', 'emptyState');
}

// Handler Aksi Pilih Poli
async function handleSelectPoli(id) {
  selectedPoli = poliData.find(p => p.id_poli === id);
  selectedDokter = null;

  if (btnAmbil) btnAmbil.disabled = true;

  // Render ulang grid untuk memperbarui tanda centang biru aktif
  executeRenderPoli();
  updateSidebarSummary(selectedPoli, selectedDokter);

  const divider = document.getElementById('dokterDivider');
  if (divider) divider.style.display = 'block';

  showDokterSkeleton('dokterList', 'dokterSection');

  try {
    dokterData = await fetchDokterByPoli(id);
  } catch {
    dokterData = [
      { id_dokter: 1, nama_dokter: 'dr. Budi Santoso', spesialisasi: 'Dokter Umum' },
      { id_dokter: 2, nama_dokter: 'dr. Siti Rahayu',  spesialisasi: 'Dokter Umum' },
    ];
  }
  renderDokterList(dokterData, 'dokterList');
}

// Handler Aksi Pilih Dokter
function handleSelectDokter(id) {
  selectedDokter = dokterData.find(d => d.id_dokter === id);
  
  // Update class active khusus dokter-item
  document.querySelectorAll('.dokter-item').forEach(d => d.classList.remove('selected'));
  const activeItem = document.getElementById('di-' + id);
  if (activeItem) activeItem.classList.add('selected');

  if (btnAmbil) btnAmbil.disabled = false;
  updateSidebarSummary(selectedPoli, selectedDokter);
}

// Handler Ambil Antrian (Submit)
async function handleAmbilAntrian() {
  if (!selectedPoli || !selectedDokter) return;
  if (btnAmbil) btnAmbil.classList.add('loading');

  const storageKey = mode === 'baru' ? 'pasien_baru' : 'pasien_lama';
  const pasien = JSON.parse(sessionStorage.getItem(storageKey) || '{}');

  try {
    let id_pasien = pasien.id_pasien;

    if (mode === 'baru' && !id_pasien) {
      const regJson = await registerPasien(pasien);
      if (regJson.status !== "success") {
        showToast(regJson.message, "error");
        btnAmbil.classList.remove("loading");
        return;
      }
      id_pasien = regJson.data.id_pasien;
    }

    const json = await postAmbilAntrian({
      id_pasien,
      id_poli: selectedPoli.id_poli,
      id_dokter: selectedDokter.id_dokter,
    });

    if (json.status === 'success') {
      sessionStorage.setItem('tiket', JSON.stringify(json.data));
      window.location.href = 'tiket.html';
    } else {
      showToast(json.message, 'error');
      if (btnAmbil) btnAmbil.classList.remove('loading');
    }
  } catch {
    // Demo mode Fallback
    sessionStorage.setItem('tiket', JSON.stringify({
      nomor_antrian: `${selectedPoli.kode_poli}-001`,
      nama_poli: selectedPoli.nama_poli,
      nama_dokter: selectedDokter.nama_dokter,
      posisi: 3,
      estimasi_menit: 30,
    }));
    window.location.href = 'tiket.html';
  }
}

// --- EVENT LISTENERS REGISTRATION ---

// Real-time search filter
if (searchInput) {
  searchInput.addEventListener('input', executeRenderPoli);
}

// Click Delegation - Kartu Poli
const poliGrid = document.getElementById('poliGrid');
if (poliGrid) {
  poliGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.poli-card');
    if (card) handleSelectPoli(Number(card.dataset.id));
  });
}

// Click Delegation - Baris Dokter
const dokterList = document.getElementById('dokterList');
if (dokterList) {
  dokterList.addEventListener('click', (e) => {
    const item = e.target.closest('.dokter-item');
    if (item) handleSelectDokter(Number(item.dataset.id));
  });
}

// Submit Button Action
if (btnAmbil) {
  btnAmbil.addEventListener('click', handleAmbilAntrian);
}

// Jalankan inisialisasi halaman saat dokumen dimuat
initPoliPage();