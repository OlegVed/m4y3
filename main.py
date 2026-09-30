import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator


# 📋 Список кодов поддерживаемых языков
LANGUAGES = {
    'en': 'английский',
    'es': 'испанский',
    'fr': 'французский',
    'de': 'немецкий',
    'it': 'итальянский',
    'pt': 'португальский',
    'ru': 'русский',
    'zh-cn': 'китайский',
    'ja': 'японский',
    'ko': 'корейский',
    'tr': 'турецкий',
    'pl': 'польский',
    'uk': 'украинский',
}


# Показываем список языков
print("📋 Доступные языки для перевода:")
for code, name in LANGUAGES.items():
    print(f"  {code} — {name}")
print()

# Спрашиваем язык перевода
dest_lang = input("На какой язык перевести? (введите код, например 'en'): ").strip().lower()

print("-" * 50)

# 🔄 Цикл для перевода нескольких фраз подряд
while True:
    # Запись
    print("🎙 Говори...")
    duration = 5
    sample_rate = 44100
    
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    
    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, теперь распознаём...")
    
    # Распознавание
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"📝 Ты сказал: {text}")
        
        # Перевод
        translator = Translator()
        translated = translator.translate(text, dest=dest_lang)
        print(f"🌍 Перевод на {dest_lang}: {translated.text}")
        
    except sr.UnknownValueError:
        print("❌ Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"❌ Ошибка сервиса: {e}")
    
    # Спрашиваем, продолжить ли
    print()
    cont = input("Продолжить? (да/нет): ").strip().lower()
    if cont not in ['да', 'yes', 'y', 'д']:
        print("\n👋 Программа завершена!")
        break
    print()