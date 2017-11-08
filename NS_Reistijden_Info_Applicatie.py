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

def StartScreen(): #Initieert het startscherm
    try:
        InfoWindow.destroy() #Vernietigt het infoWindow als het startscherm wordt opgevraagd
    except:
        None
    global Root #Zorgt ervoor dat de root variabele voor het hele programma geld
    Root = Tk() #Koppelt variabele root aan Tkinter
    Root['bg']= '#fed339' #Maakt de achtergrond van de root Geel
    Root.title('NS Reistijden Info Applicatie') #Zorgt ervoor dat de naam van de applicatie als deze wordt gestart NS Reistijden Info Applicatie is
    Root.geometry('1366x768')

    MainFrame = Frame(master=Root, bg='#fed339') #Voegt het startscherm toe aan het algemene frame
    TitleFrame = Frame(master=MainFrame,height=100, pady=10,bg='#fed339') #Maakt een frame voor de welkomstboodschap
    Title = Label(master=TitleFrame, text='Welkom bij de NS', font=('Frutiger Bold Regular',40,'bold'), bg='#fed339', fg='#000066') #Print de welkomstboodschap in de GUI
    Title.pack(ipadx= 0, ipady = 0) #Zorgt ervoor dat de welkomstboodschap op de juiste plek staat op x en y-as
    TitleFrame.grid(row=0) #Zorgt ervoor dat de welkomstboodschap op de juiste plek in de grid staat

    WindowFrame = Frame(master=MainFrame, height=100, pady=10,bg='#fed339') #Maakt een frame voor de tekst in het witte veld
    WhiteWindow = Label(master=WindowFrame, text='Klik op ga door om actuele reisinformatie op te vragen, klik op stop om het programma af te sluiten', font=('Frutiger Bold Regular',8,'bold'), bg='white', fg='#000066') #Print de tekst in het witte veld in de GUI
    WhiteWindow.pack(ipadx= 25, ipady = 100) #Zorgt ervoor dat de tekst in het witte veld op de juiste plek staat op x en y-as
    WindowFrame.grid(row=1, padx=25) #Zorgt ervoor dat de tekst in het witte veld op de juist plek in de grid staat

    ButtonFrame = Frame(master=MainFrame, width=1280, height=100, pady=10,bg='#fed339') #Maakt een frame voor de knoppen
    ButtonFrame.grid(row=2) #Plaatst het frame van de knoppen op de goede plek in de grid
    Stop = Button(master=ButtonFrame, text='Stop', command=stoppen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold')) #Print de 'Stop' knop interactief in de GUI
    Stop.grid(pady=10, padx=10,column=3,  row=0) #Zorgt ervoor dat de 'Stop' knop op de juiste plek in de grid staat
    Continue = Button(master=ButtonFrame, text='Ga door', command=Choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold')) #Print de 'Ga door' knop interactief in de GUI
    Continue.grid(pady=10, padx=10,  column=4, row=0) #Zorgt ervoor dat de 'Ga door' knop op de juiste plek in de grid staat

    MainFrame.place(relx=0.5,rely=0.25, anchor=CENTER) #Centreert het algemene Frame
    Root.mainloop()

def Choice():
    try:
        Root.destroy()
    except:
        InfoWindow.destroy()
    global ChoiceWindow
    ChoiceWindow= Tk()
    ChoiceWindow["bg"]= '#fed339'
    ChoiceWindow.geometry('1366x768')

    MainFrame=Frame(master=ChoiceWindow, bg='#fed339')

    DropdownFrame=Frame(master=MainFrame,bg='#fed339')
    global UserChoice
    UserChoice = StringVar(DropdownFrame)
    UserChoice.set(stations[0])  # default value
    Dropdown = OptionMenu(DropdownFrame, UserChoice, *stations)
    Dropdown.config(bg='#000066', fg='white', font=('Frutiger Bold Regular', 40, 'bold'))
    Dropdown.pack()
    DropdownFrame.pack()

    ButtonFrame = Frame(master=MainFrame,bg='#fed339')
    Continue = Button(master=ButtonFrame, text='ga door', command=CheckOption, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold')) #Dit geeft de opmaak van de button aan
    Continue.pack()
    ButtonFrame.pack()

    MainFrame.place(relx=0.5,rely=0.3,anchor=CENTER)


def InformationRequest(stationsNaam):
    AuthDetails = ('gerrit.vanos@student.hu.nl', 'BE66_yqU3kQWgKSQJdWPxEHZ8JFji7pM74B9fTCwQo1yZW3clRSQ4w') #Dit is om toegang te krijgen tot de NS API
    APIUrl = 'http://webservices.ns.nl/ns-api-avt?station='+stationsNaam #Dit is de URL van de API
    Response = requests.get(APIUrl, auth=AuthDetails) #Response is de variabelen waar het antwoord in opgeslagen wordt
    InformationDict = xmltodict.parse(Response.text) #Hier wordt de verkregen informatie omgezet in een dictionary en opgeslagen

    InformationDict = InformationDict['ActueleVertrekTijden']['VertrekkendeTrein']

    return InformationDict #Dat de gegevens worden terug gegeven aan de functie

def Information(station):
    ChoiceWindow.destroy()                  #Het sluiten van de vorige window
    Information = InformationRequest(station)   #Hier wordt API opgevraagd van het gekozen station

    global InfoWindow                       #Deze maakt de infoWindows globaal
    InfoWindow = Tk()                       #Aanmaken van het window
    InfoWindow["bg"]= '#fed339'              #Achtergrond kleur van het window
    InfoWindow.geometry('1366x768')
    InfoWindow.option_add('*Label.Background', 'white')                         #De kleur van de achtergrond van de tabel
    InfoWindow.option_add('*Label.Font', ('Frutiger Bold Regular', 10, 'bold'))    #Het lettertype van dit window

    MainFrame = Frame(master=InfoWindow, bg='#fed339')

    TitleFrame = Frame(master=MainFrame,width=1280, height=100, pady=10,bg='#fed339')  #Het frame waar de titel in staat zodat deze goed gecentreerd/uitgelijnd kan worden op de pagina
    Title = Label(master=TitleFrame, text='De actuele vertrektijden van station '+station+' zijn:', font=('Frutiger Bold Regular',26,'bold'), bg='#fed339', fg='#000066')   #Opmaak van de titel
    Title.pack()    #Sluit de titel af en zet deze op de pagina
    TitleFrame.grid(row=0) #Zet het Frame van de titel op regel 0 van de pagina

    InfoFrame = Frame(master=MainFrame, height=500, pady=10,bg='white', bd=5)  #Het frame waar de informatie in getoond wordt
    #Onderstaande Label statments zetten de variabelen in de goede rij en de goede kolom
    Label(master=InfoFrame, text='EindBestemming').grid(row=1, column=0, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Vertrekspoor').grid(row=1, column=1, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Vertrektijd').grid(row=1, column=2, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Vertraging').grid(row=1, column=3, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Treinsoort').grid(row=1, column=4, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Vervoerder').grid(row=1, column=5, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Routetekst').grid(row=1, column=6, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Routetips').grid(row=1, column=7, ipadx=5, ipady=10, )
    Label(master=InfoFrame, text='Opmerkingen').grid(row=1, column=8, ipadx=5, ipady=10, )

    Count =0    #Hier wordt de count op 0 gezet voor het tellen van het aantal treinen
    Row = 2     #Zorgt dat er na elke trein een nieuwe rij gebruikt wordt
    for Train in Information: #Deze for-loop wordt gebruikt om de informatie uit alle vertrekkende treinen te halen
        Column = 0
        if Count == 5:
            break
        for Key in Train:
            #Voor alle onderstaande if/elif statments zorgen ervoor dat de informatie in de goede rijen komt te staan
            if Key == 'EindBestemming':
                Column = 0
            elif Key == 'VertrekSpoor':
                Column = 1
            elif Key == 'VertrekTijd':
                Column = 2
            elif Key == 'VertrekVertraging':
                Column = 3
            elif Key == 'TreinSoort':
                Column = 4
            elif Key == 'Vervoerder':
                Column = 5
            elif Key == 'RouteTekst':
                Column = 6
            elif Key == 'ReisTip':
                Column = 7
            elif Key == 'Opmerkingen':
                Column = 8
            elif Key == 'VertrekVertragingTekst':
                continue
            #Onderstaande if/elif statements zorgen ervoor dat bepaalde gegevens juist weergegeven worden, dit omdat sommige gegevens in een dubbele orderddict zitten
            if Column == 1:#Deze if is voor het correct weergeven van het Vertrekspoor
                Label(master=InfoFrame, text='{}'.format(Train[Key]['#text'])).grid(row=Row, column=Column, ipadx=5, ipady=10)
            elif Column == 2:#Deze if is voor het correct weergeven van de vertrektijd
                DatumTijd = str(Train[Key]) #Dit zorgt ervoor dat de datum/tijd in een string wordt omgezet
                Time = DatumTijd[11:16]     #Hier wordt de tijd geselecteerd uit de datum/tijd
                Label(master=InfoFrame, text='{}'.format(Time)).grid(row=Row, column=Column, ipadx=5, ipady=10)
            elif Column == 3:#Deze if is voor het correct weergeven van de vertraging
                Delay = '+'+str(Train[Key])[2:] #Hier wordt de tijd geselecteerd van de vertraging
                Label(master=InfoFrame, text='{}'.format(Delay),fg='red').grid(row=Row, column=Column, ipadx=5, ipady=10)
            elif Column == 8:#Deze if is voor het correct weergeven van de opmerking
                Comment = str(Train[Key])[28:-4]#Dit zorgt ervoor dat de key omgezet wordt in een string
                Label(master=InfoFrame, text='{}'.format(Comment)).grid(row=Row, column=Column, ipadx=5, ipady=10)
            else: #Deze else zorgt voor het correct vergeven van alle andere labels
                Label(master=InfoFrame, text='{}'.format(Train[Key])).grid(row=Row, column=Column, ipadx=5, ipady=10)
        Row += 1 #Zorgt ervoor dat de rij met 1 verhoogd wordt
        Count +=1 #zorgt ervoor dat de count met 1 verhoogd wordt
    InfoFrame.grid(row=1,padx=25)#Dit geeft aan in welke rijhet frame word geset

    ButtonFrame = Frame(master=MainFrame, width=1280, height=100, pady=10,bg='#fed339') #Deze regel geeft aan hoe de layout van het frame van de button er uit ziet
    Back = Button(master=ButtonFrame, text='ga terug', command=StartScreen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold')) #Dit geeft de opmaak van de button aan
    Back.grid(pady=10, padx=10,column=3,  row=Row)
    Continue = Button(master=ButtonFrame, text='ga door', command=Choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 16, 'bold'))       #Dit geeft de opmaak van de button aan
    Continue.grid(pady=10, padx=10,  column=4, row=Row)
    ButtonFrame.grid(row=2) #Deze zorgt ervoor dat de buttons in de 2 rij komen te staan

    MainFrame.place(relx=0.5, rely=0.3, anchor=CENTER)
    InfoWindow.mainloop() #Het zorgt ervoor dat het window getoond wordt


def CheckOption():#Haalt de informatie uit het menu en geeft deze aan de Information
    Information(UserChoice.get())


def stoppen(): #Stopt het systeem
    sys.exit()


StartScreen()
