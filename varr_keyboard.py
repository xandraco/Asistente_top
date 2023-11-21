import nltk
from nltk.corpus import stopwords
import pyttsx3
import pywhatkit
import datetime
import json
import keyboard
import time
import shutil
import os

# se obtienen las stopwords en español
stop_words = set(stopwords.words('spanish'))

aname = ''

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

running = True

def talk(text):
    engine.say(text)
    engine.runAndWait()

# Redondeo a los 5 mins más cercanos
def round_to_nearest_5_minutes(dt):
    rounded_minutes = round(dt.minute / 5) * 5
    return dt.replace(minute=rounded_minutes)

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
    
    last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M')
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

rutinas = load_routines()

def save_routines(rutinas):
    # Delete existing execution.json if it exists
    try:
        os.remove('execution.json')
    except FileNotFoundError:
        pass

    # Save the updated rutinas to rutinas.json
    with open('rutinas.json', 'w') as file:
        json.dump(rutinas, file)
    
    # Create a copy of rutinas.json named execution.json
    shutil.copy('rutinas.json', 'execution.json')

def edit_routine():
    talk('Claro, ¿cuál rutina quieres cambiar?')
    rec = input("Escuchando... : ")
    # Remove stop words
    print(rec)

    # Map spoken words to numeric values
    number_mapping = {
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10,
        'once': 11,
        'doce': 12,
        'trece': 13,
        'catorce': 14,
        'quince': 15,
        'dieciséis': 16,
        'diecisiete': 17,
        'dieciocho': 18,
        'diecinueve': 19,
        'veinte': 20,
        'veintiuno': 21,
        'veintidós': 22,
        'veintitrés': 23,
        'veinticuatro': 24,
        'veinticinco': 25,
        'veintiséis': 26,
        'veintisiete': 27,
        'veintiocho': 28,
        'veintinueve': 29,
        'treinta': 30,
        'treinta y uno': 31,
        'treinta y dos': 32,
        'treinta y tres': 33,
        'treinta y cuatro': 34,
        'treinta y cinco': 35,
        'treinta y seis': 36,
        'treinta y siete': 37,
        'treinta y ocho': 38,
        'treinta y nueve': 39,
        'cuarenta': 40,
        'cuarenta y uno': 41,
        'cuarenta y dos': 42,
        'cuarenta y tres': 43,
        'cuarenta y cuatro': 44,
        'cuarenta y cinco': 45,
        'cuarenta y seis': 46,
        'cuarenta y siete': 47,
        'cuarenta y ocho': 48,
        'cuarenta y nueve': 49,
        'cincuenta': 50,
        'cincuenta y uno': 51,
        'cincuenta y dos': 52,
        'cincuenta y tres': 53,
        'cincuenta y cuatro': 54,
        'cincuenta y cinco': 55,
        'cincuenta y seis': 56,
        'cincuenta y siete': 57,
        'cincuenta y ocho': 58,
        'cincuenta y nueve': 59,
        'sesenta': 60,
        'sesenta y uno': 61,
        'sesenta y dos': 62,
        'sesenta y tres': 63,
        'sesenta y cuatro': 64,
        'sesenta y cinco': 65,
        'sesenta y seis': 66,
        'sesenta y siete': 67,
        'sesenta y ocho': 68,
        'sesenta y nueve': 69,
        'setenta': 70,
        'setenta y uno': 71,
        'setenta y dos': 72,
        'setenta y tres': 73,
        'setenta y cuatro': 74,
        'setenta y cinco': 75,
        'setenta y seis': 76,
        'setenta y siete': 77,
        'setenta y ocho': 78,
        'setenta y nueve': 79,
        'ochenta': 80,
        'ochenta y uno': 81,
        'ochenta y dos': 82,
        'ochenta y tres': 83,
        'ochenta y cuatro': 84,
        'ochenta y cinco': 85,
        'ochenta y seis': 86,
        'ochenta y siete': 87,
        'ochenta y ocho': 88,
        'ochenta y nueve': 89,
        'noventa': 90,
        'noventa y uno': 91,
        'noventa y dos': 92,
        'noventa y tres': 93,
        'noventa y cuatro': 94,
        'noventa y cinco': 95,
        'noventa y seis': 96,
        'noventa y siete': 97,
        'noventa y ocho': 98,
        'noventa y nueve': 99,
        'cien': 100
    }


    # Check if the spoken word is in the mapping
    if rec.lower() in number_mapping:
        routine_id_str = number_mapping[rec.lower()]
        print(routine_id_str)
        found_routine = next((routine for routine in rutinas if routine['id'] == routine_id_str), None)

        if found_routine:
            talk(f'¿Qué quieres que se haga ahora en la rutina "{found_routine["action"]}"?')
            rec = input("Escuchando... : ")
            # Remove stop words
            rec = ' '.join([word for word in rec.split() if word.lower() not in stop_words])

            # Update the routine with the new action
            found_routine['action'] = rec
            talk(f'Rutina actualizada. Ahora la rutina "{found_routine["action"]}" se ejecutará a las {found_routine["hour"]}.')
            save_routines(rutinas)
        else:
            talk(f'Lo siento, no encontré una rutina con el ID {routine_id_str}.')
    else:
        talk('Por favor, indica un I D válido')

def delete_routine():
    talk('Claro, ¿cuál es el ID de la rutina que quieres eliminar?')
    rec = input("Escuchando... : ")
    # Remove stop words
    print(rec)

    # Map spoken words to numeric values
    number_mapping = {
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10,
        'once': 11,
        'doce': 12,
        'trece': 13,
        'catorce': 14,
        'quince': 15,
        'dieciséis': 16,
        'diecisiete': 17,
        'dieciocho': 18,
        'diecinueve': 19,
        'veinte': 20,
        'veintiuno': 21,
        'veintidós': 22,
        'veintitrés': 23,
        'veinticuatro': 24,
        'veinticinco': 25,
        'veintiséis': 26,
        'veintisiete': 27,
        'veintiocho': 28,
        'veintinueve': 29,
        'treinta': 30,
        'treinta y uno': 31,
        'treinta y dos': 32,
        'treinta y tres': 33,
        'treinta y cuatro': 34,
        'treinta y cinco': 35,
        'treinta y seis': 36,
        'treinta y siete': 37,
        'treinta y ocho': 38,
        'treinta y nueve': 39,
        'cuarenta': 40,
        'cuarenta y uno': 41,
        'cuarenta y dos': 42,
        'cuarenta y tres': 43,
        'cuarenta y cuatro': 44,
        'cuarenta y cinco': 45,
        'cuarenta y seis': 46,
        'cuarenta y siete': 47,
        'cuarenta y ocho': 48,
        'cuarenta y nueve': 49,
        'cincuenta': 50,
        'cincuenta y uno': 51,
        'cincuenta y dos': 52,
        'cincuenta y tres': 53,
        'cincuenta y cuatro': 54,
        'cincuenta y cinco': 55,
        'cincuenta y seis': 56,
        'cincuenta y siete': 57,
        'cincuenta y ocho': 58,
        'cincuenta y nueve': 59,
        'sesenta': 60,
        'sesenta y uno': 61,
        'sesenta y dos': 62,
        'sesenta y tres': 63,
        'sesenta y cuatro': 64,
        'sesenta y cinco': 65,
        'sesenta y seis': 66,
        'sesenta y siete': 67,
        'sesenta y ocho': 68,
        'sesenta y nueve': 69,
        'setenta': 70,
        'setenta y uno': 71,
        'setenta y dos': 72,
        'setenta y tres': 73,
        'setenta y cuatro': 74,
        'setenta y cinco': 75,
        'setenta y seis': 76,
        'setenta y siete': 77,
        'setenta y ocho': 78,
        'setenta y nueve': 79,
        'ochenta': 80,
        'ochenta y uno': 81,
        'ochenta y dos': 82,
        'ochenta y tres': 83,
        'ochenta y cuatro': 84,
        'ochenta y cinco': 85,
        'ochenta y seis': 86,
        'ochenta y siete': 87,
        'ochenta y ocho': 88,
        'ochenta y nueve': 89,
        'noventa': 90,
        'noventa y uno': 91,
        'noventa y dos': 92,
        'noventa y tres': 93,
        'noventa y cuatro': 94,
        'noventa y cinco': 95,
        'noventa y seis': 96,
        'noventa y siete': 97,
        'noventa y ocho': 98,
        'noventa y nueve': 99,
        'cien': 100
    }


    # Check if the spoken word is in the mapping
    if rec.lower() in number_mapping:
        routine_id_str = number_mapping[rec.lower()]
        found_routine = next((routine for routine in rutinas if routine['id'] == routine_id_str), None)

        if found_routine:
            # Remove the routine from the list
            rutinas.remove(found_routine)
            talk(f'Rutina con ID {routine_id_str} eliminada.')
            save_routines(rutinas)
        else:
            talk(f'Lo siento, no encontré una rutina con el ID {routine_id_str}.')
    else:
        talk('Por favor, indica un I D válido')

def process_instruction(action):
    matching_ids = [id for id, data in registro.items() if data['action'] == action]

    if matching_ids:
        updated = False
        for id in matching_ids:
            if check_time(registro[id]['last_time']):
                registro[id]['count'] += 1

                # Store unrounded time in registro.json
                unrounded_time = datetime.datetime.now()
                registro[id]['last_time'] = unrounded_time.strftime('%Y-%m-%d %H:%M')

                # Redondear el tiempo al múltiplo de 5 más cercano
                rounded_time = round_to_nearest_5_minutes(unrounded_time)

                if registro[id]['count'] == 3:
                    existing_routine = next((routine for routine in rutinas if routine['id'] == id), None)
                    if existing_routine is None:
                        print('Instrucción alcanzó un count de 3, guardando en rutinas.json:', action)
                        rutinas.append({'id': int(id), 'action': action, 'hour': rounded_time.strftime('%H:%M')})
                updated = True
                break
        if rutinas:
            save_routines(rutinas)
        if not updated:
            print('Nueva instrucción detectada (fuera de rango de tiempo):', action)
            new_id = get_unique_id()
            unrounded_time = datetime.datetime.now()
            registro[new_id] = {'action': action, 'count': 1, 'last_time': unrounded_time.strftime('%Y-%m-%d %H:%M')}
    else:
        print('Nueva instrucción detectada (nueva):', action)
        id = get_unique_id()
        unrounded_time = datetime.datetime.now()
        registro[id] = {'action': action, 'count': 1, 'last_time': unrounded_time.strftime('%Y-%m-%d %H:%M')}

    save_data(registro)

def run():
    rec = input("Escuchando... : ")
    # Remove stop words
    rec = ' '.join([word for word in rec.split() if word.lower() not in stop_words])
    print(rec)
    if any(keyword in rec for keyword in ['enciende', 'prende', 'apaga', 'prepara', 'hazme']):
        talk('Okey')
        print('Listo')
        process_instruction(rec)
    elif any(keyword in rec for keyword in ['muestrame rutinas', 'dime cuáles rutinas', 'dime rutinas', 'cuáles rutinas']):
        talk('Claro')
        for routine in rutinas:
            print(f'ID: {routine["id"]}, Acción: {routine["action"]}, Hora: {routine["hour"]}')
            talk(f'ID: {routine["id"]}, Acción: {routine["action"]}, Hora: {routine["hour"]}')
    elif any(keyword in rec for keyword in ['cambiar rutina', 'modificar rutina', 'actualizar rutina', 'actualiza rutina', 'cambia rutina', 'modifica rutina', 'editar rutinas', 'editar rutina', 'edita rutinas', 'edita rutina']):
        edit_routine()
    elif any(keyword in rec for keyword in ['eliminar rutina', 'borrar rutina', 'quitar rutina', 'elimina rutina', 'borra rutina', 'quita rutina']):
        delete_routine()
    else:
        talk("Lo siento, no pude escucharte, vuelve a intentarlo...")

while running:
    run()
