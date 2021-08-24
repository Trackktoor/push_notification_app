import win10toast
from datetime import datetime
import platform, os
import sys
import time
import json

class Push_alert:


    def push(self, message, title):
        plt = platform.system()

        if plt == "Darwin":
            command = '''
            osascript -e 'display notification "{message}" with title "{title}"'
            '''
        elif plt == "Linux":
            command = f'''
            notify-send "{title}" "{message}"
            '''
        elif plt == "Windows":
            win10toast.ToastNotifier().show_toast(title, message)
    
    def add_new_alert(self, time, message, title):
    
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
            data['data'].append({"message": message, "title": title, "time": time})
        with open('data.json', 'w', encoding="utf-8") as f:
            json.dump(data, f,  ensure_ascii=False, indent=4)
    
    def run(self):
        while True:
            time.sleep(1)
            with open('data.json', encoding="utf-8") as f:
                data = json.load(f)
            
            i = 0
            if len(data["data"]) > 0:
                elem = data["data"][i]
                while i <= len(data["data"]):

                    if datetime.now() >= datetime.strptime(str(elem["time"]), "%Y %m %d %H %M %S"):
                        self.push(elem["message"], elem["title"])

                        del data["data"][i]

                        with open('data.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f,  ensure_ascii=False, indent=4)
                        
                        i += 1



push_alert = Push_alert()

push_alert.run()



    