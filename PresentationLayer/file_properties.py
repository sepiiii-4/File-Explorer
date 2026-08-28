from ttkbootstrap import Toplevel, Label, Entry, Button
from BusinessLogicLayer.file_business import File

class FileProperties :
    def __init__(self, path):
        self.path = path
        self.file = File()
        _location, _size, _create, _modify, _access = self.file.properties(self.path)
        self.window = Toplevel("Properties")

        self.window.grid_columnconfigure(0, weight= 1)
        self.window.grid_columnconfigure(1, weight= 1)

        self.path_label = Label(self.window, text= f"Location :     {_location}")
        self.path_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.size_label = Label(self.window, text= f"Size :     {_size}")
        self.size_label.grid(row=1, column=0, padx=10, sticky="w")

        self.created_label = Label(self.window, text= f"Created :     {_create}")
        self.created_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.modified_label = Label(self.window, text= f"Modified :     {_modify}")
        self.modified_label.grid(row=3, column=0, padx=10, sticky="w")

        self.processed_label = Label(self.window, text= f"Processed :     {_access}")
        self.processed_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    def show(self) :
        self.window.mainloop()