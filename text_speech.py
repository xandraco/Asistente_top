import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import re
import difflib
import json
import keyboard

# comentario de prueba de commit
# segundo comentario de prueba

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

# asigna un id único a cada instrucción
def get_unique_id():
    return len(registro) + 1  # Asigna un id único basado en la longitud del registro

def find_instruction(action):
    for id, data in registro.items():
        if data['action'] == action:
            return id
    return None

def load_routines():
    try:
        with open('rutinas.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_routines(rutinas):
    with open('rutinas.json', 'w') as file:
        json.dump(rutinas, file)

rutinas = load_routines()

def process_instruction(action):
    matching_ids = [id for id, data in registro.items() if data['action'] == action]
    
    if matching_ids:
        updated = False
        for id in matching_ids:
            if check_time(registro[id]['last_time']):
                registro[id]['count'] += 1
                registro[id]['last_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if registro[id]['count'] == 3:
                    print('Instrucción alcanzó un count de 3, guardando en rutinas.json:', action)
                    rutinas.append({'id': id, 'action': action})
                updated = True
                break
        
        if not updated:
            print('Nueva instrucción detectada (fuera de rango de tiempo):', action)
            new_id = get_unique_id()
            registro[new_id] = {'action': action, 'count': 1, 'last_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    else:
        print('Nueva instrucción detectada (nueva):', action)
        id = get_unique_id()
        registro[id] = {'action': action, 'count': 1, 'last_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    save_data(registro)
    
    # Guardar rutinas si se alcanza un count de 3
    for routine in rutinas:
        if registro[routine['id']]['count'] == 3:
            routine_data = {'id': routine['id'], 'action': registro[routine['id']]['action']}
            with open('rutinas.json', 'w') as file:
                json.dump(rutinas, file)
            print(f'Guardando rutina con id {routine["id"]} y acción {routine_data["action"]} en rutinas.json.')


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
            process_instruction(rec)
        elif any(keyword in rec for keyword in ['apaga']):
            print('Apagado')
            process_instruction(rec)
        else:
            talk("Lo siento, no pude escucharte, vuelve a intentarlo...")


while running:
    run()
