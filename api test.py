import requests
import xmltodict

def gegevens_opvragen(stationsNaam):
    auth_details = ('gerrit.vanos@student.hu.nl', 'BE66_yqU3kQWgKSQJdWPxEHZ8JFji7pM74B9fTCwQo1yZW3clRSQ4w')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station='+stationsNaam
    response = requests.get(api_url, auth=auth_details)
    vertrekDict = xmltodict.parse(response.text)

    vertrekDict = vertrekDict['ActueleVertrekTijden']['VertrekkendeTrein']

    return vertrekDict
def start():
    while True:
        invoer = input('wilt u informatie opvragen(ja/nee): ')
        if invoer == 'ja':
            invoer = input('geef stationsnaam in: ')
            gegevens = gegevens_opvragen(invoer)
            for trein in gegevens:
                print()
                for item in trein:
                    if item == 'VertrekSpoor':
                        print('{:20}:{}'.format(item,trein[item]['#text']))
                    else:
                        print('{:20}:{}'.format(item,trein[item]))
        elif invoer == 'nee':
            continue
        else:
            print('geen geldige waarde')
