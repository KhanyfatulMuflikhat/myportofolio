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
- Section Experience — daftar pengalaman dengan filter berdasarkan kategori, serta Create, Update, dan Delete data yang dibatasi berdasarkan peran pengguna
- Section Achievement — daftar pencapaian dengan filter berdasarkan level (school/regional/national/international), serta Create, Update, dan Delete data yang dibatasi berdasarkan peran pengguna
- Autentikasi menggunakan sistem bawaan Django: registrasi (`/register/`), login (`/login/`), dan logout (`/logout/`), dengan status login ditampilkan di navbar
- Cookie kustom `last_login` yang mencatat waktu login terakhir dan ditampilkan di halaman Profile, lalu dihapus saat logout
- Otorisasi berbasis peran (pengunjung, pengguna biasa, Editor, pemilik portofolio) yang dicek di sisi server, dan tombol aksi disembunyikan di template bagi pengguna yang tidak berhak
- Fitur star pada Experience dan Achievement: pengguna yang sudah login dapat memberi atau membatalkan star (maksimal satu per pengguna), dengan jumlah total star dan status pengguna ditampilkan di tiap kartu
- Halaman Experience dan Achievement memuat datanya lewat AJAX (`fetch()`): halaman hanya merender kerangka (loading/error/empty state), lalu data diambil dari endpoint `api/experiences/` dan `api/achievements/` yang disusun manual dengan `JsonResponse`, termasuk jumlah star dan status star pengguna yang sedang login (field `starred_by` menampilkan username, bukan `id` internal database)
- Pencarian kata kunci dengan debouncing (300ms) pada Experience dan Achievement, digabung dengan filter kategori/level yang sudah ada; permintaan lama dibatalkan otomatis lewat `AbortController` saat permintaan baru dikirim
- Tombol pengurutan hasil berdasarkan jumlah star (Terbaru/Star) pada halaman Experience dan Achievement
- Form tambah data (Achievement, Experience) ditampilkan dalam modal berbasis Popover API pada halaman daftar, dikirim lewat `fetch()` ke endpoint `*-ajax/` yang memvalidasi dengan `ModelForm` dan membalas JSON beserta status HTTP (201/400/403); daftar diperbarui tanpa reload setelah data berhasil ditambahkan
- Perlindungan XSS dua lapis: `escapeHtml()` di JavaScript (`static/js/common.js`) sebelum data disisipkan ke `innerHTML`, dan `strip_tags()` pada method `clean_<field>` di `AchievementForm`/`ExperienceForm`
- Field `started_at` pada Experience dapat diisi manual dan ditampilkan sebagai rentang tanggal mulai-selesai pada tiap kartu
- Section Projects masih menggunakan pola Tugas 3/4 (render langsung dari template, belum AJAX) dan direncanakan mengikuti pola Experience/Achievement di atas pada iterasi berikutnya
- Notifikasi aksi (tambah/ubah/hapus/gagal) ditampilkan sebagai toast popup (`showToast`, dimuat dari `static/js/toast.js` lewat `base.html`)

## Tech Stack

- Django (backend server, routing, ORM, form handling)
- HTML5 (struktur semantik, template inheritance dengan `base.html`)
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

4. Jalankan migrasi database:
```bash
   python manage.py migrate
```

5. Buat akun pemilik portofolio (superuser):
```bash
   python manage.py createsuperuser
```

6. Buat peran Editor. Data grup tersimpan di database, bukan di kode, jadi langkah ini perlu dilakukan di setiap database baru:
   - Login sebagai superuser, lalu buka `http://127.0.0.1:8000/admin/` => **Groups** => **Add group**
   - Beri nama `Editor`
   - Pindahkan permission `main | achievement | Can change achievement` dan `main | experience | Can change experience` ke kolom *Chosen*, lalu simpan
   - Daftarkan akun biasa lewat `/register/`, lalu di Admin => **Users** buka akun tersebut dan tambahkan ke grup `Editor` (jangan centang *Staff status* maupun *Superuser*)

7. Jalankan development server:
```bash
   python manage.py runserver
```

8. Buka browser dan akses `http://127.0.0.1:8000/`

## Hak Akses Pengguna

| Peran | Melihat data | Memberi star | Mengubah data | Membuat / menghapus data |
|---|---|---|---|---|
| Pengunjung (belum login) | Ya | Tidak (dialihkan ke login) | Tidak (dialihkan ke login) | Tidak (dialihkan ke login) |
| Pengguna biasa | Ya | Ya | Tidak (403) | Tidak (403) |
| Editor | Ya | Ya | Ya | Tidak (403) |
| Pemilik portofolio (superuser) | Ya | Ya | Ya | Ya |

Implementasi:
- Peran Editor dibuat lewat Django `Group` bernama `Editor` yang memiliki permission `change_achievement` dan `change_experience`. View update dilindungi `@login_required` dan `@permission_required(..., raise_exception=True)`; superuser otomatis lolos karena memiliki semua permission.
- View create dan delete dilindungi `@login_required` dan pengecekan `request.user.is_superuser` yang melempar `PermissionDenied` (HTTP 403).
- View `toggle_star_achievement` dan `toggle_star_experience` hanya memerlukan login dan hanya memproses request `POST` dengan `{% csrf_token %}`.
- Di template, tombol Add hanya tampil untuk superuser, tombol Edit untuk pengguna dengan permission `change_*` (`perms`), tombol Delete hanya untuk superuser. Ini hanya mengatur tampilan; pembatasan sebenarnya tetap ada di view.


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

### Tugas 5

1. Debouncing adalah teknik menunda eksekusi sebuah fungsi sampai suatu jeda waktu tertentu berlalu tanpa event baru yang memicunya. Setiap kali event terjadi (misalnya tiap karakter yang diketik), timer yang sedang berjalan dibatalkan lewat `clearTimeout()` dan dimulai ulang dari nol. Fungsi yang ditunda baru benar-benar dijalankan kalau tidak ada event baru sampai durasi tunggu itu habis. Pada pencarian Achievement dan Experience di proyek ini, input `search-input` dipasangi event listener `input` yang memanggil `clearTimeout(searchDebounceTimer)` lalu `setTimeout(..., SEARCH_DEBOUNCE_DELAY)` dengan jeda 300ms. Tanpa debouncing, mengetik kata kunci seperti "Universitas" akan memicu sebelas kali permintaan `fetch()` ke `get_achievements_json`/`get_experiences_json`, satu untuk tiap karakter. Ini penting dihindari karena beberapa alasan, yakni beban server dan database bertambah akibat query `filter()` yang dijalankan berulang kali padahal sebagian besar hasilnya langsung dibuang dan permintaan yang dikirim lebih dulu bisa saja selesai belakangan (urutan respons jaringan tidak terjamin sama dengan urutan pengiriman) sehingga hasil yang tampil bisa jadi bukan untuk kata kunci terakhir. Risiko ini juga ditangani lewat `AbortController` yang membatalkan permintaan sebelumnya setiap kali permintaan baru dimulai dan dari sisi pengalaman pengguna, hasil pencarian yang berubah-ubah sangat cepat saat mengetik terasa berkedip dan mengganggu dibanding menunggu sebentar lalu menampilkan hasil yang stabil. Dengan debouncing, permintaan hanya dikirim satu kali setelah pengguna berhenti mengetik selama 300ms, bukan satu kali per karakter.

2. `fetch()` adalah fungsi asinkron yang langsung mengembalikan sebuah `Promise`, bukan hasil akhirnya, karena permintaan ke server butuh waktu dan JavaScript tidak boleh berhenti (blocking) menunggu jaringan. `await` dipakai di dalam fungsi `async` untuk "menjeda" eksekusi fungsi tersebut sampai `Promise` itu selesai lalu mengembalikan nilai akhirnya secara langsung, seolah-olah kode ditulis secara sinkron. Di `fetchAchievements()`, `fetchExperiences()`, dan fungsi `addAchievement()`/`addExperience()` pada proyek ini, `await fetch(...)` dipakai supaya baris-baris setelahnya, misalnya `if (!response.ok) throw new Error(...)` atau `const data = await response.json()`, baru dijalankan setelah respons dari server benar-benar diterima. `await` kedua pada `response.json()` juga diperlukan karena membaca body respons itu sendiri adalah operasi asinkron yang terpisah dari menerima header respons. Jika `await` tidak dipakai, variabel `response` akan berisi objek `Promise` sehingga `response.ok` atau `response.json()` akan error atau mengembalikan `undefined`. Kode setelah `fetch()` juga akan tetap berjalan duluan tanpa menunggu, sehingga logika seperti `gridContainer.innerHTML = ''` atau `showToast(...)` bisa dieksekusi sebelum data dari server benar-benar tersedia. Penanganan error lewat `try/catch` juga tidak akan menangkap kegagalan jaringan dengan benar, karena `Promise` yang gagal tanpa `await` menjadi *unhandled promise rejection* yang tidak pernah masuk ke `catch`. Singkatnya, `await` memastikan urutan eksekusi kode mengikuti urutan logis dari kirim permintaan, tunggu respons, lalu proses hasil, alih-alih berjalan semua sekaligus tanpa menunggu data benar-benar sampai.

3. Cross-Site Scripting (XSS) adalah serangan ketika penyerang berhasil menyisipkan kode JavaScript miliknya ke dalam halaman web, yang kemudian ikut dijalankan oleh browser pengguna lain seolah-olah kode itu bagian sah dari situs tersebut. Salah satu bentuknya adalah *stored XSS*: kode berbahaya disimpan ke database (misalnya lewat field `title` pada form Achievement atau Experience) lalu dieksekusi ulang setiap kali data itu ditampilkan ke pengguna lain, termasuk pengunjung yang belum login. Pada template Django biasa, setiap variabel yang dirender lewat `{{ variabel }}` otomatis di-*escape* oleh sistem *auto-escaping* bawaan Django di mana karakter seperti `<` dan `>` diubah menjadi `&lt;` dan `&gt;` dan ditampilkan sebagai teks biasa. Perlindungan otomatis ini hilang begitu data dipindahkan ke AJAX. Pada `buildAchievementCardElement()` dan `buildExperienceCardElement()` di proyek ini, data dari JSON disisipkan ke dalam template literal JavaScript lalu dipasang ke DOM lewat `articleElement.innerHTML = ...`. Tidak ada lagi Django yang ikut campur di titik ini.`innerHTML` memperlakukan string apa pun yang diberikan sebagai HTML sungguhan, termasuk tag dan atribut event handler seperti `onerror`. Kalau field `title` berisi `<img src="x" onerror="alert('XSS!')">`, browser akan mencoba memuat gambar dari `x`, gagal, lalu benar-benar menjalankan isi atribut `onerror` sebagai kode JavaScript. Risikonya nyata karena cookie `csrftoken` bisa dibaca oleh JavaScript apa pun yang berjalan di halaman itu, termasuk kode yang disisipkan lewat XSS, sehingga kode tersebut berpotensi mengirim permintaan `POST` atas nama korban (misalnya memberi star, atau menghapus data kalau korbannya superuser) tanpa sepengetahuan korban. Untuk itu, proyek ini menerapkan dua lapis perlindungan: fungsi `escapeHtml()` (di `static/js/common.js`) membungkus setiap nilai teks dari JSON sebelum disisipkan ke `innerHTML` sebagai pertahanan utama, dan method `clean_title`, `clean_issuer`, `clean_description` pada `AchievementForm`/`ExperienceForm` memanggil `strip_tags()` untuk membuang tag HTML sejak data divalidasi dan disimpan, sebagai lapisan tambahan di sisi server yang otomatis berlaku untuk jalur create biasa, update, maupun AJAX karena memakai form yang sama.

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

### Tugas 4

**Tools yang digunakan:** Claude Sonnet 5 (Anthropic)

**Strategi prompting:**
Saya membagikan teks tutorial dan kode asli saya (`views.py`, template, `base.html`, dan `README.md`) ke AI, lalu meminta perbandingan antara contoh di tutorial (yang memakai model `Project`) dengan struktur proyek saya (model `Achievement` dan `Experience`) sebelum menulis kode. Setelah itu saya meminta breakdown pengerjaan dan pesan commit per file untuk Tutorial 4 dan Individual Assignment 4.

**Bagian yang dibantu AI:**
- Memetakan pola tutorial (`@login_required`, `is_superuser`, `ManyToManyField`, `toggle_star`) dari `Project` ke `Achievement` dan `Experience`
- Review `views.py` yang menemukan bahwa `update_experience` belum dikunci, serta review `base.html` yang menemukan bahwa `{% block meta %}` di halaman form, login, dan register menghasilkan `<title>` ganda
- Usulan implementasi peran Editor lewat `Group` dan `Permission` beserta breakdown pengerjaan dan pesan commit
- Penjelasan mengapa login lewat `/admin/` tidak membuat cookie `last_login`

**Bagian yang dikerjakan manual:**
- Penulisan dan penerapan seluruh kode ke file proyek, serta keputusan mengganti `PROJECT_SECRET` dengan otorisasi berbasis akun
- Pembuatan grup Editor dan akun uji di Django Admin
- Pengujian manual untuk keempat peran di browser
- Seluruh proses Git di terminal

**Refleksi kritis terhadap keterbatasan AI:**
AI awalnya memakai contoh dari tutorial secara langsung, padahal struktur proyek saya berbeda (dua model, dan proteksi `PROJECT_SECRET` yang sudah ada), sehingga saya harus memutuskan sendiri apakah proteksi lama diganti atau digabung. AI juga tidak bisa melihat kondisi environment saya: kasus cookie `last_login` yang tidak muncul baru terjawab setelah saya melaporkan bahwa saya login lewat `/admin/`, dan kekurangan di `update_experience` baru ketahuan setelah saya membagikan `views.py` yang sebenarnya. Ini menegaskan bahwa saran AI harus diverifikasi terhadap kode dan perilaku aplikasi nyata.

**Log Chat:**

### Tugas 5

**Tools yang digunakan:** Claude Sonnet 5 (Anthropic)

**Strategi prompting:**
Saya membagikan materi Tutorial 5 (toast, AJAX list, debouncing, modal, XSS protection) ke AI, lalu meminta pola tersebut diadaptasi ke struktur proyek saya yang punya dua modul (Achievement dan Experience) alih-alih satu modul seperti contoh tutorial (Project). Setelah pola itu diterapkan, saya mengirim potongan kode yang sudah saya tulis sendiri untuk direview dan meminta saran perbaikan spesifik saat ada bug atau tampilan yang belum sesuai.

**Bagian yang dibantu AI:**
- Diagnosis penyebab search box tidak ter-styling (class CSS belum didefinisikan) dan field `started_at` yang awalnya tidak bisa diisi manual (field `auto_now_add`), termasuk penyebab tanggal tampil dengan komponen jam (`DateTimeField` vs `DateField`)
- Penambahan fitur pengurutan berdasarkan jumlah star sebagai fitur di luar checklist tutorial, serta perbaikan bug (baris `fetch` yang tertulis dua kali, variabel `renderGrid`/`lastFetchedData` yang dipakai sebelum didefinisikan) saat saya salah membuat kode secara manual
- Panduan penyelesaian git merge conflict dan git push yang ditolak (`non-fast-forward`) saat menyatukan riwayat branch fitur AJAX dengan branch yang sudah lebih dulu memiliki fitur Editor role dari Tugas 4
- Draf jawaban pertanyaan reflektif di atas

**Bagian yang dikerjakan manual:**
- Penulisan dan penerapan seluruh kode ke file proyek
- Menjalankan migrasi database dan pengujian manual di browser untuk keempat peran (pengunjung, pengguna biasa, Editor, superuser)
- Pengujian perlindungan XSS secara langsung dengan payload `<img src="x" onerror="alert('XSS!')">`
- Seluruh proses Git: commit granular per unit kerja, penyelesaian merge conflict, dan push ke remote

**Refleksi kritis terhadap keterbatasan AI:**
AI sering memiliki asumsi awal soal struktur field (misalnya tipe field `started_at`) yang beberapa kali meleset dan baru terkoreksi setelah saya melaporkan hasil `makemigrations --dry-run` dan screenshot tampilan aktual. Git merge conflict dan push yang ditolak juga hanya bisa diselesaikan setelah saya membagikan hasil `git log` dan `git fetch` yang sebenarnya karena AI tidak bisa melihat riwayat commit saya secara langsung. Ini menegaskan bahwa saran AI untuk tugas yang melibatkan eksekusi nyata (migrasi, testing lintas peran, git) tetap harus diverifikasi langkah demi langkah terhadap kondisi proyek yang sebenarnya, bukan diterima mentah-mentah.