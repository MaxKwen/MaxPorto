# MaxPorto

Proyek portofolio pribadi bilingual yang menggunakan Django dan pola
Model-View-Template (MVT). Data pengalaman, proyek, keahlian, dan pencapaian
disimpan dalam model Django dan dirender melalui template HTML.

> Nama: Maximus Quinn Hertada
>
> NPM: 2506613552
>
> Kelas: PBP B

## Fitur

- Homepage bilingual: English di `/` dan Indonesia di `/id/`, dengan data
  Experience dinamis dari database.
- Halaman daftar bilingual untuk Projects, Skills, dan Achievements:
  - `/projects/` dan `/id/projects/`
  - `/skills/` dan `/id/skills/`
  - `/achievements/` dan `/id/achievements/`
- Data portofolio dirender menggunakan Django Template Language, lengkap dengan
  pesan kondisi kosong ketika belum ada data.
- Navigasi antarkomponen menggunakan named URL Django dan menu hamburger
  responsif pada layar kecil.
- Tema gelap sebagai default, dengan toggle light mode berbasis CSS.
- Katalog skill dengan filter kategori berbasis CSS, tanpa JavaScript.
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
python manage.py migrate
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` untuk halaman English atau
`http://127.0.0.1:8000/id/` untuk halaman Indonesia.

Pemeriksaan dan test dapat dijalankan dengan:

```powershell
python manage.py check
python manage.py test
```

## Struktur proyek

```text
MaxPorto/
├── main/
│   ├── migrations/         # Migrasi skema dan seed data portofolio
│   ├── models.py           # Model Project, Experience, Skill, dan Achievement
│   ├── tests.py            # Test model, view, template, route, dan seed data
│   ├── urls.py             # Named URL halaman daftar bilingual
│   └── views.py            # Query model dan context halaman daftar
├── portofolio/
│   ├── settings.py         # Konfigurasi proyek Django
│   ├── urls.py             # URL proyek dan homepage bilingual
│   └── views.py            # View dan context homepage
├── static/
│   ├── css/style.css       # Tema, layout, responsivitas, dan komponen UI
│   └── img/                # Foto dan ikon lokal
├── templates/
│   ├── index.html          # Homepage dan Experience dinamis
│   ├── projects.html       # Daftar Project
│   ├── skills.html         # Daftar Skill
│   └── achievements.html   # Daftar Achievement
├── docs/                   # Catatan arsitektur dan progres pengembangan
├── requirements.txt
└── manage.py
```

Konten antarmuka bilingual disimpan dalam kamus copy pada view. Data portofolio
diambil dari model melalui QuerySet, dimasukkan ke context oleh view, kemudian
dirender oleh template menggunakan perulangan dan kondisi Django Template
Language.

## Pertanyaan reflektif

### Tugas 1

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

### Tugas 2

### 1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.

Alur yang saya lihat ketika ada pengguna yang membuka halaman portofolio adalah contohnya ketika membuka /projects/, alurnya:
Browser -> urls.pt proyek -> urls.py aplikasi -> view.py -> model/database -> template -> browser
Penjelasannya:
a. Ketika pengguna membuka http://127.0.0.1:8000/projects/. Browser akan mengirim request GET ke server Django.
b. urls.py proyek akan menerima dan mengarahkan request tersebut. Django pertama kali akan memeriksa `portofolio/urls.py`, yaitu konfigurasi URL utama proyek. Di proyek terdapat : `path("", include("main.urls"))`. include akan memberi tahu Django bahwa URL yang belum ditangani di tingkat proyek perlu dicocokkan dengan pola URL dalam `main/urls.py`.
c. Selanjutnya urls.py aplikasi akan memilih view. Di `main/urls.py` ada route: `path("projects/", show_projects, name="show_projects")`. Karena URL yang diminta adalah /projects/, Django menjalankan view show_projects.
d. Lalu view akan mengambil daya melalui model. View show_projects pada main/views.py menjalankan `Project.objects.all()`. Project adalah model yang didefinisikan dalam `main/models.py`. Melalui Django ORM, perintah tersebut diterjemahkan menjadi query ke database untuk mengambil seluruh data proyek. Setelah itu, view menyusun context yang akan menjadi penghubung antara data Python di view dan template HTML.
e. Selanjutnya view memanggil `render(request, "projects.html", context)`. Django membuka templates/projects.html dan memberikan context tersebut. Template menampilkan setiap proyek menggunakan perulangan: `{% for project in project_list %}`. Atribut model juga dapat diakses dengan ekspresi seperti: `{{ project.title }}, {{ project.description }}, {{ project.category }}`. Jika tidak ada data, bagian `{% empty %}` akan menampilkan pesan belum ada proyek.
f. Setelah template selesai dirender, Django menghasilkan dokumen HTML lengkap. HTML tersebut dikirim sebagai HTTP response, kemudian browser membacanya dan menampilkan halaman kepada pengguna.

### 2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Karena model memisahkan data dari tampilan. Template seharusnya bertanggung jawab terhadap presentasi, bukan menjadi tempat penyimpanan data. Jika judul, deskripsi, kategori, dan tautan proyek ditulis langsung di dalam `projects.html`, setiap perubahan data mengharuskan pengembang mencari dan mengedit HTML. Hal ini menimbulkan beberapa masalah:
- Data dan struktur tampilan bercampur.
- Template menjadi panjang dan sulit dibaca.
- Data yang sama sulit digunakan kembali pada halaman lain.
- Perubahan desain berisiko ikut mengubah atau menghapus data.
- Fitur seperti pencarian, pengurutan, filter, dan halaman detail lebih sulit dikembangkan.
Jika data disimpan pada model, template cukup melakukan perulangan terhadap project_list. Menambahkan proyek baru berarti menambahkan record ke database tanpa mengubah struktur template.Contohnya, satu template ini:

{% for project in project_list %}
  {{ project.title }}
{% endfor %}

dapat menampilkan satu, sepuluh, maupun seratus proyek tanpa perlu menyalin struktur HTML secara manual. Dengan begitu, pemeliharaan website juga lebih efektif dan efisien karena struktur kode lebih terorganisasi, perubahan data tidak memerlukan perubahan template, dan kesalahan saat memperbarui data lebih mudah dicegah. Intinya, model menangani “apa datanya”, sedangkan template menangani “bagaimana data tersebut ditampilkan”. Pemisahan tanggung jawab ini membuat aplikasi lebih mudah dirawat dan dikembangkan.

### 3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

Makemigrations dan migrate sama-sama berhubungan dengan perubahan struktur database, tetapi memiliki fungsi yang berbeda. Makemigrations memeriksa perubahan yang dibuat pada `models.py`, kemudian membuat file migrasi berisi instruksi perubahan skema database. Perintah ini belum mengubah database. Ia hanya menghasilkan “rencana perubahan”, misalnya file `main/migrations/0010_project_created_at.py`. Sedangkan migrate membaca file-file migrasi yang belum diterapkan, lalu benar-benar menjalankan perubahan tersebut pada database. Contoh perubahan model:
Misalnya model Project awalnya belum memiliki tanggal pembuatan, lalu ditambahkan field berikut:

class Project(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

Setelah mengubah models.py, jalankan makemigrations dan migrate. Django akan mengeksekusi migrasi tersebut sehingga tabel Project di database benar-benar memiliki kolom created_at. Jika hanya menjalankan makemigrations, file rencana perubahan sudah ada, tetapi database belum berubah. Jika mencoba menggunakan field created_at sebelum menjalankan migrate, aplikasi dapat mengalami error karena kolom tersebut belum tersedia di database.

## Progres pengembangan

| Periode | Fokus | Hasil |
| --- | --- | --- |
| 26 Agustus – 2 September 2026 | Fondasi Django | Inisialisasi proyek, tutorial, pembangunan ulang struktur, dan konfigurasi middleware. |
| 4 September 2026 | Konten inti | Fondasi portofolio, halaman bilingual, dan struktur semantik HTML. |
| 5 September 2026 | Desain dan aksesibilitas | Polishing visual, tema light/dark, ikon sosial, dan focus state keyboard. |
| 6 September 2026 | Pengayaan portofolio | Skill catalog, footer, tautan eksternal, konten pengalaman, proyek, dan pencapaian. |
| 7 September 2026 | Responsivitas dan dokumentasi | Menu mobile, prioritas foto hero pada mobile, serta dokumentasi proyek. |
| 11–14 September 2026 | Implementasi MVT | Model, migrasi, seed data, halaman daftar bilingual, navigasi, dan test untuk data portofolio dinamis. |

## AI disclosure

### Cara AI digunakan

Saya menggunakan Hermes Agent sebagai asisten pengembangan lokal. AI membantu
menjelaskan pola MVT, menyarankan struktur model dan route, menyiapkan perubahan
kode dan test, serta menjalankan pemeriksaan teknis seperti python manage.py
check dan python manage.py test. Pengembangan dilakukan secara bertahap:
setiap bagian diimplementasikan dan diuji secara terpisah, kemudian hasilnya
saya tinjau sebelum di-commit. Keputusan fitur, pemilihan konten, aset gambar,
dan perubahan akhir tetap berada pada saya sebagai pemilik proyek.

### Chat history

Riwayat percakapan yang tersimpan selama pengembangan Tugas 2 tersedia di
folder [`docs/ai-chat-history/`](docs/ai-chat-history/). Riwayat diekspor
langsung dari sesi Hermes Agent dengan redaksi otomatis untuk informasi
sensitif.

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
