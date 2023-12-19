import os
import zipfile
import re

# Find file from the provided Filename and extension
def find_file_get_path(filename,extension,sourcepath):
    cwd1=os.getcwd()
    
    os.chdir(sourcepath)
    
    # Finding the directory of a specific file
    file_path = filename
    # Get the directory of the file
    file_dir = os.path.dirname(os.path.abspath(file_path)) 
    
    for root, dirs, files in os.walk(file_dir):
        
        for file in files:
            if file.endswith(extension):
                file_dir=os.path.join(root)
    print("File directory:", file_dir)  
    #os.chdir(cwd1)  
    print("current cwd:"+os.getcwd())  
    os.chdir(cwd1)      
    return file_dir
    
# Unzip the Artifacts from the .zip file
def unzip_artifacts(path):
    print("Unziping Customer_artifacts")
    cwd1 = os.getcwd()
    # Change the current working directory
    os.chdir(f'{path}')
     # Get the current working directory
    cwd2 = os.getcwd()
    # Print the current working directory
    print("Current working directory: {0}".format(cwd2))
    for item in os.listdir(cwd2): # loop through items in dir
        if item.endswith('.zip'): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(cwd2) # extract file to dir
            zip_ref.close() # close file
    os.chdir(f'{cwd1}')

def search_directory(directory,subdirname):
    for root, dirs, files in os.walk(directory):
        if subdirname in dirs:
            screenshots_path = os.path.join(root, 'Screenshots')
            return screenshots_path

    return None  # If the directory is not found
   
def sanitize_string(s): 
    s = s.replace(' ', '_') 
    s = re.sub('[^0-9a-zA-Z_-]+', '', s) 
    s = re.sub('[-_]+', '_', s) 
    s = s.strip('_-') 
    return s