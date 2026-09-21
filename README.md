Nama : Khanyfatul Muflikhat  
NPM : 2506589755  
Kelas : PBP A  

# Portofolio Pribadi — Khanyfatul Muflikhat

Website portofolio pribadi berbasis Django, dibuat untuk memenuhi Tutorial dan Individual Assignment mata kuliah Pemrograman Berbasis Platform (PBP) Fakultas Ilmu Komputer, Universitas Indonesia.

## Deskripsi Proyek

Website ini menampilkan profil "About Me" beserta section tambahan: **Skills**, **Education**, **Projects**, **Experience**, dan **Achievements**.

**Fitur yang tersedia:**
- Section Profile — data diri, bio, dan tautan sosial media
- Section Skills
- Section Education — riwayat pendidikan dengan pencapaian di tiap institusi
- Section Projects
- Section Experience — daftar pengalaman (internship/research/volunteer/part-time/full-time/freelance) dengan filter berdasarkan kategori, serta Create, Update, dan Delete data yang dilindungi kode rahasia (`EXPERIENCE_SECRET`)
- Section Achievement — daftar pencapaian dengan filter berdasarkan level (school/regional/national/international), serta Create, Update, dan Delete data yang dilindungi kode rahasia (`ACHIEVEMENT_SECRET`)
- Seluruh data Experience dan Achievement tersedia dalam format JSON melalui endpoint `api/experiences/` dan `api/achievements/`, dan halaman tampilan (`show_experience`, `show_achievement`) memuat data dengan mengambil JSON tersebut lalu melakukan deserialisasi
- Notifikasi aksi (tambah/ubah/hapus/gagal) ditampilkan sebagai toast popup

## Tech Stack

- Django (backend server, routing, ORM, form handling)
- HTML5 (struktur semantik, template inheritance dengan `base.html`)
- CSS3 murni (grid, flexbox, custom properties, media query)
- python-dotenv (menyimpan kode rahasia di luar version control)

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

4. Buat berkas `.env` di root project dan isi kode rahasia untuk fitur Achievement dan Experience:
```bash
   ACHIEVEMENT_SECRET=kode_rahasia_achievement
   EXPERIENCE_SECRET=kode_rahasia_experience
```

5. Jalankan migrasi database:
```bash
   python manage.py migrate
```

6. Jalankan development server:
```bash
   python manage.py runserver
```

7. Buka browser dan akses `http://127.0.0.1:8000/`


## Pertanyaan Reflektif

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, dan `<footer>` untuk membangun struktur halaman. Setiap bagian konten yang berdiri sendiri secara topik saya bungkus dalam elemen `<section>` terpisah dengan `id` masing-masing, seperti `#profile`, `#skills`, `#education`, `#projects`. Elemen semantik ini membantu dalam beberapa hal. Pertama, struktur kode jadi lebih mudah dibaca dan dipahami tanpa harus membuka file CSS untuk mengidentifikasi tiap bagian. Kedua, penggunaan `id` pada tiap `<section>` memungkinkan saya membuat navigasi anchor link (`<a href="#skills">`) yang langsung mengarah ke bagian yang relevan sehingga meningkatkan usability halaman. Ketiga, elemen semantik juga membantu aksesibilitas dan SEO, karena browser dan screen reader bisa mengenali struktur dokumen dengan lebih baik dibandingkan hanya menggunakan `<div>` generik di semua tempat. Saya belum menggunakan `<article>` atau `<aside>` karena konten yang saya buat belum ada yang benar-benar independen secara konten (seperti artikel blog) atau bersifat suplemen di luar alur utama (seperti sidebar). Namun, saya berencana mempertimbangkan `<article>` untuk tiap item di section Projects jika nanti jumlah project bertambah, karena tiap project card sebenarnya bisa berdiri sendiri sebagai unit konten yang lengkap.

2. Tantangan terbesar yang saya temui ada pada bagian hero section, karena saya menggunakan `grid-template-areas` dengan tata letak dua kolom (identity/details di kiri, foto di kanan) yang perlu berubah menjadi satu kolom vertikal di layar mobile. Saya harus memikirkan ulang urutan elemen, seperti apakah foto harus tetap di atas nama atau dipindah ke bawah, supaya alur baca tetap masuk akal saat ditumpuk secara vertikal dan bukan sekadar mengecilkan ukurannya. Tantangan lain ada di section Education yang menggunakan tata letak timeline dengan garis vertikal dan titik penanda menggunakan `position: absolute`. Saat lebar layar mengecil, posisi titik dan padding kiri perlu disesuaikan ulang lewat media query, karena jika tidak, garis dan dot-nya bisa terlihat terlalu jauh atau terlalu dekat dengan teks. Untuk mengevaluasi elemen mana yang perlu diprioritaskan, saya menggunakan pendekatan "reading priority" sebagai patokan utama — nama dan bio harus tetap jadi fokus utama di mobile, sementara elemen dekoratif (seperti `.photo-block` di belakang foto) saya biarkan menyesuaikan otomatis karena bukan elemen inti informasi. Saya juga banyak menggunakan `clamp()` pada ukuran font (misalnya di heading) supaya teks besar di desktop otomatis mengecil secara proporsional di layar sempit tanpa perlu menulis banyak media query terpisah.

3. Karena website ini murni HTML5/CSS3 tanpa backend atau database, saya merasakan beberapa batasan. Semua data (skill, riwayat pendidikan, project) harus saya tulis langsung di file HTML, sehingga setiap kali ada update saya harus mengedit kode secara manual dan melakukan deploy ulang. Ini kurang praktis untuk konten yang sifatnya akan terus berkembang seperti daftar project. Batasan lain adalah tidak adanya interaktivitas berbasis data, seperti filter project berdasarkan kategori atau form kontak yang benar-benar bisa mengirim pesan (form hanya bisa berupa tampilan visual atau menggunakan `mailto:` sebagai solusi sementara). Berdasarkan batasan ini, fungsionalitas dinamis yang paling ingin saya siapkan di iterasi berikutnya adalah menyimpan data project dan skill di database sehingga saya bisa menambah atau mengedit konten portofolio melalui halaman admin tanpa perlu mengubah kode HTML secara langsung. Selain itu, saya juga ingin menambahkan form kontak yang benar-benar fungsional dan tersimpan ke database agar pengunjung bisa mengirim pesan langsung dari halaman portofolio.

### Tugas 2

1. Ketika pengguna membuka halaman portofolio baru (misalnya `/achievement/`), permintaan pertama kali diterima oleh `portofolio/urls.py`, yaitu konfigurasi URL di level proyek. Karena `portofolio/urls.py` menggunakan `include("main.urls")` pada awalan path kosong (`""`), permintaan tersebut diteruskan ke `main/urls.py`, yaitu konfigurasi URL milik aplikasi `main`. Di sana, Django mencocokkan path `achievement/` dengan pola URL yang terdaftar dan menemukan bahwa path tersebut dipetakan ke fungsi `show_achievement` di `main/views.py`. View ini kemudian mengambil seluruh data dari model `Achievement` menggunakan `Achievement.objects.all()`, yang menjalankan query ke database dan mengembalikan QuerySet berisi seluruh objek Achievement yang tersimpan. Data ini dimasukkan ke dalam sebuah dictionary bernama `context`, bersama data lain seperti nama pemilik portofolio. View lalu memanggil `render(request, "achievement.html", context)`, yang memproses berkas `templates/achievement.html` menggunakan Django Template Language. Di dalam template, sintaks `{% for achievement in achievement_list %}` melakukan perulangan terhadap setiap objek dalam QuerySet, menampilkan atribut seperti `title`, `issuer`, dan `description` menggunakan sintaks `{{ }}`. Hasil akhirnya berupa berkas HTML yang sudah terisi data, dikembalikan sebagai response ke browser pengguna. Dengan alur ini, `urls.py` proyek berperan sebagai pintu masuk yang mendistribusikan permintaan ke aplikasi yang sesuai, `urls.py` aplikasi memilih view yang tepat berdasarkan path, view bertugas mengambil dan menyiapkan data, model merepresentasikan struktur dan sumber data dari database, dan template bertanggung jawab murni pada presentasi tanpa perlu tahu bagaimana data itu diperoleh.

2. Data sebaiknya disimpan pada model, bukan ditulis langsung di template, karena template pada dasarnya hanya bertanggung jawab terhadap tampilan, bukan pengelolaan data. Jika data ditulis langsung di HTML, setiap kali ada penambahan, pengubahan, atau penghapusan data, saya harus mengedit berkas template secara manual, yang berisiko menimbulkan kesalahan ketik atau struktur HTML yang rusak. Dengan menyimpan data di model, penambahan data cukup dilakukan melalui Django Admin, shell, atau form, tanpa perlu menyentuh kode HTML sama sekali. Pendekatan ini juga membuat aplikasi lebih mudah dikembangkan ke depannya, misalnya jika suatu saat saya ingin menambahkan fitur pencarian, filter berdasarkan kategori, atau urutan berdasarkan tanggal, semua itu bisa dilakukan di level query pada view tanpa perlu mengubah template sama sekali. Pemisahan ini juga sejalan dengan prinsip pemisahan tanggung jawab (separation of concerns) dalam pola Model-View-Template: model mengurus struktur dan penyimpanan data, view mengurus logika pengambilan data, dan template murni mengurus presentasi. Selain itu, karena data tersimpan di database, saya bisa memvalidasi dan menguji perilaku aplikasi menggunakan unit test tanpa harus mengevaluasi tampilan HTML secara manual satu per satu.

3. `makemigrations` dan `migrate` adalah dua perintah yang saling melengkapi namun memiliki fungsi berbeda dalam proses migrasi model Django. `makemigrations` bertugas membaca perubahan yang saya buat pada berkas `models.py` (misalnya penambahan model baru, penambahan field, atau perubahan tipe data), lalu menerjemahkannya menjadi berkas migrasi berupa instruksi terstruktur yang disimpan di dalam folder `migrations/`. Perintah ini belum mengubah apa pun di database, ia hanya mencatat rencana perubahan. Sementara itu, `migrate` bertugas mengeksekusi instruksi dari berkas migrasi tersebut dan benar-benar menerapkan perubahan struktur ke database, misalnya membuat tabel baru atau menambahkan kolom pada tabel yang sudah ada. Contoh konkret dari Tugas 2 ini adalah ketika saya menambahkan model baru `Achievement` pada `main/models.py`. Setelah menuliskan model tersebut, saya menjalankan `python manage.py makemigrations`, yang menghasilkan berkas migrasi baru (`0002_achievement.py`) berisi instruksi untuk membuat tabel `Achievement` beserta seluruh field-nya seperti `title`, `issuer`, `level`, dan `date_achieved`. Namun pada tahap ini, tabel tersebut belum benar-benar ada di database. Barulah setelah saya menjalankan `python manage.py migrate`, Django membaca berkas migrasi tersebut dan benar-benar membuat tabel `Achievement` di database, sehingga saya bisa mulai menyimpan dan mengambil data `Achievement` melalui model tersebut.

### Tugas 3

1. Kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual karena `ModelForm` menghubungkan definisi field langsung ke model, sehingga validasi tipe data, batas panjang karakter, keberadaan `choices`, hingga status `required`/`blank` otomatis mengikuti aturan yang sudah didefinisikan sekali di `models.py`. Pada `AchievementForm` dan `ExperienceForm` yang saya buat, saya cukup menuliskan `class Meta: model = ..., fields = [...]`, dan Django otomatis menghasilkan input HTML yang sesuai tipe data tiap field (`CharField` jadi `<input type="text">`, `DateField` jadi input tanggal, field dengan `choices` jadi `<select>`, dan seterusnya) beserta validasi server-side-nya, tanpa saya perlu menulis ulang logika tersebut secara manual di form HTML biasa. Jika saya membuat form HTML manual, saya harus menulis sendiri setiap tag `<input>`, memvalidasi tipe dan panjang data di view secara manual, dan menjaga konsistensi antara field di form dan field di model setiap kali model berubah — risiko human error jauh lebih tinggi dan kode jadi lebih panjang serta rawan tidak sinkron. `ModelForm` juga menyediakan method siap pakai seperti `form.is_valid()` untuk validasi dan `form.save()` untuk langsung menyimpan data ke database sesuai instance model terkait, sehingga proses create maupun update data menjadi jauh lebih ringkas dan konsisten.

   Kita diwajibkan menambahkan `{% csrf_token %}` pada form karena Django secara default melindungi aplikasi dari serangan **Cross-Site Request Forgery (CSRF)**, yaitu serangan di mana pihak ketiga yang tidak berwenang mencoba mengirim request (misalnya POST untuk menambah atau menghapus data) atas nama pengguna yang sedang login, tanpa sepengetahuan pengguna tersebut, biasanya melalui situs atau form berbahaya di luar aplikasi kita. `{% csrf_token %}` menyisipkan sebuah token unik dan tersembunyi ke dalam form yang di-generate khusus untuk sesi pengguna tersebut. Saat form di-submit, Django akan memeriksa apakah token yang dikirim cocok dengan token yang tersimpan di sisi server/sesi. Jika token tidak ada atau tidak cocok, Django akan menolak request tersebut dengan error 403 Forbidden. Pada fitur Create, Update, dan Delete Achievement maupun Experience yang saya buat, seluruh form (termasuk form delete yang berbentuk modal) saya beri `{% csrf_token %}`, karena tanpa token ini permintaan POST yang mengubah data di database menjadi rentan dieksploitasi oleh pihak luar.

2. JSON (JavaScript Object Notation) lebih disukai dibandingkan XML dalam pengembangan aplikasi web modern karena beberapa alasan praktis. Pertama, dari segi sintaks, JSON jauh lebih ringkas — tidak memerlukan closing tag di setiap elemen seperti XML (`<title>...</title>` vs `"title": "..."`), sehingga ukuran payload data JSON umumnya lebih kecil dan lebih hemat bandwidth, terutama penting untuk aplikasi web dan mobile yang mengandalkan banyak request API. Kedua, JSON native terhadap JavaScript — karena strukturnya memang berasal dari object literal JavaScript, browser dapat langsung mem-parsing JSON menjadi objek JavaScript menggunakan `JSON.parse()` tanpa library tambahan, sementara XML memerlukan parser terpisah (`DOMParser`) yang lebih rumit untuk diproses menjadi struktur data yang bisa langsung digunakan. Ketiga, JSON lebih mudah dibaca manusia (human-readable) dan strukturnya secara alami memetakan ke struktur data umum seperti dictionary/object dan array/list yang digunakan di hampir semua bahasa pemrograman modern (Python, JavaScript, Java, dsb), sehingga proses serialize dan deserialize menjadi lebih intuitif. Keempat, ekosistem REST API modern (termasuk Django REST Framework dan `serializers.serialize("json", ...)` yang saya pakai di `get_achievements_json`/`get_experiences_json`) sudah dirancang berorientasi JSON sebagai format pertukaran data standar, sehingga tooling, dokumentasi, dan konvensi di industri lebih banyak mendukung JSON dibanding XML. XML sendiri masih dipakai di konteks tertentu yang butuh validasi struktur ketat (via XML Schema/DTD) atau sistem enterprise/legacy, tapi untuk kebutuhan pertukaran data web modern yang mengutamakan kecepatan dan kesederhanaan, JSON jadi pilihan yang lebih efisien.

3. Alur yang terjadi saat saya menggunakan fungsi view untuk mengembalikan data portofolio (misalnya Achievement) dalam bentuk JSON dimulai dari request GET ke endpoint `api/achievements/`, yang oleh `main/urls.py` dipetakan ke fungsi `get_achievements_json` di `main/views.py`. Di dalam fungsi ini, saya mengambil parameter query opsional (`?level=`) dari `request.GET`, lalu mengambil data dari database melalui `Achievement.objects.all()` dan memfilternya jika ada parameter `level`. Hasil query ini berupa QuerySet, yaitu kumpulan objek Python (instance model `Achievement`) yang belum bisa langsung dikirim sebagai response HTTP karena objek Python/instance model tidak memiliki format teks yang dipahami secara universal oleh klien di luar Python. Di sinilah proses **serialization** diperlukan: fungsi `serializers.serialize("json", achievements)` bawaan Django mengonversi setiap objek model tersebut menjadi struktur data JSON (teks) yang berisi nama model, primary key, dan seluruh field beserta nilainya. Hasil serialisasi ini kemudian dibungkus dalam `HttpResponse` dengan `content_type="application/json"` dan dikembalikan ke klien (browser, aplikasi lain, atau bisa juga dipanggil langsung oleh fungsi view lain seperti yang saya lakukan di `show_achievement`, yang memanggil `get_achievements_json` secara internal). Proses serialization ini wajib dilakukan karena database dan objek model Django hidup di sisi server dalam bentuk representasi internal Python/ORM yang tidak bisa dikirim langsung lewat jaringan HTTP; data tersebut harus diterjemahkan dulu menjadi format teks standar (di sini JSON) yang bisa ditransmisikan lewat HTTP dan dipahami/diproses ulang oleh penerima, baik itu browser (lewat `JSON.parse()`), aplikasi frontend lain, maupun — seperti pada kasus `show_achievement` — oleh view Django itu sendiri melalui proses kebalikannya, yaitu **deserialization** (`serializers.deserialize("json", ...)`), yang mengubah teks JSON tersebut kembali menjadi objek Python yang bisa diakses atributnya (`achievement.title`, dst.) dan ditampilkan lewat template.

## AI Disclosure

### Tugas 1

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
2. *Saran struktur commit dari AI bersifat template, bukan sesuatu yang otomatis sesuai kondisi saya.* Misalnya saran awal untuk membuat branch terpisah per section (Skills/Education/Project) tidak saya ikuti mentah-mentah di mana saya memutuskan untuk menggabungkannya menjadi satu branch fitur (`feature/skills-education-projects`) karena ketiganya bagian dari satu assignment yang sama, dan saya tetap menjaga histori commit tetap terpisah per section secara manual.
3. *AI tidak memiliki akses ke isi file saya secara real-time* sehingga ketika saya lupa meng-commit CSS Education, saya harus menyadari lewat `git log` bahwa ada tahapan yang terlewat dan AI baru bisa membantu setelah saya melaporkan kondisi sebenarnya lewat `git status`.

Dari proses ini saya belajar bahwa AI paling efektif digunakan sebagai *pemandu berpikir terstruktur* (breakdown tahapan, konvensi kerja) dan *alat diagnosis awal* untuk error, dengan eksekusi, verifikasi, dan pengambilan keputusan akhir tetap sepenuhnya berada di tangan saya.

**Log Chat:** https://claude.ai/share/8c66bd51-406d-40eb-a200-a62cea6c59b3

*Catatan: Beberapa prompt dalam log chat telah diedit ulang (menggunakan fitur edit message) untuk mengeksplorasi pertanyaan lain dalam sesi yang sama, sehingga tidak semua iterasi pertanyaan awal saya masih tersimpan dalam log akhir. Namun keseluruhan strategi dan hasil prompting yang saya jelaskan di atas mencerminkan proses yang sebenarnya saya lakukan.*

### Tugas 2

**Tools yang digunakan:** Claude Sonnet 5 (Anthropic)

**Strategi prompting:**
Saya menggunakan AI terutama sebagai pendamping proses berpikir dan debugging, bukan sebagai generator kode. Strategi yang saya pakai:
- Untuk bagian yang bersifat konseptual (misalnya alur routing Django, perbedaan `makemigrations` dan `migrate`), saya meminta penjelasan terlebih dahulu sebelum menulis kode, supaya saya memahami mengapa suatu langkah dilakukan, bukan sekadar meniru instruksi.
- Untuk permasalahan seputar Git yang cukup rumit (percabangan `main` vs `master` yang sempat tercampur, commit yang perlu diperbaiki, migrasi database lokal vs production), saya meminta AI menjelaskan konsekuensi setiap command sebelum saya jalankan.

**Bagian yang dibantu AI:**
- Debugging error deployment (`NotSupportedError` versi PostgreSQL, `CSRF verification failed` pada Django Admin di PWS)
- Penjelasan alur Git branching dan penyelesaian isu ketika kerja Tutorial 2 sempat berada di branch yang salah
- Logika filtering achievement berdasarkan level
- Penyusunan kerangka jawaban pertanyaan reflektif (lalu dikembangkan dan disusun secara pribadi)

**Bagian yang dikerjakan manual:**
- Verifikasi setiap perintah Git sebelum dijalankan
- Struktur model `Achievement`, `views.py`, `urls.py`, dan kerangka `achievement.html`
- Penyusunan konten template (`<header>`, `<footer>`, navigasi) agar konsisten dengan halaman lain yang telah saya buat sebelumnya
- Filtering achievement berdasarkan level
- Pengisian data `Achievement` yang sebenarnya (nama lomba, penyelenggara, deskripsi) melalui Django Admin
- Pengujian manual di browser (lokal dan production) untuk memastikan tidak ada bug sebelum dianggap selesai

**Refleksi kritis terhadap keterbatasan AI:**
AI membantu untuk mempercepat pemahaman konsep dan menyusun kerangka kode, tetapi ada beberapa keterbatasan yang saya sadari selama proses ini. Pertama, AI dapat membuat kesalahan kecil yang mudah lolos jika tidak dicek (seperti memberikan command git yang tidak sesuai kebutuhan). Kedua, AI dapat melakukan simplifikasi tahap yang justru dapat menimbulkan error (seperti tidak melakukan migrasi atau tidak mengikutkan proses testing dalam breakdown tahapan pengerjaan tugas 2). Ketiga, AI tidak dapat memberikan ide original mengenai pengembangan web yang sesuai dengan kondisi serta keinginan pengembang.

### Tugas 3

**Tools yang digunakan:** Claude Sonnet 5 (Anthropic)

**Strategi prompting:**
Untuk Tugas 3, saya menggunakan AI terutama untuk dua hal: (1) menyusun breakdown pekerjaan yang granular per commit sebelum saya mulai menulis kode, dan (2) meminta review terhadap kode `views.py`, `urls.py`, dan `forms.py` yang sudah ada agar saya tahu bagian mana yang belum rapi atau kurang efisien sebelum saya replikasi pola yang sama ke modul Experience. Saya sengaja membagikan kode asli (`models.py`, `views.py`, `urls.py`, `forms.py`, dan template) ke AI supaya breakdown dan review yang diberikan sesuai dengan konvensi penamaan dan struktur yang sudah saya pakai, bukan sekadar pola generik.

**Bagian yang dibantu AI:**
- Breakdown tahapan kerja dan pesan commit granular untuk melengkapi fitur `update_achievement`
- Breakdown tahapan kerja dan pesan commit granular untuk mengubah Experience menjadi modul penuh (form, filter, password protection, JSON delivery) mengikuti pola Achievement
- Review kode yang sudah ada untuk menemukan bagian yang kurang rapi/efisien (import ganda di `forms.py`, `form.save(commit=False)` yang tidak perlu, data profil yang di-hardcode berulang, konsistensi penamaan parameter URL)
- Penyusunan kerangka jawaban pertanyaan reflektif (lalu dikembangkan dan disusun secara pribadi berdasarkan pemahaman saya sendiri terhadap kode yang sudah saya tulis)

**Bagian yang dikerjakan manual:**
- Penulisan seluruh kode `update_achievement`, `create_experience`, `update_experience`, `delete_experience`, `get_experiences_json`, dan refactor `show_experience` ke dalam file proyek
- Penyesuaian saran AI dengan kode asli saya (misalnya penamaan parameter `achievement_id`/`experience_id` agar konsisten dengan yang sudah saya buat sebelumnya)
- Pengujian manual tiap fitur (create, update, delete, filter, JSON endpoint) di browser lokal
- Menjalankan `python manage.py test` di tiap checkpoint sesuai catatan kehati-hatian yang sudah saya susun sendiri
- Keputusan akhir mana masukan AI yang diterapkan dan mana yang disesuaikan dengan struktur proyek saya

**Refleksi kritis terhadap keterbatasan AI:**
Karena Tugas 3 melibatkan replikasi pola dari Achievement ke Experience, saya menyadari AI cenderung menghasilkan kode berdasarkan pola yang terlihat konsisten di permukaan, tapi tetap bisa meleset kalau saya tidak membagikan kode asli secara lengkap. Misalnya saran awal sebelum saya upload `views.py`/`urls.py` masih menggunakan asumsi nama parameter (`id`) yang ternyata berbeda dengan konvensi yang sudah saya pakai (`achievement_id`). Ini menegaskan bahwa AI sangat bergantung pada konteks yang saya berikan, dan tanggung jawab untuk memverifikasi kesesuaian saran dengan kode nyata tetap ada di tangan saya. Selain itu, catatan "Hal-Hal yang Harus Hati-Hati" yang saya tulis sendiri di awal proses (migration di PWS, konsistensi nama context variable, testing di tiap checkpoint, branch `master` tidak boleh langsung dikembangkan) justru menjadi acuan yang saya gunakan untuk mengevaluasi apakah breakdown dari AI sudah menjawab risiko-risiko tersebut atau belum — bukan sebaliknya. Ini menunjukkan bahwa refleksi dan pengalaman saya sendiri dari tahap sebelumnya penting untuk menilai kualitas saran AI, bukan menerima breakdown tersebut begitu saja.