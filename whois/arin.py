def arin(ip_addr):
    import urllib3
    import csv
    import os
    import json

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
    print(parent)

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
