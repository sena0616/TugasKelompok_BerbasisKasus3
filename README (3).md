# Tugas 3 - Sistem Pakar Diagnosis Gangguan Internet

Tugas kelompok mata kuliah Inteligensi Buatan (Rule Based System), Program Studi Teknik Informatika, Institut Teknologi Sumatera.

## Anggota Kelompok

| Nama | NIM |
|---|---|
| [Sena Permatasari] | [124140018] |
| [Wulandari Lubis] | [124140066] |
| [Sere sri Rezeki Sinaga] | [124140150] |

Kelompok: [Rx]

## Deskripsi

Program ini adalah sistem pakar sederhana untuk mendiagnosis gangguan internet, ditulis dengan Python. Program memuat 8 aturan IF-THEN dan 3 fakta awal dari soal, lalu mengerjakan tiga bagian tugas:

- **(a) Forward chaining**: mencari semua kesimpulan dari fakta awal, ditampilkan sebagai tabel iterasi.
- **(b) Backward chaining**: membuktikan goal `Lapor ke Provider` dengan menelusuri mundur sampai ke fakta awal.
- **(c) Conflict resolution**: menjelaskan pemilihan aturan pada iterasi yang punya lebih dari satu aturan siap jalan.

Urutan conflict resolution: salience (prioritas), lalu spesifisitas (jumlah premis), lalu nomor aturan. Refractoriness berlaku, yaitu aturan yang sudah dijalankan tidak dijalankan lagi.

## Struktur Folder

```
TugasIntelegensiBuatan/
├── Diagnosis_internet.py
├── README.md
└── SS/
    ├── forward chaining.png
    ├── backward chaining.png
    └── conflict resolution.png
```

## Cara Menjalankan

Butuh Python 3, tanpa library tambahan.

```
python Diagnosis_internet.py
```

Di Linux atau macOS, gunakan `python3`.

## Fakta Awal

- Semua Situs Tidak Bisa Dibuka
- Perangkat Lain Juga Offline
- Tagihan Sudah Dibayar

## Hasil

### (a) Forward chaining

Aturan dijalankan berurutan R5, R4, R1, R7, lalu berhenti pada iterasi 5. Fakta baru yang dihasilkan: Gangguan Provider, Lapor ke Provider, Cek Router, dan Gunakan Tethering Sementara.

![Forward chaining](SS/forward%20chaining.png)

### (b) Backward chaining

Goal `Lapor ke Provider` terbukti lewat R4. Sub-goal Gangguan Provider dicoba lewat R2 (gagal), R3 (gagal), lalu R5 (berhasil).

![Backward chaining](SS/backward%20chaining.png)

### (c) Conflict resolution

Konflik terjadi pada iterasi 1, 2, dan 3. Pada iterasi 3, R1 dan R7 sama-sama bersalience Rendah dengan 1 premis, sehingga R1 dipilih karena nomor aturannya lebih kecil.

![Conflict resolution](SS/conflict%20resolution.png)

## Asumsi

Pada backward chaining, fakta yang tidak ada di fakta awal dan tidak bisa disimpulkan oleh aturan mana pun dianggap tidak terbukti (closed-world assumption).
