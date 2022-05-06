# pip3 install lxml
# pip install beautifulsoup4

import os
import re
import tkinter
from tkinter import ttk, filedialog
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen

serial_names = []
current_path = ""


def download_serial_subtitles(name):  # download serial subtitles
    req = Request("http://subtitlestar.com/persian-subtitles-{}/".format(name), headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    links = []
    download_links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    for link in links:
        series_format1 = re.search("(http://dl.subtitlestar.com/dlsub/)(.+)(S\d+)(.zip)", link)
        if series_format1:
            download_links.append(series_format1.group(0))
            request.urlretrieve(series_format1.group(0),
                                series_format1.group(2) + series_format1.group(3) + series_format1.group(4))
            print(series_format1.group(0))


def find_series():  # find series
    all_files = os.listdir()
    for file in all_files:
        series_format1 = re.search("(.+)[._]S\d+E\d+[._]", file)
        if series_format1:
            serial_name = series_format1.group(1).replace('.', '-').replace('_', '-')
            if serial_name not in serial_names:
                serial_names.append(serial_name)
                download_serial_subtitles(serial_name)
    quit()  # close program


def choose_path(label):  # choose_path
    global current_path
    current_path = filedialog.askdirectory()
    os.chdir(current_path)
    label.configure(text="Path : " + current_path)


def start():
    window = tkinter.Tk()
    window.minsize(250, 200)
    window.title('')
    label2 = ttk.Label(window, text="Path : ")
    label2.grid(column=0, row=2)
    button1 = ttk.Button(window, text="Choose Path", command=lambda: choose_path(label2))
    button1.grid(column=0, row=3)
    button2 = ttk.Button(window, text="Submit", command=lambda: find_series())
    button2.grid(column=0, row=4)
    window.mainloop()


start()
