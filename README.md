# Altyazı Çeviri Otomasyon Aracı  
**Subtitle Translation Automation Tool**  

Bu Python programı, `.srt` ve `.ass` formatındaki altyazı dosyalarını toplu olarak çevirmek için kullanılır.  
This Python program is used to batch translate subtitle files in `.srt` and `.ass` formats.  

Program, **DeepLX API**'lerini kullanarak hızlı ve verimli çeviri yapar ve çevrilen dosyaları kaydeder. Ayrıca eşzamanlılık, hata yönetimi ve çeviri kayıt özellikleri içerir.  
The program utilizes **DeepLX APIs** for fast and efficient translation, saves the translated files, and includes concurrency, error handling, and logging features.

---

## Özellikler | Features  

- `.srt` ve `.ass` altyazı formatlarını destekler.  
  Supports `.srt` and `.ass` subtitle formats.  
- Eşzamanlı çeviri işlemleriyle hız sağlar.  
  Provides speed with concurrent translation operations.  
- Başarısız API isteklerini tespit eder ve optimize eder.  
  Detects and optimizes failed API requests.  
- Çevrilen dosyaları takip eder ve gereksiz çevirileri engeller.  
  Tracks translated files and prevents redundant translations.  
- Çeviri günlüklerini JSON formatında kaydeder.  
  Saves translation logs in JSON format.  

---

## Gereksinimler | Requirements  

- **Python 3.7+**  
- Gerekli Python kütüphaneleri:  
  - `httpx`  
  - `pysrt`  
  - `ass`  

Program eksik kütüphaneleri otomatik olarak yükler.  
The program automatically installs missing libraries.

---

## Kurulum | Installation  

1. Bu repository'i klonlayın:  
   Clone this repository:  
   ```bash
   git clone https://github.com/username/repository.git
   cd repository

## Kullanım | Usage  

### 1. Çalıştırma Komutunu Kullanma | Using the Run Command  

Programı çalıştırmak için aşağıdaki komutu kullanın:  
To run the program, use the following command:  

```bash""
python translate.py

## 2. Dosya Taraması ve Çeviri | File Scanning and Translation

- Program, çalışma dizinindeki tüm `.srt` ve `.ass` altyazı dosyalarını otomatik olarak tarar.  
  *The program automatically scans all `.srt` and `.ass` subtitle files in the working directory.*

- Uygun dosyalar çeviri işlemine alınır.  
  *Suitable files are processed for translation.*

---

## 3. Çevrilen Dosyaların Kaydedilmesi | Saving Translated Files

- Çevrilen dosyalar aynı dizine kaydedilir, dosya adı uzantısı dil kodunu içerecek şekilde güncellenir.  
  *Translated files are saved in the same directory, with the filename updated to include the language code.*

### Örnekler | Examples:

```plaintext
example.en.srt → example.tr.srt  
video.ass → video.tr.ass

## 4. Çalışma Akışı | Workflow

### Başlangıç | Start

- Program çalıştırıldığında, dizindeki mevcut altyazı dosyaları kontrol edilir.  
  *When the program runs, it checks for existing subtitle files in the directory.*

---

### Çeviri İşlemi | Translation Process

#### 1. **API Kullanımı | API Usage**

- DeepLX API'yi kullanarak metinleri çevirir.  
  *Translates texts using the DeepLX API.*  
- Başarısız API istekleri otomatik olarak yeniden denenir.  
  *Failed API requests are automatically retried.*

#### 2. **Dosya Formatlama | File Formatting**

- `.srt` ve `.ass` dosya biçimleri doğru bir şekilde işlenir.  
  *Properly processes `.srt` and `.ass` file formats.*

#### 3. **Günlükler | Logs**

- Çeviri bilgileri `translation_log.json` dosyasına kaydedilir.  
  *Translation details are saved in the `translation_log.json` file.*

---

### Çeviri Tamamlandığında | Upon Completion

- Başarıyla çevrilen dosyalar, hata oluşan dosyalardan ayrı olarak kaydedilir.  
  *Successfully translated files are saved separately from files with errors.*

- Program sonunda bir özet verir:  
  *At the end, the program provides a summary:*

  - **Çevrilen dosya sayısı**  
    *Number of translated files*  
  - **Atlanan veya hata veren dosyalar**  
    *Skipped or errored files*
