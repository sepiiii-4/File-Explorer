from ttkbootstrap import Toplevel, Label, Entry, Button, Messagebox
from BusinessLogicLayer.file_business import File, Folder


class ZipForm :
    def __init__(self, path_tuple):
        self.path_tuple = path_tuple
        self.file = File()
        self.folder = Folder()
        self.toplevel = Toplevel("ZipForm")

        self.address_label = Label(self.toplevel, text="From :")
        self.address_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.address_entry = Entry(self.toplevel)
        self.address_entry.insert(0, self.get_address())
        self.address_entry.config(state= "readonly")
        self.address_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="w")

        self.browse_button = Button(self.toplevel, text="Browse", bootstyle="info")
        self.browse_button.grid(row=1, column=2, padx=(0,10), pady=10, sticky="w")

        self.destination_label = Label(self.toplevel, text="To :")
        self.destination_label.grid(row=1, column=0, padx=10, sticky="w")

        self.destination_entry = Entry(self.toplevel)
        self.destination_entry.grid(row=1, column=1, padx=(0,10), sticky="w")

        self.submit_button = Button(self.toplevel,text = "Submit", bootstyle="success", command= self.submit)
        self.submit_button.grid(row=2, column=2, padx=(0,10), pady=10, sticky="w")

    def submit(self) :
        destination = self.destination_entry.get()

        if self.path_tuple[1] == "Folder" :
            response = self.folder.zip(self.path_tuple[0], destination)

            if response.success :
                message = Messagebox.show_info(response.message, "Info")
            else :
                message = Messagebox.show_error(response.message, "Error")
        else :
            response = self.file.zip(self.path_tuple[0], destination)

            if response.success :
                message = Messagebox.show_info(response.message, "Info")
            else :
                message = Messagebox.show_error(response.message, "Error")


    def show(self) :
        self.toplevel.mainloop()

    def get_address(self) :
       location, name = self.file.relative_path(self.path_tuple[0])
       return location
