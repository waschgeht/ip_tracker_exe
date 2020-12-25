import tkinter as tk
from urllib.request import urlretrieve
from tkinter import ttk
import time
from os import path
from smtplib import SMTP_SSL
from _datetime import datetime
from base64 import b64encode, b64decode
from subprocess import Popen, PIPE

'''umgehe noconsole error bei convert durch pyinstaller'''
def cmd(command):
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ip = process.communicate()
    return ip

def new_update():
    try:
        newest_version = float(cmd("curl --max-time 1 -s http://softwareupdt.duckdns.org:8080/ip_tracker/version.txt")[0].decode('ascii'))
        if newest_version > 0.1:
            return True
        else:
            return False
    except Exception as error:
        logging("failed update check; " , error)

'''funktion requestet ip von ifconfig.me'''
def external_ip_requester():
    try:
        ip = str(cmd("curl -s http://ifconfig.me/ip")[0]) #self made function cmd because noconsole error
        ip= ip[2:len(ip)-1]
        int(ip[0]) #testet ob ausgabe eine IP ist. Erzeugt fehler wenn falsch und läuft in except block
        return ip
    except:
        logging("Couldnt get ip from http://ifconfig.me/ip")
        raise SystemExit(0) #schließt das programm komplett

'''Base 64 encodes and decodes messages'''
def bencode(secret):
    return b64encode(bytes(secret, encoding='utf-8')).decode('ascii')

def bdecode(secret):
    return b64decode(secret).decode('ascii')

'''
Sendet plain text message
'''
def Pfad():
    return "C:\\ip_tracker"

def send_text():
    Path = Pfad()
    with open(Path + "\\data.conf", "r") as data: #liest daten aus .conf file; Positionsabhängig!!!
        Data = data.readlines()
        for i in range(0,3):
            Data[i] = bdecode(Data[i])
    try:
        message = 'Subject: {}\n\n{}'.format("Your current IP", "Your current IP is " + Data[3]) #erstellt message mit Data[2]=IP
        server = SMTP_SSL("smtp.gmail.com", 465) #funktionierrt nur für gmail server. Applikationszugriff uss aktiviert sein
        server.login(Data[0], Data[1])  #Data[0]=your email; Data[1]=your Email password
        server.sendmail(Data[0], Data[2], message) #Data[0]=your email; Data[2]=receiver email
        server.quit()
        logging("Email was sent")
    except Exception as error:
        logging("Couldn't send email;   " + str(error))

def logging(TEXT):
    Path = Pfad()
    file_location = Path + "\\email.log"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(file_location, "a+") as log:
            log.write(date + ";   " + TEXT + " \n")
    except Exception as nopen1:
        pass

def schedule_task(frequency, time):
    Path = Pfad()
    try:
        Tasks = str(cmd('SCHTASKS'))
        Tasks.index("ip_tracker")
        try:
            cmd('SCHTASKS /DELETE /TN "ip_tracker" /f')
        except Exception as error:
            logging("Couldnt delete Task; ", error)
    except:
        pass
    try:
        cmd('SCHTASKS /CREATE /SC ' + str(frequency) + ' /TN "ip_tracker" /TR "' + Path + '\\main.exe" /ST ' + str(time))
        logging("Task wurde erstellt")
    except Exception as error:
        logging("Fehler beim erstellen von Task; ", error)

def  disable_task():
    try:
        cmd('SCHTASKS /CHANGE /TN "ip_tracker" /DISABLE')
        logging("Task disabled")
    except Exception as error:
        logging("Couldn't disable task; ", error)

def enable_task():
    try:
        cmd('SCHTASKS /CHANGE /TN "ip_tracker" /ENABLE')
        logging("Task enabled")
    except Exception as error:
        logging("Couldn't enable task; ", error)

def WriteToFile(email, password, receiver, ip):
    Path = Pfad()
    with open(Path + "\\data.conf", "w+") as file:
        file.writelines([email, "\n", password, "\n", receiver, "\n", ip])

def CancelButton():
    root.destroy()

def ApplyButton():
    if EnableDiable.get()=="disable":
        disable_task()
    elif EnableDiable.get()=="enable":
        WriteToFile(bencode(e1.get()),bencode(e2.get()), bencode(e3.get()), external_ip_requester())
        schedule_task(frequence.get(), e4.get())
        send_text()
    root.destroy()

def bar_update(bar, Wert):
    bar['value'] = Wert
    root.update_idletasks()
    time.sleep(1)

def download():
    bar = ttk.Progressbar(root, orient="horizontal", length=200)
    bar.grid(row=2, columnspan=2, padx=30, pady=20)
    bar_update(bar, 0)
    urlretrieve("http://softwareupdt.duckdns.org:8080/ip_tracker/gui.exe", "gui.exe")
    bar_update(bar, 50)
    urlretrieve("http://softwareupdt.duckdns.org:8080/ip_tracker/main.exe", "main.exe")
    bar_update(bar, 100)
    root.destroy()

try:
    root = tk.Tk()
    #photo = tk.PhotoImage(file=Pfad() + "\\icon1.png")
    #root.iconphoto(False, photo)
    root.title("IP tracker")  # titel
    tk.Label(root, text="Please be aware, for this to work you need to \n enable less safer apps on gmail!\n To do so please follow this link: \n \n https://myaccount.google.com/lesssecureapps \n").pack()
    tk.Button(root, text="Ok", command=root.destroy).pack()
    root.mainloop()
except:
    root.destroy()
    logging("Startwindow failure")

try:
    if new_update():
        try:
            root = tk.Tk()
            #photo = tk.PhotoImage(file=Pfad() + "\\icon1.png")
            #root.iconphoto(False, photo)
            root.title("Update available!")  # titel
            tk.Label(root, text="There is a new update available, \n do you want to download the newest .exe version?").grid(row=0, columnspan=2, padx=10, pady=10)
            tk.Button(root, text="   Yes   ", command=download).grid(row=1, column=0,padx=10, pady=10, sticky=tk.E)
            tk.Button(root, text="   No   ", command=root.destroy).grid(row=1, column=1,padx=10, pady=10, sticky=tk.W)
            tk.Label(root, text="     ").grid(row=2, columnspan=2, padx=30, pady=20)
            root.mainloop()
        except:
            root.destroy()
            logging("Updatewindow failure")
except:
    logging("Update failure")

'''Gui buit up with grid'''
try:
    global e1, e2, e3
    root = tk.Tk()
    #photo = tk.PhotoImage(file=Pfad() + "\\icon1.png")
    #root.iconphoto(False, photo)
    root.title("IP tracker") #titel
    tk.Label(root, text="Your Email").grid(row=0) #Label with Grid
    tk.Label(root, text="Your Password").grid(row=1)
    tk.Label(root, text="Receiver Email").grid(row=0, column=3)
    tk.Label(root, text="Frequency").grid(row=2, pady=(30,0))
    tk.Label(root, text="Enable/Disable").grid(row=2, column=4, pady=(30,0))
    tk.Label(root, text="Starttime").grid(row=2, column=1, pady=(30,0), sticky=tk.W)

    e1 = tk.Entry(root, width=40) #Eingabefelder Email
    e2 = tk.Entry(root, show="*", width=40) #Enter password
    e3 = tk.Entry(root, width=40) #Enter receiver
    e4 = tk.Entry(root)  # Enter Starttime (Format 17:30)

    e1.grid(row=0, column=1, padx=10, pady=10) #Padding applies to both sides x for x axis y for y axis
    e2.grid(row=1, column=1, padx=10, pady=10)
    e3.grid(row=0, column=4,padx=10, pady=10)
    e4.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    frequence = tk.StringVar(root) #Variable for drop down menue
    frequence.set("hourly")  # default value
    w = tk.OptionMenu(root, frequence, "hourly", "dayly").grid(row=3, column=0,padx=10) #Dropdown choices for frequency of Task Scheduler

    EnableDiable = tk.StringVar(root) #Variable for drop down menue
    EnableDiable.set("enable")  # default value
    Enabler = tk.OptionMenu(root, EnableDiable, "enable", "disable")  # Dropdown choices
    Enabler.grid(row=3, column=4, padx=10)

    '''This function toggles the entry widgets away is the ip_tracker should be disabled'''
    def toogle(*args):
        global e1,e2, e3
        if EnableDiable.get() == "disable":
            e1.grid_forget()
            e2.grid_forget()
            e3.grid_forget()
            e4.grid_forget()
        elif EnableDiable.get() == "enable":
            e1.grid(row=0, column=1, padx=10, pady=10)  # Padding applies to both sides x for x axis y for y axis
            e2.grid(row=1, column=1, padx=10, pady=10)
            e3.grid(row=0, column=4, padx=10, pady=10)
            e4.grid(row=3, column=1, padx=10, pady=10)
    EnableDiable.trace("w", toogle) #Tracks changes in the EnableDisable variable and calls the toggle function if so
    '''Set Button, that Sets all the values from the widget'''
    tk.Button(root, text="Apply Settings", command=ApplyButton).grid(row=4, column=3, padx=5, pady=(100,5))
    '''Cancel Button destroys the gui'''
    tk.Button(root, text="Cancel", command=CancelButton).grid(row=4, column=4, padx=5, pady=(100,5))
    root.mainloop()
except Exception as error:
    root.destroy()
    logging("Gui failed; " + str(error))