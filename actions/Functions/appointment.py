from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector as mc
import random
from .test_information import language

translator = Translator()
appoint = []
class ActionAskVisit(Action):
    def name(self) -> Text:
        return "action_ask_visit"
  # @action_timeout
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

class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"
  #  @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        appoint.append(text)
        date_desc = translator.translate('Enter the date on which you want to book appointment',dest=f'{language[0][:2]}').text
        dispatcher.utter_message(text=f"📅{date_desc}<br>In dd-mm-yyyy format for eg 02-05-2024",parse_mode="Markdown")

        return []
    
class ActionShowSlots(Action):
    def name(self) -> Text:
        return "action_show_slots"
   # @action_timeout
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
            password="Rasa#098",
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
        dispatcher.utter_message(text=translator.translate(f"Available slots for {appoint[0]} on date: {appoint[1]}👇",dest=f'{language[0][:2]}').text, buttons=buttons)
        cursor.close()
        db.close()
        return []
    
class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"
   # @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appoint.append(tracker.get_slot('Time'))  
        name = tracker.get_slot('Name')
        number = str(tracker.get_slot('PhoneNumber'))
        address = tracker.get_slot('Address')[0]
        random_number = random.randint(999,10000)
        db = mc.connect(
            host="localhost",
            user="root",
            password="Rasa#098",
            database="medichat"
        )
        cursor = db.cursor()

        if appoint[0][:4]=='home':
            cursor.execute("INSERT INTO user (id,name,number,address) VALUES (%s,%s,%s,%s)",(random_number,name,number,address))
            cursor.execute("INSERT INTO appointment (user_id,date,time) VALUES (%s,%s,%s)",(random_number,appoint[1],appoint[2]))
            db.commit()
            cursor.execute("SELECT user_id,date,time FROM user INNER JOIN appointment ON user.id = appointment.user_id WHERE user.id=%s",((random_number,)))
            data = cursor.fetchall()
            dispatcher.utter_message(text="✔"+translator.translate(f"The lab-testers will be arriving for 🏠 Home-visit on {data[0][1]} at {data[0][2]}<br>your <b>appointment id</b> is <b>{data[0][0]}</b> ",dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        elif appoint[0][:3]=='lab':
            cursor.execute("INSERT INTO user (id,name,number,address) VALUES (%s,%s,%s,%s)",(random_number,name,str(number),'lab-visit'));
            cursor.execute("INSERT INTO appointment (user_id,date,time) VALUES (%s,%s,%s)",(random_number,appoint[1],appoint[2]))
            db.commit()   
            cursor.execute("SELECT user_id,date,time FROM user INNER JOIN appointment ON user.id = appointment.user_id WHERE user.id=%s",((random_number,)))
            data = cursor.fetchall()
            dispatcher.utter_message(text="✔"+translator.translate(f"Your appointment for 🏥 Lab-visit is fixed on {data[0][1]} at {data[0][2]}<br>your <b>appointment id</b> is <b>{data[0][0]}</b> ",dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        
        cursor.close()
        db.close()
        appoint.clear()
        language.clear()
        return [AllSlotsReset()] 