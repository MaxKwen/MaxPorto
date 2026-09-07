# Arsitektur dan Keputusan Teknis

## Gambaran

MaxPorto memakai arsitektur server-rendered yang sengaja sederhana. Satu view melayani satu template halaman, sedangkan Python hanya menyediakan data teks berdasarkan bahasa yang diminta. Struktur ini sesuai untuk situs portofolio karena tidak ada data pengguna atau transaksi yang perlu disimpan melalui antarmuka.

```text
Browser
  └── URL `/` atau `/id/`
        └── `portofolio.urls`
              └── `landing_page()`
                    ├── memilih salinan teks dari `COPY`
                    └── merender `templates/index.html`
                          └── memuat CSS dan aset gambar lokal
```

## Pemisahan tanggung jawab

| Lokasi | Tanggung jawab |
| --- | --- |
| `portofolio/urls.py` | Memetakan URL Inggris dan Indonesia ke view yang sama. |
| `portofolio/views.py` | Menyediakan kamus konten bilingual dan merender template. |
| `templates/index.html` | Menyusun konten dan makna dokumen dengan elemen HTML semantik. |
| `static/css/style.css` | Menangani variabel tema, layout, komponen visual, state CSS, dan breakpoint. |
| `static/img/` | Menyimpan aset visual lokal yang dipanggil melalui `{% static %}`. |

Pemisahan ini membuat perubahan visual tidak perlu mengubah Python, sementara perubahan teks bilingual tidak perlu menggandakan template.

## Keputusan implementasi utama

### Konten bilingual pada view

Alih-alih membuat dua template yang hampir sama, `COPY` menyimpan salinan teks per bahasa dan view meneruskannya sebagai context. Keuntungannya adalah struktur HTML dan fitur selalu identik di kedua bahasa. Konsekuensinya, setiap penambahan konten harus diperbarui pada kedua entri bahasa agar tidak menghasilkan placeholder atau campuran bahasa.

### Interaksi tanpa JavaScript

Toggle tema menggunakan checkbox, sementara filter keterampilan menggunakan radio button dan selector `:has()`. Pendekatan ini mengurangi skrip yang dikirim ke browser dan tetap berfungsi untuk kontrol standar. Karena `:has()` memerlukan browser modern, katalog tetap menampilkan konten normal apabila state filter tidak didukung; filtering adalah peningkatan pengalaman, bukan satu-satunya cara melihat informasi.

### Responsivitas mobile

Layout hero memakai grid dua kolom. Pada breakpoint `760px`, CSS mengubahnya menjadi satu kolom dan memberi `order: -1` pada foto agar foto muncul sebelum teks. Navigasi memakai checkbox dan label sebagai tombol hamburger di mobile; nav desktop tidak dibungkus elemen yang dapat menyembunyikannya.

Pendekatan checkbox dipilih setelah pendekatan `details` terbukti menyembunyikan navigasi pada desktop ketika elemen belum `open`. Hal ini menunjukkan pentingnya memeriksa perilaku bawaan elemen HTML pada semua breakpoint.

### Aksesibilitas dan motion

Struktur memakai `header`, `nav`, `main`, `section`, dan `footer`. Kontrol yang tidak mempunyai teks visual diberi label, ikon dekoratif memakai `alt` kosong, dan focus outline disediakan untuk pengguna keyboard. Media query `prefers-reduced-motion` mempersingkat transisi untuk pengguna yang memilih gerakan minimum.

## Verifikasi

Pemeriksaan konfigurasi Django dijalankan dengan:

```powershell
python manage.py check
```

Uji manual sebaiknya mencakup kedua URL bahasa, setiap tautan anchor, toggle tema, filter keterampilan, fokus keyboard, serta breakpoint desktop dan mobile.
