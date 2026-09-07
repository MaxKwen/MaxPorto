# AI Disclosure

## Penggunaan AI

Dalam tugas individual ini, saya menggunakan Codex secara lokal sebagai asisten pengembangan. Saya memberikan arah fitur, konten, serta batasan desain; AI membantu menerjemahkan arahan tersebut menjadi perubahan pada template, CSS, dan dokumentasi. AI juga membantu menjelaskan kembali rancangan agar dapat saya tinjau sebelum perubahan diterapkan.

## Batasan AI yang perlu diperhatikan

AI tidak memahami kebutuhan tugas, identitas pribadi, maupun kondisi browser saya secara otomatis. Outputnya dapat salah secara teknis, terlalu umum, atau tampak masuk akal tanpa benar-benar sesuai konteks proyek. AI juga tidak menggantikan pertimbangan keamanan: kredensial dan konfigurasi produksi tidak boleh dibagikan kepadanya atau ditulis ke repository. Oleh karena itu, setiap saran AI perlu dibaca, diuji, dan disesuaikan secara manual.

Contoh keterbatasan yang nyata pada proyek ini adalah implementasi awal menu mobile dengan elemen `details`. Secara konseptual menu tersebut tampak tepat, tetapi perilaku bawaan `details` menyembunyikan navbar pada desktop. Masalah ini ditemukan melalui pemeriksaan browser, lalu diperbaiki secara manual dengan struktur checkbox dan label yang hanya mengendalikan menu mobile. Ini menunjukkan bahwa kode hasil AI bukan bukti kebenaran tanpa verifikasi lintas breakpoint.

## Pekerjaan dan keputusan manual

- Memasukkan serta memverifikasi informasi pribadi, pengalaman, proyek, dan pencapaian yang ditampilkan pada portofolio.
- Meninjau terjemahan Inggris dan Indonesia agar sesuai dengan maksud konten.
- Menentukan prioritas desain, termasuk hierarki hero, warna, dan konten yang relevan untuk ditampilkan.
- Menguji perilaku halaman pada desktop dan mobile, termasuk navigasi hamburger, urutan foto hero, tautan eksternal, toggle tema, dan filter keterampilan.
- Meninjau aksesibilitas dasar: fokus keyboard, label kontrol, struktur semantik, dan opsi reduced motion.
- Menjalankan pemeriksaan konfigurasi Django dan memperbaiki hasil yang tidak sesuai dengan perilaku yang diharapkan.

## Akuntabilitas

Saya bertanggung jawab atas keputusan akhir, isi portofolio, hasil pengujian, dan perubahan yang masuk ke repository. AI dipakai sebagai alat bantu percepatan, bukan sebagai pengganti pemahaman konseptual atau proses review.
