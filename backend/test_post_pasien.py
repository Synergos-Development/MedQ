import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

url = 'http://127.0.0.1:5000/api/pasien/daftar'
payload = {
    'nama_lengkap': 'E2E Test',
    'nik': '9999999999999999',
    'tanggal_lahir': '1990-01-01',
    'jenis_kelamin': 'L',
    'nomor_hp': '08123456789',
    'alamat': 'Jl Test'
}

data = json.dumps(payload).encode('utf-8')
req = Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
        print('STATUS', resp.status)
        print('BODY', body)
except HTTPError as e:
    print('HTTPERROR', e.code)
    try:
        print('BODY', e.read().decode('utf-8'))
    except:
        pass
except URLError as e:
    print('URLERROR', e.reason)
except Exception as e:
    print('ERR', e)
