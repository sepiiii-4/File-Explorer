from ttkbootstrap import Window, Entry, Button, Treeview, Combobox, Style
from ttkbootstrap.dialogs import Messagebox
from DataAccessLayer.theme_data import themes
from BusinessLogicLayer.file_business import show_table, File, Folder
from PresentationLayer import make_file, make_folder, copy, move, rename, file_properties, folder_properties


class Home :
    def __init__(self):
        self.show_table =show_table
        self.file = File()
        self.folder = Folder()
        self.item_list = []

        self.window = Window("File Explorer", iconphoto=r"Image\image.png", themename="pydata-dark")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(4, weight=1)

        self.theme_combobox = Combobox(self.window, values=themes, state="readonly")
        self.theme_combobox.set("pydata-dark")
        self.theme_combobox.grid(row=0, column=2, padx=(0,20), pady=10, sticky ="e")
        self.change_theme()

        self.add_folder_button = Button(self.window, text= "Add Folder", bootstyle="primary", command= self.make_folder)
        self.add_folder_button.grid(row=0, column=0, padx=20, pady=10, sticky ="w")

        self.rename_button = Button(self.window, text= "Rename", bootstyle="secondary", command= self.rename)
        self.rename_button.config(state="disabled")
        self.rename_button.grid(row=0, column=1, pady=10, sticky ="w")

        self.move_button = Button(self.window, text= "Move", bootstyle="secondary", command= self.move)
        self.move_button.config(state="disabled")
        self.move_button.grid(row=0, column=2, padx=(10,0), pady=10, sticky ="w")
        
        self.add_file_button = Button(self.window, text= "Add File", bootstyle="primary", command= self.make_file)
        self.add_file_button.grid(row=1, column=0, padx=20 , sticky ="w")

        self.copy_button = Button(self.window, text= "Copy", bootstyle="secondary", command= self.copy)
        self.copy_button.config(state="disabled")
        self.copy_button.grid(row=1, column=1, sticky ="w")

        self.delete_button = Button(self.window, text= "Delete", bootstyle="secondary", command= self.remove)
        self.delete_button.config(state="disabled")
        self.delete_button.grid(row=2, column=1, pady=10, sticky ="w")

        self.properties_button = Button(self.window, text= "Properties", bootstyle="primary", command= self.properties)
        self.properties_button.config(state="disabled")
        self.properties_button.grid(row=2, column=0, padx=20, pady=10, sticky ="w")

        self.search_entry = Entry(self.window, width= 50)
        self.search_entry.grid(row=3, column=0, columnspan=2, padx=(20,10), pady=10, sticky ="ew")

        self.search_button = Button(self.window, text= "Search", bootstyle="info", command= self.load_table)
        self.search_button.grid(row=3, column=2, sticky ="w")

        self.table = Treeview(self.window, columns=("Name", "Date Modified", "Type", "Size"))
        self.table.grid(row=4, column=0, columnspan=3, padx=20, pady= (0,20), sticky ="nsew")
        self.style = Style()
        self.style.configure("Treeview", rowheight=25)


        self.table.heading("#0", text="No")
        self.table.heading("#1", text="Name")
        self.table.heading("#2", text="Date Modified")
        self.table.heading("#3", text="Type")
        self.table.heading("#4", text="Size")

        self.table.column("#0", width= 50, anchor="w")
        self.table.column("#1", width= 250, anchor="w")
        self.table.column("#2", width= 200, anchor="w")
        self.table.column("#3", width= 150, anchor="w")
        self.table.column("#4", width= 120, anchor="w")

        self.table.bind("<<TreeviewSelect>>", self.manage_busttons)

        

        self.window.mainloop()
    
    def change_theme(self) :
        self.theme_combobox.bind("<<ComboboxSelected>>", lambda event : self.window.theme_use(self.theme_combobox.get()))

    def make_file(self) :
        window = make_file.FileForm()
        window.show()
        
    
    def make_folder(self) :
        windoow = make_folder.FolderForm()
        windoow.show()

    def copy(self) :
        selection_list = []
        selections = self.table.selection()
        
        for selection in selections :
            value = self.table.item(selection, "value")
            selection_list.append((selection, value[2]))

        window = copy.CopyForm(selection_list)
        window.show()

    def move(self) :
        selection = self.table.selection()
        window = move.MoveForm(selection)
        window.show()

    def rename(self) :
        selection = self.table.selection()[0]
        window = rename.RenameForm(selection)
        window.show()

        self.load_table()

    def remove(self):
        message = Messagebox.yesno("Are you sure to want to delete ?", "Warning")
        if message == "Yes" :
            selection_list = []
            selections = self.table.selection()

            for selection in selections :
                value = self.table.item(selection, "value")
                selection_list.append((selection, value[3]))

            for item in selection_list :
                if item[1] == "Folder" :
                    self.folder.remove(item[0])
                else :
                    self.file.remove(item[0])
        self.load_table()
    
    def load_table(self) :
        for item in self.item_list :
            self.table.delete(item)
        self.item_list.clear()

        serach = self.search_entry.get()

        row_number = 1
        for data in self.show_table(serach) :
            item = self.table.insert("", "end", iid= data[1], text=str(row_number), values=[item for item in data[0]])
            
            self.item_list.append(item)
            row_number+=1

    def properties(self) :
        selection = self.table.selection()[0]
        value = self.table.item(selection, "values")

        if value[2] == "File" :
            self.file_properties = file_properties.FileProperties(selection)
            self.file_properties.show()
        else :
            self.folder_properties = folder_properties.FolderProperties(selection)
            self.folder_properties.show()

    def manage_busttons(self, event) :
        selection = self.table.selection()

        count = len(selection)

        if count == 1 :
            self.properties_button.config(state= "normal")
            self.rename_button.config(state= "normal")
            self.move_button.config(state= "normal")
            self.copy_button.config(state= "normal")
            self.delete_button.config(state= "normal")
        elif count > 1 :
            self.properties_button.config(state= "disabled")
            self.rename_button.config(state= "disabled")
        else :
            self.properties_button.config(state= "disabled")
            self.rename_button.config(state= "disabled")
            self.move_button.config(state= "disabled")
            self.copy_button.config(state= "disabled")
            self.delete_button.config(state= "disabled")

    