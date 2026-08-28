import os
import shutil
import psutil
from abc import ABC, abstractmethod
from datetime import datetime
import zipfile
from Common.response import Response


class CommonThings(ABC) :

    def __init__(self):
        self.suffix_list = (
        ".txt",".csv",".html",".htm",".css",".js",
        ".json",".xml",".md",".py",".java",".c",
        ".cpp",".h",".hpp",".cs",".php",".sql",
        ".bat",".cmd",".ps1",".ini",".log",
        ".config",".yaml",".yml")

    def validate_path (self, path) :
        if not os.path.exists(path) :
            return True   

    def relative_path(self, path) :
        location, name = os.path.split(path)

        return location, name

    def join_path(self, name, location) :
        path = os.path.join(location, name)
        return path
        

    @abstractmethod
    def create(self, path, name):
        new_path = self.join_path(name, path)
        exist_path = self.validate_path(new_path)
        
        return new_path, exist_path

    @abstractmethod
    def remove(self, paths) :
        pass

    def rename(self, path : str, new_name) :
        location, name = self.relative_path(path)
        new_path = self.join_path(new_name, location)

        exist_path = self.validate_path(new_path)

        if (path.endswith(self.suffix_list) and new_path.endswith(self.suffix_list)) or (not ((path.endswith(self.suffix_list)) and not (new_path.endswith(self.suffix_list)))) :
            if exist_path :
                os.rename(path, new_path)
                return Response(None, "Renamed successfully .", True)

            return Response(None, "This name has chosen before .", False)
        
        return Response(None, "Please choose a name correctly .", False)

    def move(self, paths, new_path) :
        list1 = []
        for past_path in paths :
            location, name = self.relative_path(past_path)
            new_path = self.join_path(name, new_path)

            info = {"new_path" : new_path,
                    "past_path" : past_path }
            
            list1.append(info)

        for info in list1 :
            shutil.move(info["past_path"], info["new_path"])
            
        return Response(None, "Moved successfully", True)
            

    @abstractmethod
    def copy(self, paths, new_path) :
        list1 = []
        for past_path in paths :
            location, name = self.relative_path(past_path)
            new_path = self.join_path(name, new_path)
            exist_path = self.validate_path(new_path)

            info = {"new_path" : new_path,
                    "past_path" : past_path,
                    "exist_path" : exist_path }
            
            list1.append(info)
        
        return list1

    def properties(self, path) :
        stat = os.stat(path)

        location, name = self.relative_path(path)
        size = f"{round( stat.st_size / 1024, 2)} KB"

        creation_date = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d  %H:%M:%S")
        modified_date = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d  %H:%M:%S")
        access_date = datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d  %H:%M:%S")

        return location, size, creation_date, modified_date, access_date


class Folder(CommonThings) :
    def __init__(self):
        super().__init__()
    
    def create(self, path, name):
        new_path, exist_path = super().create(path, name)

        if exist_path :
            os.mkdir(new_path)
            return Response(None, "The folder created successfully .", True)
        
        return Response(None, "This folder has already created .", False)       
        
    def remove(self, path) :
        shutil.rmtree(path)

        return Response(None, "Folder deleted successfully .", True)
    
    
    def copy(self, past_path, new_path):
        info_list = super().copy(past_path, new_path)
        
        for info in info_list :
            if info["exist_path"]:
                shutil.copytree(past_path, new_path)
            else :
                new_path = f"{new_path} - Copy"
                shutil.copytree(info["past_path"], info["new_path"])               


class File(CommonThings) :
    def __init__(self):
        super().__init__()
        

    
    def create(self, path, name : str):
        new_path, exist_path = super().create(path, name)
    
        if not name.endswith(self.suffix_list) :
            return Response(None, "Please write file name correctly .", False)
        
        if exist_path :
            new_file = open(new_path, mode="w")
            new_file.close()

            return Response(None, "The file created successfully .", True)
        
        return Response(None, "This file has already created .", False)
    
        
    def remove(self, path) :
        os.remove(path)

        return Response(None, "Folder deleted successfully .", True)

    def copy(self, past_path, new_path):
        info_list = super().copy(past_path, new_path)
        
        for info in info_list :
            if info["exist_path"]:
                shutil.copy2(past_path, new_path)
            else :
                new_path = f"{new_path} - Copy"
                shutil.copy2(info["past_path"], info["new_path"])

        

def show_table(path) :
    entries = sorted(os.scandir(path), key= lambda entry : (entry.is_file(), entry.name.lower()))
    
    for entry in entries :
        entry_info = entry.stat()
        size = f"{round(entry_info.st_size / 1024,2)} KB"
        entry_type = "Folder" if entry.is_dir() else "File"
        
        modified_date = datetime.fromtimestamp(entry_info.st_mtime).strftime("%Y-%m-%d  %H:%M:%S")

        if entry_type == "File" :
            yield ([entry.name, modified_date, entry_type, size], entry.path)
        else :
            yield ([entry.name, modified_date, entry_type, ""], entry.path)




                
                
            

        