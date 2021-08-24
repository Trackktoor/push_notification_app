import os
from threading import Thread
from tkinter import *
import json

def flow1():
    os.system("py main_push_alert.py")

def flow2():

    def add_new_alert():
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
            data['data'].append({"message": message_entry.get(), "title": "Уведомление", "time": time_entry.get()})
        with open('data.json', 'w', encoding="utf-8") as f:
            json.dump(data, f,  ensure_ascii=False, indent=4)

    window = Tk()
    window.title("Менеджер уведомлений")

    lbl = Label(window, text="Добавь новое уведомление: ")
    lbl.grid(column=0, row=0)

    time_txt = Label(window, text="Время: ")
    time_txt.grid(column=0, row=2)
    time_entry = Entry(window, width=10)
    time_entry.grid(column=2, row=2)

    message_txt = Label(window, text="Сообщение: ")
    message_txt.grid(column=0, row=1)
    message_entry = Entry(window, width=10)
    message_entry.grid(column=2, row=1)

    btn = Button(window, text="Клик!", command=add_new_alert)  
    btn.grid(column=2, row=3)  

    window.geometry('400x250')
    
    window.mainloop()

thread1 = Thread(target=flow1)
thread2 = Thread(target=flow2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()



