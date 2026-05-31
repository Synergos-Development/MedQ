# Hospital Queue System

Sistem antrian rumah sakit berbasis web yang mengimplementasikan algoritma AVL Tree, Queue FIFO, dan Linked List.

> Tugas Kuliah — Teknik Informatika  
> Tech Stack: Python (Flask) + HTML/CSS/JS  

---

## Tim Pengembang

| Nama | Role | Tanggung Jawab |
|------|------|----------------|
| [Rasya] | Backend 1 | Implementasi algoritma (AVL Tree, Queue, Linked List) |
| [Damar] | Backend 2 | API endpoint & services |
| [Daffa] | Backend 3 | Database, models, konfigurasi |
| [Galang] | Frontend 1 | Halaman pasien (pendaftaran, verifikasi, tiket) |
| [Ihsan] | Frontend 2 | Halaman display antrian & admin panel |

---

## Struktur Proyek

```
hospital-queue-system/
├── backend/
│   ├── app/
│   │   ├── algorithms/     # implementasi algoritma murni
│   │   ├── models/         # struktur tabel database
│   │   ├── routes/         # endpoint REST API
│   │   └── services/       # logika bisnis
│   ├── database/
│   │   ├── schema.sql      # CREATE TABLE
│   │   └── seed.py         # data awal poli & dokter
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── pages/              # halaman pasien
│   ├── display/            # layar antrian & admin
│   ├── js/                 # logika & fetch API
│   └── css/                # styling
├── tests/
├── API_DOCS.md
└── README.md
```

---

## Cara Setup Project

### Prasyarat
- Python 3.10+
- Git

### 1. Clone repository

```bash
git clone https://github.com/Synergos-Development/MedQ.git
```

### 2. Setup backend

```bash
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Install dependensi
pip install -r requirements.txt
```

### 3. Konfigurasi environment

```bash
# Salin file contoh
cp ../.env.example .env

# Edit file .env sesuai konfigurasi lokal kamu
```

Isi `.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=ganti-dengan-random-string
DATABASE_URL=sqlite:///antrian.db
```

### 4. Setup database

```bash
# Masih di folder backend/
python database/seed.py
```

### 5. Jalankan backend

```bash
python run.py
```

Backend berjalan di: `http://localhost:5000`

### 6. Jalankan frontend

Buka file HTML langsung di browser, atau gunakan Live Server di VS Code:

```
frontend/pages/index.html
```

---

## Git Workflow

### Branch yang digunakan

```
main                      # kode stabil, hanya merge dari develop
develop                   # branch integrasi semua fitur
feature/avl-tree          # backend 1
feature/antrian-api       # backend 2
feature/models-db         # backend 3
feature/halaman-pasien    # frontend 1
feature/display-admin     # frontend 2
```

### Alur kerja harian

```bash
# 1. Selalu update dari develop sebelum mulai kerja
git checkout develop
git pull origin develop

# 2. Pindah ke branch kamu
git checkout feature/nama-fitur

# 3. Merge perubahan terbaru dari develop
git merge develop

# 4. Kerjakan fitur, lalu commit
git add .
git commit -m "feat: deskripsi singkat perubahan"

# 5. Push ke remote
git push origin feature/nama-fitur

# 6. Buat Pull Request ke develop di GitHub
```

### Format pesan commit

```
feat: tambah implementasi AVL Tree insert
fix: perbaiki generate nomor antrian duplikat
docs: update API_DOCS endpoint antrian
test: tambah unit test queue FIFO
refactor: pisahkan logika service dari routes
```

---

## Dokumentasi API

Lihat [API_DOCS.md](./API_DOCS.md) untuk daftar lengkap endpoint, format request, dan response.

---

## Menjalankan Tests

```bash
cd backend
python -m pytest ../tests/ -v
```

---

## Algoritma yang Diimplementasikan

| Algoritma | File | Kegunaan |
|-----------|------|----------|
| AVL Tree | `algorithms/avl_tree.py` | Simpan & cari data pasien by nomor RM — O(log n) |
| Queue FIFO | `algorithms/queue_poli.py` | Antrian per poli, generate nomor seperti `GIGI-005` |
| Linked List | `algorithms/linked_list.py` | Riwayat kunjungan pasien secara berurutan |
| Hashing | `algorithms/hash_rm.py` | Generate nomor Rekam Medis unik |