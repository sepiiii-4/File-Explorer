from ttkbootstrap import Toplevel, Label, Entry, Button, Messagebox
from BusinessLogicLayer.file_business import Folder, File


class CopyForm :
    def __init__(self, path_tuple):
        self.folder = Folder()
        self.file = File()
        self.path_tuple = path_tuple

        self.toplevel = Toplevel("Copy")

        self.address_label = Label(self.toplevel, text="From :")
        self.address_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.address_entry = Entry(self.toplevel)
        self.address_entry.insert(0, self.get_address())
        self.address_entry.config(state="readonly")
        self.address_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="w")

        self.destination_label = Label(self.toplevel, text="To :")
        self.destination_label.grid(row=1, column=0, padx=10, sticky="w")

        self.destination_entry = Entry(self.toplevel)
        self.destination_entry.grid(row=1, column=1, padx=(0,10), sticky="w")

        self.submit_button = Button(self.toplevel,text = "Submit", bootstyle="success", command= self.submit)
        self.submit_button.grid(row=2, column=2, padx=(0,10), pady=10, sticky="w")

    
    def submit(self) :
        new_path = self.destination_entry.get()

        for item in self.path_tuple :
            if item[1] == "Folder" :
                self.folder.copy(item[0], new_path)           
            else :
                self.file.copy(item[0], new_path)            
            
        message = Messagebox.show_info("Copied successfully", "info")

        self.toplevel.destroy()


    def show(self) :
        self.toplevel.mainloop()

    def get_address(self) :
        location, name = self.folder.relative_path(self.path_tuple[0][0])
        return location
