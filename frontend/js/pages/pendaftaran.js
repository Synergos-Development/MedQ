import { showToast } from '../ui/notification.js';
import { 
  validateForm, 
  scrollToFirstInvalid, 
  initNikMasking, 
  initClearInvalidState, 
  getFormData, 
  setButtonLoading 
} from '../ui/pendaftaranForm.js';

function handleSubmit() {
  if (!validateForm()) {
    showToast('Lengkapi data yang wajib diisi', 'error');
    scrollToFirstInvalid(); // Efek scroll otomatis ke field eror pertama
    return;
  }

  setButtonLoading('btnLanjut');

  const data = getFormData();
  sessionStorage.setItem('pasien_baru', JSON.stringify(data));

  setTimeout(() => {
    window.location.href = 'pilih_poli.html?mode=baru';
  }, 800);
}

// --- INITIALIZATION ---

// 1. Jalankan fitur pengetikan hanya angka untuk NIK
initNikMasking();

// 2. Jalankan fitur hapus status eror merah saat user mengetik/mengubah opsi
initClearInvalidState();

// 3. Pasang event listener klik pada tombol lanjut (gantikan onclick inline)
const btnLanjut = document.getElementById('btnLanjut');
if (btnLanjut) {
  btnLanjut.addEventListener('click', handleSubmit);
}