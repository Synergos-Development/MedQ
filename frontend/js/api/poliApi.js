const BASE_URL = 'http://localhost:5000/api';

export async function fetchPoliList() {
  const r = await fetch(`${BASE_URL}/poli/list`);
  const j = await r.json();
  return j.data;
}

export async function fetchDokterByPoli(idPoli) {
    const r = await fetch(`${BASE_URL}/poli/${idPoli}/dokter`);
    const j = await r.json();
    return j.data;
}

export async function fetchAntrianAktif(idPoli) {
  const r = await fetch(`${BASE_URL}/antrian/aktif/${idPoli}`);
  return await r.json();
}