import { 
  renderTicketData, 
  renderSidebarSummary,
  initProgressBar, 
  renderTicketDate, 
  updateTicketClock 
} from '../ui/ticketDetails.js';

// 1. Ambil data matang dari sessionStorage (Mendukung deteksi pasien_baru maupun pasien_lama)
const tiket = JSON.parse(sessionStorage.getItem("tiket") || "{}");
const pasien = JSON.parse(
  sessionStorage.getItem('pasien_baru') ||
  sessionStorage.getItem('pasien_lama') ||
  '{}'
);

// 2. Render data utama ke komponen tiket utama
renderTicketData(tiket);

// 3. Render data ke komponen sidebar summary terbaru
renderSidebarSummary(pasien, tiket);

// 4. Jalankan animasi pengisian garis progress bar
initProgressBar(tiket.posisi);

// 5. Tampilkan hari dan tanggal pendaftaran aktif
renderTicketDate("tanggal");

// 6. Jalankan mesin realtime digital clock
updateTicketClock("clock");
setInterval(() => updateTicketClock("clock"), 1000);