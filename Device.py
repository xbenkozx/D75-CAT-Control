from PySide6.QtCore import Signal, QObject, QIODevice, QTimer, QCoreApplication
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

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
    Frequency       = "FQ"
    FWVersion       = "FV"
    GPS             = "GP"
    ModelID         = "ID"

    # 0 = Manual
    # 1 = On
    # 2 = Auto
    # 3 = Auto (DC-IN)
    Backlight       = "LC"
    BandMode        = "MD"
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

    

class Device(QObject):

    DISCONNECTED        = 1
    CONNECTING          = 2
    CONNECTED           = 3
    FORCE_DISCONNECTED  = 4

    verbose         = False

    serial_port     = None
    status          = DISCONNECTED
    last_command    = None
    serial_conn: QSerialPort = None

    serial_number   = ""
    radio_type      = ""
    fw_version      = ""
    band_idx        = 0
    dv_mode         = False
    memory_mode     = False
    band_idx        = 2

    band_a_squelch  = 0
    band_b_squelch  = 0

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
    
    command_buffer = []

    def __init__(self, serial_port) -> None:
        QObject.__init__(self)

        self.serial_port    = serial_port
        self.status         = Device.DISCONNECTED

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
            self.getBandFrequency(0)
            self.getMeter(0)
            self.getSquelch(0)
            self.getOutputPower(0)

            #Band B
            self.getMemoryMode(1)
            self.getBandMode(1)
            self.getBandFrequency(1)
            self.getMeter(1)
            self.getSquelch(1)
            self.getOutputPower(1)
            return True
        
        print("Failed to connect to device!")
        return False
    
    def serialPortError(self, error):
        if error == QSerialPort.SerialPortError.ResourceError or error == QSerialPort.SerialPortError.DeviceNotFoundError:
            self.error_occurred.emit(self)
                

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
            # print("W:", self.command_buffer[0])
            if self.verbose: print('W: ', data)
            self.last_command = self.command_buffer[0].split()[0]
            self.serial_conn.write(data)
        else:
            self.command_buffer = []
    
    def __readyRead(self):
        self.status  = Device.CONNECTED
        data = self.serial_conn.readAll().data().strip()

        if(data == b'?'):
            if len(self.command_buffer) > 0: print("Invalid Command: " + str(self.command_buffer[0]))
        elif(data == b'N'):
            if len(self.command_buffer) > 0: print("Command rejected: " + str(self.command_buffer[0]))
        else:
            self.parseCommand(data)

        if len(self.command_buffer) > 0 and self.last_command != None and self.command_buffer[0].startswith(self.last_command):
            self.command_buffer.pop(0)

        if len(self.command_buffer) > 0:
            self.writeData(self.command_buffer[0])

    def parseCommand(self, serial_data):
        data = serial_data.decode("UTF-8").strip()

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
            if self.memory_mode == 1:
                self.getBandChannel(self.band_idx)
            
        elif command == CATCommand.ModelID:
            self.update_model_id.emit(command_data[0])

        elif command == CATCommand.BandMode:
            if self.memory_mode == 1:
                self.getBandChannel(self.band_idx)
            self.update_band_mode.emit(int(command_data[0]), int(command_data[1]))

        elif command == CATCommand.Frequency:
            frequency = str(int(command_data[1][:4])) + "." + command_data[1][4:7]
            self.update_band_frequency.emit(int(command_data[0]), frequency)
            if self.memory_mode:
                self.getMemChannel(int(command_data[0]))

        elif command == CATCommand.MemoryMode:
            self.memory_mode = int(command_data[1]) == 1
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
            self.update_mem_channel.emit(self.band_idx, command_data[0])

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

        else:
            print(command, command_data)

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
        # Sending the BEACON command causes the serial to freeze
        # if beacon_type_idx != 0: self.write(CATCommand.Beacon)

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