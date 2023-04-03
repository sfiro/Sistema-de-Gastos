import tkinter as tk

class SharedData:
    def __init__(self):
        self.data = None

class Window1:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        
        self.window = tk.Tk()
        
        self.entry = tk.Entry(self.window)
        self.entry.pack()
        
        self.button = tk.Button(self.window, text="Enviar", command=self.send_data)
        self.button.pack()
        
        self.window.mainloop()
        
    def send_data(self):
        self.shared_data.data = self.entry.get()

class Window2:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        
        self.window = tk.Tk()
        
        self.label = tk.Label(self.window, text="")
        self.label.pack()
        
        self.button = tk.Button(self.window, text="Mostrar", command=self.show_data)
        self.button.pack()
        
        self.window.mainloop()
        
    def show_data(self):
        self.label.configure(text=self.shared_data.data)

shared_data = SharedData()
window1 = Window1(shared_data)
window2 = Window2(shared_data)