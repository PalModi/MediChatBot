# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector as mc
import random

from .Functions.translator import database_cred
from .Functions.test_information import SelectLanguageText,ActionConvertText,ActionDisplayCard,language
from .Functions.appointment import ActionAskVisit,ActionAskDate,ActionShowSlots,ActionBookAppointment

translator = Translator()
#####################################################Medical test information#####################################################################       

#################################################################Book an Appointment############################################################################

#####################################################################Admin pannel#################################################################
admin = []    
class ActionCheckPassword(Action):
    def name(self) -> Text:
        return "action_check_password"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get('text', '').strip()
        if text=="abc@1230":
            option_to_intent_mapping = {
            '🔬'+"MedicalTests": "lab_tests1",
            '📅'+"Book An Appointment": "Appointment_booking1",
        }
            # Generate buttons dynamically
            buttons = []
            for option,intent_name in option_to_intent_mapping.items():
                buttons.append({"title": option, "payload": f"/{intent_name}"})
            button_reply = "In which of the following you want to make changes: "
            # Send the message with dynamic buttons
            dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)  
        else:
            dispatcher.utter_message(text="Wrong password!😒")
        
        return []

class AdminSelectSelTestDetail(Action):
    def name(self) -> Text:
        return "action_get_selected_test_details"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text','')
        print(text)
        if text[0]=='a' or text[:2]=="a.":
            db = database_cred(mc)
            cursor = db.cursor()
            cursor.execute("SELECT test_type,test_type_type,name,description,price,precondition,reporting FROM test INNER JOIN card ON test.test_type_type = card.test_t_t WHERE test_type_type='cbc'")
            data = cursor.fetchall()
            cursor.close()
            db.close()
            dispatcher.utter_message(data[0][0])
        else:
            dispatcher.utter_message(text="To be released soon")
        return []   

class AdminSelectLanguageText(Action):
    def name(self) -> Text:
        return "action_booking_change"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        language.append(text)
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🏠'+"Home Visit": "homevisit",
            '🏥'+"Lab Visit": "labvisit",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply ="Please choose one of the following options: "
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return [] 

class ActionShowData(Action):
    def name(self) -> Text:
        return "action_show_data"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        text = latest_message.get('text','')
        admin.append(text)
        # Connect to MySQL
        db = mc.connect(
            host="localhost",
            user="root",
            password="Rasa#098",
            database="medichat"
        )
        cursor = db.cursor()
        data = []
        
        if admin[0][:4] == 'home':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Home'")
            data = cursor.fetchall()
        elif admin[0][:3] == 'lab':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Lab'")
            data = cursor.fetchall()
        cursor.close()
        db.close()
        data_text = "Here is the previous slots mentioned <br>"
        for i in data:
            data_text+=i[0]+"<br>"
        dispatcher.utter_message(text=data_text,parse_mode="Markdown")        
        return []


class ActionAddDel(Action):
    def name(self) -> Text:
        return "action_add_upd_del"
  #  @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            option_to_intent_mapping = {
            "✔Add": "add",
            "❌Delete": "delete"
        }
            # Generate buttons dynamically
            buttons = []
            for option,intent_name in option_to_intent_mapping.items():
                buttons.append({"title": option, "payload": f"{intent_name}"})
            button_reply = "In which of the following you want change in your slots: "
            # Send the message with dynamic buttons
            dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)   

            return []

class ActionAskTime(Action):
    def name(self) -> Text:
        return "action_ask_time"
  #  @action_timeout    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            latest_message = tracker.latest_message
            text = latest_message.get('text','')
            admin.append(text)

            dispatcher.utter_message(text=f"Enter the slot time which you want to {admin[1]}<br>Example: 10:00 <b>HH:MM</b>")

            return []

class  ActionChangeTime(Action):
    def name(self) -> Text:
        return "action_change_time"
  #  @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            latest_message = tracker.latest_message
            text = latest_message.get('text','')
            admin.append(text)

            db = mc.connect(
            host="localhost",
            user="root",
            password="Rasa#098",
            database="medichat"
            )
            cursor = db.cursor()
            data = []
            if admin[0][:4]=='home':
                if admin[1]=='add':
                    cursor.execute("INSERT INTO slots (slot_time,appointment_type) VALUES (%s,%s)",(admin[2]+":00",'Home',))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='Home'")
                    data = cursor.fetchall()
                    db.commit()
                elif admin[1]=='delete':
                    cursor.execute("DELETE FROM slots WHERE slot_time= %s ",(admin[2]+":00",))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='Home'")
                    data = cursor.fetchall()
                    db.commit()
            elif admin[0][:3]=='lab':
                if admin[1]=='add':
                    cursor.execute("INSERT INTO slots (slot_time,appointment_type) VALUES (%s,%s)",(admin[2]+":00",'Lab',))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='lab'")
                    data = cursor.fetchall()
                    db.commit()
                elif admin[1]=='delete':
                    cursor.execute("DELETE FROM slots WHERE slot_time= %s ",(admin[2]+":00",))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='lab'")
                    data = cursor.fetchall()
                    db.commit()        

            cursor.close()
            db.close()
            text = "Updated Slots: <br>"
            for i in data:
                text+="  "+i[0]+'<br>'
            dispatcher.utter_message(text=text,parse_mode="Markdown")  
            admin.clear()      
            return [SlotSet("is_authenticated", None)]
    
#rasa run -m models --enable-api --cors "*" --debug  