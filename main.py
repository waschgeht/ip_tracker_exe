from sys import exit
from subprocess import Popen, PIPE
from smtplib import SMTP_SSL
from _datetime import datetime

'''funktion requestet ip von ifconfig.me'''

def cmd(command):
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ip = process.communicate()
    return ip

def external_ip_requester():
    try:
        ip = str(cmd("curl -s http://ifconfig.me/ip")[0]) #.popen erzeugt keine Ausgabe am Screen
        ip= ip[2:len(ip)-1]
        int(ip[0]) #testet ob ausgabe eine IP ist. Erzeugt fehler wenn falsch und läuft in except block
        return ip
    except:
        print("Couldnt get ip from http://ifconfig.me/ip")
        raise SystemExit(0) #schließt das programm komplett

def send_text():
    Path = "C:\\ip_tracker"
    with open(Path + "\\data.conf", "r") as data: #liest daten aus .conf file; Positionsabhängig!!!
        Data = data.readlines()
    try:
        message = 'Subject: {}\n\n{}'.format("Your current IP", "Your current IP is " + Data[3]) #erstellt message mit Data[2]=IP
        server = SMTP_SSL("smtp.gmail.com", 465) #funktionierrt nur für gmail server. Applikationszugriff uss aktiviert sein
        server.login(Data[0], Data[1])  #Data[0]=your email; Data[1]=your Email password
        server.sendmail(Data[0], Data[2], message) #Data[0]=your email; Data[2]=receiver email
        server.quit()
        logging("Email was sent")
    except Exception as error:
        print("Error, couldn't send message")
        print(error)
        logging("Couldn't send email;   " + str(error))

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




'''Main function thats gonna be startet by the schedules job!'''
def Main():
    Path = "C:\\ip_tracker"
    ip = external_ip_requester() #Requests email from ifconfig.me/ip
    with open(Path + "\\data.conf", "r+") as data: #Ließt Daten ein und ändert nur Eintrag 4 (Ip)
        ReadData = data.readlines()
        if str(ReadData[3]) == str(ip):
            exit()
        else:
            ReadData[3] = str(ip)

    with open(Path + "\\data.conf", "w+") as Data: #Schreibt änderungen zum File
        Data.writelines(ReadData)
        Data.close()
    send_text()

Main()
