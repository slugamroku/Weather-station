from tkinter import *
from tkinter import ttk
from time import *
import threading
import datetime
import w1thermsensor
import Adafruit_DHT

#import psycopg2

class Sensor():
    def __init__(self):
        self.temperature_momentary = 0.0
        self.temperature_momentary_GUI = DoubleVar()
        self.temperature_momentary_GUI.set(0.0)
        self.timestamp = ''
        
    def read(self):
        pass
    
    def start_reading(self):
        self.thread = threading.Thread(target = self.read)
        self.thread.daemon = True
        self.thread.start()
        
class Sensor_DS18B20(Sensor):
    
    def __init__(self):
        super().__init__()
        self.thermosensor = w1thermsensor.W1ThermSensor()
           
    def read(self):
        while True:
            self.temperature_momentary = self.thermosensor.get_temperature()
            self.timestamp = str(datetime.datetime.now())
            self.temperature_momentary_GUI.set(self.temperature_momentary)
            #act_temperature_DS.set(self.temperature_momentary) #TODO: now its fixed connection to GUI element because of lable refreash, needs some kind of interface to GUI
            #print('{0} DS18B20: Temp: {1:0.3f} C'.format(self.timestamp, self.temperature_momentary))
            sleep(5)

class Sensor_DHT11(Sensor):
    pass



'''
        
def readDHT():
    while True:
        humidity_momentary, temperature_momentary = Adafruit_DHT.read_retry(11, 21)
        act_humidity_DHT.set(humidity_momentary)
        act_temperature_DHT.set(temperature_momentary)
        sleep(5)
'''

###########################
##### GUI ROOT WINDOW #####
###########################

windowMain = Tk()
windowMain.minsize(300,200)
windowMain.title('Weather station v0.2')


##################
##### ENGINE #####
##################

sensorDS = Sensor_DS18B20()
sensorDS.start_reading()

######################
##### GUI LAYOUT #####
######################

styleDeafult = ttk.Style()
styleDeafult.configure('reading.TLabel', font = ('Arial', 30))
styleDeafult.configure('title.TLabel', font = ('Arial', 20, 'bold'))
styleDeafult.configure('measurement_title.TLabel', font = ('Arial', 15))

frameDS = ttk.Frame(windowMain, padding = 10, borderwidth = 2, relief = 'sunken')
frameDS.pack(fill= BOTH, expand = 1)

frameDHT = ttk.Frame(windowMain, padding = 10, borderwidth = 2, relief = 'sunken')
frameDHT.pack(fill= BOTH, expand = 1)


frameDHT_title = ttk.Frame(frameDHT, borderwidth = 2)
frameDHT_title.grid(row = 0, column = 0, columnspan = 11)

frameDHT_temperature = ttk.Frame(frameDHT, padding = 10, borderwidth = 2)
frameDHT_temperature.grid(row = 10, column = 0)

frameDHT_humidity = ttk.Frame(frameDHT, padding = 10, borderwidth = 2)
frameDHT_humidity.grid(row = 10, column = 10)

###### DS18B20 ######

ttk.Label(frameDS, text = 'DS18B20', style = 'title.TLabel').pack()
ttk.Label(frameDS, text = 'Temperature', style = 'measurement_title.TLabel').pack()
ttk.Label(frameDS, textvariable = sensorDS.temperature_momentary_GUI, style = 'reading.TLabel').pack()

###### DHT11 ######

act_temperature_DHT = DoubleVar()
act_temperature_DHT.set(0.0)

act_humidity_DHT = DoubleVar()
act_humidity_DHT.set(0.0)

ttk.Label(frameDHT_title, text = 'DHT11', style = 'title.TLabel').pack()

ttk.Label(frameDHT_temperature, text = 'Temperature', style = 'measurement_title.TLabel').grid(row = 0, column = 0, columnspan = 11)

ttk.Label(frameDHT_temperature, textvariable = act_temperature_DHT, style = 'reading.TLabel').grid(row = 10, column = 0)
ttk.Label(frameDHT_temperature, text = '[˚C]', style = 'reading.TLabel').grid(row = 10, column = 10)

ttk.Label(frameDHT_humidity, text = 'Humidity', style = 'measurement_title.TLabel').grid(row = 0, column = 0, columnspan = 11)

ttk.Label(frameDHT_humidity, textvariable = act_humidity_DHT, style = 'reading.TLabel').grid(row = 10, column = 0)
ttk.Label(frameDHT_humidity, text = '[%]', style = 'reading.TLabel').grid(row = 10, column = 10)

'''
##### START DS18B20 READING THREAD #####

threadDHT = threading.Thread(target = readDHT)
threadDHT.daemon = True
threadDHT.start()
'''


####################
##### GUI LOOP #####
####################
windowMain.mainloop()