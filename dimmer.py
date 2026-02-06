import tkinter as tk
from tkinter import messagebox
import random

# Создаем главное окно
root = tk.Tk()
root.title("Генератор кодов для игр")
root.geometry("600x500")

# Делаем окно темным
root.configure(bg='#1e1e1e')

# Заголовок
title_label = tk.Label(
    root,
    text="🎮 ГЕНЕРАТОР КОДОВ",
    font=("Arial", 24, "bold"),
    fg="#00ff88",
    bg='#1e1e1e'
)
title_label.pack(pady=20)

# Подзаголовок
subtitle_label = tk.Label(
    root,
    text="Создает случайные коды для игр",
    font=("Arial", 12),
    fg="#aaaaaa",
    bg='#1e1e1e'
)
subtitle_label.pack()

# Фрейм для настроек
settings_frame = tk.Frame(root, bg='#2d2d2d', relief='ridge', bd=2)
settings_frame.pack(pady=20, padx=40, fill='x')

# Надпись "НАСТРОЙКИ"
settings_label = tk.Label(
    settings_frame,
    text="НАСТРОЙКИ",
    font=("Arial", 14, "bold"),
    fg="#00aaff",
    bg='#2d2d2d'
)
settings_label.pack(pady=10)

# Количество кодов
count_frame = tk.Frame(settings_frame, bg='#2d2d2d')
count_frame.pack(pady=5)

tk.Label(
    count_frame,
    text="Количество кодов:",
    font=("Arial", 11),
    fg="white",
    bg='#2d2d2d'
).pack(side=tk.LEFT, padx=5)

count_var = tk.StringVar(value="10")
count_entry = tk.Entry(
    count_frame,
    textvariable=count_var,
    width=10,
    font=("Arial", 11),
    bg='#3c3c3c',
    fg='white',
    insertbackground='white'
)
count_entry.pack(side=tk.LEFT, padx=5)

# Длина кода
length_frame = tk.Frame(settings_frame, bg='#2d2d2d')
length_frame.pack(pady=5)

tk.Label(
    length_frame,
    text="Длина каждого кода:",
    font=("Arial", 11),
    fg="white",
    bg='#2d2d2d'
).pack(side=tk.LEFT, padx=5)

length_var = tk.StringVar(value="12")
length_entry = tk.Entry(
    length_frame,
    textvariable=length_var,
    width=10,
    font=("Arial", 11),
    bg='#3c3c3c',
    fg='white',
    insertbackground='white'
)
length_entry.pack(side=tk.LEFT, padx=5)

# Тип кодов
type_frame = tk.Frame(settings_frame, bg='#2d2d2d')
type_frame.pack(pady=10)

tk.Label(
    type_frame,
    text="Использовать:",
    font=("Arial", 11),
    fg="white",
    bg='#2d2d2d'
).pack(side=tk.LEFT, padx=5)

type_var = tk.StringVar(value="both")

tk.Radiobutton(
    type_frame,
    text="Буквы и цифры",
    variable=type_var,
    value="both",
    font=("Arial", 10),
    fg="white",
    bg='#2d2d2d',
    selectcolor='#3c3c3c'
).pack(side=tk.LEFT, padx=5)

tk.Radiobutton(
    type_frame,
    text="Только буквы",
    variable=type_var,
    value="letters",
    font=("Arial", 10),
    fg="white",
    bg='#2d2d2d',
    selectcolor='#3c3c3c'
).pack(side=tk.LEFT, padx=5)

tk.Radiobutton(
    type_frame,
    text="Только цифры",
    variable=type_var,
    value="numbers",
    font=("Arial", 10),
    fg="white",
    bg='#2d2d2d',
    selectcolor='#3c3c3c'
).pack(side=tk.LEFT, padx=5)

# Кнопка генерации
def generate_codes():
    try:
        count = int(count_var.get())
        length = int(length_var.get())
        code_type = type_var.get()
        
        if count <= 0 or length <= 0:
            messagebox.showerror("Ошибка", "Введите положительные числа!")
            return
        
        if count > 100:
            messagebox.showwarning("Внимание", f"Генерация {count} кодов может занять время.")
        
        # Очищаем поле
        result_text.delete(1.0, tk.END)
        
        # Генерируем коды
        chars_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars_numbers = "0123456789"
        
        if code_type == "both":
            chars = chars_letters + chars_numbers
        elif code_type == "letters":
            chars = chars_letters
        else:
            chars = chars_numbers
        
        result_text.insert(tk.END, "="*50 + "\n")
        result_text.insert(tk.END, f"СГЕНЕРИРОВАННЫЕ КОДЫ ({count} шт.):\n")
        result_text.insert(tk.END, "="*50 + "\n\n")
        
        for i in range(count):
            code = ''.join(random.choice(chars) for _ in range(length))
            result_text.insert(tk.END, f"{i+1:3d}. {code}\n")
        
        result_text.insert(tk.END, "\n" + "="*50 + "\n")
        status_label.config(text=f"✓ Сгенерировано {count} кодов!", fg="#00ff88")
        
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")

generate_btn = tk.Button(
    root,
    text="⚡ СГЕНЕРИРОВАТЬ КОДЫ",
    font=("Arial", 14, "bold"),
    bg="#ff6600",
    fg="white",
    padx=30,
    pady=10,
    command=generate_codes,
    cursor="hand2",
    relief="raised",
    bd=3
)
generate_btn.pack(pady=15)

# Фрейм для результатов
result_frame = tk.Frame(root, bg='#2d2d2d')
result_frame.pack(pady=10, padx=20, fill='both', expand=True)

# Поле с результатами
scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill='y')

result_text = tk.Text(
    result_frame,
    height=12,
    font=("Consolas", 10),
    bg='#1a1a1a',
    fg='#00ff00',
    wrap=tk.WORD,
    yscrollcommand=scrollbar.set
)
result_text.pack(side=tk.LEFT, fill='both', expand=True)
scrollbar.config(command=result_text.yview)

# Кнопка копирования
def copy_codes():
    codes = result_text.get(1.0, tk.END).strip()
    if codes:
        root.clipboard_clear()
        root.clipboard_append(codes)
        status_label.config(text="✓ Коды скопированы в буфер обмена!", fg="#00aaff")
    else:
        messagebox.showinfo("Информация", "Сначала сгенерируйте коды")

copy_btn = tk.Button(
    root,
    text="📋 КОПИРОВАТЬ ВСЕ",
    font=("Arial", 10),
    bg="#0099ff",
    fg="white",
    padx=15,
    pady=5,
    command=copy_codes,
    cursor="hand2"
)
copy_btn.pack(pady=5)

# Статус
status_label = tk.Label(
    root,
    text="Готов к работе...",
    font=("Arial", 10),
    fg="#aaaaaa",
    bg='#1e1e1e'
)
status_label.pack(pady=10)

# Информация внизу
info_label = tk.Label(
    root,
    text="Для Standoff 2, CS:GO и других игр | © 2024",
    font=("Arial", 8),
    fg="#666666",
    bg='#1e1e1e'
)
info_label.pack(pady=5)

# Запускаем главный цикл
root.mainloop()
