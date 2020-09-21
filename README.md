# sms_to_wa
Program sederhana untuk meneruskan pesan searah, dari SMS ke WA Web.

## Setup Software (VSCode)
1. Clone (atau download zip)
2. Buka main.py, dan pastikan file ini yang aktif pada jendela VSCode.
3. Ketik di terminal : ```pip install pyserial``` dan ```pip install selenium```
4. Tekan F5 (konfigurasi run Current File, dengan environment python default komputer)

## Setup Software (PyCharm)
1. Clone (atau download zip)
2. Pastikan ```pyserial``` dan ```selenium``` telah terpasang pada Python Interpreter yang digunakan pada project ini.
3. Buat Configuration baru, dengan Run, dan pilih main.py sebagai script yang di run.
4. Tekan Shift+F10, atau tekan tombol Run (tulisannya, atau tekan tombol Play hijau) di kanan atas window PyCharm.

## Setup Hardware
1. Buka config.py, dan  sesuaikan konfigurasi COM PORT, BAUDRATE, dan TIMEOUT sesuai konfigurasi modul SIM800L USB yang terpasang.
2. Masih di config.py, ubah PHONE_NUMBER sesuai nomor ponsel target
3. Jangan ubah TEXT_ENCODING, kecuali ingin dilakukan eksperimen. ```'utf-8'``` adalah encoding teks default yang digunakan.
4. Ketika browser terpilih dibuka, siapkan ponsel dengan mode Whatsapp Web login (Scan QR Code). Pastikan login WA selesai sebelum mengirim SMS, atau program akan crash karena Selenium gagal mengklik elemen-elemen terprogram.

# Keterangan terkait program
Berikut adalah penjelasan singkat terkait program.

## Struktur Folder dan File

1. Folder ```/.vscode``` berisi launch.json, yang mengatur apa yang terjadi bila kita melakukan Run Configuration (F5).
2. Folder ```/main``` adalah folder utama program.
3. Folder ```/standalones``` adalah folder berisi snippet-snippet program terpisah yang dipakai untuk menyusun program utama. 

## Pustaka Python yang digunakan

Versi Interpreter Python : 3.8.5

1. pySerial (```import serial```)<br />
    digunakan untuk melakukan pembacaan/penulisan data dari/ke device USB di COM tertentu.
2. Selenium (```import selenium```, atau ```from selenium import ...```)<br />
    digunakan untuk melakukan otomasi browser (dalam contoh ini digunakan Firefox)
3. Selenium memerlukan geckodriver.exe (Firefox) atau chromedriver.exe (Chrome). Pastikan salah satu dari file exe ini satu folder dengan folder root (dalam project ini : ```./main```)


## Changelog
Lihat CHANGELOG.md.

## Useful Sources: 
Silakan cek file CASESTUDY.md untuk mengetahui sumber di balik trik-trik pemrograman yang telah dipelajari.
