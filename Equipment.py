import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa
import numpy as np # http://www.numpy.org/
from ftplib import FTP # std ftp client
from vncdotool import api # vnc client tool
import usb.core
import libusb1

class WFG:
    def __init__(self, channel, state, idVendor=0x5345, idProduct=0x1234):
        self.channel = str(channel)
        self.state = state
        
        dev = usb.core.find(idVendor,idProduct,libusb1.get_backend()) # 
        
        if dev is None:
            raise ValueError('Device is not found')
        #print(type(back))    
        #self.dev.set_configuration()    
        print(dev)
        
        cmd_str= f"OUTPut{self.channel}:STATe {self.state}"
        print(self.send(cmd_str))

    def SHAPE(self, shape): # "[SINusoid|SQUare|RAMP]"
        self.shape = shape
        print(self.send(f"SOURce{self.channel}:FUNCtion:SHAPe {self.shape}"))

    def FREQUENCY(self, frequency): # "100[Hz/kHz/MHz]"
        self.frequency = frequency
        print(self.send(f"SOURce{self.channel}:FREQuency:FIXed {self.frequency}"))

    def AMPLITUDE(self, amplitude): # "1[Vpp/mVpp]"
        self.amplitude = amplitude
        print(self.send(f"SOURce{self.channel}:VOLTage:LEVel:IMMediate:AMPLitude {self.amplitude}"))

    def OFFSET(self, offset): # "1[Vpp/mVpp]"
        self.offset = offset
        print(self.send(f"SOURce{self.channel}:VOLTage:LEVel:IMMediate:OFFSet {self.offset}"))
    
    def send(self, cmd):
        # address taken from results of print(dev):   ENDPOINT 0x3: Bulk OUT
        dev.write(3,cmd+'\r')
        # address taken from results of print(dev):   ENDPOINT 0x81: Bulk IN
        try:
            result = (dev.read(0x81,10000,1000)).tobytes().decode('utf-8')[:-4]
            
        except usb.USBError:
            result="OK"
            
        return result


class TDS5000Scope:
    def __init__(self, ip):
        self.ip=ip
        visa_address = f'TCPIP0::{self.ip}::inst0::INSTR'
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(visa_address)
        self.scope.timeout = 10000 # ms
        self.scope.encoding = 'latin_1'
        self.scope.read_termination = '\n'
        self.scope.write_termination = None
        self.scope.write('*cls') # clear ESR
        self.scope.write('*rst') # reset
        t1 = time.perf_counter()
        r = self.scope.query('*opc?') # sync
        t2 = time.perf_counter()
        print('reset time: {} s'.format(t2 - t1))
        
        
    def format_e(self, n):
        a = '%E' % n
        return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]    
        
    def set_time_scale(self,time_scale):
        self.scope.write("HORizontal:MAIn:SCAle "+ self.format_e(time_scale))
    
    def set_sampling_rate(self,sampling_rate):
        self.scope.write("HORizontal:MAIn:SAMPLERate "+self.format_e(sampling_rate))
    
    def set_voltage_scale(self,CHX,voltage_scale):
        self.scope.write(f"CH{CHX}:SCAle " + self.format_e(voltage_scale))
        
    def set_offset(self,CHX,voltage_scale):
        self.scope.write(f"CH{CHX}:OFFSet " + self.format_e(offset))
    
    def set_trigger(self, CHX, coupling="DC", slope="RASE", level=0):
        self.scope.write(f"TRIGger:A:EDGE:SOUrce CH{CHX}")
        self.scope.write(f"TRIGger:A:EDGE:COUPling {coupling}")
        self.scope.write(f"TRIGger:A:EDGE:SLOpe {slope}")
        self.scope.write(f"TRIGger:A:LEVEL {level}")
    
    def set_record_length(self, num_samples):
        self.scope.write(f"HORizontal:RECOrdlength {num_samples}")
        
    
    def save_data(self, filename="hui-wragam-cubani"): # 'C:/Synthetic-dim-project/'
        client = api.connect(self.ip, password="sim")
        key="ctrl-e"
        client.keyPress(key)
        for char in filename:
            client.keyPress(char)
        time.sleep(1)    
        client.keyPress("enter")
        client.keyPress("enter")
        client.disconnect()
        

    
    def download_data(self,file_name):
        with FTP(self.ip,'anonymous','anonymous@') as ftp:
            with open(file_name, 'wb') as local_file:
                ftp.retrbinary(f'RETR {file_name}', local_file.write)
        
           
    def __del__(self):
        self.scope.close()
        self.rm.close()
        print('Destructor called, scope object deleted.')    


# Test example is in the comment below
'''
import time
import numpy as np

Ch2 = WFG(2, "ON")
Ch2.SHAPE("RAMP")
Ch2.AMPLITUDE("0.5Vpp")
for i in np.arange(1,10,1):
    Ch2.FREQUENCY(f"{2*i}kHz")
    time.sleep(5)

file_name ="saved-file-name"  
ts = 200*10**-9 # 200 ns time division
sl = 10**5 # number of samples
CHX = 1 # channel to select
vs = 1 # 1 Volt vertical, scale
    
scope = TDS5000Scope(ip="192.168.0.35")
scope.set_record_length(sl) # It is important to keep the order, i.e. Setting record length first and time scale after
scope.set_time_scale(ts)
scope.set_voltage_scale(CHX,vs)
scope.save_data(filename=file_name)
time.sleep(0.1)
scope.download_data(file_name=file_name+".csv")
del scope
'''