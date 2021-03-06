import urllib3
import csv
import os
import json
import arin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO: Add in reverse lookup

csvfile = open('countries_by_rir.csv', 'r')
readcsv = csv.reader(csvfile, delimiter=',')
rir = {'AFRINIC': [],
        'APNIC': [],
        'ARIN': [],
        'RIPE NCC': [],
        'LACNIC': []
        }
for row in readcsv:
    key = row[3]
    if key in rir:
        rir[key].append(row[0].lower())

def checkIPcountry(ip_addr):
    http = urllib3.PoolManager()
    page = http.request('GET', 'https://geoip-db.com/jsonp/' + ip_addr).data.decode().strip("callback").strip('(').strip(')')
    return json.loads(page)

def main():
    csvfile = open('countries_by_rir.csv', 'r')
    readcsv = csv.reader(csvfile, delimiter=',')
    http = urllib3.PoolManager()
    running = True
    while running:
        print("\nSimple WhoIs Lookup Program")
        print("1) Lookup IP")
        print("2) Resolve FQDN")
        selection = input("Selection> ")
        if selection == "quit":
            running = False
        elif selection == "1":
            print("\nWhat is the IP you want to look up?")
            ip_addr = input("IP> ")
            if ip_addr == "quit":
                running = False
            else:
                country = checkIPcountry(ip_addr)
                country = country['country_name']
                for key,value in rir.items():
                    if country.lower() in value:
                        registry = key

                if registry == "ARIN":
                    page = http.request('GET', 'http://whois.arin.net/rest/ip/' + ip_addr + '.txt')

                    status = page.status
                    data = page.data.decode().split("\n")
                    if status == 200:
                        for line in data:
                            if line == '' or '#' in line:
                                continue
                            else:
                                print(line)
                    moreinformation = True
                    parent = str([s for s in data if "Parent" in s]).split()[2].replace("'", "").replace("]","").strip("(").strip(")")
                    organization = str([s for s in data if "Organization" in s]).split()[3].replace("'", "").replace("]","").strip("(").strip(")")

                    while moreinformation:

                        print("\nWould you like to find more information?")
                        print("1) Parent Information")
                        print("2) Organization Information")
                        selection = input("Selection> ")
                        if selection == "quit":
                            moreinformation = False
                            running = False
                        elif selection == "1":
                            print()
                            page = http.request('GET', 'https://whois.arin.net/rest/net/' + parent + '.txt')
                            status = page.status
                            if status == 200:
                                for line in page.data.decode().split("\n"):
                                    if line == '' or '#' in line:
                                        continue
                                    else:
                                        print(line)
                        elif selection == "2":
                            page = http.request('GET', 'https://whois.arin.net/rest/org/' + organization + '.txt')
                            status = page.status
                            if status == 200:
                                for line in page.data.decode().split("\n"):
                                    if line == '' or '#' in line:
                                        continue
                                    else:
                                        print(line)
                elif register == "AFRINIC":
                    print("test")







if __name__ == "__main__":
    main()
