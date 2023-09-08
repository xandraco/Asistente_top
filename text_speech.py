import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import re
import difflib

aname = ''

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def nacimiento(aname):
    print('Entra a la funcion nacimiento')
    nombre = aname
    d = {}
    fecha_nacimiento = None

    with open('basetopicos.txt', 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            temp = linea.split(',')
            if nombre in temp:
                d[temp[0]] = list(temp[1:])
    fecha_nacimiento = d[nombre][0]
    print(fecha_nacimiento)
    return fecha_nacimiento

def obtener_edad(aname):
    print('Entra a la funcion obtener_edad')
    nombre = aname
    d = {}

    with open('basetopicos.txt', 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            temp = linea.split(',')
            if nombre in temp:
                d[temp[0]] = list(temp[1:])
    edad = d[nombre][1]
    print (edad)
    return edad

def coincidencias_f(aname):
    print('Entra a la funcion coincidencias')
    nombres = aname.split()  # Divide la cadena en palabras individuales
    d = {}
    coincidencias = []

    with open('basetopicos.txt', 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            temp = linea.split(',')
            nombre_base = temp[0].strip()
            
            # Verifica si alguna de las palabras en 'nombres' está en 'nombre_base'
            if any(nombre in nombre_base for nombre in nombres):
                d[nombre_base] = list(temp[1:])
                coincidencias.append(nombre_base)
    return coincidencias


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

def run():
    rec = listen()
    print(rec)
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '').strip()
        talk('Reproduciendo' + music)
        pywhatkit.playonyt(music)
    
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)

    # Encontrar el cumpleaños
    elif 'cumpleaños' in rec or 'nacimiento de' in rec:
        alumno = re.sub(r'(cumpleaños de|nacimiento de|fecha|cuál es el|cuándo es el|dime|cuál es la fecha de|cuando es el|cumpleaños|nacimiento|dime el|dime la)','', rec).strip().title()
        coincidencias = coincidencias_f(alumno)
        if coincidencias:
            if ' ' in alumno:  # Verifica si hay un espacio en el nombre (indicando nombre y apellido)
                if len(coincidencias) == 1:
                    # cuando solamente hay una coincidencia
                    mejor_coincidencia = coincidencias[0]
                else:
                    # cualquier caso cuando encuentre más de una coincidencia
                    # buscará la mejor
                    mejor_coincidencia = difflib.get_close_matches(alumno,coincidencias, n=1)[0]
                
                birthday = nacimiento(mejor_coincidencia)
                print (f'Mejor coincidencia: {mejor_coincidencia}')
                talk ('La fecha de nacimiento de '+ mejor_coincidencia + ' es ' + birthday)
                # En caso de que encuentre más de una coincidencia
                '''
                for coincidencia in coincidencias:
                    if coincidencia != mejor_coincidencia:
                        birthday = nacimiento(coincidencia)
                        print(f'Otra coincidencia {coincidencia}')
                        talk ('Otra coincidencia: la fecha de nacimiento de ' + coincidencia + ' es ' + birthday) 
                '''
            else:
                # Si solo se proporciona un nombre o un apellido, buscar todas las posibles coincidencias
                for coincidencia in coincidencias:
                    birthday = nacimiento(coincidencia)
                    print(f'La fecha de nacimiento de {coincidencia} es {birthday}')
                    talk(f'La fecha de nacimiento de {coincidencia} es {birthday}')
        else:
            talk('Lo siento, no se encontraron coincidencias para ' + alumno)
    
    # decir el nombre completo
    elif 'nombre' in rec or 'llama' in rec:
        alumno = re.sub(r'(nombre de|cuál es el|dime|cómo se|dime el|completo de|nombre|llama|dime cómo|completo)','', rec).strip().title()
        coincidencias = coincidencias_f(alumno)
        if coincidencias:
            if ' ' in alumno:  # Verifica si hay un espacio en el nombre (indicando nombre y apellido)
                if len(coincidencias) == 1:
                    # cuando solamente hay una coincidencia
                    mejor_coincidencia = coincidencias[0]
                else:
                    # cualquier caso cuando encuentre más de una coincidencia
                    # buscará la mejor
                    mejor_coincidencia = difflib.get_close_matches(alumno,coincidencias, n=1)[0]
                
                print (f'Mejor coincidencia: {mejor_coincidencia}')
                talk ('El nombre completo de '+ alumno + ' es ' + mejor_coincidencia)
            else:
                # Si solo se proporciona un nombre o un apellido, buscar todas las posibles coincidencias
                for coincidencia in coincidencias:
                    print(f'El nombre completo de {alumno} es {coincidencia}')
                    talk(f'El nombre completo de {alumno} es {coincidencia}')
        else:
            talk('Lo siento, no se encontraron coincidencias para ' + alumno)
    
    # encontrar la edad de un alumno
    elif 'años' in rec or 'edad' in rec:
        alumno = re.sub(r'(cuantos años tiene|qué edad tiene|edad de|años de|años|edad|cuántos|dime cuántos|dime la|dime los)','', rec).strip().title()
        coincidencias = coincidencias_f(alumno)
        if coincidencias:
            if ' ' in alumno:  # Verifica si hay un espacio en el nombre (indicando nombre y apellido)
                if len(coincidencias) == 1:
                    # cuando solamente hay una coincidencia
                    mejor_coincidencia = coincidencias[0]
                else:
                    # cualquier caso cuando encuentre más de una coincidencia
                    # buscará la mejor
                    mejor_coincidencia = difflib.get_close_matches(alumno,coincidencias, n=1)[0]
                
                al_edad = obtener_edad(mejor_coincidencia)
                print (f'Mejor coincidencia: {mejor_coincidencia}')
                talk ('La edad de '+ mejor_coincidencia + ' es ' + al_edad)
                # En caso de que encuentre más de una coincidencia
            else:
                # Si solo se proporciona un nombre o un apellido, buscar todas las posibles coincidencias
                for coincidencia in coincidencias:
                    al_edad = obtener_edad(coincidencia)
                    print(f'La edad de {coincidencia} es {al_edad}')
                    talk(f'La edad de {coincidencia} es {al_edad}')
        else:
            talk('Lo siento, no se encontraron coincidencias para ' + alumno)

    
    else:
        talk("Lo siento, no pude escucharte, vuelve a intentarlo...")




talk("Hola, en que puedo ayudarte?")
while True:
    run()
