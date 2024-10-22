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
    verbose = False
    device = None
    com_port_dialog = None
    in_tx = False
    port_name = ""
    
    band_a_squelch = 0
    band_b_squelch = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup MainWindow UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        self.ui.radioUpdateChbx.setVisible(False)

        # Add a label to the status bar
        self.status_bar_conn_status = QLabel("Status: Not Connected")
        self.status_bar_conn_status.setStyleSheet("padding: 0px 10px;")
        self.status_bar_fw_version = QLabel("FW:")
        self.status_bar_fw_version.setStyleSheet("padding: 0px 10px;")
        self.status_bar_sn = QLabel("S/N:")
        self.status_bar_sn.setStyleSheet("padding: 0px 10px;")
        self.status_bar_model_id = QLabel()
        self.status_bar_model_id.setStyleSheet("padding: 0px 10px;")

        self.status_bar_creator = QLabel("Created By K7DMG")
        self.status_bar_creator.setStyleSheet("padding: 0px 10px;")

        status_bar.addWidget(self.status_bar_conn_status)
        status_bar.addWidget(self.status_bar_fw_version)
        status_bar.addWidget(self.status_bar_sn)
        status_bar.addWidget(self.status_bar_model_id)
        status_bar.addWidget(self.status_bar_creator)

        
        self.ui.upBtn.clicked.connect(self.upButton)
        self.ui.dwnBtn.clicked.connect(self.downButton)
        self.ui.txBtn.clicked.connect(self.setTX)
        self.ui.volumeSlider.valueChanged.connect(self.setVolume)
        self.ui.radioUpdateChbx.clicked.connect(self.setAutoFeedback)

        
        self.ui.bandControlCbx.addItems(['Dual Band', 'Single Band'])
        self.ui.bandControlCbx.currentIndexChanged.connect(self.setDualBand)
        
        
        self.ui.bandCbx.addItem("Band A")
        self.ui.bandCbx.addItem("Band B")
        self.ui.bandCbx.currentIndexChanged.connect(self.setBandControl)

        
        self.ui.backlightCbx.addItems(['Manual', 'On', 'Auto', 'Auto (DC-IN)'])
        self.ui.backlightCbx.currentIndexChanged.connect(self.setBacklight)

        self.ui.btEnabledChbx.stateChanged.connect(self.setBtEnabled)
        self.ui.gpsEnabledChbx.stateChanged.connect(self.setGPS)
        self.ui.gpsPcOutChbx.stateChanged.connect(self.setGPS)

        self.ui.tncModeCbx.addItems(['Off', 'APRS', 'KISS'])
        self.ui.tncBandCbx.addItems(['Band A', 'Band B'])
        
        self.ui.tncModeCbx.currentIndexChanged.connect(self.setTNC)
        self.ui.tncBandCbx.currentIndexChanged.connect(self.setTNC)

        self.ui.beaconCbx.addItems(['Manual', 'PTT', 'Auto', 'SmartBeaconing'])
        self.ui.beaconCbx.currentIndexChanged.connect(self.setBeaconType)

        self.ui.bandASquelchCbx.addItems("%s" %i for i in range(0,6))
        self.ui.bandBSquelchCbx.addItems("%s" %i for i in range(0,6))
        self.ui.bandASquelchCbx.currentIndexChanged.connect(self.setSquelchA)
        self.ui.bandBSquelchCbx.currentIndexChanged.connect(self.setSquelchB)
        
        for i in range(999):
            self.ui.bandAChannelCbx.addItem(str(i).rjust(3,'0'))
            self.ui.bandBChannelCbx.addItem(str(i).rjust(3,'0'))
        self.ui.bandAChannelCbx.currentIndexChanged.connect(self.setMemChannelA)
        self.ui.bandBChannelCbx.currentIndexChanged.connect(self.setMemChannelB)

        self.ui.bandAFreqText.editingFinished.connect(self.setFrequencyA)
        self.ui.bandBFreqText.editingFinished.connect(self.setFrequencyB)

        self.ui.bandAMonitorBtn.pressed.connect(self.setOpenSquelchA)
        self.ui.bandBMonitorBtn.pressed.connect(self.setOpenSquelchB)
        self.ui.bandAMonitorBtn.released.connect(self.setClosedSquelchA)
        self.ui.bandBMonitorBtn.released.connect(self.setClosedSquelchB)

        power_arr = ["High", "Medium", "Low", "Extra Low"]
        for item in power_arr:
            self.ui.bandAPwrCbx.addItem(item)
            self.ui.bandBPwrCbx.addItem(item)
        self.ui.bandAPwrCbx.currentIndexChanged.connect(self.setOutputPowerA)
        self.ui.bandBPwrCbx.currentIndexChanged.connect(self.setOutputPowerB)

        memory_mode_arr = ["VFO", "Memory", "Call", "DV"]
        for item in memory_mode_arr:
            self.ui.bandAMemoryModeCbx.addItem(item)
            self.ui.bandBMemoryModeCbx.addItem(item)
        self.ui.bandAMemoryModeCbx.currentIndexChanged.connect(self.setMemoryModeA)
        self.ui.bandBMemoryModeCbx.currentIndexChanged.connect(self.setMemoryModeB)

        modulation_mode_arr = ["FM", "DV", "AM", "LSB", "USB", "CW", "NFM", "DR", "WFM", "R-CW"]
        for item in modulation_mode_arr:
            self.ui.bandAModeCbx.addItem(item)
            self.ui.bandBModeCbx.addItem(item)
        self.ui.bandAModeCbx.currentIndexChanged.connect(self.setBandModeA)
        self.ui.bandBModeCbx.currentIndexChanged.connect(self.setBandModeB)

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
        self.device.verbose = self.verbose
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
            self.device.update_backlight.connect(self.updateBacklight)
            self.device.update_bt_enabled.connect(self.updateBtEnabled)
            self.device.update_gps.connect(self.updateGPS)
            self.device.update_squelch.connect(self.updateSquelch)
            self.device.update_tnc.connect(self.updateTNC)
            self.device.update_beacon_type.connect(self.updateBeaconType)
            self.device.update_output_power.connect(self.updateOutputPower)
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

            if config.has_option('DEBUG', 'verbose'):
                self.verbose = config['DEBUG']['verbose'] == 'True'

            if config['SERIAL']['port'] != "" and config['SERIAL']['autoconnect'] == 'True':
                self.port_name =  config['SERIAL']['port']
                self.connectDevice(config['SERIAL']['port'])

            

    def saveConfig(self):
        config = configparser.ConfigParser()

        config['SERIAL'] = {
            'port': self.port_name,
            'autoconnect': True
        }

        config['DEBUG'] = {
            'verbose': self.verbose
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

        if idx == 0:
            self.ui.bandAWidget.setStyleSheet("#bandAWidget {background-color:lightblue;border-radius: 10px;}")
            self.ui.bandBWidget.setStyleSheet("#bandBWidget {background-color:silver;border-radius: 10px;}")
        else:
            self.ui.bandAWidget.setStyleSheet("#bandAWidget {background-color:silver;border-radius: 10px;}")
            self.ui.bandBWidget.setStyleSheet("#bandBWidget {background-color:lightblue;border-radius: 10px;}")

    def setAutoFeedback(self):
        self.device.setRealtimeFB(self.ui.radioUpdateChbx.isChecked())
    def updateAutoFeedback(self, enabled):
        self.ui.radioUpdateChbx.blockSignals(True)
        self.ui.radioUpdateChbx.setChecked(enabled)
        self.ui.radioUpdateChbx.blockSignals(False)
    
    def setBacklight(self, idx):
        self.device.setBacklight(idx)
    def updateBacklight(self, idx):
        self.ui.backlightCbx.blockSignals(True)
        self.ui.backlightCbx.setCurrentIndex(idx)
        self.ui.backlightCbx.blockSignals(False)

    def setBtEnabled(self, enabled):
        self.device.setBtEnabled(enabled)
    def updateBtEnabled(self, enabled):
        self.ui.btEnabledChbx.blockSignals(True)
        self.ui.btEnabledChbx.setChecked(enabled)
        self.ui.btEnabledChbx.blockSignals(False)

    def setGPS(self):
        self.device.setGPS(self.ui.gpsEnabledChbx.isChecked(), self.ui.gpsPcOutChbx.isChecked())
    def updateGPS(self, enabled, pc_out):
        self.ui.gpsEnabledChbx.blockSignals(True)
        self.ui.gpsEnabledChbx.setChecked(enabled)
        self.ui.gpsEnabledChbx.blockSignals(False)

        self.ui.gpsPcOutChbx.blockSignals(True)
        self.ui.gpsPcOutChbx.setChecked(pc_out)
        self.ui.gpsPcOutChbx.blockSignals(False)

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
    
    def setMemChannelA(self, idx):
        self.setMemChannel(0, self.ui.bandAChannelCbx.currentText())
    def setMemChannelB(self, idx):
        self.setMemChannel(1, self.ui.bandBChannelCbx.currentText())
    def setMemChannel(self, band_idx, channel):
        self.device.setMemChannel(str(channel).rjust(3,'0'), band_idx)
    def updateMemChannel(self, band_idx, channel):
        if band_idx == 0:
            self.ui.bandAChannelCbx.blockSignals(True)
            self.ui.bandAChannelCbx.setCurrentIndex(int(channel))
            self.ui.bandAChannelCbx.blockSignals(False)
            # self.ui.bandAChannelLbl.setText(f"Ch: {channel}")
        else:
            self.ui.bandBChannelCbx.blockSignals(True)
            self.ui.bandBChannelCbx.setCurrentIndex(int(channel))
            self.ui.bandBChannelCbx.blockSignals(False)
            # self.ui.bandBChannelLbl.setText(f"Ch: {channel}")

    def setOpenSquelchA(self):
        self.band_a_squelch = self.device.band_a_squelch
        self.openSquelch(0)
    def setOpenSquelchB(self):
        self.band_b_squelch = self.device.band_b_squelch
        self.openSquelch(1)
    def openSquelch(self, band_idx):
        self.device.setSquelch(band_idx, 0)

    def setSquelchA(self, level):
        self.setSquelch(0, level)
    def setSquelchB(self, level):
        self.setSquelch(1, level)
    def setSquelch(self, band_idx, level):
        self.device.setSquelch(band_idx, level)
    def updateSquelch(self, band_idx, sq):
        if band_idx == 0:
            self.ui.bandAChannelCbx.blockSignals(True)
            self.ui.bandASquelchCbx.setCurrentIndex(sq)
            self.ui.bandASquelchCbx.blockSignals(False)
        else:
            self.ui.bandBSquelchCbx.blockSignals(True)
            self.ui.bandBSquelchCbx.setCurrentIndex(sq)
            self.ui.bandBSquelchCbx.blockSignals(False)

    def setClosedSquelchA(self):
        self.device.setSquelch(0, self.band_a_squelch)
    def setClosedSquelchB(self):
        self.device.setSquelch(1, self.band_b_squelch)
    
    def setTNC(self):
        self.device.setTNC(self.ui.tncModeCbx.currentIndex(), self.ui.tncBandCbx.currentIndex())
    def updateTNC(self, mode, band_idx):
        self.ui.tncModeCbx.blockSignals(True)
        self.ui.tncModeCbx.setCurrentIndex(mode)
        self.ui.tncModeCbx.blockSignals(False)

        self.ui.tncBandCbx.blockSignals(True)
        self.ui.tncBandCbx.setCurrentIndex(band_idx)
        self.ui.tncBandCbx.blockSignals(False)

    def setBeaconType(self):
        self.device.setBeaconType(self.ui.beaconCbx.currentIndex())
    def updateBeaconType(self, beacon_type_idx):
        self.ui.beaconCbx.blockSignals(True)
        self.ui.beaconCbx.setCurrentIndex(beacon_type_idx)
        self.ui.beaconCbx.blockSignals(False)

    def setOutputPowerA(self, pwr):
        self.setOutputPower(0, pwr)
    def setOutputPowerB(self, pwr):
        self.setOutputPower(1, pwr)
    def setOutputPower(self, band_idx, pwr):
        self.device.setOutputPower(band_idx, pwr)
    def updateOutputPower(self, band_idx, pwr):
        if band_idx == 0:
            self.ui.bandAPwrCbx.blockSignals(True)
            self.ui.bandAPwrCbx.setCurrentIndex(pwr)
            self.ui.bandAPwrCbx.blockSignals(False)
        else:
            self.ui.bandBPwrCbx.blockSignals(True)
            self.ui.bandBPwrCbx.setCurrentIndex(pwr)
            self.ui.bandBPwrCbx.blockSignals(False)

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
        