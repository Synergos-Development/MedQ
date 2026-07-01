# API Documentation — Hospital Queue System

Base URL: `http://localhost:5000/api`

Response format selalu JSON. Untuk error, format responsenya:
```json
{
  "status": "error",
  "message": "deskripsi error"
}
```

---

## 1. Pasien `/api/pasien`

### POST `/api/pasien/daftar`
Mendaftarkan pasien baru dan generate nomor RM.

**Request:**
```json
{
  "nama_lengkap": "Budi Santoso",
  "nik": "3201234567890001",
  "tanggal_lahir": "1990-05-20",
  "alamat": "Jl. Merdeka No. 1",
  "nomor_hp": "08123456789"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Pasien berhasil didaftarkan",
  "data": {
    "id_pasien": 1,
    "nomor_rm": "RM-2026-00001",
    "nama_lengkap": "Budi Santoso"
  }
}
```

---

### POST `/api/pasien/verifikasi`
Verifikasi pasien lama berdasarkan nomor RM.

**Request:**
```json
{ "nomor_rm": "RM-2026-00001" }
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "id_pasien": 1,
    "nomor_rm": "RM-2026-00001",
    "nama_lengkap": "Budi Santoso",
    "nomor_hp": "08123456789"
  }
}
```

---

### GET `/api/pasien/cari?nama=budi`
Cari pasien berdasarkan nama (untuk admin).

**Response:**
```json
{
  "status": "success",
  "data": [ { "id_pasien": 1, "nomor_rm": "RM-2026-00001", "nama_lengkap": "Budi Santoso" } ]
}
```

---

### GET `/api/pasien/<id_pasien>/riwayat`
Ambil riwayat kunjungan pasien.

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id_kunjungan": 1,
      "tanggal": "2026-05-31",
      "nama_poli": "Poli Umum",
      "nama_dokter": "dr. Budi Santoso",
      "diagnosa": "ISPA"
    }
  ]
}
```

---

## 2. Poli `/api/poli`

### GET `/api/poli/list`
Ambil semua poli yang aktif.

**Response:**
```json
{
  "status": "success",
  "data": [
    { "id_poli": 1, "kode_poli": "UMUM", "nama_poli": "Poli Umum" },
    { "id_poli": 2, "kode_poli": "GIGI", "nama_poli": "Poli Gigi" }
  ]
}
```

---

### GET `/api/poli/<id_poli>/dokter`
Ambil daftar dokter yang tersedia di poli tertentu.

**Response:**
```json
{
  "status": "success",
  "data": [
    { "id_dokter": 1, "nama_dokter": "dr. Budi Santoso", "is_available": true }
  ]
}
```

---

### GET `/api/poli/<id_poli>/antrian-aktif`
Ambil antrian yang sedang aktif di poli (untuk layar display).

**Response:**
```json
{
  "status": "success",
  "data": {
    "sedang_dilayani": "UMUM-003",
    "antrian_menunggu": ["UMUM-004", "UMUM-005", "UMUM-006"],
    "total_menunggu": 3
  }
}
```

---

## 3. Antrian `/api/antrian`

### POST `/api/antrian/ambil`
Pasien mengambil nomor antrian.

**Request:**
```json
{
  "id_pasien": 1,
  "id_poli": 2,
  "id_dokter": 3
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Nomor antrian berhasil diambil",
  "data": {
    "id_antrian": 10,
    "nomor_antrian": "GIGI-005",
    "nama_poli": "Poli Gigi",
    "nama_dokter": "drg. Ahmad Fauzi",
    "posisi": 3,
    "estimasi_menit": 30
  }
}
```

---

### GET `/api/antrian/status/<nomor_antrian>`
Cek status antrian pasien.

**Response:**
```json
{
  "status": "success",
  "data": {
    "nomor_antrian": "GIGI-005",
    "status": "Menunggu",
    "posisi": 2,
    "estimasi_menit": 20
  }
}
```

---

### POST `/api/antrian/panggil`
Admin/dokter memanggil nomor antrian berikutnya.

**Request:**
```json
{ "id_poli": 2, "id_dokter": 3 }
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "nomor_antrian": "GIGI-005",
    "nama_pasien": "Budi Santoso",
    "id_antrian": 10
  }
}
```

---

### POST `/api/antrian/batal`
Batalkan antrian pasien.

**Request:**
```json
{ "id_antrian": 10 }
```
**Response:**
```json
{
  "status": "success",
  "message": "Antrian GIGI-005 berhasil dibatalkan"
}
```

---

## 4. Kunjungan `/api/kunjungan`

### POST `/api/kunjungan/mulai`
Dokter memulai pemeriksaan (pasien masuk ruangan).

**Request:**
```json
{
  "id_antrian": 10,
  "keluhan": "Sakit gigi sebelah kiri"
}
```
**Response:**
```json
{
  "status": "success",
  "data": { "id_kunjungan": 5, "waktu_masuk": "2026-05-31 09:30:00" }
}
```

---

### POST `/api/kunjungan/selesai`
Dokter menyelesaikan pemeriksaan dan mengisi diagnosa.

**Request:**
```json
{
  "id_kunjungan": 5,
  "diagnosa": "Karies gigi molar kiri bawah",
  "catatan_dokter": "Perlu tindakan tambal gigi",
  "resep": [
    { "nama_obat": "Amoxicillin", "dosis": "500mg", "aturan_pakai": "3x1", "jumlah": 15 },
    { "nama_obat": "Paracetamol", "dosis": "500mg", "aturan_pakai": "3x1", "jumlah": 10 }
  ]
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Kunjungan selesai",
  "data": { "id_kunjungan": 5, "id_resep": 3 }
}
```

---

### GET `/api/kunjungan/<id_kunjungan>`
Ambil detail kunjungan beserta resep.

**Response:**
```json
{
  "status": "success",
  "data": {
    "id_kunjungan": 5,
    "nama_pasien": "Budi Santoso",
    "nama_dokter": "drg. Ahmad Fauzi",
    "keluhan": "Sakit gigi sebelah kiri",
    "diagnosa": "Karies gigi molar kiri bawah",
    "catatan_dokter": "Perlu tindakan tambal gigi",
    "resep": [
      { "nama_obat": "Amoxicillin", "dosis": "500mg", "aturan_pakai": "3x1", "jumlah": 15 }
    ]
  }
}
```