import os


from document import Document

from filelibrary import FileLibrary
from databaselibrary import DatabaseLibrary
import config as cfg




# Use cmd to write this CLI 
# https://docs.python.org/3/library/cmd.html

# Regarder ceci !
# https://linuxhint.com/search_json_python/





def main():    
    #print(Document.default_metadata())
    FileLibrary.walk(cfg.main["datadir"], FileLibrary.walk_callback_print_metadata)
    Document.create_metadatafile_and_directory_interactive()

if __name__ == "__main__":
    main()
    os.system("pause")        
    

