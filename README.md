# MaxPorto

Proyek portofolio pribadi bilingual yang menggunakan Django dan pola
Model-View-Template (MVT). Data pengalaman, proyek, keahlian, dan pencapaian
disimpan dalam model Django. Halaman Experience, Projects, dan Achievements
memuat kartu melalui AJAX, sedangkan Skills dirender melalui template HTML.

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
- Data Experience, Project, dan Achievement tersedia dalam format JSON melalui:
  - `/api/experiences/`
  - `/api/projects/`
  - `/api/achievements/`
- Halaman daftar Experience, Project, dan Achievement memuat data dengan `fetch`
  dari endpoint JSON manual menggunakan `JsonResponse`, lalu menampilkan kartu
  tanpa reload. Respons menyertakan jumlah star, status star pengguna, URL aksi,
  dan izin update/delete.
- Pencarian Experience berdasarkan posisi atau organisasi, dan Achievement
  berdasarkan judul atau hasil, mencakup field English/Indonesia. Keduanya
  menggunakan debounce 300 ms; Projects menyediakan pencarian judul.
- Loading, empty, dan error state serta tombol retry tersedia pada daftar AJAX.
- Superuser dapat menambahkan Experience, Project, dan Achievement melalui modal
  AJAX dengan CSRF, validasi server-side, toast sukses/gagal, dan refresh daftar
  tanpa reload. Experience dan Achievement juga menampilkan error per field.
- Input teks Experience dan Achievement dibersihkan dengan `strip_tags`, lalu
  dirender menggunakan `textContent`. Field teks wajib yang menjadi kosong
  setelah sanitasi ditolak. Validasi mencakup rentang tahun 1900–2100,
  urutan tahun Experience, serta urutan tampilan Achievement tidak negatif.
- Relasi pengguna pada respons JSON direpresentasikan dengan username, bukan
  primary key internal, termasuk daftar natural keys `starred_by`.
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

- Python dan Django
- HTML5 semantik
- CSS3 murni
- JavaScript vanilla, Fetch API, dan DOM API

## Menjalankan proyek secara lokal

Prasyarat: Python 3 dan `pip`.

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

Pemeriksaan dan test dapat dijalankan dengan:

```powershell
python manage.py check
python manage.py test
```

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

Edit, delete, dan star tetap memakai alur halaman/form POST yang sudah ada;
ketiganya belum diubah menjadi AJAX. Halaman daftar AJAX membutuhkan JavaScript.

## Struktur proyek

Panduan alur URL → view → template/CSS → AJAX ada di [ARCHITECTURE.md](ARCHITECTURE.md).

```text
MaxPorto/
├── main/
│   ├── migrations/         # Skema dan seed data
│   ├── copy.py             # Label/pesan bilingual fitur portofolio
│   ├── permissions.py      # Pemeriksaan role Editor
│   ├── forms.py            # ModelForm dan validasi
│   ├── models.py           # Project, Experience, Skill, Achievement
│   ├── tests.py            # Test model, auth, akses, star, dan view
│   ├── test_ajax.py        # Test kontrak AJAX
│   ├── test_structure.py   # Test template, stylesheet, dan modul view
│   ├── urls.py             # Named URL halaman dan API
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

Konten antarmuka bilingual disimpan dalam kamus copy pada view. Untuk daftar
AJAX, view mengambil QuerySet, menyusun dictionary/list berisi field model,
informasi star, dan izin aksi, kemudian mengirimnya dengan `JsonResponse`.
Browser memanggil `fetch`, membaca `response.json()`, dan mengisi kartu pada DOM.
Experience dan Achievement memakai template kartu yang dikloning dan diisi
dengan `textContent`; data tidak dideserialisasi kembali menjadi model di view
halaman. `ModelForm` tetap menjadi sumber validasi dan penyimpanan data.

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
