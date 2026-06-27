const BASE_URL = "http://localhost:5000/api";

export async function fetchPoliList() {
  const response = await fetch(`${BASE_URL}/poli/list`);
  const result = await response.json();
  return result.data;
}

export async function fetchAntrianAktif(idPoli) {
  const response = await fetch(`${BASE_URL}/antrian/aktif/${idPoli}`);
  return await response.json();
}