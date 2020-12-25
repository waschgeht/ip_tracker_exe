from sys import exit
from smtplib import SMTP_SSL
from _datetime import datetime
from base64 import b64encode, b64decode
from subprocess import Popen, PIPE

def Pfad():
    return "C:\\ip_tracker"

'''umgehe noconsole error bei convert durch pyinstaller'''
def cmd(command):
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ip = process.communicate()
    return ip

'''Base 64 encodes and decodes messages'''
def bencode(secret):
    return b64encode(bytes(secret, encoding='utf-8')).decode('ascii')

def bdecode(secret):
    return b64decode(secret).decode('ascii')

def logging(TEXT):
    Path = Pfad()
    file_location = Path + "\\email.log"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(file_location, "a+") as log:
            log.write(date + ";   " + TEXT + " \n")
    except Exception as nopen1:
        pass

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


'''Main function thats gonna be startet by the schedules job!'''
def Main():
    Path = Pfad()
    ip = external_ip_requester() #Requests email from ifconfig.me/ip
    with open(Path + "\\data.conf", "r") as data: #Ließt Daten ein und ändert nur Eintrag 4 (Ip)
        ReadData = data.readlines()
        if str(ReadData[3]) == str(ip):
            exit()
        else:
            ReadData[3] = str(ip)

    with open(Path + "\\data.conf", "w") as Data: #Schreibt änderungen zum File
        Data.writelines(ReadData)
        Data.close()
    send_text()

Main()
