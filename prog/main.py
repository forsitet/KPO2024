from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
import schedule



load_dotenv()
TOKEN = os.getenv("TOKEN")
GROUP_ID = os.getenv("GROUP_ID") 
version = os.getenv("version")

url_global = "https://api.vk.com/method/"
log_file = "birthday_log.txt"


def get_group_members_with_birthdays():
    
    method_api = "groups.getMembers"
    url = url_global + method_api
    params = {"group_id": GROUP_ID, "v": version,  "access_token": TOKEN, "fields": "bdate"}
    members = requests.get(url, params).json()["response"]
    # today = (datetime.now() + timedelta(days=1)).strftime("%d.%m")
    today = "29.11"
    birthdays = []

    for member in members["items"]:
         if 'bdate' in member:  # Учитываем только полные даты (дд.мм.гггг)
             if today == ".".join(member['bdate'].split('.')[:2]):
                 birthdays.append({"name": member['first_name'] + " " + member['last_name'], 
                                   "id": member["id"]})
    
    return(birthdays)


def post_birthday_congratulations(birthdays, no_test = 1):
    
    method_api = "wall.post"
    url = url_global + method_api
    message = ""
    with open(log_file, "a", encoding="utf-8") as file:
        if birthdays:
            for member in birthdays:
                message += "🎉 Сегодня день рождения у: \n" + f"@id{member["id"]}({member["name"]})" +  "\n\nПоздравляем! 🥳"
                params = {"owner_id": "-"+ GROUP_ID, "v": version, "message":message, "publish_date": "1735624800", "access_token": TOKEN}
            if no_test:
                response = requests.get(url, params).json()
            else:
                response = {'response': {'post_id': "test"}}
            
        else:
            response = "Сегодня именинников нет."
            
        file.write(f"{datetime.now()}: {response}\n")


# schedule.every().day.at("12:00").do(post_birthday_congratulations)
# while True:
#     schedule.run_pending()
if __name__ == "__main__":
    birthdays = get_group_members_with_birthdays()
    post_birthday_congratulations(birthdays)
