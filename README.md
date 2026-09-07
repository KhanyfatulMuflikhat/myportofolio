Nama : Khanyfatul Muflikhat  
NPM : 2506589755  
Kelas : PBP A  

# Portofolio Pribadi — Khanyfatul Muflikhat

Website portofolio pribadi berbasis Django, dibuat untuk memenuhi Tutorial dan Individual Assignment mata kuliah Pemrograman Berbasis Platform (PBP) Fakultas Ilmu Komputer, Universitas Indonesia.

## Deskripsi Proyek

Website ini menampilkan profil "About Me" beserta tiga section tambahan: **Skills**, **Education**, dan **Projects**. Saat ini website masih murni menggunakan HTML5 dan CSS3 (belum menggunakan database atau arsitektur MVT), sesuai cakupan materi Tutorial 1.

**Fitur yang tersedia:**
- Section Profile — data diri, bio, dan tautan sosial media
- Section Skills — kategori technical, robotics, languages, dan photography
- Section Education — riwayat pendidikan dengan pencapaian di tiap institusi (ditampilkan sebagai timeline)
- Section Projects — SIPELAN, proyek IoT pendeteksi lawan arah lalu lintas

## Tech Stack

- Django (backend server untuk serving halaman)
- HTML5 (struktur semantik)
- CSS3 murni (grid, flexbox, custom properties, media query)

## Cara Menjalankan Proyek

### Prasyarat
- Python 3.x sudah terinstal
- Git

### Langkah Setup

1. Clone repository ini:
```bash
   git clone https://github.com/KhanyfatulMuflikhat/myportofolio.git
   cd myportofolio
```

2. Buat dan aktifkan virtual environment:
```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Jalankan development server:
```bash
   python manage.py runserver
```

5. Buka browser dan akses `http://127.0.0.1:8000/`

### Tugas 1
1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?
Ya, saya menggunakan elemen semantik HTML5 seperti <header>, <nav>, <main>, <section>, dan <footer> untuk membangun struktur halaman. Setiap bagian konten yang berdiri sendiri secara topik saya bungkus dalam elemen <section> terpisah dengan id masing-masing, seperti #profile, #skills, #education, #projects.
Elemen semantik ini membantu dalam beberapa hal. Pertama, struktur kode jadi lebih mudah dibaca dan dipahami tanpa harus membuka file CSS untuk mengidentifikasi tiap bagian. Kedua, penggunaan id pada tiap <section> memungkinkan saya membuat navigasi anchor link (<a href="#skills">) yang langsung mengarah ke bagian yang relevan sehingga meningkatkan usability halaman. Ketiga, elemen semantik juga membantu aksesibilitas dan SEO, karena browser dan screen reader bisa mengenali struktur dokumen dengan lebih baik dibandingkan hanya menggunakan <div> generik di semua tempat.
Saya belum menggunakan <article> atau <aside> karena konten yang saya buat belum ada yang benar-benar independen secara konten (seperti artikel blog) atau bersifat suplemen di luar alur utama (seperti sidebar). Namun, saya berencana mempertimbangkan <article> untuk tiap item di section Projects jika nanti jumlah project bertambah, karena tiap project card sebenarnya bisa berdiri sendiri sebagai unit konten yang lengkap.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?
Tantangan terbesar yang saya temui ada pada bagian hero section, karena saya menggunakan grid-template-areas dengan tata letak dua kolom (identity/details di kiri, foto di kanan) yang perlu berubah menjadi satu kolom vertikal di layar mobile. Saya harus memikirkan ulang urutan elemen, seperti apakah foto harus tetap di atas nama atau dipindah ke bawah, supaya alur baca tetap masuk akal saat ditumpuk secara vertikal dan bukan sekadar mengecilkan ukurannya.
Tantangan lain ada di section Education yang menggunakan tata letak timeline dengan garis vertikal dan titik penanda menggunakan position absolute. Saat lebar layar mengecil, posisi titik dan padding kiri perlu disesuaikan ulang lewat media query, karena jika tidak, garis dan dot-nya bisa terlihat terlalu jauh atau terlalu dekat dengan teks.
Untuk mengevaluasi elemen mana yang perlu diprioritaskan, saya menggunakan pendekatan "reading priority" sebagai patokan utama nama dan bio harus tetap jadi fokus utama di mobile, sementara elemen dekoratif (seperti .photo-block di belakang foto) saya biarkan menyesuaikan otomatis karena bukan elemen inti informasi. Saya juga banyak menggunakan clamp() pada ukuran font (misalnya di heading) supaya teks besar di desktop otomatis mengecil secara proporsional di layar sempit tanpa perlu menulis banyak media query terpisah.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?
Karena website ini murni HTML5/CSS3 tanpa backend atau database, saya merasakan beberapa batasan. Semua data (skill, riwayat pendidikan, project) harus saya tulis langsung di file HTML, sehingga setiap kali ada update saya harus mengedit kode secara manual dan melakukan deploy ulang. Ini kurang praktis untuk konten yang sifatnya akan terus berkembang seperti daftar project.
Batasan lain adalah tidak adanya interaktivitas berbasis data, seperti filter project berdasarkan kategorii atau form kontak yang benar-benar bisa mengirim pesan (form hanya bisa berupa tampilan visual atau menggunakan mailto sebagai solusi sementara).
Berdasarkan batasan ini, fungsionalitas dinamis yang paling ingin saya siapkan di iterasi berikutnya adalah menyimpan data project dan skill di database (menggunakan arsitektur MVT Django yang akan dipelajari di tutorial selanjutnya), sehingga saya bisa menambah atau mengedit konten portofolio melalui halaman admin tanpa perlu mengubah kode HTML secara langsung. Selain itu, saya juga ingin menambahkan form kontak yang benar-benar fungsional dan tersimpan ke database agar pengunjung bisa mengirim pesan langsung dari halaman portofolio.

## AI Disclosure

**Tools yang digunakan:** Claude Sonnet 5 (Anthropic)

**Strategi Prompting:**
Saya menggunakan AI bukan untuk generate kode secara langsung, melainkan sebagai *thinking partner* untuk merencanakan struktur kerja dan strategi Git terlebih dahulu. Alurnya:

1. Menanyakan breakdown tahapan kerja dan kapan idealnya commit dilakukan di tiap tahap, supaya riwayat commit mencerminkan progres bertahap sesuai rubrik penilaian.
2. Brainstorming konten apa yang relevan untuk section Skills, Education, dan Project berdasarkan latar belakang saya (mahasiswa CS, anggota tim robotika, hobi fotografi, pernah ikut lomba) yang kemudian saya sesuaikan dan tulis sendiri dengan data pribadi yang sebenarnya.
3. Menanyakan konvensi pesan commit yang tepat ketika saya perlu mengubah struktur HTML yang sudah ter-commit sebelumnya, termasuk cara memecah perubahan pada file yang sama menjadi commit terpisah menggunakan `git add -p`.

**Bagian yang dibantu AI:**
- Perencanaan urutan tahapan kerja dan strategi commit per section (HTML dulu → CSS → section berikutnya)
- Ide/arah konten apa yang relevan ditampilkan di Skills, Education, dan Project berdasarkan latar belakang saya
- Rekomendasi konvensi penamaan pesan commit (conventional commits) ketika saya perlu merevisi kode yang sudah ter-commit
- Troubleshooting error teknis di command line (seperti path error saat `git add`, CSS yang tidak ter-load karena belum di-commit/di-cache browser)

**Bagian yang dikerjakan manual:**
- Seluruh penulisan konten aktual 
- Eksekusi seluruh kode HTML dan CSS ke dalam file proyek
- Pengambilan keputusan desain visual (pemilihan grid vs flexbox, warna badge, layout timeline)
- Seluruh proses Git di terminal (checkout branch, staging, commit, push) dijalankan sendiri, termasuk saat menemukan masalah

**Refleksi Kritis terhadap Keterbatasan AI:**
Ada beberapa hal yang saya sadari selama proses ini:

1. *AI tidak bisa memvalidasi kondisi environment saya secara langsung.* Ketika saya menghadapi error seperti `pathspec did not match any files` atau CSS yang tidak muncul di browser, AI hanya bisa menebak kemungkinan penyebab berdasarkan pola umum (struktur folder Django, caching browser), tapi saya tetap harus menjalankan `git status`, `git log`, dan inspect DevTools sendiri untuk memastikan penyebab sebenarnya. Ini menunjukkan AI berguna untuk mempersempit kemungkinan, tapi verifikasi akhir tetap harus dilakukan manual di environment nyata.
2. *Saran struktur commit dari AI bersifat template, bukan sesuatu yang otomatis sesuai kondisi saya.* Misalnya saran awal untuk membuat branch terpisah per section (Skills/Education/Project) tidak saya ikuti mentah-mentah — saya putuskan menggabungkannya jadi satu branch fitur (`feature/skills-education-projects`) karena ketiganya bagian dari satu assignment yang sama, dan saya tetap menjaga histori commit tetap terpisah per section secara manual.
3. *AI tidak memiliki akses ke isi file saya secara real-time* sehingga ketika saya lupa meng-commit CSS Education, saya harus menyadari lewat `git log` bahwa ada tahapan yang terlewat dan AI baru bisa membantu setelah saya melaporkan kondisi sebenarnya lewat `git status`.

Dari proses ini saya belajar bahwa AI paling efektif digunakan sebagai *pemandu berpikir terstruktur* (breakdown tahapan, konvensi kerja) dan *alat diagnosis awal* untuk error, tapi eksekusi, verifikasi, dan pengambilan keputusan akhir tetap sepenuhnya berada di tangan saya.

**Log Chat:** https://claude.ai/share/8c66bd51-406d-40eb-a200-a62cea6c59b3

*Catatan: Beberapa prompt dalam log chat telah diedit ulang (menggunakan fitur edit message) untuk mengeksplorasi pertanyaan lain dalam sesi yang sama, sehingga tidak semua iterasi pertanyaan awal saya masih tersimpan dalam log akhir. Namun keseluruhan strategi dan hasil prompting yang saya jelaskan di atas mencerminkan proses yang sebenarnya saya lakukan.*