import pyttsx3
import speech_recognition as sr   # not SpeechRecognition
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import time


# escuchar nuestro microfono y devolver el audio como texto (string)
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera antes de empezar a escuchar
        r.pause_threshold = 0.8

        # informar que ha comenzado la grabación
        print("\n***  Ya puedes hablar  ***")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        # debemos tener en cuenta que va a haber errores de interpretacion del audio
        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-ar", show_all=False)

            # prueba de que pudo ingresar nuestra voz en un texto
            print(f"Dijiste: {pedido}")

            # devolver el pedido para poder utilizarlo luego
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendió el audio
            print("ups, no te entendí")

            # devolver error
            return "sigo esperando"

        # en caso de no poder resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendió como realizar la tarea
            print("lo siento, no se hacerlo")

            # devolver error
            return "sigo esperando"

        # en caso de errores inesperados
        except:

            # prueba de que no comprendió como realizar la tarea
            print("ALGO HA SALIDO MAL")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# probar distintas voces
'''engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voice)'''


# informar el dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de dias de la semana
    semana = {0: 'Lunes', 
              1: 'Martes', 
              2: 'Miércoles',
              3: 'Jueves',
              4: 'Viernes',
              5: 'Sábado',
              6: 'Domingo'}

    # decir el dia de la semana
    hablar(f"Hoy es {semana[dia_semana]}")
        

# informar que hora es
def pedir_hora():

    # crear una variable con datos de la hora
    horas = time.strftime("%I")
    minuts = time.strftime("%M")   
    hora = f"En este momento son las {horas} horas y {minuts} minutos"
    print(hora)

    # decir la hora
    hablar(hora)

 
# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 21:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 14:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(f"{momento}, soy Helena, tu asistente personal. Por favor, dime en que puedo ayudarte.")


# funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    saludo_inicial()
    
    # variable de corte
    comenzar = True

    # loop central que solo se detenga cuando digamos al programa que queremos que se atur
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Por supuesto. Estoy abriendo youtube.')
            webbrowser.open('https://www.youtube.com')
            continue

        elif 'cuál es el precio de bitcoin' in pedido:
            hablar('Buena búsqueda. Te muestro la gráfica actual de btc/usd en tradingview')
            webbrowser.open('https://es.tradingview.com/chart/Nq4CuFCW/?symbol=COINBASE%3ABTCUSD')
            continue

        elif 'qué día es' in pedido:
            pedir_dia()
            continue

        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'busca en wikipedia' in pedido:
            hablar('Claro. Dame un momento.')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente:")
            hablar(resultado)
            continue

        elif 'busca en internet' in pedido:
            hablar('Claro. Dame un momento.')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado.")
            continue

        elif 'reproducir' in pedido:
            hablar('Buena idea. Aquí tienes tu canción.')
            pywhatkit.playonyt(pedido)
            continue

        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        elif 'precio de las acciones' in pedido:
            # metodos split() y strip()
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL',
                       'tesla':'TSLA'}
            try:
                hablar("En seguida, déjame buscarlo.")
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                #precio_actual = accion_buscada.info['regularMarketPrice']
                precio_actual = accion_buscada.history(period='1d')
                todays_data = precio_actual['Close'][0]
                
                hablar(f"El precio actual de {accion} es de {todays_data.round()} dólares")
            except:
                hablar("Lo siento. No la he encontrado.")


        elif 'adiós' or 'hasta luego Elena' in pedido:
            hablar("Me voy a descansar. Si necesitas algo avísame.")
            break


pedir_cosas()
