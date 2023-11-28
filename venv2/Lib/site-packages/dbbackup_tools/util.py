"""
* Download and create a dbbackup folder for dbbackup
* from GitHub: 
* https://github.com/EmmanuelDiscors/dbbackup-skeleton/archive/master.zip
*
* Usage:
* python
* import dbbackup_tools.util
*
"""

# import some python modules for util
import os
import shutil
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

# TODO: implement logger

def create_dbbackup_folder(name):
    """
        Create a Skeleton folder for dbbackup (needs internet connection to github)
    """
    dbbackup_repo_url = ("https://github.com/EmmanuelDiscors/dbbackup-skeleton/archive/master.zip")
    dirname = "dbbackup-skeleton-master"

    try:
        url = urlopen(dbbackup_repo_url)
        zipfile = ZipFile(BytesIO(url.read()))
    except Exception as e:
        print ("Exception occurred: check your connection to GitHub")
        #logger.critical("Exception occurred", exc_info=True)

    zipfile.extractall()
    
    try:
        os.rename(dirname, name)
        print(f"skeleton folder instaled in: {name}")
    except OSError:
        print ("WARNING: dbbackup folder already exist")
        #logger.warning("dbbackup folder already exist")
        shutil.rmtree(dirname)
        #print ("skeleton folder deleted")
        #logger.info("skeleton folder deleted")
    
name = input("dbbackup folder to create: ")
create_dbbackup_folder(name)
