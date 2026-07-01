export function validateForm() {
  let ok = true;
  const rules = [
    { fieldId: 'f-nama', inputId: 'nama',          check: v => v.trim().length > 2 },
    { fieldId: 'f-nik',  inputId: 'nik',           check: v => /^\d{16}$/.test(v) },
    { fieldId: 'f-tgl',  inputId: 'tgl_lahir',     check: v => !!v },
    { fieldId: 'f-jk',   inputId: 'jenis_kelamin', check: v => !!v },
    { fieldId: 'f-hp',   inputId: 'nomor_hp',      check: v => v.trim().length > 7 },
  ];

  rules.forEach(r => {
    const inputEl = document.getElementById(r.inputId);
    const fieldEl = document.getElementById(r.fieldId);
    if (!inputEl || !fieldEl) return;

    const val = inputEl.value;
    if (!r.check(val)) {
      fieldEl.classList.add('invalid');
      ok = false;
    } else {
      fieldEl.classList.remove('invalid');
    }
  });

  return ok;
}

export function scrollToFirstInvalid() {
  const firstInvalid = document.querySelector('.field.invalid');
  if (firstInvalid) {
    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

export function initNikMasking() {
  const nikInput = document.getElementById('nik');
  if (nikInput) {
    nikInput.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '');
    });
  }
}

export function initClearInvalidState() {
  const fields = ['nama', 'nik', 'tgl_lahir', 'jenis_kelamin', 'nomor_hp'];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;

    const removeInvalid = () => {
      const field = el.closest('.field');
      if (field) field.classList.remove('invalid');
    };

    el.addEventListener('input', removeInvalid);
    el.addEventListener('change', removeInvalid); // Untuk tipe date dan select
  });
}

export function getFormData() {
  return {
    nama_lengkap:  document.getElementById('nama')?.value.trim() || '',
    nik:           document.getElementById('nik')?.value.trim() || '',
    tanggal_lahir: document.getElementById('tgl_lahir')?.value || '',
    jenis_kelamin: document.getElementById('jenis_kelamin')?.value || '',
    nomor_hp:      document.getElementById('nomor_hp')?.value.trim() || '',
    alamat:        document.getElementById('alamat')?.value.trim() || '',
  };
}

export function setButtonLoading(buttonId) {
  const btn = document.getElementById(buttonId);
  if (btn) btn.classList.add('loading');
}