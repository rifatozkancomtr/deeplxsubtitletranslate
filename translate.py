import sys
import subprocess
import importlib.util
import os
import json
import warnings
import re
import time
from datetime import timedelta, datetime
import asyncio
import logging
import httpx
import random

# Gerekli kütüphanelerin listesi
required_packages = {
    'httpx': 'httpx',
    'pysrt': 'pysrt',
    'ass': 'ass',
}

def check_and_install_packages():
    missing_packages = []
    for package, pip_name in required_packages.items():
        if importlib.util.find_spec(package) is None:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("Eksik kütüphaneler yükleniyor...")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("Tüm gerekli kütüphaneler yüklendi.")
    else:
        print("Tüm gerekli kütüphaneler mevcut.")

# Kütüphaneleri kontrol et ve gerekirse yükle
check_and_install_packages()

import pysrt
import ass

# Uyarıları bastır
warnings.filterwarnings("ignore", category=UserWarning)

# DeepLX API ayarları
DEEPLX_API_URLS = [
    "http://192.168.1.120:1187/v2/translate",
    "http://192.168.1.120:1189/v2/translate",
    "http://192.168.1.120:1186/v2/translate",
    "http://192.168.1.120:1184/v2/translate",
    "http://192.168.1.120:1183/v2/translate",
    "http://192.168.1.120:1185/v2/translate",
    "http://192.168.1.120:1188/v2/translate",
    "http://192.168.1.120:1191/v2/translate",
    "http://192.168.1.120:1192/v2/translate",
    "http://192.168.1.120:1193/v2/translate"
]
API_KEY = "1"  # API anahtarı

# API durumlarını takip etmek için bir sözlük
api_status = {url: {
    'last_used': None,
    'cooldown_until': None,
    'in_use': False,
    'success_count': 0,
    'failure_count': 0,
    'average_response_time': 0
} for url in DEEPLX_API_URLS}

# Eşzamanlı çeviri sınırı
MAX_CONCURRENT_TRANSLATIONS = 4
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TRANSLATIONS)

# Logging ayarları
def setup_logger(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(log_dir)
    logger.setLevel(logging.ERROR)
    
    file_handler = logging.FileHandler(os.path.join(log_dir, 'error.log'))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    return logger

# Çeviri log dosyası
def get_translation_log_file(directory):
    return os.path.join(directory, 'translation_log.json')

def load_translation_log(directory):
    log_file = get_translation_log_file(directory)
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_translation_log(log, directory):
    log_file = get_translation_log_file(directory)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def get_api_status(api_url):
    status = api_status[api_url]
    current_time = datetime.now()
    
    if status['in_use']:
        duration = (current_time - status['last_used']).total_seconds()
        return f"Kullanımda: {duration:.0f} saniye"
    elif status['cooldown_until'] and current_time < status['cooldown_until']:
        remaining = (status['cooldown_until'] - current_time).total_seconds()
        return f"Bekleme süresi: {remaining:.0f} saniye kaldı"
    else:
        return "Hazır"

def select_best_api():
    available_apis = [api for api, status in api_status.items() 
                      if not status['in_use'] and (status['cooldown_until'] is None or datetime.now() > status['cooldown_until'])]
    
    if not available_apis:
        return None
    
    # API'leri başarı oranı ve ortalama yanıt süresine göre sırala
    sorted_apis = sorted(available_apis, key=lambda api: (
        api_status[api]['success_count'] / (api_status[api]['success_count'] + api_status[api]['failure_count'] + 1),
        -api_status[api]['average_response_time']
    ), reverse=True)
    
    # En iyi API'yi seç, ancak bazen rastgele seçim yap
    if random.random() < 0.1:  # %10 olasılıkla rastgele seçim
        return random.choice(available_apis)
    else:
        return sorted_apis[0]

async def translate_batch(texts):
    async with httpx.AsyncClient() as client:
        attempt = 0
        while True:
            api_url = select_best_api()
            
            if api_url is None:
                # Tüm API'ler soğumadaysa, en kısa sürede hazır olacak API'yi bekle
                min_cooldown = min(status['cooldown_until'] for status in api_status.values() if status['cooldown_until'])
                wait_time = (min_cooldown - datetime.now()).total_seconds()
                if wait_time > 0:
                    print(f"Tüm API'ler soğumada. {wait_time:.2f} saniye bekleniyor...")
                    await asyncio.sleep(wait_time)
                continue
            
            try:
                api_status[api_url]['in_use'] = True
                api_status[api_url]['last_used'] = datetime.now()
                
                start_time = time.time()
                
                data = {
                    "text": texts,
                    "target_lang": "TR",
                    "source_lang": "EN",
                    "auth_key": API_KEY
                }
                response = await client.post(url=api_url, json=data, timeout=30.0)
                response.raise_for_status()
                
                end_time = time.time()
                response_time = end_time - start_time
                
                response_data = response.json()
                
                if 'translations' in response_data:
                    # Başarılı çeviri
                    api_status[api_url]['success_count'] += 1
                    api_status[api_url]['average_response_time'] = (
                        (api_status[api_url]['average_response_time'] * (api_status[api_url]['success_count'] - 1) + response_time)
                        / api_status[api_url]['success_count']
                    )
                    return [t['text'] for t in response_data['translations']]
                else:
                    raise ValueError(f"Geçersiz API yanıtı: {response_data}")
                
            except (httpx.HTTPError, ValueError) as e:
                attempt += 1
                wait_time = attempt * 10  # Her denemede 10 saniye artarak bekle
                error_msg = f"Hata (API: {api_url}, Deneme {attempt}, Bekleme süresi: {wait_time} saniye): {e}"
                print(error_msg)
                logging.error(error_msg)
                
                # API'yi dinlenmeye al ve başarısızlık sayısını artır
                api_status[api_url]['cooldown_until'] = datetime.now() + timedelta(seconds=wait_time)
                api_status[api_url]['failure_count'] += 1
                print(f"API {api_url} {wait_time} saniye dinlenmeye alındı.")
                
                # Bekleme süresi kadar bekle
                await asyncio.sleep(wait_time)
                
            finally:
                api_status[api_url]['in_use'] = False

def extract_text(subtitle):
    text = re.sub(r'<.*?>', '', subtitle)
    text = re.sub(r'{.*?}', '', text)
    text = text.replace('\\N', ' ')
    return text.strip()

def get_new_filename(file_path):
    base_name = os.path.basename(file_path)
    name_parts = base_name.split('.')
    
    if 'tr' in [part.lower() for part in name_parts]:
        return base_name
    
    name_parts = [part for part in name_parts if part.lower() != 'en']
    extension = name_parts.pop()
    new_name = '.'.join(name_parts + ['tr', extension])
    
    return new_name

def print_progress_bar(progress, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
    filled_length = int(length * progress // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    return f"{prefix} |{bar}| {percent}% {suffix}"

async def translate_subtitle_file(file_path, subtitle_type, translation_log, logger, script_directory):
    async with semaphore:
        file_identifier = os.path.relpath(file_path, start=script_directory)
        if file_identifier in translation_log:
            print(f"Bu dosya daha önce çevrilmiş: {file_path}")
            return None

        try:
            if subtitle_type == 'srt':
                subs = pysrt.open(file_path, encoding='utf-8-sig')
            elif subtitle_type == 'ass':
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    subs = ass.parse(f)
        except UnicodeDecodeError:
            try:
                if subtitle_type == 'srt':
                    subs = pysrt.open(file_path, encoding='utf-8')
                elif subtitle_type == 'ass':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        subs = ass.parse(f)
            except UnicodeDecodeError:
                if subtitle_type == 'srt':
                    subs = pysrt.open(file_path, encoding='iso-8859-9')
                elif subtitle_type == 'ass':
                    with open(file_path, 'r', encoding='iso-8859-9') as f:
                        subs = ass.parse(f)
        
        total_subs = len(subs if subtitle_type == 'srt' else subs.events)
        translated_subs = 0
        start_time = time.time()
        
        print(f"\nÇevirisi yapılan dosya: {os.path.basename(file_path)}")
        print()  # Dosya adı ve ilerleme çubuğu arasına eklenen boş satır
        
        for sub in (subs if subtitle_type == 'srt' else subs.events):
            original_text = sub.text if subtitle_type == 'srt' else sub.text
            clean_text = extract_text(original_text)
            
            if clean_text:
                translated_text = await translate_batch([clean_text])
                
                if translated_text is None:
                    error_msg = "Çeviri başarısız oldu. İşlem durduruluyor."
                    print(error_msg)
                    logger.error(error_msg)
                    return None
                
                sub.text = translated_text[0]
                translated_subs += 1
                
                elapsed_time = time.time() - start_time
                estimated_time = (elapsed_time / translated_subs) * (total_subs - translated_subs)
                estimated_time_str = str(timedelta(seconds=int(estimated_time)))
                
                progress = print_progress_bar(translated_subs, total_subs, prefix='Çeviri İlerlemesi:', 
                                              suffix=f'Tamamlandı - Tahmini kalan süre: {estimated_time_str}', length=50)
                print(f"\r{progress}", end='', flush=True)
        
        print()  # Yeni satır ekle
        
        new_file_name = get_new_filename(file_path)
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        
        if subtitle_type == 'srt':
            subs.save(new_file_path, encoding='utf-8-sig')
        elif subtitle_type == 'ass':
            with open(new_file_path, 'w', encoding='utf-8-sig') as f:
                subs.dump_file(f)
        
        translation_log[file_identifier] = {
            'original_file': os.path.basename(file_path),
            'translated_file': os.path.basename(new_file_path)
        }
        
        # Her çeviri tamamlandığında JSON dosyasını güncelle
        save_translation_log(translation_log, script_directory)
        
        return new_file_path

async def translate_directory(directory):
    translation_log = load_translation_log(directory)
    logger = setup_logger(directory)

    subtitle_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.srt', '.ass')) and ".tr." not in file.lower():
                subtitle_files.append(os.path.join(root, file))

    total_subtitles = len(subtitle_files)
    translated_subtitles = sum(1 for file in translation_log)
    remaining_subtitles = total_subtitles - translated_subtitles

    print(f"Toplam altyazı sayısı: {total_subtitles}")
    print(f"Çevirisi tamamlanan altyazı sayısı: {translated_subtitles}")
    print(f"Çevirilecek altyazı sayısı: {remaining_subtitles}")

    tasks = []
    for file_path in subtitle_files:
        subtitle_type = 'srt' if file_path.endswith('.srt') else 'ass'
        tasks.append(translate_subtitle_file(file_path, subtitle_type, translation_log, logger, directory))

    results = await asyncio.gather(*tasks)

    for file_path, result in zip(subtitle_files, results):
        if result:
            print(f"Çeviri tamamlandı. Yeni dosya: {result}")
        elif result is None:
            print(f"Dosya zaten çevrilmiş veya çeviri başarısız oldu: {file_path}")

async def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Taranacak ana dizin: {script_directory}")
    print(f"Hedef dil: TR")
    print(f"Aynı anda çevrilecek maksimum altyazı sayısı: {MAX_CONCURRENT_TRANSLATIONS}")
    print("Kullanılacak API URL'leri:")
    for url in DEEPLX_API_URLS:
        status = get_api_status(url)
        print(f"  - {url} ({status})")
    
    start_time = time.time()
    await translate_directory(script_directory)
    end_time = time.time()
    
    total_time = end_time - start_time
    print(f"\nToplam çeviri süresi: {str(timedelta(seconds=int(total_time)))}")
    
    print("\nAPI Performans İstatistikleri:")
    for url, status in api_status.items():
        total_requests = status['success_count'] + status['failure_count']
        success_rate = (status['success_count'] / total_requests * 100) if total_requests > 0 else 0
        print(f"  - {url}:")
        print(f"    Başarılı İstekler: {status['success_count']}")
        print(f"    Başarısız İstekler: {status['failure_count']}")
        print(f"    Başarı Oranı: {success_rate:.2f}%")
        print(f"    Ortalama Yanıt Süresi: {status['average_response_time']:.2f} saniye")

if __name__ == "__main__":
    asyncio.run(main())