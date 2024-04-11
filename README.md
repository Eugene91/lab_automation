# lab_automation
Scripts for automatic different lab equipment.
Equipment.py constatins classes for controlling
1. Tektronix TDS5000 via LAN/SCPI connection using pyvisa library. 
Due to the bag in firmware there is no way to get more than 5000 samples in a single SCPI readout.
The issue is solved by automatic saving the data with VNC and transfering file to a computer via FTP.
2. OWON arbitary waveform generator XDG3000 via USB/SCPI connection.  

REQUIREMENTS:
- pyvisa
- libusb1
- vncdotool
