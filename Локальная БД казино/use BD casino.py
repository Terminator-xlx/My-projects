import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Подключение к базе данных
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn, conn.cursor()

# Функция для выполнения SQL-запросов
def execute_query(query, params=()):
    conn, cursor = connect_db()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# Функция для отображения списка клиентов
def show_clients(root):
    clients = execute_query('SELECT * FROM Список_Клиентов')
    client_window = tk.Toplevel(root)
    client_window.title("Список клиентов")
    tree = ttk.Treeview(client_window, columns=("id", "Статус_Клиента", "Имя_клиента", "Страна_Клиента", "Баланс_счета", "ID_Клиента"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Статус_Клиента", text="Статус Клиента")
    tree.heading("Имя_клиента", text="Имя клиента")
    tree.heading("Страна_Клиента", text="Страна Клиента")
    tree.heading("Баланс_счета", text="Баланс счета")
    tree.heading("ID_Клиента", text="ID Клиента")
    for client in clients:
        tree.insert("", "end", values=client)
    tree.pack()

# Функция для отображения списка сотрудников
def show_employees(root):
    employees = execute_query('SELECT * FROM Список_сотрудников')
    employee_window = tk.Toplevel(root)
    employee_window.title("Список сотрудников")
    tree = ttk.Treeview(employee_window, columns=("id", "Отдел_сотрудника", "Имя_сотрудника", "ID_Сотрудника"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Отдел_сотрудника", text="Отдел сотрудника")
    tree.heading("Имя_сотрудника", text="Имя сотрудника")
    tree.heading("ID_Сотрудника", text="ID Сотрудника")
    for employee in employees:
        tree.insert("", "end", values=employee)
    tree.pack()

# Функция для редактирования списка клиентов
def edit_clients(root):
    clients = execute_query('SELECT * FROM Список_Клиентов')
    client_window = tk.Toplevel(root)
    client_window.title("Редактирование списка клиентов")
    tree = ttk.Treeview(client_window, columns=("id", "Статус_Клиента", "Имя_клиента", "Страна_Клиента", "Баланс_счета", "ID_Клиента"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Статус_Клиента", text="Статус Клиента")
    tree.heading("Имя_клиента", text="Имя клиента")
    tree.heading("Страна_Клиента", text="Страна Клиента")
    tree.heading("Баланс_счета", text="Баланс счета")
    tree.heading("ID_Клиента", text="ID Клиента")
    for client in clients:
        tree.insert("", "end", values=client)
    tree.pack()

    # Добавление функционала для редактирования
    def update_client():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        new_values = []
        for i, value in enumerate(values):
            new_value = simpledialog.askstring("Введите новое значение", tree.heading(i)["text"], initialvalue=value)
            new_values.append(new_value)
        tree.item(selected_item, values=new_values)
        execute_query('UPDATE Список_Клиентов SET Статус_Клиента=?, Имя_клиента=?, Страна_Клиента=?, Баланс_счета=?, ID_Клиента=? WHERE id=?', new_values[1:]+[new_values[0]])

    tk.Button(client_window, text="Изменить", command=update_client).pack()

# Функция для редактирования списка сотрудников
def edit_employees(root):
    employees = execute_query('SELECT * FROM Список_сотрудников')
    employee_window = tk.Toplevel(root)
    employee_window.title("Редактирование списка сотрудников")
    tree = ttk.Treeview(employee_window, columns=("id", "Отдел_сотрудника", "Имя_сотрудника", "ID_Сотрудника"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Отдел_сотрудника", text="Отдел сотрудника")
    tree.heading("Имя_сотрудника", text="Имя сотрудника")
    tree.heading("ID_Сотрудника", text="ID Сотрудника")
    for employee in employees:
        tree.insert("", "end", values=employee)
    tree.pack()

    # Добавление функционала для редактирования
    def update_employee():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        new_values = []
        for i, value in enumerate(values):
            new_value = simpledialog.askstring("Введите новое значение", tree.heading(i)["text"], initialvalue=value)
            new_values.append(new_value)
        tree.item(selected_item, values=new_values)
        execute_query('UPDATE Список_сотрудников SET Отдел_сотрудника=?, Имя_сотрудника=?, ID_Сотрудника=? WHERE id=?', new_values[1:]+[new_values[0]])

    tk.Button(employee_window, text="Изменить", command=update_employee).pack()

# Функция для редактирования таблицы Игровой_день_автоматы
def edit_game_day_machines(root):
    machines = execute_query('SELECT * FROM Игровой_день_автоматы')
    machine_window = tk.Toplevel(root)
    machine_window.title("Редактирование игровых автоматов")
    tree = ttk.Treeview(machine_window, columns=("id", "Название_игровой_зоны", "Стоимость_слотов", "Количество_автоматов", "ID_зоны_автоматов"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Название_игровой_зоны", text="Название игровой зоны")
    tree.heading("Стоимость_слотов", text="Стоимость слотов")
    tree.heading("Количество_автоматов", text="Количество автоматов")
    tree.heading("ID_зоны_автоматов", text="ID зоны автоматов")
    for machine in machines:
        tree.insert("", "end", values=machine)
    tree.pack()

    # Добавление функционала для редактирования
    def update_machine():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        new_values = []
        for i, value in enumerate(values):
            new_value = simpledialog.askstring("Введите новое значение", tree.heading(i)["text"], initialvalue=value)
            new_values.append(new_value)
        tree.item(selected_item, values=new_values)
        execute_query('UPDATE Игровой_день_автоматы SET Название_игровой_зоны=?, Стоимость_слотов=?, Количество_автоматов=?, ID_зоны_автоматов=? WHERE id=?', new_values[1:]+[new_values[0]])

    tk.Button(machine_window, text="Изменить", command=update_machine).pack()

# Функция для редактирования таблицы Игровой_день_столы
def edit_game_day_tables(root):
    tables = execute_query('SELECT * FROM Игровой_день_столы')
    table_window = tk.Toplevel(root)
    table_window.title("Редактирование игровых столов")
    tree = ttk.Treeview(table_window, columns=("id", "Название_игровой_зоны", "Стоимость_слотов", "Количество_столов", "ID_зоны_столов"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("Название_игровой_зоны", text="Название игровой зоны")
    tree.heading("Стоимость_слотов", text="Стоимость слотов")
    tree.heading("Количество_столов", text="Количество столов")
    tree.heading("ID_зоны_столов", text="ID зоны столов")
    for table in tables:
        tree.insert("", "end", values=table)
    tree.pack()

    # Добавление функционала для редактирования
    def update_table():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        new_values = []
        for i, value in enumerate(values):
            new_value = simpledialog.askstring("Введите новое значение", tree.heading(i)["text"], initialvalue=value)
            new_values.append(new_value)
        tree.item(selected_item, values=new_values)
        execute_query('UPDATE Игровой_день_столы SET Название_игровой_зоны=?, Стоимость_слотов=?, Количество_столов=?, ID_зоны_столов=? WHERE id=?', new_values[1:]+[new_values[0]])

    tk.Button(table_window, text="Изменить", command=update_table).pack()

# Функция для отправки сообщения службе безопасности
def send_security_message():
    message = simpledialog.askstring("Отправить сообщение", "Введите сообщение для службы безопасности:")
    if message:
        messagebox.showinfo("Сообщение отправлено", f"Сообщение: {message}")

# Функция для отправки сообщения клиентам
def send_client_message():
    message = simpledialog.askstring("Отправить сообщение", "Введите сообщение для клиентов:")
    if message:
        messagebox.showinfo("Сообщение отправлено", f"Сообщение: {message}")

# Функция для отправки сообщения сотрудникам
def send_employee_message():
    message = simpledialog.askstring("Отправить сообщение", "Введите сообщение для сотрудников:")
    if message:
        messagebox.showinfo("Сообщение отправлено", f"Сообщение: {message}")

# Функция для выбора пользователя и ввода пароля
def login(root):
    user = user_var.get()
    password = password_entry.get()
    if password == user:
        main_window(root, user)
    else:
        messagebox.showerror("Ошибка", "Неверный пароль")

# Основное окно после входа
def main_window(root, user):
    root.destroy()
    main_window = tk.Tk()
    main_window.title(f"Добро пожаловать в систему Казино!")

    if user in ["Финансы", "Игровая зона", "Руководство", "Служба безопасности"]:
        tk.Button(main_window, text="Список клиентов", command=lambda: show_clients(main_window)).pack()
    if user in ["Финансы", "Служба безопасности", "Руководство"]:
        tk.Button(main_window, text="Список сотрудников", command=lambda: show_employees(main_window)).pack()
    if user in ["Финансы", "Игровая зона", "Руководство"]:
        tk.Button(main_window, text="Редактировать игровые автоматы", command=lambda: edit_game_day_machines(main_window)).pack()
        tk.Button(main_window, text="Редактировать игровые столы", command=lambda: edit_game_day_tables(main_window)).pack()
    if user in ["Финансы", "Игровая зона", "Руководство"]:
        tk.Button(main_window, text="Отправить сообщение службе безопасности", command=send_security_message).pack()
    if user in ["Игровая зона", "Руководство"]:
        tk.Button(main_window, text="Отправить сообщение клиентам", command=send_client_message).pack()
    if user == "Служба безопасности":
        tk.Button(main_window, text="Отправить сообщение сотрудникам", command=send_employee_message).pack()
    if user == "Руководство":
        tk.Button(main_window, text="Редактировать список клиентов", command=lambda: edit_clients(main_window)).pack()
        tk.Button(main_window, text="Редактировать список сотрудников", command=lambda: edit_employees(main_window)).pack()

    tk.Button(main_window, text="Сменить пользователя", command=lambda: change_user(main_window)).pack()

    main_window.mainloop()

# Функция для смены пользователя
def change_user(current_window):
    current_window.destroy()
    create_login_window()

# Окно входа
def create_login_window():
    global login_window, user_var, password_entry
    login_window = tk.Tk()
    login_window.title("Вход в систему")

    user_var = tk.StringVar(value="Финансы")
    tk.Label(login_window, text="Выберите пользователя:").pack()
    tk.OptionMenu(login_window, user_var, "Финансы", "Игровая зона", "Служба безопасности", "Руководство").pack()

    tk.Label(login_window, text="Введите пароль:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Войти", command=lambda: login(login_window)).pack()

    login_window.mainloop()

# Создание окна входа
create_login_window()