from bs4 import BeautifulSoup
import requests
import re
import io

base_url = "https://www.diainternacionalde.com/mes/"

months = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12"
}

#Open file in append mode
f = open("data.csv", "a")

with io.open("data.csv", "w", encoding="utf-8") as f:
    #Loop through months
    for month in months:
        url = base_url + month
        #Get the soup from the url
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        #The list of events is in a section with the id "dias-internacionales-list"
        eventsList = soup.find("section", {"id": "dias-internacionales-list"})
        #Each event is in a article with the class "dia"
        events = eventsList.find_all("article", {"class": "dia"})
        #Loop through the events
        for event in events:
            #The date is in a span like this: <span>1 de enero - </span>
            date = event.find("span")
            #The date need to remove the last 3 characters " - "
            date = date.text[:-3]
            #The date needs to replace " de " with "/"
            date = date.replace(" de ", "/")
            #The date needs to change the month to a number
            date = date.replace(month, months[month])
            #The name of the event is in a h3 tag or an a tag inside a h3 tag
            name = event.find("h3")
            if name.find("a"):
                name = name.find("a")
            #Save the date and the name of the event in the file
            f.write(f'{date};{name.text}\r\n')



