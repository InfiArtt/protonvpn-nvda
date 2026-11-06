# Aksesibilitas Proton VPN untuk NVDA

[Read in English](../README.md)

Aksesibilitas Proton VPN adalah add-on untuk [pembaca layar NVDA](https://www.nvaccess.org/) yang membuat
aplikasi Proton VPN untuk Windows bisa dipakai dengan NVDA. Banyak tombol, opsi, dan tab di Proton VPN tidak
punya nama, sehingga NVDA hanya mengucapkan "tombol". Add-on ini memberi nama pada kontrol-kontrol itu,
membacakan pengaturan beserta statusnya, dan memberi tahu Anda saat perlindungan berubah.

Add-on ini dibuat oleh InfiArtt, bukan dibuat atau didukung oleh Proton AG.

## Awal mula add-on ini

Saya Rafli, pengguna NVDA sehari-hari. Waktu saya memasang Proton VPN di Windows, banyak bagiannya yang sulit
dipakai: NVDA hanya mengucapkan "tombol" untuk sebagian besar jendela utama, opsi pengaturan tidak punya nama,
dan tab negara membacakan nama internal yang panjang.

Jadi saya membuka [NVDA MCP](https://github.com/InfiArtt/nvda-mcp), add-on kami yang memungkinkan asisten AI melihat
apa yang dilihat NVDA, lalu menjelajahi Proton VPN bersama Claude Code, asisten pemrograman berbasis AI. Lewat
NVDA MCP, Claude Code membaca pohon aksesibilitas Proton VPN, mendaftar setiap kontrol yang tidak bisa dinamai
NVDA, membuka setiap halaman pengaturan dan flyout untuk melihat apa yang kurang, lalu menulis perbaikannya. Setiap
perubahan langsung kami muat ke NVDA yang sedang berjalan dan kami cek apa yang akan diucapkan NVDA sebelum lanjut,
sampai seluruh aplikasi terbaca dengan baik. Sesi itulah yang menjadi add-on ini.

## Apa yang dilakukan

- **Memberi nama kontrol yang tidak berlabel.** Settings, NetShield, Kill switch, Port forwarding, Split
  tunneling, dan Menu di bilah judul dibacakan namanya. Setiap negara, kota, dan profil punya tombol "Sambungkan ke",
  "Server di", dan "Opsi lain untuk".
- **Membacakan nilai beserta labelnya.** NVDA mengucapkan "VPN IP, 159.26.115.101" dan "Server load, 22%",
  bukan hanya angkanya. "Current traffic" membacakan kecepatan unduh dan unggah tanpa angka sumbu grafik.
- **Membacakan pengaturan beserta statusnya.** Di Settings, NVDA mengucapkan "Kill switch, Off" dan
  "Protocol, Smart".
- **Memberi nama opsi.** Opsi protokol, level NetShield, jenis NAT, dan driver jaringan punya nama. Protokol yang
  muncul dua kali menyebutkan kelompoknya, misalnya "WireGuard, Reliability (TCP)".
- **Menambahkan penjelasan.** Opsi dan sakelar mendapat penjelasan dari Proton VPN sebagai deskripsi. NVDA
  membacakan deskripsi jika "Laporkan deskripsi objek" aktif, di pengaturan Presentasi Objek NVDA.
- **Membacakan flyout dan pesan saat terbuka.** Menekan VPN IP, Server load, atau tombol informasi Profiles
  membacakan seluruh isi flyout, bukan hanya tautan di dalamnya.
- **Mengumumkan perubahan perlindungan.** Saat Proton VPN menampilkan Protected, Unprotected, atau Connecting
  ketika jendelanya aktif, NVDA mengucapkannya.
- **Membuat baris pengaturan bisa diaktifkan lewat NVDA.** Baris seperti Protocol dan NetShield sekarang terbuka
  saat diaktifkan dari navigasi objek, tidak hanya dengan Enter.
- **Memperbaiki nama.** Tab negara dan judul daftar tidak lagi membacakan nama internal seperti
  "ProtonVPN.Client.UI.Main…ViewModel".

## Perintah

| Perintah | Tombol | Fungsi |
|---|---|---|
| Laporkan status Proton VPN | NVDA+Shift+V | Mengucapkan apakah Anda terlindungi, server yang tersambung, dan sudah berapa lama. Berfungsi saat jendela Proton VPN aktif. |

Tombolnya bisa diubah di menu NVDA: Preferensi, Gestur input, kategori Proton VPN.

## Kebutuhan

- NVDA 2025.1 atau lebih baru. Diuji dengan NVDA 2026.3.
- Proton VPN untuk Windows versi 5. Diuji dengan versi 5.1.9.

## Cara memasang

1. Unduh `protonVpnAccess-<versi>.nvda-addon` terbaru dari
   [Releases](https://github.com/InfiArtt/protonvpn-nvda/releases), atau pasang Aksesibilitas Proton VPN dari
   Add-on Store NVDA setelah tersedia di sana.
2. Buka filenya. NVDA akan bertanya apakah add-on ini mau dipasang; pilih Ya.
3. Mulai ulang NVDA saat diminta.

## Batasan yang diketahui

- Add-on ini membacakan teks milik Proton VPN, jadi nama mengikuti bahasa Proton VPN. Kata yang ditambahkan
  add-on, seperti "Sambungkan ke", mengikuti bahasa NVDA.
- Proton VPN bisa mengubah tampilannya saat diperbarui. Jika sebuah kontrol tidak lagi terbaca dengan benar
  setelah pembaruan, silakan [buka issue](https://github.com/InfiArtt/protonvpn-nvda/issues) dan sebutkan versi
  Proton VPN yang Anda pakai.

## Melaporkan masalah

Buka issue di [github.com/InfiArtt/protonvpn-nvda/issues](https://github.com/InfiArtt/protonvpn-nvda/issues).
Sebutkan apa yang Anda tekan, apa yang diucapkan NVDA, dan apa yang seharusnya diucapkan, beserta versi NVDA dan
Proton VPN Anda.

## Lisensi

Hak cipta (C) 2026 InfiArtt. Add-on ini adalah perangkat lunak bebas di bawah GNU General Public License versi 2
atau yang lebih baru. Lihat [COPYING.txt](../COPYING.txt).
