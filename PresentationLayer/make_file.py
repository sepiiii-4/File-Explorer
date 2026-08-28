from ttkbootstrap import Toplevel, Label, Entry, Button, Messagebox
from BusinessLogicLayer.file_business import File


class FileForm :
    def __init__(self):
        self.file = File()

        self.toplevel = Toplevel("Make")

        self.destination_label = Label(self.toplevel, text="To :")
        self.destination_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.destination_entry = Entry(self.toplevel)
        self.destination_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="w")

        self.name_label = Label(self.toplevel, text="Name :")
        self.name_label.grid(row=1, column=0, padx=10, sticky="w")

        self.name_entry = Entry(self.toplevel)
        self.name_entry.grid(row=1, column=1, padx=(0,10), sticky="w")

        self.submit_button = Button(self.toplevel,text = "Submit", bootstyle= "success", command= self.submit)
        self.submit_button.grid(row=2, column=2, padx=(0,10), pady=10, sticky="w")

    def submit(self) :
        path = self.destination_entry.get()
        name = self.name_entry.get()

        response = self.file.create(path, name)

        if response.success :
            message = Messagebox.show_info(response.message, "Info")
            self.toplevel.destroy()
        else :
            message = Messagebox.show_error(response.message, "Error")

        

    def show(self) :
        self.toplevel.mainloop()

    
        