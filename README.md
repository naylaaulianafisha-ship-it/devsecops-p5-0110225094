# SecureTask — Pipeline DevSecOps (Praktikum 5)

## 1\. Nama Aplikasi \& Fungsi

**SecureTask** adalah aplikasi manajemen tugas (to-do list) berbasis command-line.
Pengguna dapat menambah, menampilkan, menyelesaikan, dan menghapus tugas, lengkap
dengan prioritas (`low/medium/high`), tenggat waktu, tag, serta ringkasan statistik
(total, selesai, tertunda, terlambat). Seluruh input divalidasi dan disanitasi.

## 2\. Bahasa \& Framework

* Python 3.12 (hanya standard library untuk aplikasi)
* `pytest` + `pytest-cov` untuk unit test dan coverage
* `Bandit` sebagai SAST tool

Struktur:

```
main.py                  # entry point
securetask/
  models.py              # dataclass Task \& enum Priority
  validators.py          # validasi \& sanitasi input
  storage.py             # penyimpanan JSON (atomik)
  service.py             # logika bisnis
  cli.py                 # antarmuka argparse
tests/                   # unit test
.github/workflows/devsecops.yml
```

## 3\. Cara Menjalankan

```bash
git clone https://github.com/naylaaulianafisha-ship-it/devsecops-p5-0110225094.git
cd devsecops-p5-0110225094
python -m venv .venv \&\& source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements-dev.txt

python main.py add "Kerjakan laporan P5" --priority high --due 2026-10-30 --tag kuliah
python main.py list
python main.py done 1
python main.py stats

pytest --cov=securetask          # menjalankan unit test
bandit -r securetask main.py     # menjalankan SAST secara lokal
```

## 4\. Overview Pipeline CI/CD

Workflow: `.github/workflows/devsecops.yml` (runner `ubuntu-latest`)

|Trigger|Keterangan|
|-|-|
|`push` ke `main`|pipeline berjalan otomatis|
|`pull\_request` ke `main`|pipeline berjalan sebelum merge|

|Job|Fungsi|Quality Gate|
|-|-|-|
|`build`|install dependency, jalankan unit test + coverage|gagal jika coverage < 80% atau ada test gagal|
|`sast-scan` (`needs: build`)|scan kode dengan **Bandit**, unggah laporan JSON sebagai artifact|gagal jika ada temuan severity **MEDIUM/HIGH**|

Jika `build` gagal, `sast-scan` tidak dijalankan.

