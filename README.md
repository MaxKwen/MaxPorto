# MaxPorto

Proyek portofolio pribadi bilingual yang menggunakan Django dan pola
Model-View-Template (MVT). Data pengalaman, proyek, keahlian, dan pencapaian
disimpan dalam model Django. Halaman Experience, Projects, dan Achievements
memuat dan mengubah data melalui REST API berbasis Django REST Framework (DRF)
di `/api/v1/`, sedangkan Skills dirender melalui template HTML.

> Nama: Maximus Quinn Hertada
>
> NPM: 2506613552
>
> Kelas: PBP B

## Fitur

- Homepage bilingual: English di `/` dan Indonesia di `/id/`, dengan hero yang
  berisi identitas, peran, foto, dan tautan sosial.
- Halaman daftar bilingual untuk Experience, Projects, Skills, dan Achievements:
  - `/experience/` dan `/id/experience/`
  - `/projects/` dan `/id/projects/`
  - `/skills/` dan `/id/skills/`
  - `/achievements/` dan `/id/achievements/`
- Pengelolaan data Experience, Project, dan Achievement melalui `ModelForm`,
  lengkap dengan halaman create dan update serta modal konfirmasi delete.
- Autentikasi pengguna melalui register, login, dan logout, termasuk session
  Django, cookie `last_login`, serta status login pada navbar.
- Authorization konsisten untuk Experience, Project, dan Achievement berdasarkan
  empat peran: guest, user biasa, Editor, dan superuser.
- Pengguna yang sudah login dapat memberi atau membatalkan star pada Experience,
  Project, dan Achievement. Setiap relasi star disimpan melalui `ManyToManyField`.
- REST API DRF untuk Experience, Project, dan Achievement di `/api/v1/`
  (daftar, detail, tambah, ubah, hapus, dan star). Detail endpoint ada di bagian
  [REST API](#rest-api-django-rest-framework).
- Halaman Experience, Projects, dan Achievements menampilkan, mencari, menambah,
  memberi star, dan menghapus data lewat API tersebut tanpa reload. Experience
  dan Achievement juga punya modal edit yang mengirim `PATCH`, dipakai oleh
  Editor dan pemilik portofolio.
- Endpoint JSON manual dari Tugas 5 (`/api/experiences/`, `/api/projects/`,
  `/api/achievements/`) masih tersedia untuk kompatibilitas, tetapi halaman
  tidak lagi memakainya.
- Pencarian Experience berdasarkan posisi atau organisasi, dan Achievement
  berdasarkan judul atau hasil, mencakup field English/Indonesia. Keduanya
  menggunakan debounce 300 ms; Projects menyediakan pencarian judul.
- Loading, empty, dan error state serta tombol retry tersedia pada daftar AJAX.
- Superuser dapat menambahkan Experience, Project, dan Achievement melalui modal
  dengan CSRF, validasi serializer, toast sukses/gagal, dan refresh daftar tanpa
  reload. Error validasi 400 dan penolakan 403 dari API ditampilkan lewat toast;
  Experience dan Achievement juga menampilkan error per field di modal.
- Input teks Experience dan Achievement dibersihkan dengan `strip_tags` (di
  `ModelForm` dan di `validate_<field>` serializer), lalu dirender menggunakan
  `textContent`. Field teks wajib yang menjadi kosong
  setelah sanitasi ditolak. Validasi mencakup rentang tahun 1900–2100,
  urutan tahun Experience, serta urutan tampilan Achievement tidak negatif.
- Respons API hanya memuat field yang ditulis eksplisit di serializer. Informasi
  star (`star_count`, `is_starred`, `starred_by_names`) bersifat read-only dan
  hanya berisi username; email dan password hash tidak pernah dikirim.
- Template memakai `base.html` sebagai root template bersama agar struktur
  navigasi, metadata, theme toggle, message, dan footer tidak diduplikasi.
- Django Template Language menyediakan kerangka halaman, kontrol sesuai role,
  form, dan template kartu; JavaScript mengisi kartu daftar AJAX dengan data API.
- Navigasi antarkomponen menggunakan named URL Django dan menu hamburger
  responsif pada layar kecil.
- Tema gelap sebagai default, dengan toggle light mode berbasis CSS.
- Katalog skill dengan filter kategori berbasis CSS, tanpa JavaScript.
- Tautan GitHub, LinkedIn, Gmail Compose, repository proyek, dan publikasi
  dibuka pada tab baru.
- Dukungan keyboard focus dan `prefers-reduced-motion` untuk aksesibilitas
  dasar.

## Teknologi

- Python dan Django 5.2
- Django REST Framework 3.18
- HTML5 semantik
- CSS3 murni
- JavaScript vanilla, Fetch API, dan DOM API

## Menjalankan proyek secara lokal

Prasyarat: Python 3.10 atau lebih baru dan `pip`. Sejak Tutorial 7, proyek
memakai Django 5.2 dan Django REST Framework 3.18 (`djangorestframework` di
`requirements.txt`).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` untuk halaman English atau
`http://127.0.0.1:8000/id/` untuk halaman Indonesia.

Jika environment sudah ada sebelum Tutorial 7, cukup jalankan ulang
`python -m pip install -r requirements.txt` untuk memperbarui Django dan
memasang DRF. Pada virtual environment buatan `uv` yang tidak memiliki `pip`,
gunakan `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`.

Pemeriksaan dan test dapat dijalankan dengan:

```powershell
python manage.py check
python manage.py test main
python manage.py test main.tests_api main.tests_api_portfolio --verbosity 2
```

Gunakan `test main`, bukan `test` tanpa nama app, agar skrip Selenium
`test_e2e.py` di root proyek tidak ikut dijalankan sebagai unit test. Perintah
ketiga hanya menjalankan test API Tutorial 7 dan Tugas 6.

## Konfigurasi peran Editor

Setelah migrasi dan pembuatan superuser, buka `/admin/`, lalu lakukan langkah
berikut:

1. Masuk menggunakan akun superuser.
2. Buka **Authentication and Authorization > Groups**.
3. Buat group bernama `Editor` dengan penulisan yang sama persis.
4. Tambahkan akun yang akan menjadi editor ke group tersebut melalui halaman
   **Users**.

Hak akses aplikasi ditentukan oleh keanggotaan group `Editor` dan status
`is_superuser`. Permission Django pada group dapat tetap disesuaikan melalui
admin, tetapi pemeriksaan akses utama pada view mengikuti matriks berikut.

| Peran | Membaca daftar | Star/unstar | Create | Update | Delete |
| --- | ---: | ---: | ---: | ---: | ---: |
| Guest | Ya | Login | Login | Login | Login |
| User biasa | Ya | Ya | 403 | 403 | 403 |
| Editor | Ya | Ya | 403 | Ya | 403 |
| Superuser | Ya | Ya | Ya | Ya | Ya |

Halaman daftar tetap dapat dibaca tanpa login. Aksi yang membutuhkan autentikasi
mengarahkan guest ke halaman login. User terautentikasi yang tidak mempunyai
hak menerima respons HTTP 403. Endpoint star/unstar dan delete hanya menerima
request POST serta dilindungi CSRF. Khusus endpoint tambah AJAX, guest, user
biasa, dan Editor menerima JSON HTTP 403, bukan redirect login. Endpoint ini
tidak memakai `csrf_exempt`; POST tanpa token CSRF yang valid tetap ditolak.

Matriks yang sama berlaku di REST API Experience dan Achievement melalui
`IsPortfolioOwnerOrEditorOrReadOnly`. Bedanya, API tidak mengarahkan guest ke
halaman login: setiap penolakan, termasuk dari guest, dijawab dengan HTTP 403
berformat JSON. API Projects mengikuti contoh Tutorial 7
(`IsPortfolioOwnerOrReadOnly`), sehingga hanya superuser yang dapat menulis.

### Menggunakan daftar dan modal AJAX

1. Buka `/experience/` atau `/achievements/`; JavaScript memuat daftar melalui API.
   Versi Indonesia tersedia dengan awalan `/id/`.
2. Ketik kata kunci pada kolom pencarian. Request dikirim setelah jeda 300 ms
   sejak input terakhir, atau langsung saat form pencarian disubmit.
3. Jika pemuatan gagal, gunakan **Try again / Coba lagi**. Pencarian yang tidak
   cocok menampilkan pesan tersendiri, bukan error jaringan.
4. Login sebagai superuser, lalu tekan **Add Experience / Add Achievement** untuk
   membuka modal. Isi form dan submit; error server muncul di bawah field dan
   pada toast. Saat berhasil, modal ditutup, form direset, dan daftar dimuat ulang
   dengan kata kunci yang masih aktif, tanpa reload halaman.
5. Login sebagai Editor atau superuser, lalu tekan **Edit** pada kartu. Modal yang
   sama terbuka dalam mode edit dengan data terisi, lalu mengirim `PATCH`.
6. Superuser dapat menekan **Delete**; konfirmasi di modal mengirim `DELETE`.
   Pengguna yang sudah login dapat menekan **Star** untuk memberi atau
   membatalkan star. Guest melihat tautan login sebagai pengganti tombol star.

Setiap request yang mengubah data mengirim header `X-CSRFToken` dari cookie
`csrftoken`. Halaman edit Tugas 3 (`/experience/<id>/edit/` dan
`/achievements/<id>/edit/`) masih dapat dipakai. Halaman daftar membutuhkan
JavaScript.

## REST API (Django REST Framework)

API dibangun dengan function-based view `@api_view` di `main/api_views.py`,
`SessionAuthentication`, serializer di `main/serializers.py`, dan permission
class di `main/permissions.py`. Semua endpoint berada di bawah `/api/v1/` dan
didaftarkan di `main/api_urls.py` dengan namespace `api`.

| Method | Endpoint | Tindakan | Siapa yang boleh |
| --- | --- | --- | --- |
| GET | `/api/v1/experiences/?q=...` | Daftar dan pencarian posisi/organisasi (EN/ID) | Semua pengunjung |
| POST | `/api/v1/experiences/` | Tambah Experience | Superuser |
| GET | `/api/v1/experiences/<id>/` | Detail | Semua pengunjung |
| PUT / PATCH | `/api/v1/experiences/<id>/` | Ubah seluruh / sebagian field | Editor dan superuser |
| DELETE | `/api/v1/experiences/<id>/` | Hapus | Superuser |
| POST | `/api/v1/experiences/<id>/star/` | Beri/batalkan star | Pengguna login |
| GET, POST | `/api/v1/achievements/?q=...` | Daftar dan pencarian judul/hasil (EN/ID); tambah | Sama seperti Experience |
| GET, PUT, PATCH, DELETE | `/api/v1/achievements/<id>/` | Detail, ubah, hapus | Sama seperti Experience |
| POST | `/api/v1/achievements/<id>/star/` | Beri/batalkan star | Pengguna login |
| GET, POST | `/api/v1/projects/?title=...` | Daftar, pencarian, tambah (Tutorial 7) | Baca: semua; tambah: superuser |
| GET, PUT, PATCH, DELETE | `/api/v1/projects/<id>/` | Detail, ubah, hapus (Tutorial 7) | Baca: semua; tulis: superuser |
| POST | `/api/v1/projects/<id>/star/` | Beri/batalkan star (Tutorial 7) | Pengguna login |

Status yang dikembalikan: `200` untuk baca dan ubah, `201` saat data dibuat,
`204` setelah data dihapus (body kosong), `400` beserta error per field untuk
input tidak valid, `403` untuk tindakan yang tidak diizinkan atau token CSRF
yang hilang, `404` untuk ID yang tidak ada, dan `405` untuk method yang tidak
didukung. Browsable API dapat dibuka langsung di browser pada alamat yang sama;
tambahkan `?format=json` untuk melihat JSON mentah.

Validasi berada di serializer: `validate_<field>` membersihkan setiap field teks
dengan `strip_tags` dan menolak field wajib yang menjadi kosong, batas tahun
1900–2100 mengikuti `ModelForm`, dan `ExperienceSerializer.validate()` menolak
tahun selesai yang lebih awal dari tahun mulai, termasuk saat `PATCH` hanya
mengirim salah satunya.

## Struktur proyek

Panduan alur URL → view → template/CSS → AJAX ada di [ARCHITECTURE.md](ARCHITECTURE.md).

```text
MaxPorto/
├── main/
│   ├── migrations/         # Skema dan seed data
│   ├── copy.py             # Label/pesan bilingual fitur portofolio
│   ├── permissions.py      # Helper role Editor dan permission class DRF
│   ├── forms.py            # ModelForm dan validasi
│   ├── models.py           # Project, Experience, Skill, Achievement
│   ├── serializers.py      # ModelSerializer + field star read-only
│   ├── api_views.py        # View @api_view: daftar, detail, star
│   ├── api_urls.py         # Route /api/v1/ (namespace api)
│   ├── tests.py            # Test model, auth, akses, star, dan view
│   ├── test_ajax.py        # Test kontrak AJAX Tugas 5
│   ├── test_structure.py   # Test template, stylesheet, dan modul view
│   ├── tests_api.py        # Test API Projects (Tutorial 7)
│   ├── tests_api_portfolio.py  # Test API Experience & Achievement (Tugas 6)
│   ├── urls.py             # Named URL halaman dan API JSON lama
│   └── views/
│       ├── __init__.py     # Ekspor fungsi untuk main.views
│       ├── auth.py
│       ├── projects.py
│       ├── experiences.py
│       ├── achievements.py
│       └── skills.py
├── portofolio/             # Konfigurasi, root URL, dan view homepage
├── static/
│   ├── css/                # base, components, forms, home, dan CSS tiap fitur
│   ├── img/                # Foto dan ikon lokal
│   └── js/                 # Experience, Achievement, dan toast
├── templates/
│   ├── base.html           # Kerangka HTML bersama dan block page_css
│   ├── components/         # Modal, star, toast, dan field form reusable
│   ├── home/               # index.html
│   ├── projects/           # list.html dan form.html
│   ├── experiences/        # list.html dan form.html
│   ├── achievements/       # list.html dan form.html
│   ├── skills/             # list.html
│   └── auth/               # login.html dan register.html
├── ai-chat-history/
├── ARCHITECTURE.md          # Panduan belajar struktur dan alur request
├── requirements.txt
└── manage.py
```

Konten antarmuka bilingual disimpan dalam kamus copy pada view. View halaman
hanya merender kerangka, form modal sesuai peran, dan alamat endpoint pada
atribut `data-*`. Browser memanggil `fetch` ke `/api/v1/`, API view mengambil
QuerySet, serializer mengubahnya menjadi JSON, lalu JavaScript mengisi kartu
dari template `<template>` dengan `textContent`. Untuk request yang mengubah
data, serializer memvalidasi input dan menyimpannya; `ModelForm` masih dipakai
oleh halaman create/update Tugas 3 dan untuk merender input modal.

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

### Tugas 3

Jawaban berikut menjelaskan implementasi saat Tugas 3. Pada Tugas 5, alur daftar
beralih dari serialization/deserialization server-side ke JSON manual dan AJAX.

### 1. Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

Saya menggunakan `ModelForm` karena form pada proyek ini berhubungan langsung
dengan model Django. Django dapat membentuk field form berdasarkan definisi
model, misalnya `CharField` menjadi input teks, `TextField` menjadi textarea,
dan `PositiveSmallIntegerField` menjadi input angka. Pada proyek ini,
`ExperienceForm`, `ProjectForm`, dan `AchievementForm` juga menggunakan
`form.is_valid()` untuk memvalidasi input serta `form.save()` untuk membuat atau
memperbarui objek. Jika form dibuat secara manual, setiap input harus
didefinisikan, diambil dari `request.POST`, divalidasi, dikonversi ke tipe yang
sesuai, dan disimpan satu per satu. Hal tersebut menghasilkan lebih banyak
duplikasi dan lebih mudah tidak konsisten dengan model.

`{% csrf_token %}` digunakan untuk melindungi request yang mengubah data dari
serangan Cross-Site Request Forgery. Django membandingkan token pada form dengan
token yang terkait dengan sesi pengguna. Tanpa perlindungan tersebut, situs
berbahaya dapat membuat form tersembunyi yang mengirim request ke aplikasi ini.
Jika pengguna masih memiliki cookie atau sesi aktif, browser dapat menjalankan
request tersebut atas nama pengguna sehingga data dapat ditambah, diubah, atau
dihapus tanpa persetujuannya. Karena itu, seluruh form POST pada proyek ini
memakai `csrf_token`, sedangkan fungsi delete juga dibatasi dengan
`@require_POST`.

### 2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

JSON lebih disukai karena sintaksnya lebih ringkas dan strukturnya sesuai dengan
objek serta array yang umum digunakan dalam JavaScript. Ukuran data JSON
biasanya lebih kecil karena tidak memerlukan tag pembuka dan penutup seperti
XML. JSON juga dapat diproses langsung dengan fungsi seperti `JSON.parse()` dan
`JSON.stringify()`, sehingga integrasinya dengan aplikasi web dan REST API lebih
sederhana.

XML tetap berguna untuk sistem yang membutuhkan namespace, atribut kompleks,
validasi berbasis schema, atau kompatibilitas dengan sistem lama. Namun, untuk
pertukaran data pada aplikasi web seperti portofolio ini, JSON lebih praktis,
mudah dibaca, dan membutuhkan lebih sedikit kode untuk diproses.

### 3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

Sebagai contoh, ketika endpoint `/api/experiences/` dibuka, Django mencocokkan
URL tersebut dengan fungsi `get_experiences_json`. Fungsi itu mengambil data
Experience melalui Django ORM sebagai `QuerySet`, kemudian menjalankan
`serializers.serialize("json", experiences)`. Hasil serialisasi dimasukkan ke
`HttpResponse` dengan content type `application/json` dan dikirim kepada
browser atau aplikasi yang meminta data.

Pada halaman Experience, fungsi `show_experiences` memperoleh response JSON
tersebut, mengubah content dari bytes menjadi string UTF-8, lalu menjalankan
`serializers.deserialize("json", ...)`. Objek hasil deserialisasi dimasukkan ke
context sebagai `experience_list` dan ditampilkan oleh `experiences.html`.
Project dan Achievement menggunakan alur serupa melalui `/api/projects/` dan
`/api/achievements/`.

Serialization diperlukan karena `QuerySet` dan objek model Django bukan data
JSON biasa dan tidak dapat langsung dikirim melalui HTTP. Serialization
mengubah objek tersebut menjadi representasi teks yang dapat dikirim melalui
jaringan, dibaca oleh aplikasi lain, dan direkonstruksi kembali melalui proses
deserialization.

## Implementasi Tugas 4

Tugas 4 menambahkan autentikasi, session, cookie, authorization, dan fitur star
ke data portofolio. Register, login, dan logout menggunakan mekanisme autentikasi
Django. Informasi pengguna tersimpan pada session, sedangkan cookie
`last_login` mencatat waktu login terakhir dan dihapus saat logout.

Authorization diterapkan sama pada Experience, Project, dan Achievement. Guest
dapat membaca halaman publik, tetapi harus login sebelum menjalankan aksi.
User biasa dapat memberi star, Editor juga dapat memperbarui data, sedangkan
create dan delete hanya tersedia bagi superuser. Selain diperiksa pada template
untuk mengatur visibilitas tombol, aturan tersebut diperiksa kembali pada view
agar URL tidak dapat dipakai untuk melewati authorization.

Fitur star menggunakan relasi many-to-many `starred_by` antara setiap jenis
entri dan User. Endpoint toggle memakai POST dan CSRF; pengguna ditambahkan ke
relasi jika belum memberi star dan dihapus jika sudah memberi star. Dengan
relasi ini, satu pengguna hanya dapat memberi satu star pada entri yang sama.
Serialization API memakai `use_natural_foreign_keys=True`, sehingga relasi User
ditampilkan sebagai username.

Test otomatis mencakup matriks akses keempat peran, visibilitas kontrol CRUD,
redirect login, respons 403, penolakan metode GET pada endpoint mutatif,
perlindungan CSRF, toggle star ketiga model, dan natural foreign keys. Seluruh
91 test lulus pada verifikasi akhir Tugas 4.

### Tugas 5

### 1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing adalah teknik menunda pemanggilan fungsi sampai tidak ada input baru
selama jeda tertentu. Pada pencarian Experience dan Achievement, setiap event
`input` membatalkan timer sebelumnya dengan `clearTimeout`, lalu memasang timer
baru menggunakan `setTimeout` selama 300 ms. Jika saya mengetik beberapa huruf
secara cepat, request pencarian baru dikirim setelah saya berhenti mengetik
selama jeda tersebut, bukan pada setiap huruf.

Teknik ini mengurangi request HTTP dan query database yang tidak diperlukan,
sehingga server tidak perlu memproses semua kata kunci sementara. Antarmuka juga
tidak terlalu sering berganti ke loading state. Pada proyek ini, submit form
pencarian tetap menjalankan pencarian langsung tanpa menunggu timer.

Debouncing tidak dengan sendirinya menjamin urutan respons. Request lama bisa
selesai setelah request yang lebih baru. Karena itu, implementasi juga memakai
`AbortController` untuk membatalkan request sebelumnya dan memeriksa controller
aktif sebelum menampilkan hasil, agar respons lama tidak menimpa hasil terbaru.

### 2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

`fetch()` mengembalikan `Promise`, bukan langsung objek `Response`. Di dalam
fungsi `async`, `await fetch(url)` menunda kelanjutan fungsi tersebut sampai
Promise selesai sehingga hasilnya dapat dipakai untuk memeriksa status HTTP.
`await` tidak memblokir seluruh browser; event loop tetap dapat menangani
interaksi lain selama request berlangsung.

Pada proyek ini, setelah menerima respons, saya juga menggunakan
`await response.json()` karena pembacaan dan parsing body JSON mengembalikan
Promise. Setelah data tersedia, kartu baru diisi dan loading state diganti
dengan daftar atau empty state. Pada penambahan data, respons server diperiksa
sebelum modal ditutup dan daftar dimuat kembali.

Jika `await` dihapus tanpa mengganti cara penanganan Promise, variabel respons
masih berisi Promise. Pemanggilan seperti `response.json()` akan gagal karena
Promise tidak memiliki method tersebut, dan proses berikutnya bisa berjalan
sebelum datanya tersedia. Bukan berarti request tidak dikirim: tanpa `await`,
kita tetap dapat menangani hasilnya memakai `.then()` dan `.catch()`.

Saya juga memeriksa `response.ok` atau status respons, karena `fetch()` tidak
otomatis menolak Promise hanya karena server mengembalikan HTTP 400 atau 403.
Status tersebut perlu ditangani agar pesan validasi atau kegagalan ditampilkan
dengan benar.

### 3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

XSS adalah serangan ketika input yang tidak dipercaya ditafsirkan sebagai kode
aktif oleh browser, sehingga penyerang dapat menjalankan JavaScript dalam
konteks situs. Contohnya, input berupa tag `img` dengan atribut `onerror` dapat
menjalankan kode saat gambar gagal dimuat jika input itu disisipkan sebagai HTML.

Template Django secara default melakukan autoescaping pada variabel. Karakter
seperti `<` dan `>` diubah menjadi representasi aman sehingga input tidak
langsung menjadi tag HTML. Sebaliknya, data JSON yang diterima melalui AJAX
tidak otomatis mendapat perlindungan template tersebut saat dimasukkan ke DOM.
Jika JavaScript menggabungkan data ke `innerHTML` tanpa escaping, browser akan
mem-parsing-nya sebagai HTML dan dapat menjalankan payload berbahaya.

Jadi, AJAX sendiri bukan penyebab XSS; risikonya berasal dari cara data
ditampilkan. Pada Experience dan Achievement, saya mengisi judul, deskripsi
atau hasil, kategori, dan teks lainnya dengan `textContent`, bukan mem-parsing
input sebagai HTML. Di server, `ModelForm` memakai `strip_tags` pada field teks
dan menolak field wajib yang menjadi kosong setelah dibersihkan.

`strip_tags` merupakan lapisan tambahan untuk kebutuhan input teks biasa,
bukan jaminan bahwa hasilnya aman dimasukkan ke `innerHTML`. Rendering aman tetap
diperlukan. Template Django juga dapat rentan jika autoescaping dimatikan atau
data tidak dipercaya diberi filter `safe`; perlindungan harus mengikuti konteks
tempat data dipakai.

### Tugas 6

### 1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!

REST (Representational State Transfer) adalah gaya arsitektur untuk merancang
web API, bukan library atau format data. Data diperlakukan sebagai resource
yang punya alamat sendiri, misalnya `/api/v1/experiences/` untuk kumpulan
pengalaman dan `/api/v1/experiences/3/` untuk satu pengalaman. Tindakan
dinyatakan lewat HTTP method: `GET` membaca, `POST` membuat, `PUT`/`PATCH`
mengubah, dan `DELETE` menghapus. Klien dan server bertukar representasi data
(di proyek ini JSON), status hasilnya disampaikan lewat kode HTTP, dan setiap
request seharusnya membawa informasi yang dibutuhkan server (stateless).

Karena itu, JSON hanyalah format representasi. Endpoint Tugas 5 juga
mengembalikan JSON, tetapi desainnya belum RESTful: tindakan ditulis di URL
(`POST /experience/add-ajax/`, `POST /experience/<id>/delete/`), resource yang
sama tersebar di beberapa alamat, dan hapus/star mengembalikan redirect HTML,
bukan status seperti `204`. Pada Tugas 6, satu alamat resource dipakai dengan
method yang berbeda, dan hasilnya dinyatakan dengan status `201`, `204`, `400`,
`403`, `404`, atau `405`. API ini juga tidak sepenuhnya mengikuti REST:
`SessionAuthentication` menyimpan session di server, dan `/star/` lebih mirip
aksi daripada resource. Yang saya jaga adalah kontrak API yang jelas dan
konsisten.

`PUT` mengirim representasi pengganti yang lengkap, sehingga semua field wajib
harus ada. `PATCH` hanya mengirim field yang ingin diubah; di DRF ini berarti
serializer dipanggil dengan `partial=True`, dan field yang tidak dikirim tetap
memakai nilai lama. Di proyek ini, `PUT` yang hanya berisi `title` ditolak
dengan `400` karena field wajib lain tidak ada, sedangkan `PATCH` dengan
`title` saja berhasil dan deskripsi tetap sama. `PUT` cocok ketika klien
memegang seluruh data dan ingin menggantinya sekaligus, misalnya menyinkronkan
satu entri dari sumber lain. `PATCH` cocok untuk perubahan sebagian, seperti
mengubah judul atau tahun selesai. Modal edit saya memakai `PATCH`. Validasi
lintas field tetap berjalan pada `PATCH`: jika hanya `end_year` yang dikirim,
`ExperienceSerializer.validate()` membandingkannya dengan `start_year` yang
sudah tersimpan.

### 2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?

Serializer bekerja dua arah. Saat membaca (`GET`), serializer mengubah objek
model atau QuerySet menjadi tipe data Python yang dirender DRF menjadi JSON
(serialization). Saat menulis (`POST`, `PUT`, `PATCH`), serializer menerima
`request.data`, memvalidasinya lewat `is_valid()`, lalu `save()` memanggil
`create()` atau `update()` (deserialization). `ExperienceSerializer` dan
`AchievementSerializer` di proyek ini menentukan daftar `fields` secara
eksplisit, membersihkan teks di `validate_<field>`, dan mewarisi
`StarInfoMixin` yang menyediakan `star_count`, `is_starred`, dan
`starred_by_names` sebagai field hasil perhitungan yang read-only.

Pada `get_experiences_json` Tutorial/Tugas 5, saya menulis dictionary field
demi field, menghitung star sendiri, lalu membungkusnya dengan `JsonResponse`.
Validasi input dilakukan terpisah oleh `ModelForm` di view lain, dan status
HTTP serta bentuk error (`form.errors.get_json_data()`) diatur manual di setiap
view. Dengan serializer:

- representasi dan validasi didefinisikan sekali, lalu dipakai oleh daftar,
  detail, tambah, ubah, dan star;
- field yang tidak dicantumkan tidak akan bocor. Ini penting karena relasi ke
  `User` bisa membawa email atau password hash;
- field read-only otomatis diabaikan saat menulis. Test saya mengirim
  `star_count: 99` dan `starred_by` palsu, dan keduanya tidak tersimpan;
- `is_valid(raise_exception=True)` langsung menghasilkan `400` dengan error per
  field dalam format yang konsisten, sehingga frontend cukup punya satu
  pembaca error;
- update sebagian cukup dengan `partial=True`, tanpa logika tambahan.

Kekurangannya, serializer tidak menjalankan `clean_<field>` milik `ModelForm`.
Karena halaman edit Tugas 3 masih memakai form, aturan validasi yang sama perlu
dijaga di dua tempat. Kesesuaiannya saya pastikan lewat test.

### 3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?

Autentikasi menjawab "siapa pengirim request ini?", sedangkan otorisasi
menjawab "bolehkah pengirim ini melakukan tindakan tersebut?". Di DRF keduanya
dipisahkan. Authentication class, di proyek ini `SessionAuthentication`,
membaca cookie session dan mengisi `request.user`; jika tidak ada session,
pengguna diperlakukan sebagai anonim. Setelah itu permission class memutuskan
izinnya. `IsPortfolioOwnerOrEditorOrReadOnly` mengizinkan `GET` untuk semua,
`PUT`/`PATCH` untuk Editor dan superuser, serta `POST`/`DELETE` hanya untuk
superuser. Endpoint star memakai `IsAuthenticated`, dan akun yang memberi star
selalu diambil dari `request.user`. Pemeriksaan ini berjalan sebelum isi view.
Karena `SessionAuthentication` tidak mengirim header `WWW-Authenticate`,
request tulis dari guest dijawab `403`, bukan `401`.

Menyembunyikan tombol hanya mengatur tampilan. Siapa pun tetap dapat mengirim
request langsung, misalnya `fetch("/api/v1/experiences/3/", {method: "DELETE"})`
dari Console, lewat `curl`, atau dari tab lama yang masih menampilkan tombol.
Pada pengujian browser, saya mencabut status superuser di database ketika
halaman pemilik masih terbuka. Tombol Delete masih terlihat, tetapi server
menolak dengan `403` dan toast menampilkan pesan dari permission class. Test
API juga memeriksa bahwa penolakan tidak mengubah isi database. Saat permission
sengaja dilonggarkan untuk uji mutasi, test peran langsung gagal. Jadi,
template mengatur pengalaman pengguna, sedangkan permission class di server
yang benar-benar menjaga data.

### 4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?

Dengan `SessionAuthentication`, identitas pengguna dibawa oleh cookie session.
Browser melampirkan cookie itu secara otomatis ke setiap request menuju
domain portofolio, termasuk request yang dipicu oleh form atau script di situs
lain. Tanpa CSRF, situs berbahaya dapat membuat browser pemilik yang masih
login mengirim `DELETE` atau `PATCH` atas namanya. Token CSRF membuktikan
bahwa request berasal dari halaman kita sendiri. Halaman Experience dan
Achievement merender `{% csrf_token %}` agar cookie `csrftoken` tersedia untuk
pengguna biasa dan Editor, lalu `getCookie("csrftoken")` mengirim nilainya
lewat header `X-CSRFToken` pada setiap `POST`, `PUT`, `PATCH`, dan `DELETE`.
View `@api_view` dibebaskan dari middleware CSRF Django, tetapi
`SessionAuthentication` memeriksa ulang CSRF untuk method yang mengubah data
dari pengguna yang terautentikasi lewat session. Saat saya coba, login lewat
session lalu `POST` tanpa token menghasilkan
`403 CSRF Failed: CSRF cookie not set.`, sedangkan `GET` tetap `200`.

`force_authenticate` melewati proses autentikasi sepenuhnya: test client
langsung menetapkan `request.user` tanpa session dan tanpa
`SessionAuthentication`. Akibatnya pemeriksaan CSRF tidak pernah dijalankan.
Dalam percobaan, `APIClient(enforce_csrf_checks=True)` yang memakai
`force_authenticate` tetap berhasil `POST` dengan status `201` tanpa token sama
sekali. Test seperti itu berguna untuk menguji permission, tetapi tidak
membuktikan perlindungan CSRF. Karena itu,
`test_session_write_without_csrf_token_is_rejected` memakai
`APIClient(enforce_csrf_checks=True)` dan `.login()` agar session sungguhan
terbentuk, lalu memastikan `POST`/`PATCH` tanpa token ditolak dan database
tidak berubah. Pasangannya, `test_session_write_with_token_from_page_succeeds`,
mengambil token dari cookie halaman sebagai Editor dan membuktikan `PATCH`
dengan token berhasil.

## Progres pengembangan

| Periode | Fokus | Hasil |
| --- | --- | --- |
| 26 Agustus – 2 September 2026 | Fondasi Django | Inisialisasi proyek, tutorial, pembangunan ulang struktur, dan konfigurasi middleware. |
| 4 September 2026 | Konten inti | Fondasi portofolio, halaman bilingual, dan struktur semantik HTML. |
| 5 September 2026 | Desain dan aksesibilitas | Polishing visual, tema light/dark, ikon sosial, dan focus state keyboard. |
| 6 September 2026 | Pengayaan portofolio | Skill catalog, footer, tautan eksternal, konten pengalaman, proyek, dan pencapaian. |
| 7 September 2026 | Responsivitas dan dokumentasi | Menu mobile, prioritas foto hero pada mobile, serta dokumentasi proyek. |
| 11–14 September 2026 | Implementasi MVT | Model, migrasi, seed data, halaman daftar bilingual, navigasi, dan test untuk data portofolio dinamis. |
| 14–19 September 2026 | Form dan data delivery | Root template bersama, halaman Experience terpisah, ModelForm, create, update, delete, modal konfirmasi, endpoint JSON, deserialisasi data, serta test untuk Experience, Project, dan Achievement. |
| 19–28 September 2026 | Authentication dan authorization | Register, login, logout, session, cookie, empat peran akses, star/unstar untuk Experience, Project, dan Achievement, natural foreign keys, serta test authorization dan star. |
| Tugas 5; verifikasi 5 Oktober 2026 | Interaktivitas AJAX | Daftar JSON manual, pencarian debounce, loading/empty/error/retry, modal tambah AJAX, CSRF, sanitasi, toast, dan refresh tanpa reload untuk Experience dan Achievement. Full suite lulus 114/114 test; tiga refleksi tentang debouncing, await, dan XSS ditambahkan. |
| 6 Oktober – 3 November 2026 | Refactor dan settings | Views dipecah per fitur, template dan CSS per halaman; `DEBUG` mengikuti `PRODUCTION` dan `STATIC_ROOT` dikonfigurasi. |
| 3–4 November 2026 | Tutorial 7 (DRF) | Upgrade ke Django 5.2 dan DRF 3.18; serializer, permission, API view, dan route `/api/v1/projects/`; halaman Projects memakai API; 13 test API. |
| 6–7 November 2026 | Tugas 6 (DRF) | API Experience dan Achievement dengan matriks empat peran, halaman memakai API termasuk modal edit `PATCH`, 38 test API, dan empat refleksi. Dikerjakan per branch fitur dengan conventional commits; full suite `test main` lulus 168/168 test. |

## AI disclosure

### Cara AI digunakan

Saya menggunakan Hermes Agent sebagai asisten pengembangan lokal. AI membantu
menjelaskan pola MVT, autentikasi, session, cookie, authorization, relasi
many-to-many, serta alur AJAX dengan Fetch API; menyarankan struktur model dan route; menyiapkan perubahan kode
dan test; serta menjalankan pemeriksaan teknis seperti `python manage.py check`
dan `python manage.py test`. Pengembangan dilakukan secara bertahap:
setiap bagian diimplementasikan dan diuji secara terpisah, kemudian hasilnya
saya tinjau sebelum di-commit. Keputusan fitur, pemilihan konten, aset gambar,
dan perubahan akhir tetap berada pada saya sebagai pemilik proyek.

Untuk Tugas 5, AI membantu mengadaptasi pola Tutorial 5 untuk Experience dan
Achievement: JSON manual, pencarian debounce, DOM rendering, modal tambah,
validasi/sanitasi, CSRF, authorization, dan toast. AI menulis perubahan
implementasi serta memperbarui test lama dan menambahkan 21 test AJAX.
AI juga membantu menyusun draf tiga jawaban refleksi Tugas 5 berdasarkan
pertanyaan resmi dan implementasi proyek; draf tersebut perlu saya tinjau
agar sesuai dengan pemahaman saya.
Pemeriksaan browser dilakukan dengan Chrome headless berprofil sementara,
bukan dengan mengontrol browser pribadi tanpa izin. Data sementara pada
pengecekan dikembalikan melalui rollback atau dibersihkan sesudahnya.

Pada verifikasi tahap test, seluruh 114 test Django lulus. Pengecekan browser
kedua model mencakup debounce, error/retry, modal, toast, submit ganda, refresh
tanpa reload, dan viewport mobile. Pengujian ini tidak menjamin semua bug atau
perbedaan lingkungan deployment sudah teratasi. Saya mengelola branch, merge,
dan commit; AI tidak membuat commit pada tahap Tugas 5 ini.

#### Tutorial 7 dan Tugas 6

Tools: Hermes Agent (aplikasi desktop) dengan model Claude (`claude-opus-5-5`).
Strategi prompting yang saya pakai:

- AI diminta membaca PDF resmi Tutorial 7 dan Tugas 6 terlebih dahulu, lalu
  memetakan setiap checklist ke kondisi repository sebelum menulis kode.
- Pekerjaan dibagi per tahap kecil. AI berhenti setelah setiap tahap,
  melaporkan file yang berubah serta hasil verifikasi, lalu saya meninjau dan
  membuat commit sendiri.
- Keputusan desain diajukan sebagai pilihan, dan saya yang menentukan. Keputusan
  saya: Tutorial 7 dikumpulkan persis sesuai contoh (API Projects khusus
  pemilik), Tugas 6 diterapkan pada Experience dan Achievement, edit memakai
  modal `PATCH`, serta Git memakai branch per fitur dengan conventional commits.
  Branch dan merge saya buat sendiri.

Bagian yang dibantu AI:

- Tutorial 7: upgrade dependency, serializer Project, permission class, API
  view, route, penggantian script halaman Projects, dan adaptasi 13 test
  tutorial ke model saya (primary key integer, field `category`/`thumbnail`).
- Tugas 6: `ExperienceSerializer`, `AchievementSerializer`, `StarInfoMixin`,
  helper API bersama (`create_response`, `detail_response`, `toggle_star`),
  endpoint `/api/v1/experiences/` dan `/api/v1/achievements/`, JavaScript dan
  template halaman beserta modal edit, penyesuaian test lama yang mengunci
  kontrak lama, serta 38 test di `main/tests_api_portfolio.py`.
- Draf README ini, termasuk empat jawaban refleksi Tugas 6. Klaim pada jawaban
  dicek dengan percobaan nyata (misalnya `force_authenticate` vs `.login()`
  pada CSRF), tetapi draf tetap saya tinjau agar sesuai pemahaman saya.

Verifikasi yang dilakukan selain menjalankan test:

- probe matriks peran dengan `APITestCase` client di dalam transaksi yang
  di-rollback;
- pengujian Chrome headless untuk keempat peran pada salinan database dengan
  akun sementara, yang dihapus setelah pengujian;
- uji mutasi: permission, `strip_tags`, `IsAuthenticated`, `{% csrf_token %}`,
  dan validasi tahun sengaja dirusak satu per satu untuk memastikan test benar-
  benar gagal, lalu kode dipulihkan.

Catatan kritis tentang keterbatasan AI selama tahap ini:

- AI sempat menyarankan agar Editor boleh mengubah Projects lewat API, demi
  konsistensi dengan halaman HTML. Setelah saya menanyakan apakah itu sesuai
  Tutorial 7, AI membaca ulang PDF dan mengoreksi sarannya: tutorial
  mensyaratkan Projects khusus pemilik dan ada test yang mengharapkan Editor
  ditolak. Saran AI perlu dicek terhadap spesifikasi, bukan diterima begitu saja.
- Saya sempat ingin mengumpulkan commit refactor lama sebagai bagian dari
  Tutorial 7. AI menyarankan untuk tidak melakukannya karena isi dan tanggal
  commit itu tidak sesuai materi tutorial, jadi commit tersebut hanya menjadi
  fondasi.
- Upgrade Django di folder OneDrive gagal di tengah jalan karena folder menjadi
  read-only, sehingga Django terhapus sebagian dari virtual environment. AI
  memperbaikinya, tetapi kejadian ini menunjukkan perintah otomatis tetap bisa
  merusak environment lokal dan perlu dicek ulang.
- Ke-38 test baru langsung lulus pada percobaan pertama. Karena test yang selalu
  lulus belum tentu menguji apa pun, uji mutasi dilakukan untuk membuktikan
  test tersebut bisa gagal.
- Pengujian otomatis berjalan di lingkungan lokal. Deployment PWS, termasuk
  `collectstatic`, `PRODUCTION=true`, dan instalasi dependency baru, tetap perlu
  saya cek sendiri.

### Chat history

Riwayat percakapan yang tersimpan selama pengembangan Tugas 2 sampai Tugas 5
tersedia di folder [`ai-chat-history/`](ai-chat-history/). Riwayat
Tugas 3 diekspor dari sesi Hermes Agent ke
[`20260919_072342_16904e-activate-.venv-in-powershell-2.md`](ai-chat-history/20260919_072342_16904e-activate-.venv-in-powershell-2.md)
dengan redaksi otomatis untuk informasi sensitif. Bagian pengembangan Tugas 4
tersedia pada
[`20260928_tugas-4-development.md`](ai-chat-history/20260928_tugas-4-development.md).

Snapshot terbaru tersedia pada
[`20261005_tugas-3-to-5-development.md`](ai-chat-history/20261005_tugas-3-to-5-development.md).
Ekspor ini dimulai dari permintaan pengerjaan Tugas 3 pada 19 September 2026
hingga waktu ekspor 5 Oktober 2026: 994 pesan asli dari 1.000 pesan yang diekspor,
dengan enam pesan awal aktivasi virtual environment dikecualikan. Ekspor memakai
redaksi otomatis dan penyamaran tambahan nilai kredensial. Riwayat lama tidak
ditimpa, dan snapshot tidak mencakup percakapan setelah waktu ekspornya.
Jumlah pesan, cakupan ekspor, serta checksum SHA-256 dicatat dalam
[`manifest.jsonl`](ai-chat-history/manifest.jsonl).

Percakapan Tutorial 7 dan Tugas 6 tersedia pada
[`20261107_tutorial-7-and-tugas-6-development.md`](ai-chat-history/20261107_tutorial-7-and-tugas-6-development.md).
Ekspor ini berasal dari satu sesi Hermes Agent, mulai 3 November 2026 hingga
snapshot 7 November 2026, dan berisi 322 pesan (27 pesan dari saya). Selain
redaksi otomatis, sisa potongan `SECRET_KEY` disamarkan secara manual.
Snapshot diambil sebelum tahap dokumentasi selesai, sehingga penyusunan akhir
README ini tidak tercakup di dalamnya.

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
filter berubah. Batasan tanpa JavaScript berlaku pada tahap awal tugas;
pada Tutorial/Tugas 5, JavaScript digunakan untuk daftar, pencarian, modal, dan
toast. Setiap perubahan tetap perlu ditinjau dan dipahami, bukan dianggap benar
hanya karena dihasilkan AI atau lolos test.

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
