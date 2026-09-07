# MaxPorto

Proyek portofolio ini menggunakan Django untuk merender satu halaman portofolio
bilingual dan HTML/CSS murni untuk antarmuka.

> Nama: Maximus Quinn Hertada
>
> NPM: 2506613552
>
> Kelas: PBP B

## Fitur

- Halaman bilingual: English di `/` dan Indonesia di `/id/`.
- Navigasi anchor untuk setiap section utama dan menu hamburger responsif pada
  layar kecil.
- Tema gelap sebagai default, dengan toggle light mode berbasis CSS.
- Katalog skill dengan filter kategori berbasis CSS, tanpa JavaScript.
- Konten pengalaman, proyek, pencapaian, dan tautan sosial yang responsif.
- Tautan GitHub, LinkedIn, Gmail Compose, repository proyek, dan publikasi
  dibuka pada tab baru.
- Dukungan keyboard focus dan `prefers-reduced-motion` untuk aksesibilitas
  dasar.

## Teknologi

- Python dan Django
- HTML5 semantik
- CSS3 murni

## Menjalankan proyek secara lokal

Prasyarat: Python 3 dan `pip`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` untuk halaman English atau
`http://127.0.0.1:8000/id/` untuk halaman Indonesia.

Pemeriksaan dasar Django dapat dijalankan dengan:

```powershell
python manage.py check
```

## Struktur proyek

```text
MaxPorto/
├── portofolio/
│   ├── urls.py             # URL English dan Indonesia
│   └── views.py            # Konten bilingual dan view halaman utama
├── static/
│   ├── css/style.css       # Tema, layout, responsivitas, dan komponen UI
│   └── img/                # Foto dan ikon lokal
├── templates/index.html    # Struktur halaman portofolio
├── docs/                   # Catatan arsitektur dan progres pengembangan
├── requirements.txt
└── manage.py
```

Konten teks dipusatkan pada kamus `COPY` di `portofolio/views.py`. Kedua
halaman memakai template yang sama, sehingga struktur dan fitur tetap
konsisten tanpa menduplikasi HTML.

## Tugas 1

### 1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `section`, `article`, atau `aside`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Ya, website ini menggunakan elemen semantik HTML5 seperti `header`, `nav`,
`main`, `section`, `article`, dan `footer`. `header` digunakan dengan diisi oleh
identitas situs dan navigasi utama. `main` membungkus isi pokok halaman, sedangkan setiap
bagian portofolio—Experience, Skills, Projects, Achievements, dan Contact—
dibuat sebagai `section` yang memiliki anchor sendiri. Setiap entri pengalaman,
proyek, pencapaian, serta skill card menggunakan `article` karena merupakan
unit konten yang tetap bermakna apabila dibaca terpisah. Informasi hak cipta
diletakkan pada `footer`.

Elemen-elemen tersebut membantu static web karena struktur dokumen menjadi
jelas. Navigasi anchor dapat langsung mengarah ke section yang tepat, pembaca 
memperoleh landmark yang bermakna, dan CSS dapat menargetkan komponen 
berdasarkan perannya. Elemen `aside` tidak digunakan karena tidak ada konten 
pendukung yang terpisah dari narasi utama portofolio.

### 2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Tantangan utama adalah menjaga hero section, navigasi, dan katalog skill tetap
nyaman pada layar sempit. Di desktop, hero memakai dua kolom agar biodata dan
foto dapat tampil seimbang. Pada suatu breakpoint, grid berubah menjadi satu
kolom dan foto diprioritaskan tampil sebelum teks agar pembuka halaman tetap
kuat secara visual. Navigasi desktop yang panjang juga berubah menjadi menu
hamburger berbasis checkbox CSS supaya tautan tidak saling bertabrakan.

Saya mengatur prioritas berdasarkan urutan informasi yang dibutuhkan
pengunjung: identitas, cara menghubungi, navigasi, kemudian detail pengalaman
dan proyek. Pengujian dilakukan dengan mengubah lebar viewport dan memeriksa 
apakah teks tetap terbaca, target klik masih cukup besar, serta grid turun 
menjadi satu kolom ketika ruang horizontal tidak lagi memadai.

### 3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Walaupun Django merender halaman, pengalaman pengguna saat ini tetap bersifat
static: konten portofolio disimpan di kode, perubahan data harus dilakukan
secara manual lalu di-deploy ulang, dan preferensi light/dark mode kembali ke
default saat halaman dimuat ulang. Selain itu, tombol email hanya mengarahkan pengguna
ke Gmail Compose karena website belum memiliki form kontak dan mekanisme penerimaan
pesan sendiri.

Mungkin untuk berikutnya, yang paling bermanfaat adalah membuat model Django dan
dashboard admin untuk Experience, Project, dan Achievement. Dengan itu,
portofolio dapat diperbarui tanpa mengubah template. Fitur lanjutan lain yang
ingin dipersiapkan adalah form kontak yang aman dengan validasi server-side,
penyimpanan preferensi tema, serta halaman detail proyek.

## Progres pengembangan

| Periode | Fokus | Hasil |
| --- | --- | --- |
| 26 Agustus – 2 September 2026 | Fondasi Django | Inisialisasi proyek, tutorial, pembangunan ulang struktur, dan konfigurasi middleware. |
| 4 September 2026 | Konten inti | Fondasi portofolio, halaman bilingual, dan struktur semantik HTML. |
| 5 September 2026 | Desain dan aksesibilitas | Polishing visual, tema light/dark, ikon sosial, dan focus state keyboard. |
| 6 September 2026 | Pengayaan portofolio | Skill catalog, footer, tautan eksternal, konten pengalaman, proyek, dan pencapaian. |
| 7 September 2026 | Responsivitas dan dokumentasi | Menu mobile, prioritas foto hero pada mobile, serta dokumentasi proyek. |

## AI disclosure

### Cara AI digunakan

Saya menggunakan Codex sebagai asisten pengembangan lokal. AI membantu
menjelaskan opsi desain, menyarankan struktur HTML/CSS, menyiapkan perubahan
kode, serta membantu membuat pemeriksaan teknis seperti `python manage.py
check`. Keputusan fitur, pemilihan konten, aset gambar, dan perubahan akhir
tetap berada pada saya sebagai pemilik proyek.

### Keterbatasan AI

AI tidak dapat menjadi sumber kebenaran untuk informasi pribadi, pengalaman,
atau pencapaian. AI dapat menghasilkan teks yang terdengar meyakinkan tetapi
tidak sesuai fakta, salah menerjemahkan konteks, atau menyarankan solusi yang
tidak sesuai batasan tugas. AI juga tidak dapat menggantikan penilaian visual
di browser; ukuran aset, jarak antarelemen, dan perilaku responsif perlu
ditinjau secara langsung oleh pengembang.

Pada proyek ini, batasan tersebut ditangani dengan memverifikasi isi yang
diambil dari resume, memilih sendiri informasi yang layak dipublikasikan, dan
tidak memasukkan nomor telepon maupun alamat rumah ke dalam website. Saya juga
meninjau hasil perubahan secara manual, termasuk ukuran dan alignment ikon,
navigasi mobile, urutan konten, terjemahan, serta ukuran skill card ketika
filter berubah. Implementasi sengaja tidak memakai JavaScript karena merupakan
batasan tugas; solusi interaktif yang digunakan harus dapat dijelaskan dan
ditinjau melalui HTML/CSS.

### Pekerjaan manual

- Menentukan identitas visual: nuansa biru gelap, electric blue, dan gaya
  minimal-profesional.
- Memilih dan memverifikasi pengalaman, proyek, pencapaian, serta tautan yang
  ditampilkan.
- Menambahkan aset foto dan logo lokal.
- Menetapkan konten bilingual dan meninjau hasil terjemahannya.
- Menjalankan proyek serta menguji perubahan antarmuka pada ukuran layar yang
  berbeda.
- Meninjau setiap perubahan sebelum di-commit dan menjaga data pribadi tetap
  di luar repository publik.
