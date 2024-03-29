import threading
import time
import sys
import serial
import csv
import urllib.request
from  bs4 import BeautifulSoup
from datetime import datetime


class bluetooth:
    def __init__(self, port: str, baudrate: int=9600):
        """ Initialize an BT object, and auto-connect it. """
        # The port name is the name shown in control panel
        # And the baudrate is the communication setting, default value of HC-05 is 9600.
        self.ser = serial.Serial(port, baudrate=baudrate)
        
    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting

    def do_connect(self, port: str, baudrate: int=9600) -> bool:
        """ Connect to the specify port with particular baudrate """
        # Connection function. Disconnect the previous communication, specify a new one.
        self.disconnect()

        try:
            self.ser = serial.Serial(port, baudrate=baudrate)
            return True
        except:
            return False

    def disconnect(self):
        """ Close the connection. """
        self.ser.close()

    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        send = output.encode("utf-8")
        self.ser.write(send)

    def readString(self) -> str:
        # Scan the input buffer until meet a '\n'. return none if doesn't exist.
        if(self.waiting()):
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]

        return receiveMsg

def read():
    while True:
        if bt.waiting():
            print(bt.readString())

def write():
    while True:
        msgWrite = input()
        
        if msgWrite == "exit": sys.exit()
    
        bt.write(msgWrite + "\n")

if __name__ == "__main__":
    # Need to modify the port name.
    bt = bluetooth("COM5")
    while not bt.is_open(): pass
    print("BT Connected!")

    readThread = threading.Thread(target=read)
    readThread.setDaemon(True)
    readThread.start()

url = "http://www.weather.com.cn/weather/101340101.shtml"
header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")  # 設置頭部信息
opener = urllib.request.build_opener()  
opener.addheaders = [header]         
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
html = response.read()  
html = html.decode('utf-8') 


final = []   
bs = BeautifulSoup(html,"html.parser")  
body = bs.body 
data = body.find('div',{'id':'7d'})
ul = data.find('ul') 
li = ul.find_all('li')

i = 0
for day in li:
    if i < 7:
        temp = []
        date = day.find('h1').string
        temp.append(date) 
        inf = day.find_all('p')

        temp.append(inf[0].string) 
        if inf[1].find('span') is None:
            temperature_highest = None
        else:
            temperature_highest = inf[1].find('span').string 
            temperature_highest = temperature_highest.replace('℃', '')
        temperature_lowest = inf[1].find('i').string 
        temperature_lowest = temperature_lowest.replace('℃', '')
        temp.append(temperature_highest)
        temp.append(temperature_lowest)
        final.append(temp)
        i = i +1
        
weather = [final[1][1],final[1][2],final[1][3]]

## 以下只能顯示天氣(且天氣型態僅略舉主要數個) (此處並非重點，故並沒有多加著墨，所有天氣型態詳見https://www.cwb.gov.tw/V8/C/K/Weather_Icon.html)
while True:
    d = datetime.now().strftime('%H')
    # print(d)  
    # if msgWrite == "exit": sys.exit()
    if d>=8:
        if(str(final[1][1]) == "多云"):
            print("cloudy")
            bt.write("c")
        if(str(final[1][1]) == "晴天"):
            bt.write("s")
        if(str(final[1][1]) == "雨天"):
            bt.write("r")
    time.sleep(10)