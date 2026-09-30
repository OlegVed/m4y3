import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

error = 0
print("Выбери сложность:")
print("1 Лёгкая")
print("2 Средняя")
print("3 Сложная")
print()
cont = input("Укажите сложность:")
if cont not in ['1', '2', '3']:
    print("Ответ неверный")
elif cont == "1":
    cont = "easy"
elif cont == "2":
    cont = "medium"
elif cont == "3":
    cont = "hard"

for i in range(5):
    word = random.choice(words_by_level[cont])
    print(f"🎙️ Переведи {word} ")
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
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print(f"📝 Ты сказал: {text}")
        
        # Перевод
        translator = Translator()
        translated = translator.translate(word, dest="en").text.lower()
        print(f"🌍 Перевод на английский: {translated}")
        if text == translated:
            print("Всё правильно.")
        else: 
            print("Неправильно")
            error += 1
        if error == 3:
            print("Вы проиграли")
            break
    except sr.UnknownValueError:
        print("❌ Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"❌ Ошибка сервиса: {e}")
else: print("Ты дошёл-(шла) до финиша")
print("Тестируем ветви")