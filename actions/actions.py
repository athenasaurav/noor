from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
# This action is a default action on rasa to make the fallback action execute
class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from email.mime.text import MIMEText
import smtplib

class ActionEmailGenerate(Action):
    def name(self) -> Text:

        return "action_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        advisor_name = tracker.get_slot("advisor_name") #fill the variable with advisor_name slot
        stu_id= tracker.get_slot("id_stu")#fill the variable with id_stu slot
        stu_email = stu_id + "@student.ksu.edu.sa" #concatenate stu_id slot with email after validating the email
        inquiry = tracker.get_slot("inquiry")#fill the variable with inquiry slot

        smtp = smtplib.SMTP('smtp.gmail.com',587)
        smtp.starttls()

        # SENDERS EMAIL ADDRESS = type the senders email address down below (You can add yours email address here to test)
        # PASSWORD = type the senders email password down below inside brackets
        smtp.login('arshidniksu@gmail.com', 'AGNRN@55')# loging in with the chatbot email

        # insert the body of the email inside of the brackets 
        msg = MIMEText("مرحبا {0}\n تم تحويل هذا الاستفسار من قبل طالبتك صاحبة الرقم الجامعي: {1}\n {2} \n\n يرجى الإجابة الاستفسار أعلاه على ايميل الطالبة ({3}) \n شاكرين ومقدرين جهودكم \n فريق أرشدني".format(advisor_name,stu_id,inquiry,stu_email))

        sender = 'arshidniksu@gmail.com' # the sender will be the chatbot
        # retrieving receiver email form the database based on the advisor name
        conn = sqlite3.connect('advisors.db') 
        cursor = conn.cursor()
        sql ="SELECT email FROM advisors WHERE name LIKE '%{}%' ;".format(advisor_name)
        cursor.execute(sql)
        advisor= cursor.fetchone()
        receiver = advisor[0]
        cursor.close() 
        conn.close()
        recipients = [receiver]

        # the subject of the email 
        msg['Subject'] = "استفسار موجه من احدى طالباتك - أرشدني"
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        smtp.sendmail(sender, recipients, msg.as_string())
        smtp.quit()
        dispatcher.utter_message(text = "تم تحويل الاستفسار بنجاح") # message indicates that the email has been sent successfully

        return [] 


from typing import Dict, Text, List, Any
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset
import sqlite3
from sqlalchemy import true

# displaying advisors name by buttons
class AskForSlotAction(Action):
    def name(self) -> Text:
        return "action_ask_advisor_name"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         adviserDep = tracker.get_slot('dep_advisor') #fill the variable with dep_advisor slot
        # retrieving advisor names form the database based on the advisor department
         conn = sqlite3.connect('advisors.db') 
         cursor = conn.cursor()
         sql_placeholder ="SELECT name FROM advisors WHERE departmentName LIKE '%{}%' ;".format(adviserDep)
         cursor.execute(sql_placeholder)
 
         # get all records
         records = cursor.fetchall()
         buttons = []
         for row in records: 
             buttons.append({"title": row[0] , "payload": row[0]})
         # Display them using dispatcher
         dispatcher.utter_message(text="يرجى اختيار اسم مرشدتك الاكاديمية",buttons=buttons)
           
         cursor.close()
         conn.close()

# validating the form number
class ValidateFormNumber(FormValidationAction): #Validation + Sending forms
    def name(self) -> Text:
        return "validate_form_num_form"

    def validate_form_num(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate form_num."""

        if slot_value== "1" or slot_value== "١":
            dispatcher.utter_message(text="تفضلي، هذا النموذج طلبتيه \n https://docdro.id/ZxSepou")
            return {"form_num": slot_value}
        elif slot_value== "2" or slot_value== "٢":
            dispatcher.utter_message(text="تفضلي، هذا النموذج طلبتيه \n https://docdro.id/Rq7pZig")
            return {"form_num": slot_value}
        elif slot_value== "3" or slot_value== "٣":
            dispatcher.utter_message(text="تفضلي، هذا النموذج طلبتيه \n https://docdro.id/EKDllLw")
            return {"form_num": slot_value}
        elif slot_value== "4" or slot_value== "٤":
            dispatcher.utter_message(text="تفضلي، هذا النموذج طلبتيه \n https://docdro.id/cdk0UN6")
            return {"form_num": slot_value}
        elif slot_value== "5" or slot_value== "٥": 
            dispatcher.utter_message(text="تفضلي، هذا النموذج طلبتيه \n https://docdro.id/Qq7tMPU") 
            return {"form_num": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="القيمة المدخلة غير صحيحة، يرجى اعادة ارسالها \n تأكدي من ارسال رقم النموذج لا اسمه")
            return {"form_num": None}
            
# validating the student id to make sure they entered valid id that creat valid email
class ValidateStudentIDSlot(FormValidationAction):
    def name(self) -> Text:
        return "validate_id_form"

    def validate_id_stu(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate id_stu."""
 # make sure that the id is consist of 9 numbers and the first three numbers are valid     
        if len(slot_value)==9 and slot_value.isdecimal(): 
            
            if (slot_value.startswith("435") or slot_value.startswith("436") or slot_value.startswith("437") or
                slot_value.startswith("438") or slot_value.startswith("439") or slot_value.startswith("440") or
                slot_value.startswith("441") or slot_value.startswith("442")):
               # validation succeeded, set the value of the "id_stu" slot to value
                return {"id_stu": slot_value}
            
            else:
                # validation failed, set this slot to None so that the
                # user will be asked for the slot again
                dispatcher.utter_message(text="الرقم المدخل غير صحيح")
                return {"id_stu": None}
        
        else:
             # validation failed, set this slot to None so that the
             # user will be asked for the slot again
             dispatcher.utter_message(text="الرقم المدخل غير صحيح")
             return {"id_stu": None}

class ValidateDepartmentSlot(FormValidationAction):
    def name(self) -> Text:
        return "validate_dep_form"

    def validate_dep_advisor(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate dep_advisor."""
# make sure that the departments are valid

        if (slot_value== "نظم المعلومات" or slot_value== "تقنية المعلومات" 
            or slot_value== "علوم الحاسب" or slot_value== "هندسة البرمجيات"): 
            # validation succeeded, set the value of the "id_stu" slot to value
            return {"dep_advisor": slot_value}

        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="القيمة المدخلة غير صحيحة")
            return {"dep_advisor": None}

# هذي خلوها الين أتاكد أن مافيه طريقة،بس الحين سحبت عليها عشان نكمل الاشياء الأهم الباقية 
# class ValidateAdvisorNameSlot(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_advisor_name_form"

#     def validate_advisor_name(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate advisor_name."""
        
#         conn = sqlite3.connect('advisors.db') 
#         cursor = conn.cursor()
#         sql_placeholder = "SELECT * FROM advisors WHERE name LIKE '%{}%' ;".format(slot_value)
#         cursor.execute(sql_placeholder)
#         # get all records
#         records = cursor.fetchall()

#         if records == []:
#             dispatcher.utter_message(text="القيمة المدخلة غير صحيحة")
#             return {"advisor_name": None}
#         else:
#             return {"advisor_name": slot_value}


class ActionResetForwardingSlots(Action):
    def name(self) -> Text:
        return "action_forward_slots_reset"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            """Sets slotsvalue to None"""

            return[SlotSet(key = "id_stu", value = None),
                   SlotSet(key = "dep_advisor", value = None),
                   SlotSet(key = "advisor_name", value = None),
                   SlotSet(key = "inquiry", value = None)]

# This function reset the slot value to "None"
class ActionResetFormNumber(Action):
    def name(self) -> Text:
        return "action_reset_form_num"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            """Sets form_num to None"""

            return[SlotSet(key = "form_num", value = None)]
