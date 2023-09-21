# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from pyswip import Prolog
import ast

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
        estado_animo = tracker.get_slot("estado_animo")

        if estado_animo == "feliz":
            dispatcher.utter_message("Me alegro! Que siga asi!")

        elif estado_animo == "triste":
            dispatcher.utter_message("Lamento que te sientas asi, mira la siguiente imagen y dime..")
            dispatcher.utter_image_url("https://cdn.buenavibra.es/wp-content/uploads/2018/05/03092006/bigstock-A-Wooden-Bowl-Of-Popcorn-And-T-236238289-1170x600.jpg")

        elif estado_animo == "enojado":
            dispatcher.utter_message("Tal vez necesitas relajarte..")

        else:
            dispatcher.utter_message("Te tengo un plan..")

        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Mensaje cuando el bot no entienda el input
        dispatcher.utter_message(template="utter_default")
        
        return []

