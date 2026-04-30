import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

# Путь к файлу избранных пользователей
FAVORITES_FILE = "favorites.json"

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

def search_user():
    username = entry_username.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.HTTPError:
        messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def display_user(user_data):
    listbox_results.delete(0, tk.END)
    listbox_results.insert(tk.END, f"Логин: {user_data.get('login')}")
    listbox_results.insert(tk.END, f"Имя: {user_data.get('name')}")
    listbox_results.insert(tk.END, f"URL: {user_data.get('html_url')}")
    # Сохраняем данные пользователя для избранного
    global current_user
    current_user = user_data

def add_to_favorites():
    if not current_user:
        messagebox.showwarning("Ошибка", "Сначала выполните поиск пользователя.")
        return

    favorites = load_favorites()
    # Проверяем, нет ли уже в избранном
    if any(u.get('login') == current_user.get('login') for u in favorites):
        messagebox.showinfo("Информация", "Пользователь уже в избранном.")
        return

    favorites.append(current_user)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное.")

# --- GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("400x400")

frame_search = tk.Frame(root)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Введите логин пользователя:").pack(side=tk.LEFT)
entry_username = tk.Entry(frame_search, width=30)
entry_username.pack(side=tk.LEFT, padx=5)
tk.Button(frame_search, text="Поиск", command=search_user).pack(side=tk.LEFT)

listbox_results = tk.Listbox(root, width=50, height=10)
listbox_results.pack(pady=10)

tk.Button(root, text="Добавить в избранное", command=add_to_favorites).pack(pady=5)

current_user = None

root.mainloop()