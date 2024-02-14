import tkinter as tk
from tkinter import ttk
from Keypad import Keypad


class CalculatorUI:

    def __init__(self, keynames=[], columns=1):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.keynames = keynames
        self.resize = (0, 0)
        self.init_component(columns)

    def init_component(self, columns) -> None:
        self.keypad = Keypad(self.root)

    def bind(self):
        pass

    def configure(self, cnf=None, **kwargs):
        pass

    def frame(self):
        return self.frame

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def run(self):
        self.root.mainloop()

