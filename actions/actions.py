# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .translator import response_further_test,test_descript
import mysql.connector as mc

language = []
translator = Translator()
typ=[]
class ActionConvertText(Action):

    def name(self) -> Text:
        return "action_further_test_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        
        if text=="blood-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("COMPLETE BLOOD COUNT (CBC)", dest=f'{language[0][:2]}').text, "payload": "cbc"},
                {"title": translator.translate("RED BLOOD CELLS (RBC COUNT)", dest=f'{language[0][:2]}').text, "payload": "rbc"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        elif text=="urine-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE, R/E", dest=f'{language[0][:2]}').text, "payload": "RE"},
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE R/E, AUTOMATED", dest=f'{language[0][:2]}').text, "payload": "REA"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of urine-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        elif text=="imaging-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("Magnetic Resonance imaging(MRI)", dest=f'{language[0][:2]}').text, "payload": "mri"},
                {"title": translator.translate("X-ray", dest=f'{language[0][:2]}').text, "payload": "xray"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of imaging-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        # language.clear()

        return []

class ActionDisplayCard(Action):

    def name(self) -> Text:
        return "action_display_card"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        typ.append(text)
        card = test_descript(typ[0],typ[1],response_further_test)
        dispatcher.utter_message(translator.translate(card, dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        language.clear()
        typ.clear()
        return []

class SelectLanguageText(Action):
    def name(self) -> Text:
        return "action_select_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        language.append(text)
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🔬'+translator.translate("MedicalTests", dest=f'{language[0][:2]}').text: "lab_tests",
            '📅'+translator.translate("Book An Appointment", dest=f'{language[0][:2]}').text: "Appointment_booking",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"/{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+'👇'
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []

class ActionTestType(Action):

    def name(self) -> Text:
        return "action_test_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        option_to_intent_mapping = {
            '🩸'+translator.translate("Blood-Tests", dest=f'{language[0][:2]}').text: "blood-test",
            '💧'+translator.translate("Urine-Tests", dest=f'{language[0][:2]}').text: "urine-test",
            '📷'+translator.translate("Imaging-Tests", dest=f'{language[0][:2]}').text: "imaging-test",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+'👇'
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []
    
#################################################################Book an Appointment############################################################################
appoint = []
class ActionAskVisit(Action):
    def name(self) -> Text:
        return "action_ask_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🏠'+translator.translate("Home Visit", dest=f'{language[0][:2]}').text: "homevisit",
            '🏥'+translator.translate("Lab Visit", dest=f'{language[0][:2]}').text: "labvisit",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+"👇"
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []   
#'🩸'+translator.translate("Blood-Tests", dest=f'{language[0][:2]}').text
class SelectLanguageText(Action):
    def name(self) -> Text:
        return "action_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        appoint.append(text)
        date_desc = translator.translate('Enter the date on which you want to book appointment',dest=f'{language[0][:2]}').text
        dispatcher.utter_message(text=f"{date_desc}\n Enter date in dd-mm-yyyy format\nfor eg 02-05-2024")

        return []
    
class SelectLanguageText(Action):
    def name(self) -> Text:
        return "action_show_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        appoint.append(text)  # Split the message into words
        # Connect to MySQL
        db = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="medichat"
        )
        cursor = db.cursor()
        data = []
        if appoint[0][:4] == 'home':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Home'")
            data = cursor.fetchall()
        elif appoint[0][:3] == 'lab':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Lab'")
            data = cursor.fetchall()
        buttons = []
        for slot in data:
            slot_time = str(slot[0])
            buttons.append({"title": slot_time, "payload": slot_time})
        dispatcher.utter_message(text=f"Available slots for {appoint[0]} on date: {appoint[1]}", buttons=buttons)
        cursor.close()
        db.close()
        return []
    
class SelectLanguageText(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        appoint.append(tracker.get_slot('Time'))  # Split the message into words
        print(appoint)
        name = tracker.get_slot('Name')
        number = tracker.get_slot('PhoneNumber')
        address = tracker.get_slot('Address')[0]
        dispatcher.utter_message(text=f"To be Continued\n{name} {number} {address}")
        return [] 
#rasa run -m models --enable-api --cors "*" --debug  
