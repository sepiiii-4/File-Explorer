from ttkbootstrap import Toplevel, Label, Entry, Button, Messagebox
from BusinessLogicLayer.file_business import Folder


class FolderForm :
    def __init__(app):
        app.folder = Folder()

        app.toplevel = Toplevel("Make")

        app.destination_label = Label(app.toplevel, text="To :")
        app.destination_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        app.destination_entry = Entry(app.toplevel)
        app.destination_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="w")

        app.name_label = Label(app.toplevel, text="Name :")
        app.name_label.grid(row=1, column=0, padx=10, sticky="w")

        app.name_entry = Entry(app.toplevel)
        app.name_entry.grid(row=1, column=1, padx=(0,10), sticky="w")

        app.submit_button = Button(app.toplevel,text = "Submit", bootstyle= "success", command= app.submit)
        app.submit_button.grid(row=2, column=2, padx=(0,10), pady=10, sticky="w")

    def submit(self) :
        path = self.destination_entry.get()
        name = self.name_entry.get()

        response = self.folder.create(path, name)

        if response.success :
            message = Messagebox.show_info(response.message, "Info")
            self.toplevel.destroy()
        else :
            message = Messagebox.show_error(response.message, "Error")

    def show(app) :
        app.toplevel.mainloop()

    
        