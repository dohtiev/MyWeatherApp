import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tkinter import *
from tkinter import Tk
import sys
import random

headers1 = {
    "Accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 RuxitSynthetic/1.0 v12287870774 t4049208960939529445 athfa3c3975 altpub cvcv=2 smf=0"
}

options = webdriver.ChromeOptions()

options.add_argument(
    f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 RuxitSynthetic/1.0 v12287870774 t4049208960939529445 athfa3c3975 altpub cvcv=2 smf=0")
options.add_argument("--disable-blink-features=AutomationControlled")
caps = DesiredCapabilities().CHROME
options.add_argument('headless')
caps["pageLoadStrategy"] = "eager"  # interactive
driver = webdriver.Chrome(
    desired_capabilities=caps,
    executable_path="D:\\weathe\\chromedriver",
    options=options
)

root = Tk()
root.title("Моя погода")
root.geometry("670x640+100+100")
root.resizable(False, False)
img = PhotoImage(file='background_img.png')
root.iconbitmap('D:\weather\icon.png')
Label(
    root,
    image=img
).place(x=0, y=0)
data = []
alldata = []

def show(alldata):
    for i in range(0, 9):
        if i < 3:
            colnum = i
            Label(text=alldata[i]['nameOfDay'], bg="#BFDCE8", font=("Calibri", 12, "italic")).grid(row=3, column=colnum)
            Label(text=alldata[i]['currentDay'], bg="#BFDCE8", font=('times', 15, 'italic')).grid(row=4, column=colnum)
            Label(text=alldata[i]['weatherInfo'], bg="#BFDCE8", padx=25).grid(row=5, column=colnum)
            Label(text=alldata[i]['minTemp'], bg="#BFDCE8").grid(row=6, column=colnum)
            Label(text=alldata[i]['maxTemp'], bg="#BFDCE8").grid(row=7, column=colnum)
            Button(text="Додаткова інформація", bg="#BFDCE8", command=lambda: more(alldata)).grid(row=8, column=colnum)
            Label(text="", bg="#BFDCE8").grid(row=9, column=colnum)
        elif i >= 3 and i <= 5:
            colnum = i - 3
            Label(text=alldata[i]['nameOfDay'], bg="#BFDCE8", font=("Calibri", 12, "italic")).grid(row=10,
                                                                                                   column=colnum)
            Label(text=alldata[i]['currentDay'], bg="#BFDCE8", font=('times', 15, 'italic')).grid(row=11, column=colnum)
            Label(text=alldata[i]['weatherInfo'], bg="#BFDCE8", padx=25).grid(row=12, column=colnum)
            Label(text=alldata[i]['minTemp'], bg="#BFDCE8").grid(row=13, column=colnum)
            Label(text=alldata[i]['maxTemp'], bg="#BFDCE8").grid(row=14, column=colnum)
            Button(text="Додаткова інформація", bg="#BFDCE8", command=lambda: more(alldata)).grid(row=15, column=colnum)
            Label(text="", bg="#BFDCE8").grid(row=16, column=colnum)
        elif i >= 6 and i <= 8:
            colnum = i - 6
            Label(text=alldata[i]['nameOfDay'], bg="#BFDCE8", font=("Calibri", 12, "italic")).grid(row=17,
                                                                                                   column=colnum)
            Label(text=alldata[i]['currentDay'], bg="#BFDCE8", font=('times', 15, 'italic')).grid(row=18, column=colnum)
            Label(text=alldata[i]['weatherInfo'], bg="#BFDCE8", padx=25).grid(row=19, column=colnum)
            Label(text=alldata[i]['minTemp'], bg="#BFDCE8").grid(row=20, column=colnum)
            Label(text=alldata[i]['maxTemp'], bg="#BFDCE8").grid(row=21, column=colnum)
            Button(text="Додаткова інформація", bg="#BFDCE8", command=lambda: more(alldata)).grid(row=22, column=colnum)

def end():
    sys.exit("Exit")

def more(alldata):
    Label(text="Додаткова інформація:", bg="#BFDCE8", font=("Calibri", 12, "italic")).place(x=0, y=535)
    text = Text(width=77, height=10, wrap=WORD, bg="#BFDCE8")
    text.insert(1.0, alldata[random.randint(0, 8)]['description'])
    text.place(x=0, y=560)

def start(driver):
    cityName = cityNameUI.get()
    url = f'https://ua.sinoptik.ua/погода-{cityName}/10-днів'
    driver.get(url)
    page_content = driver.page_source
    for i in range(1, 10):
        soup = BeautifulSoup(page_content, 'lxml')
        clickable = driver.find_element("id", f'bd{i}')
        clickable.click()
        q = requests.get(url=driver.current_url, headers=headers1)
        result = q.content
        soup = BeautifulSoup(result, 'lxml')
        nameOfDay = soup.find(id=f"bd{i}").find(class_="day-link").text
        month = soup.find(id=f"bd{i}").find(class_="month").text
        date = soup.find(id=f"bd{i}").find(class_="date").text
        currentDay = '%s %s' % (date, month)
        weatherInfo = soup.find(id=f"bd{i}").find("div").get("title")
        minTemp = soup.find(id=f"bd{i}").find("div", class_="min").text
        maxTemp = soup.find(id=f"bd{i}").find("div", class_="max").text
        description = soup.find(class_="description").text
        data.append(nameOfDay)
        data.append(currentDay)
        data.append(weatherInfo)
        data.append(minTemp)
        data.append(maxTemp)
        data.append(description)
        alldata.append({
            "nameOfDay": nameOfDay,
            "currentDay": currentDay,
            "weatherInfo": weatherInfo,
            "minTemp": minTemp,
            "maxTemp": maxTemp,
            "description": description
        })
    show(alldata)
    driver.quit()

cityNameUI = StringVar()
Label(text="Введить назву міста:", bg="#BFDCE8").place(x=10, y=0)
Entry(width=30, textvariable=cityNameUI).place(x=125, y=0)
Button(text="Вихід", command=exit, bg="#BFDCE8").place(x=210, y=22)
Button(text="Пошук", command=lambda: start(driver), bg="#BFDCE8").place(x=258, y=22)
Label(text="", bg="#BFDCE8").grid(row=0, column=0)
Label(text="", bg="#BFDCE8").grid(row=1, column=0)
Label(text="", bg="#BFDCE8").grid(row=2, column=0)
root.mainloop()
