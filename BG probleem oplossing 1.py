#Onderstaande modules zijn nodig voor verschillende onderdelen van de code
import requests         #Deze module wordt gebruikt voor het opvragen van de API
import xmltodict        #Deze module wordt gebtuikt voor het omzetten van de gegevens naar een dict
import sys
from tkinter import *

stations = ['Hilversum','Kampen', 'Culemborg', 'Utrecht Lunetten', 'Driebergen-Zeist', 'Utrecht Centraal']
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
    infoWindow.option_add('*Label.Background', '#fed339')
    infoWindow.option_add('*Label.Ipady',10)
    infoWindow.option_add('*Label.Font',('Frutiger Bold Regular',12,'bold'))
    titel = Label(master=infoWindow, text='De actuele vertrektijden van station '+station+' is', font=('Frutiger Bold Regular',16,'bold'), bg='#000066', fg='white')
    titel.grid(row=0, columnspan=7)

    Label(master=infoWindow, text='EindBestemming').grid(row=1, column=0, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Vertrekspoor').grid(row=1, column=1, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Vertrektijd').grid(row=1, column=2, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Vertraging').grid(row=1, column=3, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Treinsoort').grid(row=1, column=4, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Vervoerder').grid(row=1, column=5, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Routetekst').grid(row=1, column=6, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Routetips').grid(row=1, column=7, ipadx=10, ipady=10, )
    Label(master=infoWindow, text='Opmerkingen').grid(row=1, column=8, ipadx=10, ipady=10, )

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
                Label(master=infoWindow, text='{}'.format(trein[key]['#text'])).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            elif kolom == 2:
                tijd = str(trein[key])
                tijd = tijd[11:16]
                Label(master=infoWindow, text='{}'.format(tijd)).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            else:
                Label(master=infoWindow, text='{}'.format(trein[key])).grid(row=rij, column=kolom, ipadx=10, ipady=10)
        rij += 1
        count +=1

    gaterug = Button(master=infoWindow, text='ga terug', command=stoppen, bg='#000066', fg='white', font=('Frutiger Bold Regular', 40, 'bold'))
    gaterug.grid(pady=10, padx=10,column=3,  row=rij)
    gadoor = Button(master=infoWindow, text='ga door', command=choice, bg='#000066', fg='white', font=('Frutiger Bold Regular', 40, 'bold'))
    gadoor.grid(pady=10, padx=10,  column=4, row=rij)
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


root = Tk()
root['bg']='#fed339'

gadoor = Button(master=root, text='ga door', command=choice, bg='#000066',fg='white', font=('Frutiger Bold Regular',40,'bold'))
gadoor.grid(pady=10)
gaterug = Button(master=root, text='ga terug', command=stoppen, bg='#000066',fg='white', font=('Frutiger Bold Regular',40,'bold'))
gaterug.grid(pady=10)

root.mainloop()