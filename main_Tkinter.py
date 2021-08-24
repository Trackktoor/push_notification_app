from tkinter import *
from tkinter import messagebox  
import psycopg2
import os
from validate_email import validate_email

# ФУНКЦИИ ДЛЯ БАЗЫ ДАННЫХ
#=================================================================================================================#
# функция подклюения к базе данных
def connecting_to_DB():
    con = psycopg2.connect(
        database="push_alert_DB",
        user="postgres",
        password="roma.ru12",
        host="127.0.0.1",
        port="5432"
    )
    return con

# функция создания пользователя в базе данных
def create_user_in_DB(con, name, email, password):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO USERS (NAME,EMAIL,PASSWORD) VALUES('{0}', '{1}', '{2}')".format(name, email, password)
    )
    con.commit()
    con.close()

# функция для проверкаи пользователя в базе данных, если есть возвращает True, иначе False
def сhecking_user_in_DB(con, email):
    cur = con.cursor()
    cur.execute("SELECT EMAIL from USERS")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == email:
            return True
        else:
            continue

    return False

# функция для проверки валидности пароля 
def checking_password_for_user(con, email, password):
    cur = con.cursor()
    cur.execute("SELECT EMAIL, PASSWORD from USERS")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == email and row[1] == password:
            con.close()
            return True
        else:
            continue

    con.close()


#=================================================================================================================#


# ФУНКЦИИ ДЛЯ РЕАЛИЗАЦИИ ПРОВЕРКИ ВВЕДЁННЫХ ДАННЫХ И ЗАНЕСЕНИЯ ИХ В БД (registrate)
#=================================================================================================================#
# проверка полей
def checking_data_fileds(name, email, password):
    password_check = entry_for_password_check.get()

    if (
        # Проверки на пустоту полей
        len(name) != 0 and
        len(email) != 0 and  
        len(password) != 0
    ):  
        if password == password_check: # Проверка совпадения пароля в двух полях
            if not email.endswith("@gmail.com") or validate_email(email, verify=True) == None: # проерка на влидность и существование почты
                messagebox.showinfo("Уведомление", "Ошибка регистрации: неправильная почта!")
                return False

            elif len(name) <= 3:
                messagebox.showinfo("Уведомление", "Ошибка регистрации: Ник слишком маленький!")
                return False

            elif len(password) < 6:
                messagebox.showinfo("Уведомление", "Ошибка регистрации: Пароль слишком маленький!")
                return False

            else:
                return True

        else:
            messagebox.showinfo("Уведомление", "Ошибка регистрации: Пароли не совпдают!")
            return False
    else:
        messagebox.showinfo("Уведомление", "Ошибка регистрации: Есть незаполненные поля!")
        return False

# Проеврка юзера в базе данных если его там нет, выдает сообщение об этом, если есть регистрирует и выводит сообщение о регистрации
def registrate():
    global entry_for_name
    global entry_for_email
    global entry_for_password

    name = entry_for_name.get()
    email = entry_for_email.get()
    password = entry_for_password.get()
    con = connecting_to_DB()

    if checking_data_fileds(name, email, password):
        if not сhecking_user_in_DB(con, email):
            create_user_in_DB(con, name, email, password)
            messagebox.showinfo("Уведомление", "Регистрация прошла успешно!")
        else:
            messagebox.showinfo("Уведомление", "Ошибка регистрации: Аккаунт с такой почтой уже зарегестрирован!")
#=================================================================================================================#


# ФУНКЦИИ ДЛЯ РЕАЛИЗАЦИИ ПРОВЕРКИ ВВЕДЁННЫХ ДАННЫХ И НАХОЖДЕНИЯ ИХ В БД (login)
#=================================================================================================================#
def login():

    con = connecting_to_DB()
    email = entry_for_email.get()
    password = entry_for_password.get()

    if сhecking_user_in_DB(con, email):
        if checking_password_for_user(con, email, password):
            window.destroy()
            os.system('py Untitled-1.pyw')
        else:
            messagebox.showinfo("Уведомление", "Ошибка входа: Не правельный пароль или логин")
    else:
        messagebox.showinfo("Уведомление", "Ошибка входа: Не правельный пароль или логин")
#=================================================================================================================#


# GUI ДЛЯ ВОХОДА/РЕГИСТРАЦИИ
#=================================================================================================================#

def clear_window():
    for child in window.winfo_children():
        child.destroy()

def GUI_for_registrate():
    clear_window()

    global entry_for_name
    global entry_for_email
    global entry_for_password
    global entry_for_password_check

    welcome_lbl = Label(window, text="Здравствуйте", font=("Arial Bold", 15))
    welcome_lbl.grid(column=0, row=0, sticky=(N, W), pady=(7,0))
    welcome_lbl.grid_configure(pady=20)

    registrate_lbl = Label(window, text="Пожалуйста зарегестрируйтесь!", font=("Arial Bold", 13))
    registrate_lbl.grid(column=0, row=1, sticky=(N, W))

    name_lbl = Label(window, text="Ник:")
    name_lbl.grid(column=0, row=2, sticky=(N,W))

    entry_for_name = Entry(window, width=WIDTH)
    entry_for_name.grid(column=1, row=2, sticky=(N, W))
    entry_for_name.focus()

    email_lbl = Label(window, text="Почта:")
    email_lbl.grid(column=0, row=3, sticky=(N,W))

    entry_for_email = Entry(window, width=WIDTH)
    entry_for_email.grid(column=1, row=3, sticky=(N, W))

    password_lbl = Label(window, text="Пароль:")
    password_lbl.grid(column=0, row=4, sticky=(N,W))

    entry_for_password = Entry(window, width=WIDTH)
    entry_for_password.grid(column=1, row=4, sticky=(N, W))

    password_check_lbl = Label(window, text="Повторите пароль:")
    password_check_lbl.grid(column=0, row=5, sticky=(N,W))

    entry_for_password_check = Entry(window, width=WIDTH)
    entry_for_password_check.grid(column=1, row=5, sticky=(N, W))

    btn_for_registrate = Button(window, text="Регистрация", fg="Blue", command=registrate)
    btn_for_registrate.grid(row=6, sticky=(N, W), pady=10)


def GUI_for_login():
    clear_window()

    global entry_for_email
    global entry_for_password

    welcome_lbl = Label(window, text="Вход в аккаунт", font=("Arial Bold", 15))
    welcome_lbl.place(relx=0.5, rely=0.07, anchor=CENTER)

    email_lbl = Label(window, text="Email:", font=("Arial Bold", 10))
    email_lbl.place(relx=0.3, rely=0.3, anchor=CENTER)

    entry_for_email = Entry(window, width=WIDTH)
    entry_for_email.place(relx=0.6, rely=0.3, anchor=CENTER)

    password_lbl = Label(window, text="Пароль:", font=("Arial Bold", 10))
    password_lbl.place(relx=0.3, rely=0.5, anchor=CENTER)

    entry_for_password = Entry(window, width=WIDTH)
    entry_for_password.place(relx=0.6, rely=0.5, anchor=CENTER)

    btn_login = Button(window, text="Вход", font=("Arial Bold", 10), command=login)
    btn_login.place(relx=0.5, rely=0.7, anchor=CENTER, width=60)



#=================================================================================================================#   


window = Tk()
window.title("Alert")

window.geometry("450x230")

WIDTH = 30

lbl1 = Label(window, text="Добро пожаловать", font=("Arial Bold", 15), width=WIDTH)
lbl1.place(relx=0.5, rely=0.07, anchor=CENTER)

lbl2 = Button(window, text="Вход", font=("Arial Bold", 15), command=GUI_for_login)
lbl2.place(relx=0.4, rely=0.5, anchor=E)

lbl3 = Button(window, text="Регистрация", font=("Arial Bold", 15), command=GUI_for_registrate)
lbl3.place(relx=0.6, rely=0.5, anchor=CENTER)


window.mainloop()