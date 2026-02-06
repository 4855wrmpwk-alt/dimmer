import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
from datetime import datetime

class LightDimmerController:
    def __init__(self, root):
        self.root = root
        self.root.title("Контроллер диммера света")
        self.root.geometry("800x600")
        
        # Настройки по умолчанию
        self.brightness = 50  # Яркость от 0 до 100%
        self.is_on = False
        self.connection_status = False
        self.simulation_mode = True  # Режим симуляции по умолчанию
        
        # Цвета
        self.colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'accent': '#00a8ff',
            'on': '#4cd137',
            'off': '#e84118',
            'panel': '#2d3436'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="💡 Управление диммером света",
            font=('Arial', 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # Фрейм подключения
        connection_frame = tk.LabelFrame(
            self.root,
            text="Подключение",
            font=('Arial', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['panel'],
            relief=tk.GROOVE,
            bd=2
        )
        connection_frame.pack(fill='x', padx=20, pady=10, ipady=5)
        
        # Режим работы
        mode_frame = tk.Frame(connection_frame, bg=self.colors['panel'])
        mode_frame.pack(pady=5)
        
        tk.Label(
            mode_frame,
            text="Режим:",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['panel']
        ).pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="simulation")
        
        tk.Radiobutton(
            mode_frame,
            text="Симуляция",
            variable=self.mode_var,
            value="simulation",
            command=self.toggle_mode,
            font=('Arial', 10),
            fg=self.colors['fg'],
            bg=self.colors['panel'],
            selectcolor=self.colors['panel'],
            activebackground=self.colors['panel']
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            mode_frame,
            text="Реальное устройство",
            variable=self.mode_var,
            value="real",
            command=self.toggle_mode,
            font=('Arial', 10),
            fg=self.colors['fg'],
            bg=self.colors['panel'],
            selectcolor=self.colors['panel'],
            activebackground=self.colors['panel']
        ).pack(side=tk.LEFT, padx=10)
        
        # Порт для реального устройства
        self.device_frame = tk.Frame(connection_frame, bg=self.colors['panel'])
        self.device_frame.pack(pady=5)
        
        tk.Label(
            self.device_frame,
            text="COM порт:",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['panel']
        ).pack(side=tk.LEFT, padx=5)
        
        # Имитация COM портов
        self.port_var = tk.StringVar(value="COM3")
        self.port_combo = ttk.Combobox(
            self.device_frame,
            textvariable=self.port_var,
            width=15,
            state='readonly'
        )
        self.port_combo['values'] = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5']
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        connect_btn = tk.Button(
            self.device_frame,
            text="Подключить",
            command=self.connect_device,
            font=('Arial', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            padx=20
        )
        connect_btn.pack(side=tk.LEFT, padx=10)
        
        # Статус подключения
        self.status_label = tk.Label(
            connection_frame,
            text="🟢 Режим симуляции",
            font=('Arial', 11),
            fg=self.colors['on'],
            bg=self.colors['panel']
        )
        self.status_label.pack(pady=5)
        
        # Основной блок управления
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая панель - управление
        left_panel = tk.Frame(control_frame, bg=self.colors['panel'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Кнопка включения/выключения
        self.power_btn = tk.Button(
            left_panel,
            text="ВКЛЮЧИТЬ",
            command=self.toggle_power,
            font=('Arial', 16, 'bold'),
            bg=self.colors['off'],
            fg='white',
            height=2,
            width=15
        )
        self.power_btn.pack(pady=20)
        
        # Слайдер яркости
        brightness_frame = tk.LabelFrame(
            left_panel,
            text="Яркость",
            font=('Arial', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['panel']
        )
        brightness_frame.pack(fill='x', padx=20, pady=10)
        
        self.brightness_label = tk.Label(
            brightness_frame,
            text=f"{self.brightness}%",
            font=('Arial', 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['panel']
        )
        self.brightness_label.pack(pady=5)
        
        self.brightness_slider = tk.Scale(
            brightness_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_brightness,
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            troughcolor='#34495e',
            highlightbackground=self.colors['panel'],
            sliderrelief='raised',
            sliderlength=30
        )
        self.brightness_slider.set(self.brightness)
        self.brightness_slider.pack(pady=10, padx=20)
        
        # Предустановки
        presets_frame = tk.LabelFrame(
            left_panel,
            text="Предустановки",
            font=('Arial', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['panel']
        )
        presets_frame.pack(fill='x', padx=20, pady=10)
        
        presets_grid = tk.Frame(presets_frame, bg=self.colors['panel'])
        presets_grid.pack(pady=10)
        
        presets = [
            ("Ночник", 10, "#3498db"),
            ("Чтение", 60, "#2ecc71"),
            ("Работа", 80, "#f1c40f"),
            ("Максимум", 100, "#e74c3c")
        ]
        
        for name, value, color in presets:
            btn = tk.Button(
                presets_grid,
                text=name,
                command=lambda v=value: self.set_preset(v),
                font=('Arial', 10),
                bg=color,
                fg='white',
                width=8,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Правая панель - визуализация
        right_panel = tk.Frame(control_frame, bg=self.colors['panel'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Визуализация света
        self.light_canvas = tk.Canvas(
            right_panel,
            bg='black',
            width=300,
            height=300,
            highlightthickness=2,
            highlightbackground=self.colors['accent']
        )
        self.light_canvas.pack(pady=20)
        
        # Создаем эффект света
        self.light_circle = self.light_canvas.create_oval(
            50, 50, 250, 250,
            fill='#333333',
            outline=''
        )
        
        # Информация
        info_frame = tk.Frame(right_panel, bg=self.colors['panel'])
        info_frame.pack(fill='x', padx=20, pady=10)
        
        self.info_label = tk.Label(
            info_frame,
            text="Состояние: Выключено\nЯркость: 0%\nРежим: Симуляция",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['panel'],
            justify=tk.LEFT
        )
        self.info_label.pack()
        
        # Лог
        log_frame = tk.LabelFrame(
            right_panel,
            text="Журнал событий",
            font=('Arial', 10, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['panel'],
            height=100
        )
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(
            log_frame,
            height=5,
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Consolas', 9)
        )
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Кнопки внизу
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        save_btn = tk.Button(
            bottom_frame,
            text="💾 Сохранить настройки",
            command=self.save_settings,
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            padx=20
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        auto_btn = tk.Button(
            bottom_frame,
            text="🔄 Авторегулировка",
            command=self.auto_adjust,
            font=('Arial', 10),
            bg='#1abc9c',
            fg='white',
            padx=20
        )
        auto_btn.pack(side=tk.LEFT, padx=5)
        
        schedule_btn = tk.Button(
            bottom_frame,
            text="⏰ Расписание",
            command=self.show_schedule,
            font=('Arial', 10),
            bg='#e67e22',
            fg='white',
            padx=20
        )
        schedule_btn.pack(side=tk.LEFT, padx=5)
        
        # Инициализация
        self.update_light_visualization()
        self.log_event("Приложение запущено в режиме симуляции")
        
    def toggle_mode(self):
        mode = self.mode_var.get()
        self.simulation_mode = (mode == "simulation")
        if self.simulation_mode:
            self.log_event("Переключен в режим симуляции")
            self.status_label.config(text="🟢 Режим симуляции", fg=self.colors['on'])
        else:
            self.log_event("Переключен в режим реального устройства")
            self.status_label.config(text="⚠️ Для реального устройства установите pyserial", fg='orange')
            messagebox.showinfo("Внимание", 
                              "Для работы с реальным устройством установите модуль pyserial:\n"
                              "Откройте командную строку и выполните:\n"
                              "pip install pyserial")
        
    def connect_device(self):
        """Подключение к устройству"""
        if self.simulation_mode:
            messagebox.showinfo("Информация", "В режиме симуляции подключение не требуется")
            return
            
        port = self.port_var.get()
        if not port:
            messagebox.showerror("Ошибка", "Выберите COM порт")
            return
            
        try:
            # В симуляционном режиме просто показываем сообщение
            self.connection_status = True
            self.status_label.config(text=f"🟢 Подключено к {port}", fg=self.colors['on'])
            self.log_event(f"Подключено к {port} (симуляция)")
            messagebox.showinfo("Успех", 
                              f"Подключение к {port} успешно (симуляция)\n\n"
                              "Для реального подключения:\n"
                              "1. Установите pyserial: pip install pyserial\n"
                              "2. Подключите реальное устройство")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться: {str(e)}")
            self.log_event(f"Ошибка подключения: {str(e)}")
            
    def toggle_power(self):
        """Включение/выключение света"""
        self.is_on = not self.is_on
        
        if self.is_on:
            self.power_btn.config(text="ВЫКЛЮЧИТЬ", bg=self.colors['on'])
            self.log_event("Свет включен")
        else:
            self.power_btn.config(text="ВКЛЮЧИТЬ", bg=self.colors['off'])
            self.log_event("Свет выключен")
            
        self.send_command()
        self.update_light_visualization()
        
    def update_brightness(self, value):
        """Обновление яркости"""
        self.brightness = int(value)
        self.brightness_label.config(text=f"{self.brightness}%")
        
        if self.is_on:
            self.send_command()
            self.update_light_visualization()
            
    def set_preset(self, value):
        """Установка предустановки"""
        self.brightness = value
        self.brightness_slider.set(value)
        self.brightness_label.config(text=f"{value}%")
        
        if not self.is_on:
            self.toggle_power()
            
        self.send_command()
        self.update_light_visualization()
        self.log_event(f"Установлен пресет: {value}%")
        
    def send_command(self):
        """Отправка команды на устройство"""
        if self.simulation_mode:
            # В режиме симуляции просто логируем
            state = "вкл" if self.is_on else "выкл"
            self.log_event(f"Команда: {state}, яркость: {self.brightness}%")
        else:
            # В режиме реального устройства - симуляция отправки
            if self.connection_status:
                power = 1 if self.is_on else 0
                command = f"P{power}B{self.brightness:03d}"
                self.log_event(f"Отправлено (симуляция): {command}")
                    
    def update_light_visualization(self):
        """Обновление визуализации света"""
        if not self.is_on:
            self.light_canvas.itemconfig(self.light_circle, fill='#333333')
            brightness = 0
        else:
            # Вычисляем цвет в зависимости от яркости
            intensity = self.brightness / 100.0
            r = int(255 * intensity)
            g = int(255 * intensity * 0.8)  # Немного меньше зеленого
            b = int(100 * intensity)  # Синего совсем немного
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.light_canvas.itemconfig(self.light_circle, fill=color)
            brightness = self.brightness
            
        # Обновляем информацию
        mode = "Симуляция" if self.simulation_mode else "Реальное устройство"
        state = "Включено" if self.is_on else "Выключено"
        self.info_label.config(
            text=f"Состояние: {state}\nЯркость: {brightness}%\nРежим: {mode}"
        )
        
    def auto_adjust(self):
        """Автоматическая регулировка яркости"""
        self.log_event("Запущена авторегулировка")
        
        def adjust():
            if not self.is_on:
                self.is_on = True
                self.power_btn.config(text="ВЫКЛЮЧИТЬ", bg=self.colors['on'])
                
            for i in range(0, 101, 10):
                if not hasattr(self, 'brightness_slider'):
                    break
                self.brightness = i
                self.brightness_slider.set(i)
                self.brightness_label.config(text=f"{i}%")
                self.update_light_visualization()
                time.sleep(0.2)
                
            self.log_event("Авторегулировка завершена")
            
        thread = threading.Thread(target=adjust)
        thread.daemon = True
        thread.start()
        
    def show_schedule(self):
        """Окно расписания"""
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Расписание")
        schedule_window.geometry("400x300")
        schedule_window.configure(bg=self.colors['bg'])
        
        tk.Label(
            schedule_window,
            text="Расписание включения/выключения",
            font=('Arial', 14, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        ).pack(pady=10)
        
        # Простой планировщик
        schedule_frame = tk.Frame(schedule_window, bg=self.colors['bg'])
        schedule_frame.pack(pady=10)
        
        # Время включения
        tk.Label(
            schedule_frame,
            text="Включить в:",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.on_hour = tk.StringVar(value="18")
        self.on_minute = tk.StringVar(value="00")
        
        tk.Entry(
            schedule_frame,
            textvariable=self.on_hour,
            width=3,
            font=('Arial', 11),
            bg='#3c3c3c',
            fg='white'
        ).grid(row=0, column=1, padx=2)
        
        tk.Label(
            schedule_frame,
            text=":",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).grid(row=0, column=2)
        
        tk.Entry(
            schedule_frame,
            textvariable=self.on_minute,
            width=3,
            font=('Arial', 11),
            bg='#3c3c3c',
            fg='white'
        ).grid(row=0, column=3, padx=2)
        
        # Время выключения
        tk.Label(
            schedule_frame,
            text="Выключить в:",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        self.off_hour = tk.StringVar(value="23")
        self.off_minute = tk.StringVar(value="00")
        
        tk.Entry(
            schedule_frame,
            textvariable=self.off_hour,
            width=3,
            font=('Arial', 11),
            bg='#3c3c3c',
            fg='white'
        ).grid(row=1, column=1, padx=2)
        
        tk.Label(
            schedule_frame,
            text=":",
            font=('Arial', 11),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).grid(row=1, column=2)
        
        tk.Entry(
            schedule_frame,
            textvariable=self.off_minute,
            width=3,
            font=('Arial', 11),
            bg='#3c3c3c',
            fg='white'
        ).grid(row=1, column=3, padx=2)
        
        # Кнопка сохранения расписания
        save_schedule_btn = tk.Button(
            schedule_window,
            text="💾 Сохранить расписание",
            command=self.save_schedule,
            font=('Arial', 11),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=5
        )
        save_schedule_btn.pack(pady=20)
        
    def save_schedule(self):
        """Сохранение расписания"""
        try:
            on_time = f"{self.on_hour.get()}:{self.on_minute.get()}"
            off_time = f"{self.off_hour.get()}:{self.off_minute.get()}"
            self.log_event(f"Расписание сохранено: включение {on_time}, выключение {off_time}")
            messagebox.showinfo("Сохранено", f"Расписание сохранено!\nВключение: {on_time}\nВыключение: {off_time}")
        except:
            messagebox.showerror("Ошибка", "Проверьте введенное время")
            
    def save_settings(self):
        """Сохранение настроек"""
        settings = {
            'brightness': self.brightness,
            'is_on': self.is_on,
            'simulation_mode': self.simulation_mode,
            'port': self.port_var.get()
        }
        
        try:
            with open('dimmer_settings.json', 'w') as f:
                json.dump(settings, f)
            self.log_event("Настройки сохранены")
            messagebox.showinfo("Сохранено", "Настройки успешно сохранены")
        except Exception as e:
            self.log_event(f"Ошибка сохранения: {str(e)}")
            
    def load_settings(self):
        """Загрузка настроек"""
        try:
            if os.path.exists('dimmer_settings.json'):
                with open('dimmer_settings.json', 'r') as f:
                    settings = json.load(f)
                    
                self.brightness = settings.get('brightness', 50)
                self.is_on = settings.get('is_on', False)
                self.brightness_slider.set(self.brightness)
                self.brightness_label.config(text=f"{self.brightness}%")
                
                if self.is_on:
                    self.power_btn.config(text="ВЫКЛЮЧИТЬ", bg=self.colors['on'])
                    self.update_light_visualization()
                    
                self.log_event("Настройки загружены")
        except Exception as e:
            self.log_event(f"Ошибка загрузки настроек: {str(e)}")
            
    def log_event(self, message):
        """Логирование событий"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = LightDimmerController(root)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
