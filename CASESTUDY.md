# Latar Belakang

File ini berisi deskripsi masalah dan langkah-langkah penyelesaian masalah program. Algoritma ini disusun oleh "tim Software" **(HARD QUOTE)** pada "Tim Pekerja Proyek Lab Indi" **(HARDER QUOTE)** (JS saja sih isinya, as you know), dalam proyek produk mini "SMS to WA Forwarder". Basis program nya adalah Python, tanpa antar muka.

# Checkpoint #1 : Memahami Sikap Modul SIM800 USB

Sikap yang dimaksud di sini adalah bagaimana cara kita (programmer) mengakses modul SIM800. Penulis sudah mencoba modul ini dalam 3 jenis kemasan yang berbeda :

1. Shield Arduino Uno
2. Modul Breakout Board Arduino
3. Modul USB Serial

Kesimpulan penulis per tanggal penulisan Case Study ini adalah, ketiganya mirip dalam penggunaan. Apapun yang kita ingin lakukan, semua berkutat di dalam _penulisan_ **AT COMMAND yang tepat**, dan _menangkap data Serial_ dari modul, yang merupakan **balasan dari AT COMMAND** tadi.

Hal ini adalah salah satu keunikan dari modul SIMx00, yaitu di mana pun kita mengakses nya, pola nya melibatkan _penulisan_ dan _penerimaan_ data serial.

Sebagai contoh, bila kita ingin mengatur konfigurasi agar modul SIM800 mengaktifkan mode "terima SMS", maka kita melakukan ini di Arduino: (buka contoh program di Daftar Pustaka poin 1.1.)
```c++
SIM800L.println("AT"); 
//Once the handshake test is successful, it will back to OK

SIM800L.println("AT+CMGF=1"); 
// Configuring TEXT mode

SIM800L.println("AT+CNMI=1,2,0,0,0");
//configuring Receive SMS mode and parameters needed
```

Di Python, perintah yang sama harus dituliskan sbb:

```python
SerialPort.write(b'AT\r');
SerialPort.write(b'AT+CMGF=1');
SerialPort.write(b'\r');
SerialPort.write(b'AT+CNMI=1,2,0,0,0');
SerialPort.write(b'\r');
```
Tidak jauh berbeda, bukan? Sebagai catatan, ```'\r'``` bisa digabung atau dipisah dalam satu fungsi ```write```. Pada contoh Arduino, kita tidak perlu menulis ```'\r'``` karena perintah yang kita gunakan adalah ```Serial.println```, yang melakukan penulisan serial _DAN_ menambahkan karakter "newline". Karakter "newline" ini dapat dipilih pada kotak diaog Serial Monitor Arduino, dalam contoh ini dipilih "Both NL / CR".

# Chekpoint #2 : Bentuk Pesan SMS
Pesan SMS yang dikirim dari Ponsel dikirim dalam satu balon percakapan, bukan? Kita sudah akrab dengan perilakunya. Misalnya, memisah baris per baris dengan tombol Enter, sehingga menjadi seperti ini :
```
aku tak biasaa
bila engkau tak di sisiku
aku tak biasaa bila ku tak mendengar
suaramu
```
Pesan ini, bila diterima oleh Modul SIM800, akan membuat modul melakukan pengiriman data serial ke program Python sebagai berikut:
```python
b'+CMT: "+6281xxxxxxxxx","","20/09/18,15:07:32+28"\r\n'
b'aku tak biasaa\n'
b'bila engkau tak di sisiku\n'
b'aku tak biasaa bila ku tak mendengar\n'
b'suaramu\r\n'
```
Satu baris mewakili satu variabel _binary_ milik Python (diawali dengan huruf ```b``` dan isi nya diapit kutip tunggal (```'```). Singkatnya, variabel _binary_ setara dengan string, tapi tanpa encoding (misal utf-8). 

Masalah berikutnya yang timbul adalah : **bagaimana caranya mengambil isi pesan nya saja**. Pada program ini, buffer yang dicetak ke console hanya memuat satu baris pesan saja. Pada contoh di atas, terdapat 5 kali pencetakan serial, yang artinya variabel buffer berubah isinya sebanyak 5 kali. 

Kalimat tebal tadi dapat disusun ulang sbb:<br/>
_Bagaimana cara kita melakukan pencuplikan cetakan console hanya jika 1 baris sebelumnya mengandung +CMT (status : ada sms masuk), dan terus lakukan pencuplikan hingga ditemukan_ ```'\r\n'``` _(perhatikan bahwa pada badan pesan, setiap enter diwakili dengan_ ```'\n'```, _sedangkan_ ```'\r\n'``` _adalah akhir badan pesan (dan juga akhir dari kiriman +CMT dari SIM800)._

Atau versi singkatnya: _bagaimana caranya mencuplik **hanya bagian badan pesan** dari keseluruhan badan respon SIM800 bila ada SMS masuk._

Semua ini tertuang di dalam codeblock loop yang diawali dengan
```python 
while True:
```
Variabel-variabel yang dilibatkan dalam logic adalah sbb: <br/>
1. ```SerialIn```, adalah variabel buffer yang menangkap pesan apapun yang diberikan SIM800 ke modul SerialPort Python. Akan diisi setiap kali ada pesan masuk, dan isinya dapat diakhiri dengan ```'\r'``` atau ```'\r\n'```
2. ```MsgBuffer```, adalah variabel buffer yang hanya diisi jika ```SerialIn``` merupakan **badan pesan**. Hanya diisi jika deskripsi memenuhi deskripsi masalah (cerita yang dimiringkan).
3. ```MsgFlag```, adalah "bendera" yang hanya bernilai ```True``` jika saat ini pesan sedang direkam (1 baris setelah +CMT, sampai baris yang ada ```'\r\n'```n ya).
4. ```MsgAvailable```, adalah "bendera" yang hanya bernilai ```True``` jika saat ini ada satu badan pesan di dalam ```MsgBuffer```. Setelah bendera ini ```True```, pesan langsung dikirimkan via WA, ```MsgBuffer``` dikosongkan, dan ```MsgFlag``` dibuat ```False```. 

# Chekpoint #3 : Selenium dan WebWhatsapp
Variabel MsgBuffer berisi pesan tadi hendak dikirimkan ke Whatsapp. Modul program Python yang bertindak menangani operasi Whatsapp otomatis adalah yang berbasis pustaka Selenium. Pustaka ini sebenarnya menangani "otomasi operasi browser", dan melakukan klik, ketik, dan drag otomatis.

Selenium diarahkan untuk memuat halaman Whatsapp Web yang membuka chat ke nomor ponsel tujuan yang dilewatkan sebagai argumen. Setelah chat ini terbuka, diketiklah seluruh isi badan pesan ```MsgBuffer```.

Karena sifat kotak chat yang mengirim pesan bila tombol Enter ditekan (setara dengan mengetik ```\n```), maka penekanan tombol diganti menjadi (```(Left)Shift + Enter```) setiap kali ditemukan ```\n```. Penggantian ini tidak diterapkan pada baris terakhir, karena memang baris terakhir menutup badan pesan dan mengirimkannya ke nomor tujuan.

# Daftar Pustaka
1. Pemrograman dasar SIM800L Breakout Board di Arduino:<br />
    1.1. https://lastminuteengineers.com/sim800l-gsm-module-arduino-tutorial/ <br />
    1.2. https://www.nyebarilmu.com/tutorial-arduino-mengakses-modul-gsm-sim800l/<br />
2. Pustaka Python pySerial <br/>
    2.1. https://github.com/pyserial/pyserial
3. Penanganan tipe data Python : mengubah bytes ke string. Bermanfaat dalam pengriman pesan ke jendela browser yang membuka WA <br/>
    3.1. https://stackoverflow.com/questions/606191/convert-bytes-to-a-string

