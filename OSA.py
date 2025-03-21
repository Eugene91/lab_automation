#To use the class, enter Optscan=OSA.AQ6317B("192.168.1.103",1234); 192.168.1.105 = HOST (IP Address) , 1234 Port number

#Optscan.send_GPIB_cmd('SGL\r\n',rcv=False) ; rcv = receive data
import time
import socket
import pandas as pd
from matplotlib import pyplot as plt

class AQ6317B:
    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT

    def send_GPIB_cmd(self, str, rcv=False):
        self.soc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.HOST, self.PORT))
        self.soc.send(str.encode('ascii'))
        measurement_return=0.0
        if rcv:
            data = self.soc.recv(1024)
            print(float(data[0:8]))
            measurement_return=float(data[0:8])
        time.sleep(1)
        self.soc.close()
        return measurement_return

    def send_GPIB_large_cmd(self, str, rcv=False):
        self.soc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.HOST, self.PORT))
        self.soc.send(str.encode('ascii'))
        measurement_return=0.0
        if rcv:
            data = self.soc.recv(65536)
            measurement_return=data
        time.sleep(1)
        self.soc.close()
        return measurement_return
    
    def send_GPIB_cmd_ref(self, str, rcv=False):
        self.soc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.HOST, self.PORT))
        self.soc.send(str.encode('ascii'))
        if rcv:
            data = self.soc.recv(1024)
            print(float(data[0:8]))
            print(data)
        time.sleep(1)
        self.soc.close()     

    
    def repeat_sweep_analysis(self,nb_sweeps=10):
        #set a timer from one sweep to the next
        self.send_GPIB_cmd(f'SWPI{nb_sweeps}\r\n',rcv=False)
        self.send_GPIB_cmd('RPT\r\n',rcv=False)
        print("scan in progress")
        time.sleep(10)
        print("scan done")
        result = self.send_GPIB_cmd('ANA?\r\n',rcv=True)
        return result
        
    def sample_sweep_analysis(self):
        self.send_GPIB_cmd('SMEAS\r\n',rcv=False)
        print("scan in progress")
        time.sleep(20)
        print("scan done")
        result = self.send_GPIB_cmd('ANA?\r\n',rcv=True)
        return result
    
    def single_sweep_analysis(self):
        self.send_GPIB_cmd('SGL\r\n',rcv=False)
        print("scan in progress")
        time.sleep(10)
        print("scan done")
        result = self.send_GPIB_cmd('ANA?\r\n',rcv=True)
        return result

    def set_sampling_count(self, sample_count):
        if sample_count >= 0 and sample_count <= 20001:
            self.send_GPIB_cmd(f'SEGP{sample_count}\r\n',rcv=False)
        elif  sample_count>20001:
            print("Sample size too high, needs to be <= 20001")
        
        else :
            print("Invalid input, input non int an or negative number")
    
    def analyze(self):
        result = self.send_GPIB_cmd('ANA?\r\n',rcv=True)
        return result
    
    def sample_count_sweep_analysis(self):
        self.send_GPIB_cmd('SMEAS\r\n',rcv=False)
        print("scan in progress")
        time.sleep(10)
        print("scan done")
        result = self.send_GPIB_cmd('ANA?\r\n',rcv=True)
        return result
    
    def stop_sweep(self):
        self.send_GPIB_cmd('STP\r\n',rcv=False)
    
    # #1 = on , 0 = off
    # def set_marker_to_marker_sweep(self,nb):
    #     self.send_GPIB_cmd(f'SWPM{nb}\r\n',rcv=False)

    #format of the wavelength -> 2nd decimal
    def set_center_wavelength(self,nb):
        if 600.00 <= nb and  nb <= 1750.00 :
            self.send_GPIB_cmd(f'CTRWL{nb}\r\n',rcv=False)
        else:
            print("invalid input, needs to be a float between 600.00 and 1750.00")
        
    #format of the frequency -> 2nd decimal (units : THz)
    def set_center_frequency(self,nb):
        if 171.500 <= nb and nb <= 499.500 :
            self.send_GPIB_cmd(f'CTRF{nb}\r\n',rcv=False)
        else :
            print("invalid input, needs to be a float between 171.500 and 499.500")
    
    #format of the wavelength -> 2nd decimal
    def set_measurement_end_wavelength(self,nb):
        if 600.00 <= nb and  nb <= 2350.00 :
            self.send_GPIB_cmd(f'CTRWL{nb}\r\n',rcv=False)
        else:
            print("invalid input, needs to be a float between 600.00 and 2350.00")

    def waveform_peak_to_center(self):
        self.send_GPIB_cmd('CTR=P\r\n',rcv=False)

    # #1 = on , 0 = off
    # def each_sweep_peak_center(self,nb):
    #     if 0 <= int(nb) and int(nb) <= 1 :
    #         self.send_GPIB_cmd(f'ATCTR{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be either 0 for deactivation or 1 for activation")
    
    # #starts from 0 to the assigned size in nm
    # def set_wavelength_span(self,nb):
    #     if 0.5 <= nb and nb <= 1200.0 :
    #         self.send_GPIB_cmd(f'SPAN{nb}\r\n',rcv=False)
    #     else:
    #         print("invalid input, needs to be a float between 0.5 and 1200.0")
    
    # #starts from 0 to the assigned size in THz
    # def set_wavelength_span_in_hz(self,nb):
    #     if 0.100 <= nb and nb <= 350.000 :
    #         self.send_GPIB_cmd(f'SPANF{nb}\r\n',rcv=False)
    #     else:
    #         print("invalid input, needs to be a float between 0.100 and 350.000")
            
    # def set_span_to_spectral_width(self):
    #     self.send_GPIB_cmd('SPN=W\r\n',rcv=False)
        
    # def set_peak_to_ref_level(self):
    #     self.send_GPIB_cmd('REF=P\r\n',rcv=False)

    # def each_sweep_peak_to_ref(self,nb):
    #     if 0<=int(nb) and int(nb) <=1 :
    #         self.send_GPIB_cmd(f'ATREF{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be either 0 for deactivation or 1 for activation")
            
    # def auto_scaling_display(self,nb):
    #     if 0<= int(nb) <=1 :
    #         self.send_GPIB_cmd(f'ATSCL{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be either 0 for deactivation or 1 for activation")
        
    # def set_resolution(self,nb):
    #     if 0.01<=nb and nb <=2.0 :
    #         self.send_GPIB_cmd(f'ATSCL{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be either 0 for deactivation or 1 for activation")

    # def set_resolution_wavelength(self,nb):
    #     if 0.01<=nb and nb <=2.0 :
    #         self.send_GPIB_cmd(f'RESLN{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be a float between 0.01 and 2.0")
    
    # def set_resolution_frequency(self,nb):
    #     if nb==2 or nb==4 or nb==10 or nb==20 or nb==40 or nb==100 or nb==200 or nb==400:
    #         self.send_GPIB_cmd(f'RESLNF{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be equal to either 2,4,10,20,40,100,200 or 400")
            
    # def set_average_times(self,nb):
    #     if 1<=nb and nb <=1000 :
    #         self.send_GPIB_cmd(f'AVG{nb}\r\n',rcv=False)
    #     else : 
    #         print("invalid input, needs to be an int between 1 and 1000 (1 step)")
            
    #def full_spectrum(self,channel,min,max):
    def full_spectrum(self,export_default=False,export_file_name=None):
        full_wavelength=[]
        full_dBm=[]
        for n in range(9) :       
            min=(n*50)+1
            max=((n+1)*50)
            
            # Fetch byte data from GPIB device
            wavelength_bytes = bytearray(self.send_GPIB_large_cmd(f'WDATA R{min}-R{max}\r\n', rcv=True))
            #print(wavelength_bytes)
            wavelength_bytes = wavelength_bytes[6:]
            #print(wavelength_bytes)
            dBm_bytes = bytearray(self.send_GPIB_large_cmd(f'LDATA R{min}-R{max}\r\n', rcv=True))
            dBm_bytes = dBm_bytes[6:]
            # Convert byte data to string
            wavelength_str = wavelength_bytes.decode('utf-8')
            dBm_str = dBm_bytes.decode('utf-8')
        
            # Split the string by commas (assuming data is comma-separated)
            wavelength_parts = wavelength_str.split(',')
            dBm_parts = dBm_str.split(',')
        
            # Convert parts to integers (assuming they represent numerical values)
            for part in wavelength_parts:
                try:
                    full_wavelength.append(float(part))
                except:
                    pass
            
            for part in dBm_parts:
                try:
                    full_dBm.append(float(part))
                except:
                    pass
        #Export data in a default named file:
        if export_default==True:
            data_to_exp=pd.DataFrame(zip(full_wavelength,full_dBm),columns=['Wavelength(nm)','full_dBm'])
            data_to_exp.to_csv('OSA_Scan.csv',sep=',')

        if export_file_name is not None :
            data_to_exp=pd.DataFrame(zip(full_wavelength,full_dBm),columns=['Wavelength(nm)','full_dBm'])
            data_to_exp.to_csv(f'{export_file_name}.csv', sep=',')
        
        plt.plot(full_wavelength,full_dBm)
        plt.xlabel('Wavelength(nm)')
        plt.ylabel('dBm')
        plt.ylim((-80,0))
        plt.show()
        #return full_wavelength,full_dBm