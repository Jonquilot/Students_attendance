import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


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
