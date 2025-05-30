import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


# Функция загрузки списка студентов
def load_students(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            messagebox.showerror("Ошибка", "Файл поврежден или некорректный формат.") # Тимур
            return {}
    else:
        return {}

# Функция сохранения списка студентов
def save_students(filename, students):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(students, file, ensure_ascii=False, indent=4)
    except IOError:
        messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

# Функция добавления студента
def add_student():
    name = simpledialog.askstring("Добавить студента", "Введите фамилию студента:") # Яна
    if name:
        if name in students:
            messagebox.showinfo("Инфо", "Студент уже существует.")
        else:
            students[name] = []
            save_students(file_path, students)
            update_display()

# Функция удаления студента
def remove_student():
    name = simpledialog.askstring("Удалить студента", "Введите фамилию студента:") # Кира
    if name:
        if name in students:
            del students[name]
            save_students(file_path, students)
            update_display()
        else:
            messagebox.showerror("Ошибка", "Студент не найден.")

# Функция единичной отметки посещаемости
def mark_attendance():
    name = simpledialog.askstring("Отметить посещение", "Введите фамилию студента:") # Настя
    if name:
        if name not in students:
            students[name] = []
        status = simpledialog.askstring("Посещение", "Был ли студент? (был/не был):")
        if status == "был":
            students[name].append(1)
            save_students(file_path, students)
            update_display()
        elif status == "не был":
            students[name].append(0)
            save_students(file_path, students)
            update_display()
        else: 
            messagebox.showerror("Ошибка", "Введите 'был' или 'не был'.")

# Функция вывода низкой посещаемости
def show_low_attendance():
    result = ""
    for student, records in students.items():
        if records:
            percent = sum(records) / len(records)
            if percent < 0.75:
                result += f"{student}: {percent*100:.1f}%\n"
    if result:
        messagebox.showinfo("Низкая посещаемость (<75%)", result)
    else:
        messagebox.showinfo("Низкая посещаемость", "Нет студентов с низкой посещаемостью.")

# Функция вывода процента посещаемости
def show_attendance_percent():
    result = ""
    for student, records in students.items():
        if records:
            percent = sum(records) / len(records) * 100
            result += f"{student}: {percent:.1f}%\n"
    if result:
        messagebox.showinfo("Процент посещаемости", result)
    else:
        messagebox.showinfo("Процент посещаемости", "Нет данных о посещаемости.")

# Функция обновления дисплея
def update_display():
    text_box.delete("1.0", tk.END)
    for student, records in students.items():
        text_box.insert(tk.END, f"{student}: {records}\n")

# Функция массового добавления
def add_many_students():
    names = input("Массовое добавление", "Введите фамилии через запятую:")
    if names:
        for name in map(str.strip, names.split(',')):
            if name and name not in students:
                students[name] = []
        save_students(file_path, students)

# Функция поиска студента по фамилии
def search_student():
    name = input("Поиск студента", "Введите фамилию студента:") # Тимур
    if name:
        if name in students:
            records = students[name]
            if records:
                percent = sum(records) / len(records) * 100
                print("Результат поиска", f"{name}: посещаемость {percent:.1f}% ({records})")
            else:
                print("Результат поиска", f"{name}: пока нет данных о посещении.")
        else:
            print("Ошибка", "Студент не найден.")

# Функция сохранения файла при закрытии
def on_closing():
    save_students(file_path, students)
    root.destroy()


# Начало программы
root = tk.Tk()
root.title("Учёт посещаемости студентов")
root.geometry("600x400")

# Запрос пути к файлу у пользователя
file_path = simpledialog.askstring("Выбор файла", "Введите путь к файлу списка студентов (оставьте пустым для нового):")
if not file_path:
    file_path = "attendance list.json"

students = load_students(file_path)

# Элементы интерфейса
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Добавить студента", command=add_student).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Удалить студента", command=remove_student).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Отметить посещение", command=mark_attendance).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Массовое добавление", command=add_many_students).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Низкая посещаемость", command=show_low_attendance).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Процент посещаемости", command=show_attendance_percent).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Поиск студента", command=search_student).grid(row=1, column=2, padx=5, pady=5)

text_box = tk.Text(root, height=15, width=70)
text_box.pack(pady=10)

update_display()# Яна

root.protocol("WM_DELETE_WINDOW", on_closing) # Яна
root.mainloop() # Яна
