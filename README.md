Overview
This Python script is a sophisticated, asynchronous subtitle translation tool designed to automatically translate subtitle files (SRT and ASS formats) from English to Turkish using multiple DeepLX API endpoints.


# Subtitle Translation Automation Script

## Purpose
This script is designed to automatically translate subtitle files (SRT and ASS formats) from English to Turkish using multiple DeepLX API endpoints, making it easier to localize media content.

## Usage Instructions

### Prerequisites
- Python 3.8+
- Install required libraries: `httpx`, `pysrt`, `ass`

### How to Use
1. Place the script in the directory containing subtitle files
2. Run the script directly:
   ```
   python subtitle_translator.py
   ```

### Example Scenario
- Input: `movie_subtitle.en.srt`
- Output: `movie_subtitle.tr.srt`

## Features (Türkçe)

### Özellikler
- Otomatik altyazı çevirisi
- Birden fazla API endpoint desteği
- Eş zamanlı çeviri işleme
- Detaylı hata günlüğü
- Çeviri durumu takibi
- Farklı altyazı formatları desteği

## Features (English)

### Key Capabilities
- Automatic subtitle translation
- Multiple API endpoint support
- Concurrent translation processing
- Detailed error logging
- Translation status tracking
- Support for different subtitle formats

## Technical Details

### Translation Process
1. Detect subtitle files in the directory
2. Clean and extract text
3. Send text to DeepLX API
4. Translate in batches
5. Preserve original subtitle timing
6. Save translated subtitles

### API Management
- Intelligent API selection
- Performance tracking
- Cooldown mechanism
- Failure handling

## Example Workflow

```
Input Directory:
- movie1.en.srt
- series.en.ass
- documentary.en.srt

Running Script ->

Output Directory:
- movie1.tr.srt
- series.tr.ass
- documentary.tr.srt
```

## Limitations
- Requires local DeepLX API setup
- Limited to English to Turkish translation
- Dependent on API availability

## Recommended Use Cases
- Personal media library localization
- Subtitle translation for educational content
- Multilingual content preparation

## Performance Metrics
- Concurrent translations: Configurable
- API endpoint management
- Real-time progress tracking

## Configuration Options
- Modify `DEEPLX_API_URLS` for custom endpoints
- Adjust `MAX_CONCURRENT_TRANSLATIONS`
- Configure logging settings

## Potential Improvements
- Multi-language support
- Advanced caching
- More robust error handling
- Additional API provider integration

## Security Considerations
- Use secure API key management
- Implement rate limiting
- Handle API endpoint failures gracefully

## Contribution
Feel free to fork, improve, and submit pull requests to enhance the script's functionality.


# Altyazı Çeviri Otomasyonu Komut Dosyası

## Amaç
Bu komut dosyası, medya içeriğini yerelleştirmeyi kolaylaştırmak için DeepLX API uç noktalarını kullanarak altyazı dosyalarını (SRT ve ASS formatları) İngilizceden Türkçeye otomatik olarak çevirmeye tasarlanmıştır.

## Kullanım Talimatları

### Ön Gereksinimler
- Python 3.8+
- Gerekli kütüphaneleri yükleyin: `httpx`, `pysrt`, `ass`

### Nasıl Kullanılır
1. Komut dosyasını altyazı dosyalarını içeren dizine yerleştirin
2. Komut dosyasını doğrudan çalıştırın:
   ```
   python subtitle_translator.py
   ```

### Örnek Senaryo
- Girdi: `film_altyazi.en.srt`
- Çıktı: `film_altyazi.tr.srt`

## Özellikler

### Teknik Özellikler
- Otomatik altyazı çevirisi
- Birden fazla API uç noktası desteği
- Eş zamanlı çeviri işleme
- Detaylı hata günlüğü
- Çeviri durumu takibi
- Farklı altyazı formatları desteği

### Çeviri Süreci
1. Dizindeki altyazı dosyalarını tespit etme
2. Metni temizleme ve çıkarma
3. Metni DeepLX API'sine gönderme
4. Toplu çeviri yapma
5. Orijinal altyazı zamanlamasını koruma
6. Çevrilen altyazıları kaydetme

### API Yönetimi
- Akıllı API seçimi
- Performans takibi
- Bekleme mekanizması
- Hata işleme

## Örnek İş Akışı

```
Girdi Dizini:
- film1.en.srt
- dizi.en.ass
- belgesel.en.srt

Komut Dosyasını Çalıştırma ->

Çıktı Dizini:
- film1.tr.srt
- dizi.tr.ass
- belgesel.tr.srt
```

## Sınırlamalar
- Yerel DeepLX API kurulumu gerektirir
- Yalnızca İngilizceden Türkçeye çeviri
- API kullanılabilirliğine bağlıdır

## Önerilen Kullanım Alanları
- Kişisel medya kütüphanesi yerelleştirmesi
- Eğitim içeriği için altyazı çevirisi
- Çok dilli içerik hazırlama

## Performans Ölçümleri
- Eş zamanlı çeviriler: Yapılandırılabilir
- API uç noktası yönetimi
- Gerçek zamanlı ilerleme takibi

## Yapılandırma Seçenekleri
- Özel uç noktalar için `DEEPLX_API_URLS`'yi değiştirin
- `MAX_CONCURRENT_TRANSLATIONS`'ı ayarlayın
- Günlük kayıt ayarlarını yapılandırın

## Olası İyileştirmeler
- Çoklu dil desteği
- Gelişmiş önbellek
- Daha sağlam hata işleme
- Ek API sağlayıcı entegrasyonu

## Güvenlik Hususları
- Güvenli API anahtarı yönetimi
- Hız sınırlaması uygulama
- API uç nokta hatalarını zarif bir şekilde işleme

## Katkı
Çatallamak, geliştirmek ve pull request göndermek için çekinmeyin.

## Lisans
[Uygun Lisans Bilgisi]

## İletişim
Herhangi bir soru veya geri bildirim için info@rifat.org

## License
Open-source project - Contributions welcome!
