import os

import config as cfg
from document import Document
from databaselibrary import DatabaseLibrary

class FileLibrary:
    # # Print all directories and files, recursively, for testing
    # def walk_tree(self, r):
    #     for dirpath, _, files in os.walk(r):	# I do not use dirnames here (files contain also directories). I use _ to ask editor to not complain about an unused variable
    #         print("dirpath = ", dirpath)
    #         pathparts = dirpath.split(os.path.sep)
    #         level = len(pathparts) - r.count(os.path.sep)
    #         print('|', level * '-', '[',os.path.basename(dirpath),']')
    #         for f in files:
    #             print('|', level * '-', f)
    
    @staticmethod
    def walk(rootpath, callback):
        for dirpath, _, files in os.walk(rootpath):	 # I do not use dirnames here (files contain also directories). I use _ to ask editor to not complain about an unused variable
            pathparts = dirpath.split(os.path.sep)
            level = len(pathparts) - rootpath.count(os.path.sep)
            callback(level, "directory", dirpath)        
            for f in files:
                callback(level, "file", os.path.join(rootpath, dirpath, f))
            

    # callback pour walk: Liste tous les fichiers
    @staticmethod
    def walk_callback_print_filename(level, filetype, filepath):
        print(str(level), filetype, filepath)


    # callback pour walk: Liste les fichiers de métadonnées
    @staticmethod
    def walk_callback_print_metadatafilepath(level, filetype, filepath):
        if filepath.endswith(".metadoc.json"):
            print(str(level), filetype, filepath)    
    
    # callback pour walk: Liste les fichiers de métadonnées et leur contenu
    @staticmethod
    def walk_callback_print_metadata(level, filetype, filepath):
        if filepath.endswith(".metadoc.json"):
            print(str(level), filetype, filepath)        
            doc = Document()
            doc.read_metadatafile(filepath) 
            for key, value in doc.metadata.items():
                print('|', (level + 1) * '-', key, ":", value)
        
    # callback pour walk: Ajoute tous les doc json a la collection, sans se soucier de leur existence préalable
    @staticmethod
    def walk_callback_mongo_add_json(level, filetype, filepath):
        if filepath.endswith(".metadoc.json"):
            doc = Document()
            doc.read_metadatafile(filepath) 
            new_id = DatabaseLibrary.collection.insert_one(doc.metadata).inserted_id

    



    # export metadata files (to a archive file)
    def export_metadata(self):    
        print("todo")




