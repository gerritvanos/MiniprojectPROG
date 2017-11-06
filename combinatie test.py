import requests
import xmltodict
from tkinter import *
stations = ['Hilversum','Kampen', 'Culemborg']
def gegevens_opvragen(stationsNaam):
    auth_details = ('gerrit.vanos@student.hu.nl', 'BE66_yqU3kQWgKSQJdWPxEHZ8JFji7pM74B9fTCwQo1yZW3clRSQ4w')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station='+stationsNaam
    response = requests.get(api_url, auth=auth_details)
    vertrekDict = xmltodict.parse(response.text)

    vertrekDict = vertrekDict['ActueleVertrekTijden']['VertrekkendeTrein']

    return vertrekDict

def info(station):
    gegevens = gegevens_opvragen(station)
    rij = 2
    kolom = 0
    info = Tk()
    titel = Label(master=info, text='De actuele vertrektijden van station '+station+' is', font=('Helvetica', 16, 'bold italic'))
    titel.place(anchor=CENTER,relx=0.5, rely=0.5,)

    Label(master=info, text='RitNummer').grid(row=1,column=0,ipadx=10,ipady=10,)
    Label(master=info, text='VertrekTijd').grid(row=1, column=1, ipadx=10, ipady=10,)
    Label(master=info, text='EindBestemming').grid(row=1, column=2, ipadx=10, ipady=10,)
    Label(master=info, text='TreinSoort').grid(row=1, column=3, ipadx=10, ipady=10,)
    Label(master=info, text='Vervoerder').grid(row=1, column=4, ipadx=10, ipady=10,)
    Label(master=info, text='VertrekSpoor').grid(row=1, column=5, ipadx=10, ipady=10,)
    Label(master=info, text='Opmerkingen').grid(row=1, column=6, ipadx=10, ipady=10,)
    Label(master=info, text='RouteTips').grid(row=1, column=7, ipadx=10, ipady=10,)
    Label(master=info, text='RouteTekst').grid(row=1, column=8, ipadx=10, ipady=10,)
    for trein in gegevens:
        kolom =0
        for key in trein:
            if key == 'RitNummer':
                kolom =0
            elif key =='VertrekTijd':
                kolom = 1
            elif key == 'EindBestemming':
                kolom =2
            elif key == 'TreinSoort':
                kolom =3
            elif key == 'Vervoerder':
                kolom =4
            elif key == 'VertrekSpoor':
                kolom = 5
            elif key == 'Opmerkingen':
                kolom =6
            elif key == 'ReisTip':
                kolom =7
            elif key == 'RouteTekst':
                kolom=8
            elif key == 'VertrekVertraging' or key == 'VertrekVertragingTekst':
                continue
            if kolom ==5:
                Label(master=info, text='{}'.format(trein[key]['#text'])).grid(row=rij, column=kolom, ipadx=10, ipady=10)
            else:
                Label(master=info, text='{}'.format(trein[key])).grid(row=rij,column=kolom,ipadx=10,ipady=10)
        rij +=1
    info.mainloop()


def controleer():
    info(variable.get())



root = Tk()

gadoor = Button(master=root, text='ga door', command=controleer)
gadoor.pack(pady=10)


variable = StringVar(root)
variable.set(stations[0]) # default value
dropdown = OptionMenu(root, variable, *stations)
dropdown.pack()




root.mainloop()
