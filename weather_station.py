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
        self.timestamp = ''
        
    def read(self):
        pass
    
    def start_reading(self):
        self.thread = threading.Thread(target = self.read)
        self.thread.daemon = True
        self.thread.start()
        
class Sensor_temperature(Sensor):
    def __init__(self):
        super().__init__()
        self.temperature_momentary = 0.0
        self.temperature_momentary_GUI = DoubleVar()
        self.temperature_momentary_GUI.set(0.0)
        
class Sensor_humidity(Sensor):
    def __init__(self):
        super().__init__()
        self.humidity_momentary = 0.0
        self.humidity_momentary_GUI = DoubleVar()
        self.humidity_momentary_GUI.set(0.0)
        
class Sensor_pressure(Sensor):
    def __init__(self):
        super().__init__()
        self.pressure_momentary = 0.0
        self.pressure_momentary_GUI = DoubleVar()
        self.pressure_momentary_GUI.set(0.0)         
        
class Sensor_DS18B20(Sensor_temperature):    
    def __init__(self):
        super().__init__()
        self.thermosensor = w1thermsensor.W1ThermSensor()
           
    def read(self):
        while True:
            self.temperature_momentary = self.thermosensor.get_temperature()
            self.timestamp = str(datetime.datetime.now())
            self.temperature_momentary_GUI.set(self.temperature_momentary)
            print('{0} DS18B20: Temp: {1:0.3f} C'.format(self.timestamp, self.temperature_momentary))
            sleep(5)

class Sensor_DHT11(Sensor_temperature, Sensor_humidity):
    def __init__(self, gpio):
        super().__init__()
        self.gpio = gpio
            
    def read(self):
        while True:
            self.humidity_momentary, self.temperature_momentary = Adafruit_DHT.read_retry(11, self.gpio)
            self.timestamp = str(datetime.datetime.now())
            self.humidity_momentary_GUI.set(self.humidity_momentary)
            self.temperature_momentary_GUI.set(self.temperature_momentary)
            print('{0} DHT11:   Temp: {1:0.1f} C | Hum: {2:0.1f} %'.format(self.timestamp, self.temperature_momentary, self.humidity_momentary))
            sleep(5)
            
class Sensor_BME280(Sensor_temperature, Sensor_humidity, Sensor_pressure):
    def read(self):
        while True:
            self.timestamp = str(datetime.datetime.now())
            print('{0} BME280:  Temp: {1:0.3f} C | Hum: {2:0.3f} % | Press: {3:0.3f}'.format(self.timestamp, self.temperature_momentary, self.humidity_momentary, self.pressure_momentary))
            sleep(5)
            


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

sensorDHT = Sensor_DHT11(21)
sensorDHT.start_reading()

sensorBME = Sensor_BME280()
sensorBME.start_reading()

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

ttk.Label(frameDHT_temperature, textvariable = sensorDHT.temperature_momentary_GUI, style = 'reading.TLabel').grid(row = 10, column = 0)
ttk.Label(frameDHT_temperature, text = '[˚C]', style = 'reading.TLabel').grid(row = 10, column = 10)

ttk.Label(frameDHT_humidity, text = 'Humidity', style = 'measurement_title.TLabel').grid(row = 0, column = 0, columnspan = 11)

ttk.Label(frameDHT_humidity, textvariable = sensorDHT.humidity_momentary_GUI, style = 'reading.TLabel').grid(row = 10, column = 0)
ttk.Label(frameDHT_humidity, text = '[%]', style = 'reading.TLabel').grid(row = 10, column = 10)

####################
##### GUI LOOP #####
####################
windowMain.mainloop()