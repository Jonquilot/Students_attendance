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
        status = print("Посещение", "Был ли студент? (был/не был):")
        if status == "был":
            students[name].append(1)
            save_students(file_path, students)
        elif status == "не был":
            students[name].append(0)
            save_students(file_path, students)
        else: 
            print("Ошибка", "Введите 'был' или 'не был'.")

# Функция вывода низкой посещаемости
def show_low_attendance():
    result = ""
    for student, records in students.items():
        if records:
            percent = sum(records) / len(records)
            if percent < 0.75:
                result += f"{student}: {percent*100:.1f}%\n"
    if result:
        print("Низкая посещаемость (<75%)", result)
    else:
        print("Низкая посещаемость", "Нет студентов с низкой посещаемостью.")

# Функция вывода процента посещаемости
def show_attendance_percent():
    result = ""
    for student, records in students.items():
        if records:
            percent = sum(records) / len(records) * 100
            result += f"{student}: {percent:.1f}%\n"
    if result:
        print("Процент посещаемости", result)
    else:
        print("Процент посещаемости", "Нет данных о посещаемости.")
