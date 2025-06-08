
# Nurgul's Hamming SEC-DED Simülatörü

Bu proje, kullanıcıdan alınan 8, 16 veya 32 bitlik ikil veriyi **Hamming SEC-DED (Single Error Correction, Double Error Detection)** koduna dönüştüren ve sonrasında kullanıcıya hata ekleme/düzeltme işlemleri yapma imkanı tanıyan grafiksel bir simülasyondur.

##  Kullanılan Teknolojiler

- **Python**
- **tkinter** (GUI arayüz kütüphanesi)
- **random** kütüphanesi(random sayı üretmek için)


##  Kurulum

.py uzantılı kodu kopyalayıp kaydettikten sonra


**```bash**


**python secded.py**

şeklinde kodu kullandığınız ideye göre değişebilecek şekilde terminalden çalıştırabilirsiniz


## Nasıl Çalışır?

Arayüzde sırasıyla şu işlemler yapılır:

1. **Veri Girişi**
  Kullanıcıdan 8, 16 veya 32 bitlik bir ikili veri girişi yapılır (örneğin `10110011`).

2. **Hamming Kod Oluştur**
   Girilen veriden Hamming SEC-DED kodu oluşturulur. Parite bitleri ve genel parite hesaplanır.

3. **Hata Ekle**
   Hamming kodunun rastgele bir bitine hata eklenir (bit ters çevrilir).

4. **Hata Düzelt**
   Kod incelenerek tek hata varsa düzeltilir, çift hata varsa kullanıcıya bilgi verilir.


## Kodun Bazi Ana Fonksiyonları İçin Açıklama

### `encodeHamming()`

Kullanıcının girdiği binary veriden parite bitlerini ve genel kontrol bitini hesaplayarak Hamming kodu üretir.

### `decode()`

Hamming kodunu alarak:

* Hata olup olmadığını kontrol eder,
* Tekli hatayı bulup düzeltir,
* Çift hata varsa uyarı verir.

### `addError()`

Hamming kodunun rastgele bir pozisyonuna hata ekler (0 ↔ 1).

### `correct()`

Kod üzerinde hata varsa tespit eder ve düzeltilmiş halini gösterir.


##  Örnek Giriş/Çıkış

### Giriş:

Kullanıcı girişi: 10110011

### Encode Sonucu:

Oluşturulan Hamming Kodu: 011100101011011

### Hata Eklendikten Sonra:

Hata Eklenmiş Kod: 011100101111011 (örneğin 10. bit değiştirildi)

### Düzeltme:

Hata tespit edildi ve düzeltildi! Pozisyon: 10
Düzeltilmiş Kod: 011100101011011
Orijinal Veri: 10110011



## Geliştirici

**Nurgül Sarıtaş**


Bilgisayar Mühendisliği Öğrencisi

