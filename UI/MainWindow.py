import os, logging, configparser
from PySide6.QtWidgets import QDialog, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStatusBar
from PySide6.QtSerialPort import QSerialPortInfo
from UI.windows.ui_main_window import Ui_MainWindow
from Device import Device
from UI.windows.ui_com_port_dialog import Ui_ComPortDialog
# from UI.ComPortDialog import ComPortDialog

logger = logging.getLogger(__name__)

config_file_path = './config.cfg'

class MainWindow(QMainWindow):
    device = None
    com_port_dialog = None
    in_tx = False
    port_name = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup MainWindow UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Add a label to the status bar
        self.status_bar_conn_status = QLabel("Status: Not Connected")
        self.status_bar_conn_status.setStyleSheet("padding: 0px 10px;")
        self.status_bar_fw_version = QLabel("FW:")
        self.status_bar_fw_version.setStyleSheet("padding: 0px 10px;")
        self.status_bar_sn = QLabel("S/N:")
        self.status_bar_sn.setStyleSheet("padding: 0px 10px;")
        self.status_bar_model_id = QLabel()
        self.status_bar_model_id.setStyleSheet("padding: 0px 10px;")

        status_bar.addWidget(self.status_bar_conn_status)
        status_bar.addWidget(self.status_bar_fw_version)
        status_bar.addWidget(self.status_bar_sn)
        status_bar.addWidget(self.status_bar_model_id)

        
        self.ui.upBtn.clicked.connect(self.upButton)
        self.ui.dwnBtn.clicked.connect(self.downButton)
        self.ui.txBtn.clicked.connect(self.setTX)
        self.ui.volumeSlider.valueChanged.connect(self.setVolume)
        self.ui.radioUpdateChbx.clicked.connect(self.setAutoFeedback)

        self.ui.bandControlCbx.currentIndexChanged.connect(self.setDualBand)
        self.ui.bandControlCbx.addItems(['Dual Band', 'Single Band'])
        
        self.ui.bandCbx.currentIndexChanged.connect(self.setBandControl)
        self.ui.bandCbx.addItem("Band A")
        self.ui.bandCbx.addItem("Band B")

        self.ui.bandAFreqText.editingFinished.connect(self.setFrequencyA)
        self.ui.bandBFreqText.editingFinished.connect(self.setFrequencyB)

        memory_mode_arr = ["VFO", "Memory", "Call", "DV"]
        self.ui.bandAMemoryModeCbx.currentIndexChanged.connect(self.setMemoryModeA)
        self.ui.bandBMemoryModeCbx.currentIndexChanged.connect(self.setMemoryModeB)
        for item in memory_mode_arr:
            self.ui.bandAMemoryModeCbx.addItem(item)
            self.ui.bandBMemoryModeCbx.addItem(item)

        modulation_mode_arr = ["FM", "DV", "AM", "LSB", "USB", "CW", "NFM", "DR", "WFM", "R-CW"]
        self.ui.bandAModeCbx.currentIndexChanged.connect(self.setBandModeA)
        self.ui.bandBModeCbx.currentIndexChanged.connect(self.setBandModeB)
        for item in modulation_mode_arr:
            self.ui.bandAModeCbx.addItem(item)
            self.ui.bandBModeCbx.addItem(item)

        self.com_port_dialog = ComPortDialog(self)

        self.ui.actionPort.triggered.connect(self.showComPortDialog)
        self.ui.actionConnect.triggered.connect(self.connectDevice)

        self.loadConfig()

    def showComPortDialog(self):
        self.com_port_dialog.show()

    def closeEvent(self, event):
        if self.device != None and self.device.serial_conn != None and self.device.serial_conn.isOpen():
            self.device.setRealtimeFB(False)
            self.device.serial_conn.close()

    def connectDevice(self, com_port=None):
        if self.device != None and self.device.serial_conn != None and self.device.serial_conn.isOpen():
            self.device.serial_conn.close()
        
        if com_port == None or type(com_port) != str:
            com_port = self.port_name

        self.device = Device(com_port)
        if(self.device.initConnection()):
            self.port_name = com_port
            self.status_bar_conn_status.setText(f"{self.port_name}: Connected")
            self.device.update_model_id.connect(self.updateModelId)
            self.device.update_serial_number.connect(self.updateSerialNumber)
            self.device.update_auto_feedback.connect(self.updateAutoFeedback)
            self.device.update_fw.connect(self.updateFW)
            self.device.update_band_control.connect(self.updateBandControl)
            self.device.update_band_mode.connect(self.updateBandMode)
            self.device.update_memory_mode.connect(self.updateMemoryMode)
            self.device.update_band_frequency.connect(self.updateFrequency)
            self.device.update_tx.connect(self.updateTX)
            self.device.error_occurred.connect(self.errorOccurred)
            self.device.update_s_meter.connect(self.updateSMeter)
            self.device.update_af_gain.connect(self.updateVolume)
            self.device.update_mem_channel.connect(self.updateMemChannel)
            self.device.update_dual_band.connect(self.updateDualBand)
            self.device.setRealtimeFB(True)
            self.device.getRealtimeFB()
            self.saveConfig()
        else:
            self.errorOccurred("Could not connect to device", "COM Port Error")
            self.status_bar_conn_status.setText(f"{self.port_name}: Error")
            # self.device.getBand()

    def loadConfig(self):
        if os.path.isfile(config_file_path):
            config = configparser.ConfigParser()
            config.read(config_file_path)

            if config['SERIAL']['port'] != "" and config['SERIAL']['autoconnect'] == 'True':
                self.port_name =  config['SERIAL']['port']
                self.connectDevice(config['SERIAL']['port'])

    def saveConfig(self):
        config = configparser.ConfigParser()

        config['SERIAL'] = {
            'port': self.port_name,
            'autoconnect': True
        }
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    
    #SLOTS
    def errorOccurred(self, message, title="Error"):
        QMessageBox.critical(self, title, message)

    def updateModelId(self, model_id):
        self.status_bar_model_id.setText(model_id)
    def updateSerialNumber(self, sn):
        self.status_bar_sn.setText("S/N: " + sn)
    def updateFW(self, fw_version):
        self.status_bar_fw_version.setText("FW: " + fw_version)
    def updateSMeter(self, band, level):
        if band == 0:
            self.ui.bandAMeter.setValue(level)
        else:
            self.ui.bandBMeter.setValue(level)
    
    def setDualBand(self):
        self.device.setDualSingleBand(self.ui.bandControlCbx.currentIndex())
    def updateDualBand(self, opt):
        self.ui.bandControlCbx.setCurrentIndex(opt)

    def setTX(self):
        if self.in_tx:
            self.in_tx = False
            self.ui.txBtn.setStyleSheet("")
        else:
            self.in_tx = True
            self.ui.txBtn.setStyleSheet("QPushButton{background-color:red;color:white;}")
        self.device.setTX(self.in_tx)
    def updateTX(self, enabled):
        self.in_tx = enabled
        if self.in_tx:
            self.ui.txBtn.setStyleSheet("background-color:red; color:white;")
        else:
            self.ui.txBtn.setStyleSheet("")
    
    def setVolume(self):
        self.device.setAfGain(self.ui.volumeSlider.value())
    def updateVolume(self, level):
        self.ui.volumeSlider.blockSignals(True)
        self.ui.volumeSlider.setValue(level)
        self.ui.volumeSlider.blockSignals(False)

    def setBandControl(self):
        self.device.setBandControl(self.ui.bandCbx.currentIndex())
    def updateBandControl(self, idx):
        self.ui.bandCbx.blockSignals(True)
        self.ui.bandCbx.setCurrentIndex(idx)
        self.ui.bandCbx.blockSignals(False)

    def setAutoFeedback(self):
        self.device.setRealtimeFB(self.ui.radioUpdateChbx.isChecked())
    def updateAutoFeedback(self, enabled):
        self.ui.radioUpdateChbx.blockSignals(True)
        self.ui.radioUpdateChbx.setChecked(enabled)
        self.ui.radioUpdateChbx.blockSignals(False)
    
    def setMemoryModeA(self):
        self.setMemoryMode(self.ui.bandAMemoryModeCbx.currentIndex(), 0)
    def setMemoryModeB(self):
        self.setMemoryMode(self.ui.bandBMemoryModeCbx.currentIndex(), 1)
    def setMemoryMode(self, mode, band):
        self.device.setMemoryMode(mode, band)
    def updateMemoryMode(self, band, mode_idx):
        if band == 0:
            self.ui.bandAMemoryModeCbx.blockSignals(True)
            self.ui.bandAMemoryModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandAMemoryModeCbx.blockSignals(False)

            if mode_idx == 0:
                self.ui.bandAFreqText.setEnabled(True)
                self.ui.bandAModeCbx.setEnabled(True)
            else:
                self.ui.bandAFreqText.setEnabled(False)
                self.ui.bandAModeCbx.setEnabled(False)

            # if mode_idx == 1:
            #     self.ui.bandAChannelLbl.setVisible(True)
            # else:
            #     self.ui.bandAChannelLbl.setVisible(False)
        else:
            self.ui.bandBMemoryModeCbx.blockSignals(True)
            self.ui.bandBMemoryModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandBMemoryModeCbx.blockSignals(False)

            if mode_idx == 0:
                self.ui.bandBFreqText.setEnabled(True)
                self.ui.bandBModeCbx.setEnabled(True)
            else:
                self.ui.bandBFreqText.setEnabled(False)
                self.ui.bandBModeCbx.setEnabled(False)

            # if mode_idx == 1:
            #     self.ui.bandBChannelLbl.setVisible(True)
            # else:
            #     self.ui.bandBChannelLbl.setVisible(False)

    def setBandModeA(self):
        self.device.setBandMode(self.ui.bandAModeCbx.currentIndex(), 0)
    def setBandModeB(self):
        self.device.setBandMode(self.ui.bandBModeCbx.currentIndex(), 1)
    def setBandMode(self, mode, band):
        self.device.setBandMode(mode, band)
    def updateBandMode(self, band, mode_idx):
        if band == 0:
            self.ui.bandAModeCbx.blockSignals(True)
            self.ui.bandAModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandAModeCbx.blockSignals(False)
        else:
            self.ui.bandBModeCbx.blockSignals(True)
            self.ui.bandBModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandBModeCbx.blockSignals(False)
    
    def updateMemChannel(self, channel):
        pass
        # self.ui.channelLbl.setText(f"CH: {channel}")

    def upButton(self):
        self.device.upButton()
    def downButton(self):
        self.device.downButton()
    
    def setFrequencyA(self):
        self.setFrequency(self.ui.bandAFreqText.text(), 0)
    def setFrequencyB(self):
        self.setFrequency(self.ui.bandBFreqText.text(), 1)
    def setFrequency(self, frequency, band_idx):
        self.device.setBandFrequency(frequency, band_idx)    
    def updateFrequency(self, band, freq):
        if band == 0:
            self.ui.bandAFreqText.blockSignals(True)
            self.ui.bandAFreqText.setText(freq)
            self.ui.bandAFreqText.blockSignals(False)
        else:
            self.ui.bandBFreqText.blockSignals(True)
            self.ui.bandBFreqText.setText(freq)
            self.ui.bandBFreqText.blockSignals(False)


class ComPortDialog(QDialog):

    parent: MainWindow = None

    def __init__(self, parent: MainWindow=None):
        super().__init__(parent)

        self.parent = parent
        
        # Setup MainWindow UI
        self.ui = Ui_ComPortDialog()
        self.ui.setupUi(self)

        self.ui.connectBtn.clicked.connect(self.connectDevice)

    def show(self):
        super().show()
        self.ui.portCbx.clear()
        self.scanDevices()


    def scanDevices(self):
        self.serial_list = QSerialPortInfo().availablePorts()
        for serial_info in self.serial_list:
            self.ui.portCbx.addItem(serial_info.portName() + ' (' + serial_info.description() + ')')
        self.ui.portCbx.setCurrentIndex(0)

    def connectDevice(self):
        self.parent.connectDevice(self.serial_list[self.ui.portCbx.currentIndex()].portName())
        self.hide()
        