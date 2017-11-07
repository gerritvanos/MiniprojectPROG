#Onderstaande modules zijn nodig voor verschillende onderdelen van de code
import requests         #Deze module wordt gebruikt voor het opvragen van de API
import xmltodict        #Deze module wordt gebtuikt voor het omzetten van de gegevens naar een dict
import sys              #Deze module wordt gebruikt om het programma af te kunnen sluiten
from tkinter import *   #Deze module wordt gebruikt voor de GUI

stations = ['Hilversum','Kampen', 'Culemborg', 'Utrecht Lunetten', 'Driebergen-Zeist', 'Utrecht Centraal'] #Deze lijst is de lijst met stations die opgevraagd kunnen worden

def gegevens_opvragen(stationsNaam):
    auth_details = ('gerrit.vanos@student.hu.nl', 'BE66_yqU3kQWgKSQJdWPxEHZ8JFji7pM74B9fTCwQo1yZW3clRSQ4w')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station='+stationsNaam
    response = requests.get(api_url, auth=auth_details)
    vertrekDict = xmltodict.parse(response.text)

    vertrekDict = vertrekDict['ActueleVertrekTijden']['VertrekkendeTrein']

    return vertrekDict

def info(station):
    choiceWindow.destroy()
    gegevens = gegevens_opvragen(station)
    rij = 2
    global infoWindow
    infoWindow = Tk()

    infoWindow["bg"]='#fed339'
    infoWindow.option_add('*Label.Background', 'white')
    infoWindow.option_add('*Label.Font',('Frutiger Bold Regular',12,'bold'))

    titelFrame = Frame(master=infoWindow,width=1280, height=100, pady=10,bg='#fed339')
    titel = Label(master=titelFrame, text='De actuele vertrektijden van station '+station+' zijn:', font=('Frutiger Bold Regular',26,'bold'), bg='#fed339', fg='#000066')
    titel.grid(row=0, columnspan=7)
    titelFrame.grid(row=0)

    infoFrame = Frame(master=infoWindow, width=1000, height=500, pady=10,bg='white', bd=5)
    Label(master=infoFrame, text='EindBestemming').grid(row=1, column=0, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Vertrekspoor').grid(row=1, column=1, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Vertrektijd').grid(row=1, column=2, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Vertraging').grid(row=1, column=3, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Treinsoort').grid(row=1, column=4, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Vervoerder').grid(row=1, column=5, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Routetekst').grid(row=1, column=6, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Routetips').grid(row=1, column=7, ipadx=10, ipady=10, )
    Label(master=infoFrame, text='Opmerkingen').grid(row=1, column=8, ipadx=10, ipady=10, )

    count =0
    for trein in gegevens:
        kolom = 0
        if count == 5:
            break
        for key in trein:
            if key == 'EindBestemming':
                kolom = 0
            elif key == 'VertrekSpoor':
                kolom = 1
            elif key == 'VertrekTijd':
                kolom = 2
            elif key == 'VertrekVertraging':
                kolom = 3
            elif key == 'TreinSoort':
                kolom = 4
            elif key == 'Vervoerder':
                kolom = 5
            elif key == 'RouteTekst':
                kolom = 6
            elif key == 'ReisTip':
                kolom = 7
            elif key == 'Opmerkingen':
                kolom = 8
            elif key == 'VertrekVertragingTekst':
                continue
            if kolom == 1:
                Label(master=infoFrame, text='{}'.format(trein[key]['#text'])).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            elif kolom == 2:
                tijd = str(trein[key])
                tijd = tijd[11:16]
                Label(master=infoFrame, text='{}'.format(tijd)).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            elif kolom == 3:
                vertraging = '+'+str(trein[key])[2:]
                Label(master=infoFrame, text='{}'.format(vertraging)).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            else:
                Label(master=infoFrame, text='{}'.format(trein[key])).grid(row=rij, column=kolom, ipadx=10, ipady=10)
        rij += 1
        count +=1
    infoFrame.grid(row=1,padx=100)

    buttonFrame = Frame(master=infoWindow, width=1280, height=100, pady=10,bg='#fed339')
    gaterug = Button(master=buttonFrame, text='ga terug', command=stoppen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gaterug.grid(pady=10, padx=10,column=3,  row=rij)
    gadoor = Button(master=buttonFrame, text='ga door', command=choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gadoor.grid(pady=10, padx=10,  column=4, row=rij)
    buttonFrame.grid(row=2)

    infoWindow.mainloop()


def controleer():
    info(variable.get())

def stoppen():
    sys.exit()

def choice():
    try:
        root.destroy()
    except:
        infoWindow.destroy()
    global choiceWindow
    choiceWindow= Tk()
    choiceWindow["bg"]='#fed339'
    global variable
    variable = StringVar(choiceWindow)
    variable.set(stations[0])  # default value
    dropdown = OptionMenu(choiceWindow, variable, *stations)
    dropdown.config(bg='#000066', fg='white', font=('Frutiger Bold Regular', 40, 'bold'))
    dropdown.pack()
    okButton = Button(master=choiceWindow, text='OK', command=controleer, bg='#000066',fg='white', font=('Frutiger Bold Regular',40,'bold'))
    okButton.pack(pady=10)

def StartScreen(): #Initieert het startscherm
    global root
    root = Tk()
    root['bg']='#fed339'

    titelFrame = Frame(master=root,width=1280, height=100, pady=10,bg='#fed339')
    titel = Label(master=titelFrame, text='Welkom bij de NS', font=('Frutiger Bold Regular',40,'bold'), bg='#fed339', fg='#000066')
    titel.pack(ipadx= 0, ipady = 0) #Print de welkomsboodschap in de GUI
    titelFrame.grid(row=0)

    windowFrame = Frame(master=root,width=1280, height=100, pady=10,bg='#fed339')
    whiteWindow = Label(master=windowFrame, text='Klik op ga door om actuele reisinformatie op te vragen, klik op stop om het programma af te sluiten', font=('Frutiger Bold Regular',8,'bold'), bg='white', fg='#000066')
    whiteWindow.pack(ipadx= 5, ipady = 5) #Print de informatie over opties in de GUI
    windowFrame.grid(row=1, padx=100)

    buttonFrame = Frame(master=root, width=1280, height=100, pady=10,bg='#fed339')
    gaterug = Button(master=buttonFrame, text='ga terug', command=stoppen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gaterug.grid(pady=10, padx=10,column=3,  row=0)
    gadoor = Button(master=buttonFrame, text='ga door', command=choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gadoor.grid(pady=10, padx=10,  column=4, row=0)
    buttonFrame.grid(row=2)
    root.mainloop()

StartScreen()
