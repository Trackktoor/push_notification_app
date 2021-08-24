import os
from threading import Thread
from tkinter import *
from tkinter import messagebox  
import json

def flow1():
    os.system("py main_push_alert.py")

def flow2():

    def add_new_alert():
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
            time_for_alert  = [
                time_year_entry.get(),
                time_mounth_entry.get(),
                time_day_entry.get(),
                time_H_entry.get(),
                time_minute_entry.get(),
                time_second_entry.get()
                ]

            for el in time_for_alert:
                try:
                    int(el)
                    if el == '':
                        messagebox.showinfo("Ошибка", "Все поля должны быть заполнены")   
                        return
                    else:
                        data['data'].append({"message": message_entry.get(), "title": "Уведомление", "time": ' '.join(
                            time_for_alert
                    )})
                except:
                    messagebox.showinfo("Ошибка", "Пожалуйста, вводите только числа")
                    return
        
        with open('data.json', 'w', encoding="utf-8") as f:
            json.dump(data, f,  ensure_ascii=False, indent=4)

    window = Tk()
    window.title("Менеджер уведомлений")

    lbl = Label(window, text="Добавь новое уведомление: ")
    lbl.grid(column=0, row=0)

    # Поля для времени уведомления
    #=================================================================================================================#
    time_year_txt = Label(window, text="Год: ")
    time_year_txt.grid(column=0, row=2)
    time_year_entry = Entry(window, width=10)
    time_year_entry.grid(column=2, row=2)

    time_mounth_txt = Label(window, text="Месяц: ")
    time_mounth_txt.grid(column=0, row=3)
    time_mounth_entry = Entry(window, width=10)
    time_mounth_entry.grid(column=2, row=3)

    time_day_txt = Label(window, text="День: ")
    time_day_txt.grid(column=0, row=4)
    time_day_entry = Entry(window, width=10)
    time_day_entry.grid(column=2, row=4)

    time_H_txt = Label(window, text="Час: ")
    time_H_txt.grid(column=0, row=5)
    time_H_entry = Entry(window, width=10)
    time_H_entry.grid(column=2, row=5)

    time_minute_txt = Label(window, text="Минуты: ")
    time_minute_txt.grid(column=0, row=6)
    time_minute_entry = Entry(window, width=10)
    time_minute_entry.grid(column=2, row=6)

    time_second_txt = Label(window, text="Секкунды: ")
    time_second_txt.grid(column=0, row=7)
    time_second_entry = Entry(window, width=10)
    time_second_entry.grid(column=2, row=7)
    #=================================================================================================================#

    message_txt = Label(window, text="Сообщение: ")
    message_txt.grid(column=0, row=8)
    message_entry = Entry(window, width=10)
    message_entry.grid(column=2, row=8)

    btn = Button(window, text="Клик!", command=add_new_alert)  
    btn.grid(column=2, row=9)  

    window.geometry('400x250')
    
    window.mainloop()

thread1 = Thread(target=flow1)
thread2 = Thread(target=flow2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()



