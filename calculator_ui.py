import tkinter as tk
from tkinter import ttk
import math
import pygame

class CalculatorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.entry = ttk.Entry(self.root, font=('Arial', 20))
        self.entry.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.init_component()
        self.history = []
        self.history_window = None
        self.root.mainloop()

    def init_component(self):
        number_frame = ttk.Frame(self.root)
        number_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        operator_frame = ttk.Frame(self.root)
        operator_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        number_buttons = [
            ('7',), ('8',), ('9',),
            ('4',), ('5',), ('6',),
            ('1',), ('2',), ('3',),
            ('🎵',), ('0',), ('.',),
        ]
        operator_buttons = [
            ('/',), ('*',), ('-',), ('+'),
            ('(',), (')',), ('DEL',), ('CLR',), ('sqrt',), ('log',), ('=',), ('HISTORY',)
        ]
        for i, btn_info in enumerate(number_buttons):
            row, col = divmod(i, 3)
            button = ttk.Button(number_frame, text=btn_info[0], width=5, style='Blue.TButton')
            button.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            button.bind('<Button-1>', lambda event, key=btn_info[0]: self.button_click(key))
            number_frame.grid_columnconfigure(col, weight=1)
            number_frame.grid_rowconfigure(row, weight=1)
        for i, btn_info in enumerate(operator_buttons):
            row, col = divmod(i, 2)
            button_style = 'TButton'
            button_styles = {
                '=': 'Lime.TButton',
                'HISTORY': 'Yellow.TButton'
            }
            button_style = button_styles.get(btn_info[0], 'Brown.TButton')
            button = ttk.Button(operator_frame, text=btn_info[0], width=5, style=button_style)
            button.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            button.bind('<Button-1>', lambda event, key=btn_info[0]: self.button_click(key))
            operator_frame.grid_columnconfigure(col, weight=1)
            operator_frame.grid_rowconfigure(row, weight=1)

        style = ttk.Style()
        style.configure("TButton", font=('Arial', 14))

        style.map('Lime.TButton',
                  background=[('active', 'lime green')],
                  foreground=[('active', 'black')],
                  )
        style.configure('Lime.TButton', background='lime green', foreground='Green')

        style.map('Yellow.TButton',
                  background=[('active', 'yellow')],
                  foreground=[('active', 'black')],
                  )
        style.configure('Yellow.TButton', background='yellow', foreground='Orange')

        style.map('Blue.TButton',
                  background=[('active', 'blue')],
                  foreground=[('active', 'black')],
                  )
        style.configure('Blue.TButton', background='blue', foreground='Purple')

        style.map('Brown.TButton',
                  background=[('active', 'brown')],
                  foreground=[('active', 'black')],
                  )
        style.configure('Brown.TButton', background='brown')

    def button_click(self, key):
        expression = self.get_expression()
        operators = {'+', '-', '*', '/'}

        actions = {
            '+': lambda: self.insert_operator(key, expression, operators),
            '*': lambda: self.insert_operator(key, expression, operators),
            '/': lambda: self.insert_operator(key, expression, operators),
            'sqrt': lambda: self.insert_sqrt(expression, operators),
            'log': self.add_log,
            '=': self.evaluate_expression,
            'CLR': self.clear_display,
            'DEL': self.delete_last_char,
            '(': lambda: self.insert_character('('),
            ')': lambda: self.insert_character(')'),
            'HISTORY': self.show_history,
            '🎵': self.play_music
        }

        action = actions.get(key, lambda: self.insert_character(key))
        action()

    def insert_operator(self, key, expression, operators):
        if not expression or expression[-1] in operators:
            return
        self.insert_character(key)

    def insert_sqrt(self, expression, operators):
        if expression and expression[-1] not in operators:
            self.insert_character('*')
        self.insert_character('sqrt(')

    def add_log(self):
        expression = self.get_expression()
        if expression.strip():
            self.clear_display()
            self.insert_character("log(")
            self.entry.insert(tk.END, expression)
            self.insert_character(")")

    def evaluate_expression(self):
        expression = self.get_expression()
        try:
            result = None
            if "log" in expression:
                log_index = expression.index("log(")
                base_start = log_index + 4
                comma_index = expression.find(",", base_start)
                base_end = comma_index if comma_index != -1 else expression.index(")", base_start)
                base_str = expression[base_start:base_end].strip()
                base = float(base_str) if base_str else math.e

                if comma_index != -1:
                    value_start = comma_index + 1
                    value_end = expression.index(")", value_start)
                    value_str = expression[value_start:value_end].strip()
                    value = float(value_str)
                else:
                    value = None
                result = math.log(value, base) if value is not None else math.log(base)
            else:
                result = eval(expression)
            self.history.append(f"{expression} = {result}")
            if result is not None:
                self.entry.config(foreground="black")
                self.clear_display()
                self.entry.insert(tk.END, str(result))
        except Exception as e:
            self.clear_display()
            self.entry.config(foreground="red")
            self.entry.insert(tk.END, "Error alert")
            self.root.after(3000, lambda: self.entry.delete(0, tk.END))
            self.root.after(3000, lambda: self.entry.config(foreground="black"))
            pygame.init()
            pygame.mixer.music.load("C:\\Users\\Picha Wiwattanawongs\\Downloads\\ara-ara-sound-effect-127279.mp3")
            pygame.mixer.music.play()
            return

    def play_music(self):
        if not hasattr(self, 'music_playing') or not self.music_playing:
            pygame.init()
            pygame.mixer.music.load("C:\\Users\\Picha Wiwattanawongs\\Downloads\\toothless-dancing_rT0J7Pn.mp3")
            pygame.mixer.music.play()
            self.music_playing = True
        else:
            pygame.mixer.music.stop()
            self.music_playing = False

    def show_history(self):
        if not self.history_window:
            self.history_window = tk.Toplevel(self.root)
            self.history_window.title("History")
            history_text = '\n'.join(self.history)
            history_label = ttk.Label(self.history_window, text=history_text, font=('Arial', 14))
            history_label.pack()
            self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)

    def close_history_window(self):
        self.history_window.destroy()
        self.history_window = None

    def clear_display(self):
        self.entry.delete(0, tk.END)

    def delete_last_char(self):
        expression = self.get_expression()
        self.clear_display()
        self.entry.insert(tk.END, expression[:-1])

    def insert_character(self, char):
        self.entry.insert(tk.END, char)

    def get_expression(self):
        return self.entry.get()

    def run(self):
        self.root.mainloop()
