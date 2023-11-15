# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from pyswip import Prolog
import ast
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

class ActionObtenerSeriesMasVistas(Action):

    def name(self) -> Text:
        return "action_top_10_series"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # URL de la página web que contiene la información sobre las series más vistas
        url_pagina_series = 'https://www.netflix.com/tudum/top10/es/tv-non-english'

        # Realizar la solicitud HTTP
        respuesta = requests.get(url_pagina_series)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if respuesta.status_code == 200:
            # Parsear el contenido HTML con BeautifulSoup
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Encuentra las series más vistas en el HTML de la página web
            series_mas_vistas = soup.find_all('tr', {'data-id': True})

            # Mostrar las 10 series más vistas
            mensaje = "Las 10 series más vistas actualmente son:"
            for i, serie in enumerate(series_mas_vistas[:10], start=1):
                # Extraer información de cada serie
                nombre_serie = serie.find('td', class_='tbl-cell-name').text.strip()

                # Le quito los tildes si los tiene
                nombre_serie = unidecode(nombre_serie)

                # Construir el mensaje
                mensaje += f"\n{i}. {nombre_serie}"

            # Enviar el mensaje al usuario a través del dispatcher
            dispatcher.utter_message(text=mensaje)
        else:
            # Enviar mensaje de error al usuario
            dispatcher.utter_message(text=f"Error al obtener la página. Código de estado: {respuesta.status_code}")

        return []


class ActionRecomendacion(Action):
    def name(self) -> Text:
        return "action_recomendacion"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtenemos las entidades
        final = tracker.get_slot("respuesta1")
        evolucionPersonajes = tracker.get_slot("respuesta2")
        ritmo = tracker.get_slot("respuesta3")

        # Verificamos que se entendieron correctamente
        if(final == None):
            dispatcher.utter_message(text="No entiendo cual tipo de final es tu preferido")
            return 
        if(evolucionPersonajes == None):
            dispatcher.utter_message(text="No entiendo como prefieres que evolucionen los personajes")
            return
        if(ritmo == None):
            dispatcher.utter_message(text="No entendi cual ritmo prefieres")
            return
        
        # convertimos a string y a minúsculas
        final = final.lower()
        evolucionPersonajes = evolucionPersonajes.lower()
        ritmo = ritmo.lower()

        # convertimos a one-hot encoding
        Final_Cerrado = "1" if final == "cerrado" else "0"
        EvolucionPersonajes_Evolucionan = "1" if evolucionPersonajes == "evolucionan" else "0"
        Ritmo_Rapido = "1" if ritmo == "rapido" else "0"
                
        #Dataframe con los datos
        user_data = pd.DataFrame({
            'Final_Cerrado': [Final_Cerrado],
            'EvolucionPersonajes_Evolucionan': [EvolucionPersonajes_Evolucionan],  
            'Ritmo_Rapido': [Ritmo_Rapido], 
        })

        # predecimos y respondemos al usuario
        y_pred = model.predict(user_data)

        if(y_pred[0] == 1):
            dispatcher.utter_message(text="Te recomiendo mirar una serie, puedes preguntarme por opciones y te ayudare con gusto!")
        else:
            dispatcher.utter_message(text="Te recomiendo mirar una pelicula, puedes preguntarme por opciones y te ayudare con gusto!")

        return[]
    
class ActionCustomGoodbye(Action):
    def name(self) -> Text:
        return "action_custom_goodbye"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mood = tracker.get_slot("estado_animo")
        name = tracker.get_slot("nombre")

        if mood == "feliz":
            dispatcher.utter_message(f"Nos vemos, {name}! Que sigas bien!")
        elif mood == "triste":
            dispatcher.utter_message(f"Nos vemos, {name}. Espero que te sientas mejor.")
        elif mood == "enojado":
            dispatcher.utter_message(f"Nos vemos, {name}. Ojala haya podido ser de ayuda.")
        else:
            dispatcher.utter_message(f"Nos vemos, {name}!")
                
        return[]

class ActionRecomendarPelicula(Action):
    def name(self) -> Text:
        return "action_recomendar_pelicula"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        estado_animo = tracker.get_slot("estado_animo")
        genero = tracker.get_slot("genero_pelicula")
        
        prolog = Prolog()
        prolog.consult("c:/Users/Usuario/ChatBotNetflix/recomendar_pelicula.pl")
        for solucion in prolog.query(f"obtener_pelicula_recomendada('{estado_animo}', '{genero}', Pelicula, Sinopsis)"):
            pelicula_recomendada = solucion["Pelicula"]
            sinopsis_pelicula = solucion["Sinopsis"]

        if pelicula_recomendada:
            dispatcher.utter_message(text=f"Te recomiendo la película: {pelicula_recomendada}")


        return [SlotSet("sinopsis_pelicula", sinopsis_pelicula)]

class ActionBasedOnMood(Action):
    def name(self) -> Text:
        return "action_based_on_mood"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtener el intent detectado
        intent = tracker.latest_message['intent'].get('name')

        # Lógica para establecer el valor del slot basado en el intent
        if intent == 'greet_happy':
            slot_value = 'feliz'
            dispatcher.utter_message("Hola! Aqui te habla tu asesor de Netflix!")
        elif intent == 'greet_sad':
            slot_value = 'triste'
            dispatcher.utter_message("Holaa! Estas listo para un buen plan que suba ese estado de animo?!")
            dispatcher.utter_image_url("https://cdn.buenavibra.es/wp-content/uploads/2018/05/03092006/bigstock-A-Wooden-Bowl-Of-Popcorn-And-T-236238289-1170x600.jpg")
        elif intent == 'greet_mad':
            slot_value = 'enojado'
            dispatcher.utter_message("Buenas! Tal vez necesitas relajarte..")
        else:
            # Valor predeterminado o manejo de casos no específicos
            slot_value = 'normal'
            dispatcher.utter_message("Hola! Aqui te habla tu asesor de Netflix!")

        # Establecer el valor del slot
        return [SlotSet('estado_animo', slot_value)]

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Mensaje cuando el bot no entienda el input
        dispatcher.utter_message(template="utter_default")
        
        return []

#Arbol de decision

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from sklearn import tree

# Obtenemos el dataset a entrenar
nombre_archivo = 'c:/Users/Usuario/ChatBotNetflix/decisionTree.csv'

df = pd.read_csv(nombre_archivo)
#df = df.drop(columns=['Unnamed: 0']) 

print(df)

# Imprimimos 5 filas aleatorias
print("5 EJEMPLOS DE LOS DATOS....................................................")
print(df.sample(5))
print("INFORMACIÓN DEL DATASET....................................................")
print(df.info())


# convertimos las variables categóricas en one-hot encoding
df = pd.get_dummies(data=df, drop_first=True)

# Imprimimos 5 filas aleatorias
print("5 EJEMPLOS CON FORMATO ONE-HOT....................................................")
print(df.sample(5))

# Separamos las features y el target
x = df.drop(columns='Contenido_Serie')     # features
y = df['Contenido_Serie']                  #target

print("DATASET DE LOS FEATURES....................................................")
print(x.info())

# Creamos el modelo
model = DecisionTreeClassifier(max_depth=3)
# Entrenamos el modelo
model.fit(x,y)

# pasamos las features y el target para que nos diga que tan bien predice
print("ACCURACY DEL MODELO....................................................")
print(model.score(x, y))
