const BASE_URL = "http://localhost:5000/api";

export async function postAmbilAntrian(payload) {
  const res = await fetch(`${BASE_URL}/antrian/ambil`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return await res.json();
}

// TAMBAHKAN FUNGSI BARU INI:
export async function fetchAntrianAktif(idPoli) {
  const res = await fetch(`${BASE_URL}/antrian/aktif/${idPoli}`);
  return await res.json();
}