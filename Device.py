"""
File name Device.py:
Project Name: D75 CAT Control
Author: Ben Kozlowski - K7DMG
Created: 2024-10-22
Version: 1.0.0
Description: 
    CAT Control Software for the Kenwood D75/D75

License: 
    This file is part of D75 CAT Control.

    D75 CAT Control is free software: you can redistribute it and/or modify it under the terms of the GNU General
    Public License as published by the Free Software Foundation, either version 3 of the License, or (at
    your option) any later version.

    D75 CAT Control is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
    implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
    License for more details.

    You should have received a copy of the GNU General Public License along with D75 CAT Control. If not, see <https://www.gnu.org/licenses/>.
Contact: k7dmg@protonmail.com
Dependencies: PySide6
"""
from time import sleep
from PySide6.QtCore import Signal, QObject, QIODevice, QTimer
from PySide6.QtSerialPort import QSerialPort
from Constants import Constants
from GPSData import GPSData

# ---------- CATCommand Class ---------- #
class CATCommand():
    SerialNumber    = "AE"
    AFGain          = "AG"
    RealTimeFB      = "AI"
    BandControl     = "BC"
    Beacon          = "BE"
    BatteryLevel    = "BL"
    Bluetooth       = "BT"
    SquelchOpen     = "BY"
    DualSingleBand  = "DL"
    BtnDown         = "DW"
    FrequencyInfo   = "FO"
    Frequency       = "FQ"
    FWVersion       = "FV"
    GPS             = "GP"
    ModelID         = "ID"
    Backlight       = "LC"
    BandMode        = "MD"
    MemChannelFreq  = "ME"
    MemChannel      = "MR"
    OutputPower     = "PC"
    BeaconType      = "PT"
    RX              = "RX"
    S_Meter         = "SM"
    Squelch         = "SQ"
    TNC             = "TN"
    TX              = "TX"
    BtnUp           = "UP"
    MemoryMode      = "VM"
# ---------- CATCommand Class ---------- #

# ---------- ChannelFrequency Class ---------- #
class ChannelFrequency():
    band                = 0
    frequency           = ""
    offset              = ""
    step                = ""
    tx_step             = ""
    mode                = ""
    fine_mode           = ""
    fine_step_size      = ""
    tone_status         = ""
    ctcss_status        = ""
    dcs_status          = ""
    ctcss_dcs_status    = ""
    reversed            = ""
    shift_direction     = ""
    tone_freq           = ""
    ctcss_freq          = ""
    dcs_freq            = ""
    cross_encode        = ""
    urcall              = ""
    dstar_sq_type       = ""
    dstar_sq_code       = ""

    def __init__(self, data):
        self.band               = int(data[0])
        self.frequency          = str(int(data[1][:4])) + '.' + data[1][4:7]
        self.offset             = str(int(data[2][:4])) + '.' + data[2][4:7]
        self.step               = data[3]
        self.tx_step            = data[4]
        self.mode               = data[5]
        self.fine_mode          = data[6]
        self.fine_step_size     = data[7]
        self.tone_status        = data[8] == '1'
        self.ctcss_status       = data[9] == '1'
        self.dcs_status         = data[10] == '1'
        self.ctcss_dcs_status   = data[11] == '1'
        self.reversed           = data[12]
        self.shift_direction    = data[13]
        self.tone_freq          = int(data[14])
        self.ctcss_freq         = int(data[15])
        self.dcs_freq           = int(data[16])
        try:
            self.cross_encode   = int(data[17])
        except:
            self.cross_encode   = 0

        self.urcall             = data[18]
        if data[17] != 'D':
            self.dstar_sq_type      = data[19]
            self.dstar_sq_code      = data[20]

    def getToneType(self) -> int:
        if not (self.tone_status or self.ctcss_status or self.dcs_status or self.ctcss_dcs_status):
            return 0
        elif self.tone_status:
            return 1
        elif self.ctcss_status:
            return 2
        elif self.dcs_status:
            return 3
        elif self.ctcss_dcs_status:
            return 4

        return 0
    
    def setToneType(self, type: int):
        if type == 0:
            self.tone_status = False
            self.ctcss_status = False
            self.dcs_status = False
            self.ctcss_dcs_status = False
        elif type == 1:
            self.tone_status = True
            self.ctcss_status = False
            self.dcs_status = False
            self.ctcss_dcs_status = False
        elif type == 2:
            self.tone_status = False
            self.ctcss_status = True
            self.dcs_status = True
            self.ctcss_dcs_status = False
        elif type == 3:
            self.tone_status = False
            self.ctcss_status = False
            self.dcs_status = True
            self.ctcss_dcs_status = False
        elif type == 4:
            self.tone_status = False
            self.ctcss_status = False
            self.dcs_status = False
            self.ctcss_dcs_status = True


    def toRadio(self):
        data                    = [''] * 21
        data[0]                 = str(self.band)
        data[1]                 = self.frequency.split('.')[0].rjust(4, '0') + self.frequency.split('.')[1].ljust(6, '0')
        data[2]                 = self.offset.split('.')[0].rjust(4, '0') + self.offset.split('.')[1].ljust(6, '0')
        data[3]                 = self.step         
        data[4]                 = self.tx_step
        data[5]                 = self.mode
        data[6]                 = self.fine_mode
        data[7]                 = self.fine_step_size
        data[8]                 = '1' if self.tone_status else '0'
        data[9]                 = '1' if self.ctcss_status else '0'
        data[10]                = '1' if self.dcs_status else '0'
        data[11]                = '1' if self.ctcss_dcs_status else '0'
        data[12]                = self.reversed
        data[13]                = self.shift_direction
        data[14]                = str(self.tone_freq).rjust(2, '0')
        data[15]                = str(self.ctcss_freq).rjust(2, '0')
        data[16]                = str(self.dcs_freq).rjust(3, '0')
        data[17]                = str(self.cross_encode)
        data[18]                = self.urcall         
        data[19]                = self.dstar_sq_type
        data[20]                = self.dstar_sq_code

        return ','.join(data)

    def toString(self):
        s = "Band: " + str(self.band) + '\n'
        s+= "Freq: " + self.frequency + '\n'
        s+= "Offset: " + self.offset + '\n'
        s+= "Step: " + self.step + '\n'
        s+= "TX Step: " + self.tx_step + '\n'
        s+= "Mode: " + self.mode + '\n'
        s+= "Fine Mode: " + self.fine_mode + '\n'
        s+= "Fine Step Size: " + self.fine_step_size + '\n'
        s+= "Tone Status: " + str(self.tone_status) + '\n'
        s+= "CTCSS Status: " + str(self.ctcss_status) + '\n'
        s+= "DCS Status: " + str(self.dcs_status) + '\n'
        s+= "CTCSS/DCS Status: " + str(self.ctcss_dcs_status) + '\n'
        s+= "Reversed: " + self.reversed + '\n'
        s+= "Shift Dir: " + self.shift_direction + '\n'
        s+= "Tone: " + str(self.tone_freq) + '\n'
        s+= "CTCSS: " + str(self.ctcss_freq) + '\n'
        s+= "DCS: " + str(self.dcs_freq) + '\n'
        s+= "D/O: " + str(self.cross_encode) + '\n'
        s+= "URCALL: " + self.urcall + '\n'
        s+= "D-Star Sq Type: " + self.dstar_sq_type + '\n'
        s+= "D-Star Sq Code: " + self.dstar_sq_code + '\n'

        return s
# ---------- ChannelFrequency Class ---------- #

# ---------- Device Class ---------- #
class Device(QObject):

    DISCONNECTED        = 1
    CONNECTING          = 2
    CONNECTED           = 3
    FORCE_DISCONNECTED  = 4

    timeout_period          = 2000
    ch_refresh_interval     = 1000
    verbose                 = False
    timeout_timer: QTimer   = None
    refresh_timer: QTimer   = None
    serial_port             = None
    status                  = DISCONNECTED
    last_command            = None
    serial_conn: QSerialPort = None

    serial_number           = ""
    radio_type              = ""
    fw_version              = ""
    band_idx                = 0
    dv_mode                 = False
    memory_mode             = False
    band_idx                = 2
    band_a_squelch          = 0
    band_b_squelch          = 0

    error_occurred          = Signal(str, str)
    update_model_id         = Signal(str)
    update_serial_number    = Signal(str)
    update_fw               = Signal(str)
    update_freq             = Signal(int, str)
    update_auto_feedback    = Signal(bool)
    update_band_control     = Signal(int)
    update_band_mode        = Signal(int, int)
    update_band_frequency   = Signal(int, str)
    update_tx               = Signal(bool)
    update_memory_mode      = Signal(int, int)
    update_s_meter          = Signal(int, int)
    update_af_gain          = Signal(int)
    update_mem_channel      = Signal(int, str)
    update_dual_band        = Signal(int)
    update_backlight        = Signal(int)
    update_bt_enabled       = Signal(bool)
    update_gps              = Signal(bool, bool)
    update_squelch          = Signal(int, int)
    update_tnc              = Signal(int, int)
    update_beacon_type      = Signal(int)
    update_output_power     = Signal(int, int)
    update_mem_channel_freq = Signal(int)
    update_band_freq_info   = Signal(ChannelFrequency)
    update_gps_data         = Signal(GPSData)
    
    command_buffer = []

    def __init__(self, serial_port) -> None:
        QObject.__init__(self)

        self.serial_port    = serial_port
        self.status         = Device.DISCONNECTED

        self.gps_data       = GPSData()

        self.timeout_timer  = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.connectionTimeout)

        self.refresh_timer  = QTimer()
        self.refresh_timer.setInterval(self.ch_refresh_interval)
        self.refresh_timer.timeout.connect(self.refreshBandFrequencyInfo)

    def initConnection(self, reconnect_count=0):
        if self.status != Device.CONNECTING:
            self.status = Device.CONNECTING

        self.serial_conn = QSerialPort(self.serial_port, baudRate=QSerialPort.Baud9600, readyRead=self.__readyRead)
        self.serial_conn.setDataBits(QSerialPort.Data8)
        self.serial_conn.setParity(QSerialPort.NoParity)
        self.serial_conn.setStopBits(QSerialPort.OneStop)
        self.serial_conn.setFlowControl(QSerialPort.FlowControl.HardwareControl)
        self.serial_conn.errorOccurred.connect(self.serialPortError)

        if self.serial_conn.open(QIODevice.ReadWrite):
            self.serial_conn.setDataTerminalReady(True)
            self.command_buffer = []
            self.getSerialNumber()
            self.getFWVersion()
            self.getModelID()
            self.getRealtimeFB()
            self.getDualSingleBand()
            self.getBandControl()
            self.getAfGain()
            self.getBacklight()
            self.getBtEnabled()
            self.getGPS()
            self.getTNC()
            self.getBeaconType()

            #Band A
            self.getMemoryMode(0)
            self.getBandMode(0)
            # self.getBandFrequency(0)
            self.getMeter(0)
            self.getSquelch(0)
            self.getOutputPower(0)
            self.getBandFrequencyInfo(0)

            #Band B
            self.getMemoryMode(1)
            self.getBandMode(1)
            # self.getBandFrequency(1)
            self.getMeter(1)
            self.getSquelch(1)
            self.getOutputPower(1)
            self.getBandFrequencyInfo(1)

            # self.refresh_timer.start()
            return True
        
        print("Failed to connect to device!")
        return False
    def serialPortError(self, error):
        if error == QSerialPort.SerialPortError.ResourceError or error == QSerialPort.SerialPortError.DeviceNotFoundError:
            print("error")
            self.error_occurred.emit("Device not found.", "Serial Port Error")
                
    def write(self, cmd, payload=None):
        
        if payload == None:
            data = (cmd + '\r').encode("UTF-8")
        else:
            data = (cmd + " " + payload + '\r').encode("UTF-8")
        
        self.command_buffer.append(data)

        if len(self.command_buffer) == 1:
            self.writeData(data)
    def writeData(self, data):
        if self.serial_conn.isOpen():
            self.timeout_timer.stop()
            self.timeout_timer.start(self.timeout_period)

            if self.verbose: print('W: ', data)
            self.last_command = self.command_buffer[0].split()[0]
            self.serial_conn.write(data)
        else:
            self.command_buffer = []
    
    serial_buffer = b''
    gps_data: GPSData = None

    def __readyRead(self):
        self.status  = Device.CONNECTED
        self.timeout_timer.stop()

        data = self.serial_conn.readAll().data().strip()

        if data.startswith(b'FO') and len(data) < 72:
            self.serial_buffer = data
        elif len(self.serial_buffer) > 0 and len(self.serial_buffer) < 72:
            self.serial_buffer += data
        
        if len(self.serial_buffer) > 0 and len(self.serial_buffer) < 72:
            return
        elif len(self.serial_buffer) == 72:
            data = self.serial_buffer
            self.serial_buffer = b''

        if (len(data)) == 0: return
        if(data == b'?'):
            if len(self.command_buffer) > 0:
                if self.verbose: print("Invalid Command: " + str(self.command_buffer[0]))
                self.command_buffer.pop(0)
        elif(data == b'N'):
            if len(self.command_buffer) > 0: 
                if self.verbose: print("Command rejected: " + str(self.command_buffer[0]))
                self.command_buffer.pop(0)
            
        else:
            try:
                self.parseCommand(data)
            except:
                print("Parsing error:", data)

        if len(self.command_buffer) > 0 and self.last_command != None and data.startswith(self.command_buffer[0].split()[0]):
            self.command_buffer.pop(0)

        if len(self.command_buffer) > 0:
            self.writeData(self.command_buffer[0])
    def parseCommand(self, serial_data):
        data: str = serial_data.decode("UTF-8").strip()

        if data.startswith('$'):
            self.gps_data.parseData(data)
            self.update_gps_data.emit(self.gps_data)
            return

        exploded_data = data.split()
        command = exploded_data[0]
        command_data = ""

        if(len(exploded_data) > 1):
            command_data = exploded_data[1].split(',')

        if self.verbose: print('R: ', command, command_data)

        if(command == CATCommand.SerialNumber):
            self.serial_number = command_data[0]
            self.radio_type = command_data[1]
            self.update_serial_number.emit(self.serial_number)

        elif(command == CATCommand.FWVersion):
            self.fw_version = command_data[0]
            self.update_fw.emit(self.fw_version)

        elif command == CATCommand.RealTimeFB:
            self.update_auto_feedback.emit(command_data[0] == "1")

        elif command == CATCommand.BandControl:
            self.update_band_control.emit(int(command_data[0]))
            self.band_idx = int(command_data[0])
            self.getBandFrequencyInfo(self.band_idx)
            # if self.memory_mode == 1:
            self.getBandChannel(self.band_idx)
            
        elif command == CATCommand.ModelID:
            self.update_model_id.emit(command_data[0])

        elif command == CATCommand.BandMode:
            if self.memory_mode == 1:
                self.getBandChannel(self.band_idx)
            else:
                self.getBandFrequencyInfo(self.band_idx)
            self.update_band_mode.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.Frequency:
            frequency = str(int(command_data[1][:4])) + "." + command_data[1][4:7]
            self.update_band_frequency.emit(int(command_data[0]), frequency)
            if self.memory_mode:
                self.getMemChannel(int(command_data[0]))
            
            self.refreshBandFrequencyInfo()

        elif command == CATCommand.FrequencyInfo:
            self.update_band_freq_info.emit(ChannelFrequency(command_data))

        elif command == CATCommand.MemoryMode:
            self.memory_mode = int(command_data[1])
            self.update_memory_mode.emit(int(command_data[0]), int(command_data[1]))
            if self.memory_mode == 1:
                self.getBandChannel(self.band_idx)

        elif command == CATCommand.TX:
            self.update_tx.emit(True)

        elif command == CATCommand.RX:
            self.update_tx.emit(False)

        elif command == CATCommand.SquelchOpen:
            if int(command_data[1]) == 0:
                self.update_s_meter.emit(int(command_data[0]), 0)
            else:
                self.getMeter(command_data[0])

        elif command == CATCommand.S_Meter:
            self.update_s_meter.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.AFGain:
            self.update_af_gain.emit(int(command_data[0]))

        elif command == CATCommand.MemChannel:
            if len(command_data) == 1:
                self.update_mem_channel.emit(self.band_idx, command_data[0])

        elif command == CATCommand.MemChannelFreq:
            self.update_mem_channel_freq.emit(int(command_data[0]))

        elif command == CATCommand.DualSingleBand:
            self.update_dual_band.emit(int(command_data[0]))

        elif command == CATCommand.Backlight:
            self.update_backlight.emit(int(command_data[0]))

        elif command == CATCommand.Bluetooth:
            self.update_bt_enabled.emit(int(command_data[0])==1)

        elif command == CATCommand.GPS:
            self.update_gps.emit(int(command_data[0])==1, int(command_data[1])==1)
        
        elif command == CATCommand.Squelch:
            if int(command_data[0]) == 0:
                self.band_a_squelch = int(command_data[1])
            else:
                self.band_b_squelch = int(command_data[1])
            self.update_squelch.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.TNC:
            self.update_tnc.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.BeaconType:
            self.update_beacon_type.emit(int(command_data[0]))

        elif command == CATCommand.OutputPower:
            self.update_output_power.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.BtnDown or command == CATCommand.BtnUp:
            pass # Do nothing so it doesn't print out on console
        else:
            print(command, command_data)

    def connectionTimeout(self):
        if self.verbose: print("SerialPortError: Serial connection has timed out.")
        self.error_occurred.emit("Serial connection has timed out.", "Serial Connection Error")

    #COMMANDS
    def getMeter(self, band):
        self.write(CATCommand.S_Meter, str(band))
    def getModelID(self):
        self.write(CATCommand.ModelID)
    def getSerialNumber(self):
        self.write(CATCommand.SerialNumber)
    def getFWVersion(self):
        self.write(CATCommand.FWVersion)
    
    def getRealtimeFB(self):
        self.write(CATCommand.RealTimeFB)
    def setRealtimeFB(self, enabled):
        data = CATCommand.RealTimeFB
        if enabled:
            data += " 1"
        else:
            data += " 0"
        self.write(data)
    
    def getBandControl(self):
        self.write(CATCommand.BandControl)
    def setBandControl(self, idx):
        self.write(CATCommand.BandControl, str(idx))

    def getBandMode(self, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.BandMode, str(band_idx))
    def setBandMode(self, mode_idx, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.BandMode, str(band_idx) + ',' + str(mode_idx))
    
    def getMemoryMode(self, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.MemoryMode, str(band_idx))
    def setMemoryMode(self, mode_idx, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.MemoryMode, str(band_idx) + ',' + str(mode_idx))
        self.getBandMode()
        self.getBandFrequency()

    def getBandChannel(self, band_idx):
        self.write(CATCommand.MemChannel, str(band_idx))
    def setBandChannel(self, band_idx, channel):
        padded_channel = str(channel).ljust(3,'0')
        self.write(CATCommand.MemChannel, str(band_idx)+ ","+ padded_channel)
    
    def getBandFrequency(self, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.Frequency, str(band_idx))
    def setBandFrequency(self, freq, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        frequency = ""

        f_arr = freq.split('.')
        frequency = f_arr[0].rjust(4, '0') + f_arr[1].ljust(6, '0')

        self.write(CATCommand.Frequency, str(band_idx) + ',' + frequency)
    
    def getBandFrequencyInfo(self, band_idx):
        self.write(CATCommand.FrequencyInfo, str(band_idx))
    def setBandFrequencyInfo(self, info: ChannelFrequency):
        self.write(CATCommand.FrequencyInfo, info.toRadio())
    def refreshBandFrequencyInfo(self):
        self.getBandFrequencyInfo(self.band_idx)
    
    def getDualSingleBand(self):
        self.write(CATCommand.DualSingleBand)
    def setDualSingleBand(self, opt):
        self.write(CATCommand.DualSingleBand, str(opt))
    
    def getAfGain(self):
        self.write(CATCommand.AFGain)
    def setAfGain(self, level):
        # print(CATCommand.AFGain, str(level).rjust(3, '0'))
        self.write(CATCommand.AFGain, str(level).rjust(3, '0'))

    def getMemChannel(self, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.MemChannel, str(band_idx))
    def setMemChannel(self, channel, band_idx=None):
        if band_idx == None: band_idx = self.band_idx
        if band_idx == None: return
        self.write(CATCommand.MemChannel, str(band_idx) + ',' + str(channel))

    def getMemChannelFreq(self, band_idx):
        self.write(CATCommand.MemChannelFreq, str(band_idx))
    def setMemChannelFreq(self, mem_ch_info):
        pass

    def getBacklight(self):
        self.write(CATCommand.Backlight)
    def setBacklight(self, enabled):
        self.write(CATCommand.Backlight, str(1 if enabled else 0))
                   
    def getBtEnabled(self):
        self.write(CATCommand.Bluetooth)
    def setBtEnabled(self, enabled):
        self.write(CATCommand.Bluetooth, str(1 if enabled else 0))

    def getGPS(self):
        self.write(CATCommand.GPS)
    def setGPS(self, enabled, pc_out):
        self.write(CATCommand.GPS, str(1 if enabled else 0) + ',' + str(1 if pc_out else 0))

    def getSquelch(self, band_idx):
        self.write(CATCommand.Squelch, str(band_idx))
    def setSquelch(self, band_idx, level):
        self.write(CATCommand.Squelch, str(band_idx) + ',' + str(level))

    def getTNC(self):
        self.write(CATCommand.TNC)
    def setTNC(self, mode, band_idx):
        self.write(CATCommand.TNC, str(mode) + ',' + str(band_idx))

    def getBeaconType(self):
        self.write(CATCommand.BeaconType)
    def setBeaconType(self, beacon_type_idx):
        self.write(CATCommand.BeaconType, str(beacon_type_idx))

    def toggleBeacon(self):
        self.write(CATCommand.Beacon)

    def getOutputPower(self, band_idx):
        self.write(CATCommand.OutputPower, str(band_idx))
    def setOutputPower(self, band_idx, pwr):
        self.write(CATCommand.OutputPower, str(band_idx) + ',' + str(pwr))

    def upButton(self):
        self.write(CATCommand.BtnUp)
    def downButton(self):
        self.write(CATCommand.BtnDown)
    def setTX(self, enabled):
        if enabled:
            data = CATCommand.TX
        else:
            data = CATCommand.RX
        self.write(data)
# ---------- Device Class ---------- #