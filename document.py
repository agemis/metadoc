
import os
import json
import os.path
from datetime import date, datetime
import unicodedata

import config as cfg





# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


# Un fichier, son fichier de métadonnées associé, et les métadonnées
class Document:
    def __init__(self):
        self.reset()
        
    # To overload str
    def __str__(self):
        r = "document '" + str(self.filepath) + "'"
        return r 

    # Reset
    def reset(self):
        self.filetype = None
        self.fileexists = None        
        self.metadatafileexists = None
        self.filepath = None        
        self.metadatafilepath = None
        self.metadata = None
    
    # Supprime tous les caractères spéciaux
    @staticmethod
    def normalize_string(s):
        s1 = s

        # Je ne retiens que les caractères ascii, b1 est un tableau de bytes
        b1 = unicodedata.normalize('NFD', s1).encode('ascii', 'ignore')
        s1 = b1.decode()

        s1 = s1.strip()
        s1 = s1.lower()
        s1 = s1.replace(' ', '_')
        s1 = s1.replace('*', '_')
        s1 = s1.replace('.', '_')
        s1 = s1.replace('\'', '_')
        s1 = s1.replace('/', '_')
        s1 = s1.replace('\\', '_')
        s1 = s1.replace('[', '_')
        s1 = s1.replace(']', '_')
        s1 = s1.replace(':', '_')
        s1 = s1.replace(';', '_')
        s1 = s1.replace('|', '_')
        s1 = s1.replace('=', '_')
        s1 = s1.replace('-', '_')
        s1 = s1.replace(',', '_')
        s1 = s1.replace('<', '_')
        s1 = s1.replace('>', '_')
        s1 = s1.replace('<', '_')
        s1 = s1.replace(')', '_')

        # Remplacement de __ par _
        for _ in range(10): # brute force
            s1 = s1.replace('__', '_')

        return s1


    # From a dictionnary, using a template, make a JSON doc string
    @staticmethod
    def metadatadictionnary_to_str(filepath, metadatadictionnary = {}):
        # To be replaced in template
        values = metadatadictionnary
        #values["[id]"] = str(uuid.uuid4()) # id -> valeur auto
        
        # Use default for not defined keys
        if not "[meta_modification_date]" in values.keys(): 
            values["[meta_modification_date]"] = datetime.today().strftime('%Y-%m-%d') # creation_date -> valeur auto
        
        # Read template
        f = open(os.path.join(cfg.main["datadir"], ".metadoc.json.template"), "r")
        templatetext = f.read()
        f.close()
        
        # Replace values in template
        text = templatetext
        for key, val in values.items():
            text = text.replace(key, val)
        
        return text


    # Crée un fichier de métadata pour le document de filepath indiqué
    @staticmethod    
    def create_metadatafile(filepath, metadatadictionnary = {}):
        s = Document.metadatadictionnary_to_str(filepath, metadatadictionnary)
        
        # crée le fichier  
        if os.path.isdir(filepath):
            f = open(os.path.join(filepath, ".metadoc.json"), "w")
            f.write(s)
            f.close()
        else:
            if os.path.isfile(filepath):
                f = open(filepath + ".metadoc.json", "w")
                f.write(s)
                f.close()



    # create a new directory document
    @staticmethod
    def create_metadatafile_and_directory_interactive():
        # ask for title
        # toto intelissense
        title = input("title:")  
        # toto intelisense
        category = input("category:")          
        
        doc_production_date = input("production_date:")          
        doc_modification_date = doc_production_date
        
        
        
        
        directory = Document.normalize_string(title)        
        # TODO: use config "directory scheme"
        now = datetime.now()
        filepath = os.path.join(cfg.main["datadir"], now.strftime("%Y"), now.strftime("%m"), now.strftime("%Y%m%d") + "_" + directory) 
        os.makedirs(filepath, exist_ok = True)


        d = {}
        d["[title]"] = title
        d["[category]"] = category
        d["[doc_production_date]"] = doc_production_date
        d["[doc_modification_date]"] = doc_modification_date
        Document.create_metadatafile(filepath, d)





    # def check(self):
       # self.fileexists
       # self.metadatafileexists
       # self.metadatadatabaseexists

        

    # Lit un fichier de metadonnées
    def read_metadatafile(self, metadatafilepath):
        self.reset()
        if os.path.isfile(metadatafilepath):
            self.metadatafileexists = True
            self.metadatafilepath = metadatafilepath            
            metadatafilepathparts = metadatafilepath.split(os.path.sep)
            
            if metadatafilepath.endswith(os.path.sep + ".metadoc.json"):
                if os.path.isdir(os.path.sep.join(metadatafilepathparts[:-1])):
                    self.filetype = "directory"
                    self.fileexists = True
                    self.filepath = os.path.sep.join(metadatafilepathparts[:-1])
            else:
                if os.path.isfile(metadatafilepath[:-13]):
                    self.filetype = "file"   
                    self.fileexists = True
                    self.filepath = metadatafilepath[:-13] 
                
            with open(self.metadatafilepath, "r") as jsonfile:
                jsonstr = jsonfile.read()
                self.metadata = json.loads(jsonstr)
    

    # Lit un "fichier" de métadonnées, en base
    # def read_database(self, metadatafilepath):

    # ecrit le fichier + database
    # def write(self):  


