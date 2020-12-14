import tkinter as tk
from _datetime import datetime
from subprocess import PIPE, Popen


#umgehe noconsole error
def cmd(command):
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ip = process.communicate()
    return ip


'''funktion requestet ip von ifconfig.me'''
def external_ip_requester():
    try:
        ip = str(cmd("curl -s http://ifconfig.me/ip")[0]) #.popen erzeugt keine Ausgabe am Screen
        ip= ip[2:len(ip)-1]
        int(ip[0]) #testet ob ausgabe eine IP ist. Erzeugt fehler wenn falsch und läuft in except block
        return ip
    except:
        print("Couldnt get ip from http://ifconfig.me/ip")
        raise SystemExit(0) #schließt das programm komplett



def logging(TEXT):
    Path = "C:\\ip_tracker"
    file_location = Path + "\\email.log"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(file_location, "a+") as log:
            log.write(date + ";   " + TEXT + " \n")
    except Exception as nopen1:
        print("Couldn't write to file")
        print(nopen1)

def schedule_task(frequency, time):
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
        cmd('SCHTASKS /CREATE /SC ' + str(frequency) + ' /TN "ip_tracker" /TR "C:\\ip_tracker\\main.exe" /ST ' + str(time))
        logging("Task wurde erstellt")
    except Exception as error:
        logging("Fehler beim erstellen von Task; ", error)

def  disable_task():
    try:
        cmd('SCHTASKS /CHANGE /TN "ip_tracker" /DISABLE')
        logging("Task disabled")
    except Exception as error:
        logging("Couldn't disable task; ", error)


def WriteToFile(email, password, receiver, ip):
    Path = "C:\\ip_tracker"
    with open(Path + "\\data.conf", "w+") as file:
        file.writelines([email, "\n", password, "\n", receiver, "\n", ip])





def CancelButton():
    root.destroy()

def ApplyButton():
    if EnableDiable.get()=="disable":
        disable_task()
    elif EnableDiable.get()=="enable":
        WriteToFile(e1.get(),e2.get(), e3.get(), external_ip_requester())
        schedule_task(frequence.get(), e4.get())
    root.destroy()

try:
    root = tk.Tk()
    tk.Label(root, text="Please be aware, for this to work you need to \n enable less safer apps on gmail!\n To do so please follow this link: \n \n https://myaccount.google.com/lesssecureapps \n").pack()
    tk.Button(root, text="Ok", command=root.destroy).pack()
    root.mainloop()
except:
    root.destroy()
    logging("Startwindow failure")


'''Gui buit up with grid'''
try:
    global e1, e2, e3
    root = tk.Tk()
    root.title("IP tracker") #titel
    tk.Label(root, text="Your Email").grid(row=0) #Label with Grid
    tk.Label(root, text="Your Password").grid(row=1)
    tk.Label(root, text="Receiver Email").grid(row=0, column=3)
    tk.Label(root, text="Frequency").grid(row=2, pady=(30,0))
    tk.Label(root, text="Enable/Disable").grid(row=2, column=4, pady=(30,0))
    tk.Label(root, text="Starttime").grid(row=2, column=1, pady=(30,0))

    e1 = tk.Entry(root) #Eingabefelder Email
    e2 = tk.Entry(root) #Enter password
    e3 = tk.Entry(root) #Enter receiver
    e4 = tk.Entry(root)  # Enter Starttime (Format 17:30)

    e1.grid(row=0, column=1, padx=10, pady=10) #Padding applies to both sides x for x axis y for y axis
    e2.grid(row=1, column=1, padx=10, pady=10)
    e3.grid(row=0, column=4,padx=10, pady=10)
    e4.grid(row=3, column=1, padx=10, pady=10)

    frequence = tk.StringVar(root) #Variable for drop down menue
    frequence.set("hourly")  # default value
    w = tk.OptionMenu(root, frequence, "hourly", "dayly").grid(row=3, column=0,padx=10) #Dropdown choices for frequency of Task Scheduler

    EnableDiable = tk.StringVar(root) #Variable for drop down menue
    EnableDiable.set("enable")  # default value
    Enabler = tk.OptionMenu(root, EnableDiable, "enable", "disable")  # Dropdown choices
    Enabler.grid(row=3, column=4, padx=10)
    print(EnableDiable.get())
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