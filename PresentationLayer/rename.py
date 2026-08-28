from ttkbootstrap import Toplevel, Label, Entry, Button, Messagebox
from BusinessLogicLayer.file_business import File


class RenameForm :
    def __init__(self, path):
        self.past_path = path
        self.file = File()
        self.toplevel = Toplevel("Rename")

        self.pastname_label = Label(self.toplevel, text="Name :")
        self.pastname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.pastname_entry = Entry(self.toplevel)
        self.pastname_entry.insert(0, self.get_name())
        self.pastname_entry.config(state="readonly")
        self.pastname_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="w")

        self.newname_label = Label(self.toplevel, text="New name :")
        self.newname_label.grid(row=1, column=0, padx=10, sticky="w")

        self.newname_entry = Entry(self.toplevel)
        self.newname_entry.grid(row=1, column=1, padx=(0,10), sticky="w")

        self.submit_button = Button(self.toplevel,text = "Submit", bootstyle= "success", command= self.submit)
        self.submit_button.grid(row=2, column=2, padx=(0,10), pady=10, sticky="w")

    def submit(self) :
        new_name = self.newname_entry.get()
        response = self.file.rename(self.past_path, new_name)

        if response.success :
            message = Messagebox.show_info(response.message, "Info")
            self.toplevel.destroy()
        else :
            message = Messagebox.show_error(response.message, "Error")


    def show(self) :
        self.toplevel.mainloop()

    def get_name(self) :
        location, name = self.file.relative_path(self.past_path)

        return name