try:
    import pip
    pip.main(['install','requests'])
    pip.main(['install','xmltodict'])
except:
    None

#Onderstaande modules zijn nodig voor verschillende onderdelen van de code
import requests         #Deze module wordt gebruikt voor het opvragen van de API
import xmltodict        #Deze module wordt gebtuikt voor het omzetten van de gegevens naar een dict
import sys              #Deze module wordt gebruikt om het programma af te kunnen sluiten
from tkinter import *   #Deze module wordt gebruikt voor de GUI

stations = ['Hilversum','Kampen', 'Culemborg', 'Utrecht Lunetten', 'Driebergen-Zeist', 'Utrecht Centraal'] #Deze lijst is de lijst met stations die opgevraagd kunnen worden

def gegevens_opvragen(stationsNaam):
    auth_details = ('gerrit.vanos@student.hu.nl', 'BE66_yqU3kQWgKSQJdWPxEHZ8JFji7pM74B9fTCwQo1yZW3clRSQ4w') #Dit is om toegang te krijgen tot de NS API
    api_url = 'http://webservices.ns.nl/ns-api-avt?station='+stationsNaam #Dit is de URL van de API
    response = requests.get(api_url, auth=auth_details) #Response is de variabelen waar het antwoord in opgeslagen wordt
    vertrekDict = xmltodict.parse(response.text) #Hier wordt de verkregen informatie omgezet in een dictionary en opgeslagen

    vertrekDict = vertrekDict['ActueleVertrekTijden']['VertrekkendeTrein']

    return vertrekDict #Dat de gegevens worden terug gegeven aan de functie

def Information(station):
    choiceWindow.destroy()                  #Het sluiten van de vorige window
    gegevens = gegevens_opvragen(station)   #Hier wordt API opgevraagd van het gekozen station

    global infoWindow                       #Deze maakt de infoWindows globaal
    infoWindow = Tk()                       #Aanmaken van het window
    infoWindow["bg"]='#fed339'              #Achtergrond kleur van het window
    infoWindow.geometry('1366x768')
    infoWindow.option_add('*Label.Background', 'white')                         #De kleur van de achtergrond van de tabel
    infoWindow.option_add('*Label.Font',('Frutiger Bold Regular',10,'bold'))    #Het lettertype van dit window

    MainFrame = Frame(master=infoWindow,bg='#fed339')

    titelFrame = Frame(master=MainFrame,width=1280, height=100, pady=10,bg='#fed339')  #Het frame waar de titel in staat zodat deze goed gecentreerd/uitgelijnd kan worden op de pagina
    titel = Label(master=titelFrame, text='De actuele vertrektijden van station '+station+' zijn:', font=('Frutiger Bold Regular',26,'bold'), bg='#fed339', fg='#000066')   #Opmaak van de titel
    titel.pack()    #Sluit de titel af en zet deze op de pagina
    titelFrame.grid(row=0) #Zet het Frame van de titel op regel 0 van de pagina

    infoFrame = Frame(master=MainFrame, height=500, pady=10,bg='white', bd=5)  #Het frame waar de informatie in getoond wordt
    #Onderstaande Label statments zetten de varibalen in de goede rij en de goede kolom
    Label(master=infoFrame, text='EindBestemming').grid(row=1, column=0, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Vertrekspoor').grid(row=1, column=1, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Vertrektijd').grid(row=1, column=2, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Vertraging').grid(row=1, column=3, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Treinsoort').grid(row=1, column=4, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Vervoerder').grid(row=1, column=5, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Routetekst').grid(row=1, column=6, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Routetips').grid(row=1, column=7, ipadx=5, ipady=10, )
    Label(master=infoFrame, text='Opmerkingen').grid(row=1, column=8, ipadx=5, ipady=10, )

    count =0    #Hier wordt de count op 0 gezet voor het tellen van het aantal treinen
    rij = 2     #Zorgt dat er na elke trein een nieuwe rij gebruikt wordt
    for trein in gegevens: #Deze for-loop wordt gebruikt om de informatie uit alle vertrekkende treinen te halen
        kolom = 0
        if count == 5:
            break
        for key in trein:
            #Voor alle onderstaande if/elif statments zorgen ervoor dat de informatie in de goede rijen komt te staan
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
            #Onderstaande if/elif statements zorgen ervoor dat bepaalde gegevens juist weergegeven worden, dit omdat sommige gegevens in een dubbele orderddict zitten
            if kolom == 1:#Deze if is voor het correct weergeven van het Vertrekspoor
                Label(master=infoFrame, text='{}'.format(trein[key]['#text'])).grid(row=rij, column=kolom, ipadx=5, ipady=10)
            elif kolom == 2:#Deze if is voor het correct weergeven van de vertrektijd
                DatumTijd = str(trein[key]) #Dit zorgt ervoor dat de datum/tijd in een string wordt omgezet
                Tijd = DatumTijd[11:16]     #Hier wordt de tijd geselecteerd uit de datum/tijd
                Label(master=infoFrame, text='{}'.format(Tijd)).grid(row=rij, column=kolom, ipadx=5, ipady=10)
            elif kolom == 3:#Deze if is voor het correct weergeven van de vertraging
                vertraging = '+'+str(trein[key])[2:] #Hier wordt de tijd geselecteerd van de vertraging
                Label(master=infoFrame, text='{}'.format(vertraging),fg='red').grid(row=rij, column=kolom, ipadx=5, ipady=10)
            elif kolom == 8:#Deze if is voor het correct weergeven van de opmerking
                opmerking = str(trein[key])[28:-4]#Dit zorgt ervoor dat de key omgezet wordt in een string
                Label(master=infoFrame, text='{}'.format(opmerking)).grid(row=rij, column=kolom, ipadx=5, ipady=10)
            else: #Deze else zorgt voor het correct vergeven van alle andere labels
                Label(master=infoFrame, text='{}'.format(trein[key])).grid(row=rij, column=kolom, ipadx=5, ipady=10)
        rij += 1 #Zorgt ervoor dat de rij met 1 verhoogd wordt
        count +=1 #zorgt ervoor dat de count met 1 verhoogd wordt
    infoFrame.grid(row=1,padx=25)#Dit geeft aan in welke rijhet frame word geset

    buttonFrame = Frame(master=MainFrame, width=1280, height=100, pady=10,bg='#fed339') #Deze regel geeft aan hoe de layout van het frame van de button er uit ziet
    gaterug = Button(master=buttonFrame, text='ga terug', command=StartScreen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold')) #Dit geeft de opmaak van de button aan
    gaterug.grid(pady=10, padx=10,column=3,  row=rij)
    gadoor = Button(master=buttonFrame, text='ga door', command=choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))       #Dit geeft de opmaak van de button aan
    gadoor.grid(pady=10, padx=10,  column=4, row=rij)
    buttonFrame.grid(row=2) #Deze zorgt ervoor dat de buttons in de 2 rij komen te staan

    MainFrame.place(relx=0.5, rely=0.3, anchor=CENTER)
    infoWindow.mainloop() #Het zorgt ervoor dat het window getoond wordt


def CheckOption():#Haalt de informatie uit het menu en geeft deze aan de Information
    Information(UserChoice.get())

#Stopt het systeem
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
    choiceWindow.geometry('1366x768')

    MainFrame=Frame(master=choiceWindow,bg='#fed339')

    DropdownFrame=Frame(master=MainFrame,bg='#fed339')
    global UserChoice
    UserChoice = StringVar(DropdownFrame)
    UserChoice.set(stations[0])  # default value
    dropdown = OptionMenu(DropdownFrame, UserChoice, *stations)
    dropdown.config(bg='#000066', fg='white', font=('Frutiger Bold Regular', 40, 'bold'))
    dropdown.pack()
    DropdownFrame.pack()

    ButtonFrame = Frame(master=MainFrame,bg='#fed339')
    gadoor = Button(master=ButtonFrame, text='ga door', command=CheckOption, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))       #Dit geeft de opmaak van de button aan
    gadoor.pack()
    ButtonFrame.pack()

    MainFrame.place(relx=0.5,rely=0.3,anchor=CENTER)

def StartScreen(): #Initieert het startscherm
    try:
        infoWindow.destroy()
    except:
        None
    global root
    root = Tk()
    root['bg']='#fed339'
    root.title('Startscherm')
    root.geometry('1366x768')

    MainFrame = Frame(master=root ,bg='#fed339')
    titelFrame = Frame(master=MainFrame,height=100, pady=10,bg='#fed339')
    titel = Label(master=titelFrame, text='Welkom bij de NS', font=('Frutiger Bold Regular',40,'bold'), bg='#fed339', fg='#000066')
    titel.pack(ipadx= 0, ipady = 0) #Print de welkomsboodschap in de GUI
    titelFrame.grid(row=0)

    windowFrame = Frame(master=MainFrame, height=100, pady=10,bg='#fed339')
    whiteWindow = Label(master=windowFrame, text='Klik op ga door om actuele reisinformatie op te vragen, klik op stop om het programma af te sluiten', font=('Frutiger Bold Regular',8,'bold'), bg='white', fg='#000066')
    whiteWindow.pack(ipadx= 25, ipady = 100) #Print de informatie over opties in de GUI
    windowFrame.grid(row=1, padx=25)

    buttonFrame = Frame(master=MainFrame, width=1280, height=100, pady=10,bg='#fed339')
    gaterug = Button(master=buttonFrame, text='ga terug', command=stoppen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gaterug.grid(pady=10, padx=10,column=3,  row=0)
    gadoor = Button(master=buttonFrame, text='ga door', command=choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))
    gadoor.grid(pady=10, padx=10,  column=4, row=0)
    buttonFrame.grid(row=2)

    MainFrame.place(relx=0.5,rely=0.25, anchor=CENTER)
    root.mainloop()

StartScreen()
