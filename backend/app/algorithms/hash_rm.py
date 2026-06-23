"""
hash_rm.py

Generator Nomor Rekam Medis (RM) unik.

Menggunakan hashing berbasis:
- timestamp nanosecond
- counter yang terus bertambah

Format:
    RM-YYYY-XXXXX

Contoh:
    RM-2026-00042
"""

import hashlib
import re
import time
from datetime import datetime

# Counter global dalam memori
_counter = 0


def generate_nomor_rm() -> str:
    """
    Generate nomor rekam medis unik.

    Mekanisme:
    1. Ambil timestamp nanosecond + counter.
    2. Hash menggunakan MD5.
    3. Ambil 8 karakter pertama hasil hash.
    4. Konversi ke integer.
    5. Batasi menjadi 5 digit.
    6. Format ke RM-YYYY-XXXXX.

    Returns:
        str: Nomor RM.
    """
    global _counter
    _counter += 1

    tahun = datetime.now().year

    bahan = f"{time.time_ns()}-{_counter}"

    hash_hex = hashlib.md5(
        bahan.encode()
    ).hexdigest()[:8]

    hash_int = int(hash_hex, 16)

    nomor = (hash_int % 99999) + 1

    return f"RM-{tahun}-{str(nomor).zfill(5)}"


def validasi_format_rm(nomor_rm: str) -> bool:
    """
    Validasi format nomor rekam medis.

    Format yang valid:
        RM-YYYY-XXXXX

    Args:
        nomor_rm: Nomor RM yang akan diperiksa.

    Returns:
        bool
    """
    pola = r"^RM-\d{4}-\d{5}$"
    return bool(re.match(pola, nomor_rm))