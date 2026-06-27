const BASE_URL = 'http://localhost:5000/api';

export async function registerPasien(payload) {
  const res = await fetch(`${BASE_URL}/pasien/daftar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return await res.json();
}
