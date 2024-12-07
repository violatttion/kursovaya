import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# Создание базы данных
def initialize_database():
    conn = sqlite3.connect('cafe_orders.db')
    c = conn.cursor()

    # Таблица пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')

    # Таблица заказов
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    order_details TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')

    # Создание аккаунтов администратора и сотрудника (при первом запуске)
    c.execute("SELECT * FROM users WHERE role='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('admin', 'admin', 'admin'))
    c.execute("SELECT * FROM users WHERE role='employee'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('employee', 'employee', 'employee'))

    conn.commit()
    conn.close()


# Функция регистрации
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        conn = sqlite3.connect('cafe_orders.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
        else:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, password, 'user'))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация завершена")
        conn.close()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля")


# Функция авторизации
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        conn = sqlite3.connect('cafe_orders.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            role = user[3]
            if role == 'user':
                user_interface(user[0])
            elif role == 'admin':
                admin_interface()
            elif role == 'employee':
                employee_interface()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля")


# Интерфейс пользователя
def user_interface(user_id):
    def place_order():
        order_details = []
        if var_pasta.get():
            order_details.append("Паста Карбонара")
        if var_soup.get():
            order_details.append("Грибной крем-суп")
        if var_tiramisu.get():
            order_details.append("Тирамису")

        if order_details:
            conn = sqlite3.connect('cafe_orders.db')
            c = conn.cursor()
            c.execute("INSERT INTO orders (user_id, order_details, status) VALUES (?, ?, ?)",
                      (user_id, ', '.join(order_details), 'Принят'))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Ваш заказ оформлен")
        else:
            messagebox.showerror("Ошибка", "Выберите хотя бы одно блюдо")

    user_window = tk.Toplevel()
    user_window.title("Меню кафе")

    tk.Label(user_window, text="Выберите блюда:").pack()

    var_pasta = tk.BooleanVar()
    var_soup = tk.BooleanVar()
    var_tiramisu = tk.BooleanVar()

    tk.Checkbutton(user_window, text="Паста Карбонара", variable=var_pasta).pack()
    tk.Checkbutton(user_window, text="Грибной крем-суп", variable=var_soup).pack()
    tk.Checkbutton(user_window, text="Тирамису", variable=var_tiramisu).pack()

    tk.Button(user_window, text="Оформить заказ", command=place_order).pack()


# Интерфейс администратора
def admin_interface():
    def refresh_orders():
        conn = sqlite3.connect('cafe_orders.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE status='Принят'")
        orders = c.fetchall()
        conn.close()

        tree_orders.delete(*tree_orders.get_children())
        for order in orders:
            tree_orders.insert('', 'end', values=(order[0], order[2], order[3]))

    def send_to_employee():
        selected_item = tree_orders.selection()
        if selected_item:
            order_id = tree_orders.item(selected_item)['values'][0]
            conn = sqlite3.connect('cafe_orders.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET status='Передан сотруднику' WHERE id=?", (order_id,))
            conn.commit()
            conn.close()
            refresh_orders()
            messagebox.showinfo("Успех", "Заказ передан сотруднику")

    admin_window = tk.Toplevel()
    admin_window.title("Управление заказами")

    tree_orders = ttk.Treeview(admin_window, columns=("ID", "Заказ", "Статус"), show='headings')
    tree_orders.heading("ID", text="ID")
    tree_orders.heading("Заказ", text="Заказ")
    tree_orders.heading("Статус", text="Статус")
    tree_orders.pack()

    tk.Button(admin_window, text="Обновить", command=refresh_orders).pack()
    tk.Button(admin_window, text="Передать сотруднику", command=send_to_employee).pack()

    refresh_orders()


# Интерфейс сотрудника
def employee_interface():
    def refresh_orders():
        conn = sqlite3.connect('cafe_orders.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE status='Передан сотруднику'")
        orders = c.fetchall()
        conn.close()

        tree_orders.delete(*tree_orders.get_children())
        for order in orders:
            tree_orders.insert('', 'end', values=(order[0], order[2], order[3]))

    def mark_as_ready():
        selected_item = tree_orders.selection()
        if selected_item:
            order_id = tree_orders.item(selected_item)['values'][0]
            conn = sqlite3.connect('cafe_orders.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET status='Готов' WHERE id=?", (order_id,))
            conn.commit()
            conn.close()
            refresh_orders()
            messagebox.showinfo("Успех", "Заказ помечен как готовый")

    employee_window = tk.Toplevel()
    employee_window.title("Сбор заказов")

    tree_orders = ttk.Treeview(employee_window, columns=("ID", "Заказ", "Статус"), show='headings')
    tree_orders.heading("ID", text="ID")
    tree_orders.heading("Заказ", text="Заказ")
    tree_orders.heading("Статус", text="Статус")
    tree_orders.pack()

    tk.Button(employee_window, text="Обновить", command=refresh_orders).pack()
    tk.Button(employee_window, text="Пометить как готовый", command=mark_as_ready).pack()

    refresh_orders()


# Главный экран
root = tk.Tk()
root.title("Система управления заказами в кафе")

tk.Label(root, text="Имя пользователя:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Пароль:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Войти", command=login_user).pack()
tk.Button(root, text="Регистрация", command=register_user).pack()

initialize_database()
root.mainloop()
