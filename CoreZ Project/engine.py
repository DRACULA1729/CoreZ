import hashlib
import os
import psutil
import winreg

#global variable
virusinfo=list(open("Database/virusinfo.txt","r").read().split('\n'))
malware_hashes= list(open("Database/virushashe.txt","r").read().split('\n'))
   
#get hash of flie
def sha256_hashes(filename):
    with open(filename, "rb") as f:
        bytes = f.read()
        sha256hash = hashlib.sha256(bytes).hexdigest()
        f.close()
    return sha256hash


#for malware detection
def malware_checker(pathoffile):
    global malware_hashes
    global virusinfo
    hash_malware_check= sha256_hashes(pathoffile)
    counter=0
    for i in malware_hashes:
        if i== hash_malware_check:
             return virusinfo[counter]
        counter += 1
            
    return 0

#malware detection in a folder
virusName=[]
virusPath=[]

#Quick Scan

def quickScan(path):
    #get the directory list
    dir_list = list()
    for(dirpath,filenames) in os.walk(path):
        dir_list+= [os.path.join(dirpath,file) for file in filenames] 

    
    for i in dir_list:
        if malware_checker(i) != 0:
            virusName.append(malware_checker(i)+"::File:: "+i)
            virusPath.append(i)
        else:
            print(f"{i} file is clean!")




def virusScanner(path):
    #get the directory list
    dir_list = list()
    for(dirpath,filenames) in os.walk(path):
        dir_list+= [os.path.join(dirpath,file) for file in filenames] 

    
    for i in dir_list:
        if malware_checker(i) != 0:
            virusName.append(malware_checker(i)+"::File:: "+i)
            virusPath.append(i)
        else:
            print("File Is Clean")

#Virus Remover
def virusRemover(path):
    virusScanner(path)
    if virusPath:
        for i in virusPath:
            os.remove(i)
    else:
        return 0



#RAM BOOSTER DONE
def get_installed_software_executables():
    software_executables = []

    # Registry paths where installed software details are stored
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for path in registry_paths:
        try:
            # Open the registry key
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        # Get each subkey
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            # Fetch software name and executable name (if available)
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            try:
                                display_icon = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                                executable_ = os.path.basename(display_icon)  # Extract executable name
                                executable_name =executable_.split(".exe")[0] + ".exe"
                                if display_name and executable_name:
                                    software_executables.append((display_name, executable_name))
                            except FileNotFoundError:
                                continue
                    except EnvironmentError:
                        continue
        except EnvironmentError:
            continue

    return software_executables






def ramboost():
 running_processes=[proc.name().lower() for proc in psutil.process_iter()]
 tasklist=[]
 names=[]
 exe=[]
 for name, executable in get_installed_software_executables():
    names.append(name)
    exe.append(executable.lower())

 for i in exe:
     if i in running_processes:
         tasklist.append(i)

 
 for i in tasklist:
    try:
       print("Cleaning....{}".format(i))
       os.system("TASKKILL /IM {} /F".format(i))
       
    except Exception as e:
        print(f"Failed to kill {i}: {e}")
 return ("Ram Boosted Sucessfully " )









quickScan("C:/Desktop")