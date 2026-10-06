# Panduan membaca MaxPorto

## Mulai dari satu fitur, bukan semua file sekaligus

Untuk belajar, ikuti fitur Experience lebih dulu:

1. `main/urls.py`: cari route `experience/` dan nama `show_experiences`.
2. `main/views/experiences.py`: baca `show_experiences()`. View memilih teks bahasa dan menyiapkan form/context, lalu merender `experiences/list.html`.
3. `main/copy.py`: `EXPERIENCE_COPY` menyimpan label dan pesan Inggris/Indonesia.
4. `templates/experiences/list.html`: menyusun halaman, state loading/error/empty, modal, dan template kartu. Template ini mewarisi `base.html`.
5. `static/css/experiences.css`: mengatur tampilan khusus kartu pengalaman. Layout, tombol, pencarian, dan modal bersama ada di `components.css`.
6. `static/js/experiences.js`: mengambil JSON, membuat kartu, menangani pencarian, serta submit modal tambah.
7. Kembali ke `main/views/experiences.py`: baca `get_experiences_json()` untuk melihat query ORM dan payload JSON; lalu `create_experience_ajax()` untuk validasi form dan penyimpanan.
8. `main/models.py` dan `main/forms.py`: definisi data dan aturan validasinya.

Setelah paham, bandingkan alurnya dengan Achievement dan Project.

## Peta folder

```text
main/
  copy.py                 teks bilingual untuk fitur portofolio
  permissions.py          is_editor(): pemeriksaan keanggotaan grup Editor
  models.py               Project, Experience, Skill, Achievement
  forms.py                validasi input untuk tambah/edit
  urls.py                 pemetaan URL ke fungsi view
  views/
    __init__.py           ekspor fungsi untuk import main.views yang sudah ada
    auth.py               register, login, logout, dan cookie last_login
    projects.py           halaman, JSON, CRUD, AJAX tambah, dan star proyek
    experiences.py        halaman, JSON, CRUD, AJAX tambah, dan star pengalaman
    achievements.py       halaman, JSON, CRUD, AJAX tambah, dan star prestasi
    skills.py             halaman katalog keahlian
  tests.py                test perilaku model, akses, dan halaman
  test_ajax.py            test kontrak AJAX
  test_structure.py       test template, stylesheet, dan modul view

portofolio/
  urls.py                 root URL, homepage, dan include main.urls
  views.py                homepage dan teks bilingual homepage

templates/
  base.html               kerangka dokumen, navbar, pesan, footer, dan toast
  components/             potongan HTML reusable, termasuk form_fields.html
  home/index.html
  projects/list.html
  projects/form.html
  experiences/list.html
  experiences/form.html
  achievements/list.html
  achievements/form.html
  skills/list.html
  auth/login.html
  auth/register.html

static/css/
  base.css                tema, reset, tipografi, navbar, footer, aksesibilitas
  components.css          layout daftar, tombol, pencarian, modal, star, toast
  forms.css               input/form yang dipakai semua fitur dan auth
  home.css                hero, foto profil, tautan sosial
  projects.css            kartu proyek
  experiences.css         kartu pengalaman
  achievements.css        kartu dan grid prestasi
  skills.css              katalog dan filter keahlian
```

## Tiga alur request yang perlu dibedakan

### 1. Membuka halaman daftar

```text
GET /experience/
  -> portofolio/urls.py -> main/urls.py
  -> show_experiences()
  -> templates/experiences/list.html + base.html
  -> browser menerima HTML dan memuat stylesheet
  -> experiences.js meminta GET /api/experiences/
  -> get_experiences_json() -> Experience.objects... -> JSON
  -> JavaScript membuat kartu di halaman
```

Halaman Project dan Achievement juga memuat daftar melalui AJAX. Jadi `show_*()` tidak perlu mengambil daftar model untuk dirender sebagai kartu di server. Skill berbeda: `show_skills()` mengambil model lalu template melakukan perulangan langsung.

### 2. Menambah melalui modal AJAX

```text
submit modal
  -> JavaScript mengirim POST + token CSRF
  -> create_experience_ajax()
  -> pemeriksaan superuser
  -> ExperienceForm(request.POST).is_valid()
  -> form.save() jika valid
  -> JSON 201, atau JSON error 400/403
  -> JavaScript menampilkan toast dan memuat ulang daftar
```

Ada juga `create_experience()` untuk form tambah biasa. Keduanya tetap tersedia; AJAX tidak menghapus route form biasa.

### 3. Edit, delete, dan star

Edit memakai form halaman dan redirect setelah berhasil. Delete dan star memakai POST biasa, bukan AJAX. Perubahan nama folder tidak mengubah nama URL maupun aturan akses: superuser dapat tambah/hapus, Editor dapat edit, pengguna login dapat memberi star.

## Cara memilih file yang perlu diubah

- Ubah struktur halaman: template di folder fiturnya.
- Ubah navbar/footer: `templates/base.html`.
- Ubah tampilan satu fitur: CSS fitur tersebut.
- Ubah tombol/modal/pencarian yang dipakai banyak fitur: `components.css`.
- Ubah input/form: `forms.css`.
- Ubah teks Inggris/Indonesia: `main/copy.py`; untuk homepage masih di `portofolio/views.py`.
- Ubah data yang dikirim/diterima server: view fitur tersebut.
- Ubah aturan validasi: `main/forms.py`.
- Ubah struktur data: `main/models.py`, lalu buat migrasi yang sesuai.
- Ubah perilaku interaksi Experience/Achievement: JavaScript di `static/js/`.
- JavaScript Project masih berada di `templates/projects/list.html`; tidak dipindahkan pada refactor ini.

## Kenapa bukan satu CSS untuk setiap HTML?

Form tambah dan edit memakai template/form styling yang sama. Login dan register juga memakai `forms.css`, jadi tidak dibuat `auth.css` kosong atau duplikasi styling. `base.html` selalu memuat `base.css` dan `components.css`; child template menambahkan stylesheet yang diperlukan melalui block `page_css`.

Beberapa nama kelas bersama masih memakai awalan `project-*` karena sejak awal dipakai ulang oleh Experience, Achievement, dan Skill. Letaknya sekarang di `components.css`. Nama itu sengaja dipertahankan agar refactor tidak sekaligus mengubah selector JavaScript atau tampilan.

`main/views.py` berubah menjadi package `main/views/`. `__init__.py` mengekspor fungsi agar `from main.views import show_projects` tetap valid. Implementasinya dibaca di `projects.py`, bukan di `__init__.py`.

## Verifikasi saat mengubah kode

Gunakan environment proyek `.venv` (Django sesuai `requirements.txt`), bukan `env` yang memiliki versi Django berbeda.

```bash
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py test main --noinput
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
```

Refactor organisasi file ini tidak membutuhkan perubahan model atau migrasi database.
