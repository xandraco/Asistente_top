import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import re
import difflib
import json
import keyboard

aname = ''

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

running = True

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language = "es-ES")
            rec = rec.lower()
    except:
        pass

    return rec

# Lectura y escritura de datos
def load_data():
    try:
        with open('registro.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('registro.json', 'w') as file:
        json.dump(data, file)

registro = load_data()

# Función para verificar el tiempo
def check_time(last_time):
    if last_time is None:
        return True
    
    last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.datetime.now()
    time_difference = current_time - last_time
    
    return 23.75 <= time_difference.total_seconds() / 3600 <= 24.25

def run():
    if keyboard.is_pressed('enter'):
            rec = listen()
            print(rec)
            if 'reproduce' in rec:
                music = rec.replace('reproduce', '').strip()
                talk('Reproduciendo ' + music)
                pywhatkit.playonyt(music)
            
            elif 'hora' in rec:
                hora = datetime.datetime.now().strftime('%I:%M %p')
                talk("Son las " + hora)

            elif any(keyword in rec for keyword in ['enciende', 'prende']):
                print('Encendido')
                registro[rec] = registro.get(rec, {'count': 0, 'last_time': None})
                if check_time(registro[rec]['last_time']):
                    registro[rec]['count'] += 1
                    registro[rec]['last_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    print('Aún no ha pasado suficiente tiempo desde la última instrucción.')

            elif any(keyword in rec for keyword in ['apaga']):
                print('Apagado')
                registro[rec] = registro.get(rec, {'count': 0, 'last_time': None})
                if check_time(registro[rec]['last_time']):
                    registro[rec]['count'] += 1
                    registro[rec]['last_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    print('Aún no ha pasado suficiente tiempo desde la última instrucción.')
            
            
            else:
                talk("Lo siento, no pude escucharte, vuelve a intentarlo...")

            save_data(registro)


while running:
    run()
