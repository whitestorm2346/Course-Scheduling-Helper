from tkinter import *
from tkinter import ttk
import threading


class MainUI:
    def __init__(self) -> None:
        self.threads: List[threading, ...] = []
        self.root = Tk()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    win = MainUI()
    win.run()
