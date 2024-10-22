from PySide6.QtCore import Signal, QObject, QIODevice, QTimer, QCoreApplication
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

class CATCommand():
    SerialNumber    = "AE"
    AFGain          = "AG"
    RealTimeFB      = "AI"
    BandControl     = "BC"
    BatteryLevel    = "BL"
    Squelch         = "BY"
    DualSingleBand  = "DL"
    BtnDown         = "DW"
    Frequency       = "FQ"
    FWVersion       = "FV"
    ModelID         = "ID"
    BandMode        = "MD"
    MemChannel      = "MR"
    TX              = "TX"
    RX              = "RX"
    S_Meter         = "SM"
    BtnUp           = "UP"
    MemoryMode      = "VM"
class Device(QObject):

    DISCONNECTED        = 1
    CONNECTING          = 2
    CONNECTED           = 3
    FORCE_DISCONNECTED  = 4

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
    update_mem_channel      = Signal(str)
    update_dual_band        = Signal(int)
    
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

            #Band A
            self.getMemoryMode(0)
            self.getBandMode(0)
            self.getBandFrequency(0)
            self.getMeter(0)

            #Band B
            self.getMemoryMode(1)
            self.getBandMode(1)
            self.getBandFrequency(1)
            self.getMeter(1)
            return True
        
        print("Failed to connect to device!")
        return False
    
    def serialPortError(self, error):
        if error == QSerialPort.SerialPortError.ResourceError or error == QSerialPort.SerialPortError.DeviceNotFoundError:
            if self.status != Device.CONNECTING:
                self.updated.emit(self)

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
            self.last_command = self.command_buffer[0].split()[0]
            self.serial_conn.write(data)
        else:
            self.command_buffer = []
    
    def __readyRead(self):
        self.status  = Device.CONNECTED
        data = self.serial_conn.readAll().data().strip()

        if(data == b'?'):
            print("Invalid Command: " + str(self.command_buffer[0]))
        elif(data == b'N'):
            print("Command rejected: " + str(self.command_buffer[0]))
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
            
        elif command == CATCommand.ModelID:
            self.update_model_id.emit(command_data[0])
        elif command == CATCommand.BandMode:
            self.update_band_mode.emit(int(command_data[0]), int(command_data[1]))
        elif command == CATCommand.Frequency:
            frequency = str(int(command_data[1][:4])) + "." + command_data[1][4:7]
            self.update_band_frequency.emit(int(command_data[0]), frequency)

            if self.memory_mode:
                self.getMemChannel(int(command_data[0]))
        elif command == CATCommand.MemoryMode:
            self.memory_mode = int(command_data[1]) == 1
            self.update_memory_mode.emit(int(command_data[0]), int(command_data[1]))
        elif command == CATCommand.TX:
            self.update_tx.emit(True)
        elif command == CATCommand.RX:
            self.update_tx.emit(False)
        elif command == CATCommand.Squelch:
            if int(command_data[1]) == 0:
                self.update_s_meter.emit(int(command_data[0]), 0)
            else:
                self.getMeter(command_data[0])
        elif command == CATCommand.S_Meter:
            self.update_s_meter.emit(int(command_data[0]), int(command_data[1]))
        elif command == CATCommand.AFGain:
            self.update_af_gain.emit(int(command_data[0]))
        elif command == CATCommand.MemChannel:
            self.update_mem_channel.emit(command_data[0])
        elif command == CATCommand.DualSingleBand:
            self.update_dual_band.emit(int(command_data[0]))
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