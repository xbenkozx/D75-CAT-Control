"""
File name MainWindow.py:
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

import os, logging, configparser, json
from time import sleep
from PySide6.QtCore import QTimer, QObject, QEvent
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QComboBox, QVBoxLayout, QLabel, QHBoxLayout, QStatusBar
from PySide6.QtSerialPort import QSerialPortInfo
from UI.windows.ui_main_window import Ui_MainWindow
from Device import Device, ChannelFrequency
from UI.windows.ui_com_port_dialog import Ui_ComPortDialog
from UI.windows.ui_about_dialog import Ui_AboutDialog

logger = logging.getLogger(__name__)

config_file_path = './config.cfg'

class MouseClickEventFilter(QObject):
    ui: Ui_MainWindow = None
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # print('mouse pressed', type(obj.objectName()), obj.objectName())
            if obj.objectName() == 'bandAWidget':
                self.ui.bandCbx.setCurrentIndex(0)
            elif obj.objectName() == 'bandBWidget':
                self.ui.bandCbx.setCurrentIndex(1)

        return super(MouseClickEventFilter, self).eventFilter(obj, event)
    
class MainWindow(QMainWindow):
    is_dark_mode = False

    verbose = False
    device = None
    autoconnect = False
    com_port_dialog = None
    about_dialog = None
    in_tx = False
    port_name = ""
    
    band_a_squelch = 0
    band_b_squelch = 0
    band_a_tone_type = -1
    band_a_cross_type = -1
    band_b_tone_type = -1
    band_b_cross_type = -1
    band_a_current_channel_frequency_info:ChannelFrequency = None
    band_b_current_channel_frequency_info:ChannelFrequency = None

    mem_channel_a_input_timer: QTimer = None
    mem_channel_a_input_lock = False
    mem_channel_b_input_timer: QTimer = None
    mem_channel_b_input_lock = False

    mouseEventFilter:MouseClickEventFilter = None

    styles = {
        "default" :
        { 
            "bandWidgetActive": "{background-color:lightblue;border-radius: 10px;}",
            "bandWidgetInactive": "{background-color:silver;border-radius: 10px;}"
        },
        "dark_mode":
        {
            "bandWidgetActive": "{background-color:#01344f;border-radius: 10px;}",
            "bandWidgetInactive": "{background-color:#333;border-radius: 10px;}"
        }
    }

    ctcss_tones = [
        "67.0", "69.3", "71.9", "74.4", "77.0", "79.7", "82.5", "85.4", "88.5", 
        "91.5", "94.8", "97.4", "100.0", "103.5", "107.2", "110.9", "114.8", 
        "118.8", "123.0", "127.3", "131.8", "136.5", "141.3", "146.2", "151.4", 
        "156.7", "162.2", "167.9", "173.8", "179.9", "186.2", "192.8", "203.5", 
        "210.7", "218.1", "225.7", "233.6", "241.8", "250.3"
    ]

    dcs_tones = [
        "023", "025", "026", "031", "032", "036", "043", "047", "051", "053", "054", 
        "065", "071", "072", "073", "074", "114", "115", "116", "122", "125", "131", 
        "132", "134", "143", "145", "152", "155", "156", "162", "165", "172", "174", 
        "205", "212", "223", "225", "226", "243", "244", "245", "246", "251", "252", 
        "255", "261", "263", "265", "266", "271", "274", "306", "311", "315", "325", 
        "331", "332", "343", "346", "351", "356", "364", "365", "371", "411", "412", 
        "413", "423", "431", "432", "445", "446", "452", "454", "455", "462", "464", 
        "465", "466", "503", "506", "516", "523", "526", "532", "546", "565", "606", 
        "612", "624", "627", "631", "632", "654", "662", "664", "703", "712", "723", 
        "731", "732", "734", "743", "754"
    ]

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

        self.ui.beaconBtn.clicked.connect(self.toggleBeacon)

        self.ui.bandASquelchCbx.addItems("%s" %i for i in range(0,6))
        self.ui.bandBSquelchCbx.addItems("%s" %i for i in range(0,6))
        self.ui.bandASquelchCbx.currentIndexChanged.connect(self.setSquelchA)
        self.ui.bandBSquelchCbx.currentIndexChanged.connect(self.setSquelchB)
        
        mem_names = [''] * 1000
        if os.path.exists("channel_memory.json"):
            with open("channel_memory.json", 'r') as f:
                mem_names = json.loads(f.read())
        for i in range(999):
            ch_name = str(i).rjust(3,'0')
            if len(mem_names[i]) > 0: ch_name += " - " + mem_names[i]
            self.ui.bandAChannelCbx.addItem(ch_name)
            self.ui.bandBChannelCbx.addItem(ch_name)
        self.ui.bandAChannelCbx.currentIndexChanged.connect(self.setMemChannelA)
        self.ui.bandBChannelCbx.currentIndexChanged.connect(self.setMemChannelB)

        # self.ui.bandAChannelCbx.currentTextChanged.connect(self.setMemChannelA)
        # self.ui.bandBChannelCbx.currentTextChanged.connect(self.setMemChannelB)

        self.ui.bandAFreqText.editingFinished.connect(self.setFrequencyA)
        self.ui.bandBFreqText.editingFinished.connect(self.setFrequencyB)

        self.ui.bandAMonitorBtn.pressed.connect(self.setOpenSquelchA)
        self.ui.bandBMonitorBtn.pressed.connect(self.setOpenSquelchB)
        self.ui.bandAMonitorBtn.released.connect(self.setClosedSquelchA)
        self.ui.bandBMonitorBtn.released.connect(self.setClosedSquelchB)

        tone_types = ['Off', 'Tone', 'CTCSS', 'DCS', 'Cross']
        self.ui.bandAToneCbx.addItems(tone_types)
        self.ui.bandBToneCbx.addItems(tone_types)

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

        cross_code_types = ['DCS/Off', 'Tone/DCS', 'DCS/CTCSS', 'Tone/CTCSS']
        self.ui.bandACrossCbx.addItems(cross_code_types)
        self.ui.bandBCrossCbx.addItems(cross_code_types)

        self.com_port_dialog = ComPortDialog(self)
        self.about_dialog = AboutDialog()

        self.ui.comPortBtn.clicked.connect(self.showComPortDialog)
        self.ui.portConnectBtn.clicked.connect(lambda: self.connectDevice())
        self.ui.aboutDialogBtn.clicked.connect(self.showAboutDialog)

        self.mem_channel_a_input_timer = QTimer()
        self.mem_channel_a_input_timer.setSingleShot(True)
        self.mem_channel_a_input_timer.setInterval(100)
        self.mem_channel_a_input_timer.timeout.connect(self.unlockMemChannelA)

        self.mem_channel_b_input_timer = QTimer()
        self.mem_channel_b_input_timer.setSingleShot(True)
        self.mem_channel_b_input_timer.setInterval(100)
        self.mem_channel_b_input_timer.timeout.connect(self.unlockMemChannelB)


        self.ui.bandAToneCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIA)
        self.ui.bandACrossCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIA)
        self.ui.bandAEncodeCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIA)
        self.ui.bandADecodeCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIA)

        self.ui.bandBToneCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIB)
        self.ui.bandBCrossCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIB)
        self.ui.bandBEncodeCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIB)
        self.ui.bandBDecodeCbx.currentIndexChanged.connect(self.updateFrequencyInfoUIB)

        self.mouseEventFilter = MouseClickEventFilter()
        self.mouseEventFilter.ui = self.ui
        self.ui.bandAWidget.installEventFilter(self.mouseEventFilter)
        self.ui.bandBWidget.installEventFilter(self.mouseEventFilter)

        self.disableUI()

        self.loadConfig()
    def closeDevice(self):
        self.device.command_buffer = []
        self.device.serial_conn.clear()
        self.device.serial_conn.close()
        self.device = None

    def connectDevice(self, com_port=None):
        if self.ui.portConnectBtn.text() == "Disconnect":
            if self.device != None and self.device.serial_conn != None and self.device.serial_conn.isOpen():
                self.device.setRealtimeFB(False)
                self.disableUI()
                if len(self.device.command_buffer) > 0:
                    QTimer.singleShot(100, self.closeDevice)
                else:
                    self.closeDevice()
                self.ui.portConnectBtn.setText("Connect")
                return
            

        if com_port == None or type(com_port) != str:
            com_port = self.port_name

        self.ui.portConnectBtn.setEnabled(False)
        self.ui.portConnectBtn.setText("Connecting")
        QApplication.processEvents()
        self.device = Device(com_port)
        self.device.verbose = self.verbose
        if(self.device.initConnection()):
            
            self.port_name = com_port
            self.status_bar_conn_status.setText(f"{self.port_name}: Connected")

            self.device.error_occurred.connect(self.errorOccurred)
            self.device.update_model_id.connect(self.updateModelId)
            self.device.update_serial_number.connect(self.updateSerialNumber)
            self.device.update_auto_feedback.connect(self.updateAutoFeedback)
            self.device.update_fw.connect(self.updateFW)
            self.device.update_band_control.connect(self.updateBandControl)
            self.device.update_band_mode.connect(self.updateBandMode)
            self.device.update_memory_mode.connect(self.updateMemoryMode)
            self.device.update_band_frequency.connect(self.updateFrequency)
            self.device.update_band_freq_info.connect(self.updateFrequencyInfo)
            self.device.update_tx.connect(self.updateTX)
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
            self.ui.portConnectBtn.setText("Disconnect")
            self.enableUI()
        else:
            self.ui.portConnectBtn.setText("Connect")
            self.errorOccurred("Could not connect to device", "COM Port Error")
            self.status_bar_conn_status.setText(f"{self.port_name}: Error")
            # self.device.getBand()
        self.ui.portConnectBtn.setEnabled(True)

    def loadConfig(self):
        if os.path.isfile(config_file_path):
            config = configparser.ConfigParser()
            config.read(config_file_path)

            if config.has_option('DEBUG', 'verbose'):
                self.verbose = config['DEBUG']['verbose'] == 'True'

            if config.has_option('SERIAL', 'autoconnect'):
                self.autoconnect = config['SERIAL']['autoconnect'] == 'True'

            if config['SERIAL']['port'] != "":
                self.port_name =  config['SERIAL']['port']
                self.status_bar_conn_status.setText(f"{self.port_name}: Not Connected")
                

    def saveConfig(self):
        config = configparser.ConfigParser()

        config['SERIAL'] = {
            'port': self.port_name,
            'autoconnect': self.autoconnect
        }

        config['DEBUG'] = {
            'verbose': self.verbose
        }
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    
    def showEvent(self, event):
        QApplication.processEvents()
        if self.autoconnect: QTimer.singleShot(10, lambda: self.connectDevice(self.port_name))
        
    def closeEvent(self, event):
        if self.device != None and self.device.serial_conn != None and self.device.serial_conn.isOpen():
            self.device.setRealtimeFB(False)
            QTimer.singleShot(100, self.__close)
            event.ignore()
    def __close(self):
        if self.device != None and self.device.serial_conn != None and self.device.serial_conn.isOpen():
            self.device.serial_conn.close()
        self.close()

    def showComPortDialog(self):
        self.com_port_dialog.show()
    def showAboutDialog(self):
        self.about_dialog.show()

    def enableUI(self):
        self.ui.bandControlCbx.setEnabled(True)
        self.ui.bandCbx.setEnabled(True)
        self.ui.txBtn.setEnabled(True)
        self.ui.upBtn.setEnabled(True)
        self.ui.dwnBtn.setEnabled(True)
        self.ui.volumeSlider.setEnabled(True)
        self.ui.backlightCbx.setEnabled(True)
        self.ui.btEnabledChbx.setEnabled(True)
        self.ui.gpsEnabledChbx.setEnabled(True)
        self.ui.gpsPcOutChbx.setEnabled(True)
        self.ui.tncModeCbx.setEnabled(True)
        self.ui.tncBandCbx.setEnabled(True)
        self.ui.beaconCbx.setEnabled(True)
        self.ui.beaconBtn.setEnabled(True)

        self.ui.bandAChannelCbx.setEnabled(True)
        self.ui.bandAMeter.setEnabled(True)
        self.ui.bandASquelchCbx.setEnabled(True)
        self.ui.bandAMonitorBtn.setEnabled(True)
        self.ui.bandAToneCbx.setEnabled(True)
        self.ui.bandACrossCbx.setEnabled(True)
        self.ui.bandAEncodeCbx.setEnabled(True)
        self.ui.bandADecodeCbx.setEnabled(True)
        self.ui.bandAPwrCbx.setEnabled(True)
        self.ui.bandAMemoryModeCbx.setEnabled(True)
        self.ui.bandAModeCbx.setEnabled(True)
        self.ui.bandAFreqText.setEnabled(True)

        self.ui.bandBChannelCbx.setEnabled(True)
        self.ui.bandBMeter.setEnabled(True)
        self.ui.bandBSquelchCbx.setEnabled(True)
        self.ui.bandBMonitorBtn.setEnabled(True)
        self.ui.bandBToneCbx.setEnabled(True)
        self.ui.bandBCrossCbx.setEnabled(True)
        self.ui.bandBEncodeCbx.setEnabled(True)
        self.ui.bandBDecodeCbx.setEnabled(True)
        self.ui.bandBPwrCbx.setEnabled(True)
        self.ui.bandBMemoryModeCbx.setEnabled(True)
        self.ui.bandBModeCbx.setEnabled(True)
        self.ui.bandBFreqText.setEnabled(True)
    def disableUI(self):
        self.ui.bandControlCbx.setEnabled(False)
        self.ui.bandCbx.setEnabled(False)
        self.ui.txBtn.setEnabled(False)
        self.ui.upBtn.setEnabled(False)
        self.ui.dwnBtn.setEnabled(False)
        self.ui.volumeSlider.setEnabled(False)
        self.ui.backlightCbx.setEnabled(False)
        self.ui.btEnabledChbx.setEnabled(False)
        self.ui.gpsEnabledChbx.setEnabled(False)
        self.ui.gpsPcOutChbx.setEnabled(False)
        self.ui.tncModeCbx.setEnabled(False)
        self.ui.tncBandCbx.setEnabled(False)
        self.ui.beaconCbx.setEnabled(False)
        self.ui.beaconBtn.setEnabled(False)

        self.ui.bandAChannelCbx.setEnabled(False)
        self.ui.bandAMeter.setEnabled(False)
        self.ui.bandASquelchCbx.setEnabled(False)
        self.ui.bandAMonitorBtn.setEnabled(False)
        self.ui.bandAToneCbx.setEnabled(False)
        self.ui.bandACrossCbx.setEnabled(False)
        self.ui.bandAEncodeCbx.setEnabled(False)
        self.ui.bandADecodeCbx.setEnabled(False)
        self.ui.bandAPwrCbx.setEnabled(False)
        self.ui.bandAMemoryModeCbx.setEnabled(False)
        self.ui.bandAModeCbx.setEnabled(False)
        self.ui.bandAFreqText.setEnabled(False)

        self.ui.bandBChannelCbx.setEnabled(False)
        self.ui.bandBMeter.setEnabled(False)
        self.ui.bandBSquelchCbx.setEnabled(False)
        self.ui.bandBMonitorBtn.setEnabled(False)
        self.ui.bandBToneCbx.setEnabled(False)
        self.ui.bandBCrossCbx.setEnabled(False)
        self.ui.bandBEncodeCbx.setEnabled(False)
        self.ui.bandBDecodeCbx.setEnabled(False)
        self.ui.bandBPwrCbx.setEnabled(False)
        self.ui.bandBMemoryModeCbx.setEnabled(False)
        self.ui.bandBModeCbx.setEnabled(False)
        self.ui.bandBFreqText.setEnabled(False)

        self.ui.bandAWidget.setStyleSheet("")
        self.ui.bandBWidget.setStyleSheet("")


    #SLOTS
    def errorOccurred(self, message, title="Error"):
        if self.device != None:
            self.closeDevice()
        self.disableUI()
        self.ui.portConnectBtn.setText("Connect")
        self.status_bar_conn_status.setText(f"{self.port_name}: Error")
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
        if self.device != None: self.device.setDualSingleBand(self.ui.bandControlCbx.currentIndex())
    def updateDualBand(self, opt):
        self.ui.bandControlCbx.setCurrentIndex(opt)

    def setTX(self):
        if self.in_tx:
            self.in_tx = False
            self.ui.txBtn.setStyleSheet("")
        else:
            self.in_tx = True
            self.ui.txBtn.setStyleSheet("QPushButton{background-color:red;color:white;}")
        if self.device != None: self.device.setTX(self.in_tx)
    def updateTX(self, enabled):
        self.in_tx = enabled
        if self.in_tx:
            self.ui.txBtn.setStyleSheet("background-color:red; color:white;")
        else:
            self.ui.txBtn.setStyleSheet("")
    
    def setVolume(self):
        if self.device != None: self.device.setAfGain(self.ui.volumeSlider.value())
    def updateVolume(self, level):
        self.ui.volumeSlider.blockSignals(True)
        self.ui.volumeSlider.setValue(level)
        self.ui.volumeSlider.blockSignals(False)

    def setBandControl(self):
        if self.device != None: self.device.setBandControl(self.ui.bandCbx.currentIndex())
    def updateBandControl(self, idx):
        self.ui.bandCbx.blockSignals(True)
        self.ui.bandCbx.setCurrentIndex(idx)
        self.ui.bandCbx.blockSignals(False)

        if idx == 0:
            self.ui.bandAWidget.setStyleSheet(f"#bandAWidget {self.styles['dark_mode' if self.is_dark_mode else 'default']['bandWidgetActive']}")
            self.ui.bandBWidget.setStyleSheet(f"#bandBWidget {self.styles['dark_mode' if self.is_dark_mode else 'default']['bandWidgetInactive']}")
        else:
            self.ui.bandAWidget.setStyleSheet(f"#bandAWidget {self.styles['dark_mode' if self.is_dark_mode else 'default']['bandWidgetInactive']}")
            self.ui.bandBWidget.setStyleSheet(f"#bandBWidget {self.styles['dark_mode' if self.is_dark_mode else 'default']['bandWidgetActive']}")

    def setAutoFeedback(self):
        if self.device != None: self.device.setRealtimeFB(self.ui.radioUpdateChbx.isChecked())
    def updateAutoFeedback(self, enabled):
        self.ui.radioUpdateChbx.blockSignals(True)
        self.ui.radioUpdateChbx.setChecked(enabled)
        self.ui.radioUpdateChbx.blockSignals(False)
    
    def setBacklight(self, idx):
        if self.device != None: self.device.setBacklight(idx)
    def updateBacklight(self, idx):
        self.ui.backlightCbx.blockSignals(True)
        self.ui.backlightCbx.setCurrentIndex(idx)
        self.ui.backlightCbx.blockSignals(False)

    def setBtEnabled(self, enabled):
        if self.device != None: self.device.setBtEnabled(enabled)
    def updateBtEnabled(self, enabled):
        self.ui.btEnabledChbx.blockSignals(True)
        self.ui.btEnabledChbx.setChecked(enabled)
        self.ui.btEnabledChbx.blockSignals(False)

    def setGPS(self):
        if self.device != None: self.device.setGPS(self.ui.gpsEnabledChbx.isChecked(), self.ui.gpsPcOutChbx.isChecked())
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
        if self.device != None: self.device.setMemoryMode(mode, band)
    def updateMemoryMode(self, band, mode_idx):
        if band == 0:
            self.ui.bandAMemoryModeCbx.blockSignals(True)
            self.ui.bandAMemoryModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandAMemoryModeCbx.blockSignals(False)

            if mode_idx == 0:
                self.ui.bandAFreqText.setEnabled(True)
                # self.ui.bandAChannelCbx.setEnabled(False)
            else:
                self.ui.bandAFreqText.setEnabled(False)
                # self.ui.bandAChannelCbx.setEnabled(True)

            if mode_idx == 1:
                self.ui.bandAChannelCbx.setEnabled(True)
            else:
                self.ui.bandAChannelCbx.setEnabled(False)
        else:
            self.ui.bandBMemoryModeCbx.blockSignals(True)
            self.ui.bandBMemoryModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandBMemoryModeCbx.blockSignals(False)

            if mode_idx == 0:
                self.ui.bandBFreqText.setEnabled(True)
                # self.ui.bandBChannelCbx.setEnabled(False)
            else:
                self.ui.bandBFreqText.setEnabled(False)
                # self.ui.bandBChannelCbx.setEnabled(True)

            if mode_idx == 1:
                self.ui.bandBChannelCbx.setEnabled(True)
            else:
                self.ui.bandBChannelCbx.setEnabled(False)

    def setBandModeA(self):
        self.device.setBandMode(self.ui.bandAModeCbx.currentIndex(), 0)
    def setBandModeB(self):
        self.device.setBandMode(self.ui.bandBModeCbx.currentIndex(), 1)
    def setBandMode(self, mode, band):
        if self.device != None: self.device.setBandMode(mode, band)
    def updateBandMode(self, band, mode_idx):
        if band == 0:
            self.ui.bandAModeCbx.blockSignals(True)
            self.ui.bandAModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandAModeCbx.blockSignals(False)
        else:
            self.ui.bandBModeCbx.blockSignals(True)
            self.ui.bandBModeCbx.setCurrentIndex(mode_idx)
            self.ui.bandBModeCbx.blockSignals(False)
    
    def unlockMemChannelA(self):
        self.mem_channel_a_input_lock = False
    def unlockMemChannelB(self):
        self.mem_channel_b_input_lock = False

    def setMemChannelA(self, idx):
        self.mem_channel_a_input_lock = True
        self.mem_channel_a_input_timer.stop()
        self.mem_channel_a_input_timer.start()
        self.setMemChannel(0, self.ui.bandAChannelCbx.currentText()[:3])
    def setMemChannelB(self, idx):
        self.mem_channel_b_input_lock = True
        self.mem_channel_b_input_timer.stop()
        self.mem_channel_b_input_timer.start()
        self.setMemChannel(1, self.ui.bandBChannelCbx.currentText()[:3])
    def setMemChannel(self, band_idx, channel):
        if self.device != None: self.device.setMemChannel(str(channel).rjust(3,'0'), band_idx)

    def updateMemChannel(self, band_idx, channel):
        if band_idx == 0 and not self.mem_channel_a_input_lock:
            self.ui.bandAChannelCbx.blockSignals(True)
            self.ui.bandAChannelCbx.setCurrentIndex(int(channel))
            self.ui.bandAChannelCbx.blockSignals(False)
        elif band_idx == 1 and not self.mem_channel_b_input_lock:
            self.ui.bandBChannelCbx.blockSignals(True)
            self.ui.bandBChannelCbx.setCurrentIndex(int(channel))
            self.ui.bandBChannelCbx.blockSignals(False)

    def setOpenSquelchA(self):
        self.band_a_squelch = self.device.band_a_squelch
        self.openSquelch(0)
    def setOpenSquelchB(self):
        self.band_b_squelch = self.device.band_b_squelch
        self.openSquelch(1)
    def openSquelch(self, band_idx):
        if self.device != None: self.device.setSquelch(band_idx, 0)

    def setSquelchA(self, level):
        self.setSquelch(0, level)
    def setSquelchB(self, level):
        self.setSquelch(1, level)
    def setSquelch(self, band_idx, level):
        if self.device != None: self.device.setSquelch(band_idx, level)
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
        if self.device != None: self.device.setSquelch(0, self.band_a_squelch)
    def setClosedSquelchB(self):
        if self.device != None: self.device.setSquelch(1, self.band_b_squelch)
    
    def setTNC(self):
        if self.device != None: self.device.setTNC(self.ui.tncModeCbx.currentIndex(), self.ui.tncBandCbx.currentIndex())
    def updateTNC(self, mode, band_idx):
        self.ui.tncModeCbx.blockSignals(True)
        self.ui.tncModeCbx.setCurrentIndex(mode)
        self.ui.tncModeCbx.blockSignals(False)

        self.ui.tncBandCbx.blockSignals(True)
        self.ui.tncBandCbx.setCurrentIndex(band_idx)
        self.ui.tncBandCbx.blockSignals(False)

    def setBeaconType(self):
        if self.device != None: self.device.setBeaconType(self.ui.beaconCbx.currentIndex())
    def updateBeaconType(self, beacon_type_idx):
        self.ui.beaconCbx.blockSignals(True)
        self.ui.beaconCbx.setCurrentIndex(beacon_type_idx)
        self.ui.beaconCbx.blockSignals(False)
    def toggleBeacon(self):
        if self.device != None: self.device.toggleBeacon()

    def setOutputPowerA(self, pwr):
        self.setOutputPower(0, pwr)
    def setOutputPowerB(self, pwr):
        self.setOutputPower(1, pwr)
    def setOutputPower(self, band_idx, pwr):
        if self.device != None: self.device.setOutputPower(band_idx, pwr)
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
        if self.device != None: self.device.upButton()
    def downButton(self):
        if self.device != None: self.device.downButton()
    
    def setFrequencyA(self):
        self.setFrequency(self.ui.bandAFreqText.text(), 0)
    def setFrequencyB(self):
        self.setFrequency(self.ui.bandBFreqText.text(), 1)
    def setFrequency(self, frequency, band_idx):
        if self.device != None: self.device.setBandFrequency(frequency, band_idx)
    def updateFrequency(self, band, freq):
        if band == 0:
            self.ui.bandAFreqText.blockSignals(True)
            self.ui.bandAFreqText.setText(freq)
            self.ui.bandAFreqText.blockSignals(False)
        else:
            self.ui.bandBFreqText.blockSignals(True)
            self.ui.bandBFreqText.setText(freq)
            self.ui.bandBFreqText.blockSignals(False)

    def bandTCodeUpdate(self, encode_cbx: QComboBox, decode_cbx: QComboBox, cross_cbx: QComboBox, info: ChannelFrequency):
        
        if (info.band == 0 and (self.band_a_tone_type != info.getToneType() or self.band_a_cross_type != info.cross_encode)) or (info.band == 1 and (self.band_b_tone_type != info.getToneType() or self.band_b_cross_type != info.cross_encode)):
            
            encode_cbx.blockSignals(True)
            decode_cbx.blockSignals(True)
            cross_cbx.blockSignals(True)

            encode_cbx.clear()
            decode_cbx.clear()

            encode_items = []
            decode_items = []
            if info.getToneType() == 1 or info.getToneType() == 2:
                encode_items = self.ctcss_tones
            elif info.getToneType() == 3:
                encode_items = self.dcs_tones
            elif info.getToneType() == 4:
                if info.cross_encode == 0:
                    encode_items = self.dcs_tones
                    decode_items = ['Off']
                elif info.cross_encode == 1:
                    encode_items = self.ctcss_tones
                    decode_items = self.dcs_tones
                elif info.cross_encode == 2:
                    encode_items = self.dcs_tones
                    decode_items = self.ctcss_tones
                elif info.cross_encode == 3:
                    encode_items = self.ctcss_tones
                    decode_items = self.ctcss_tones

            encode_cbx.addItems(encode_items)
            decode_cbx.addItems(decode_items)

            if info.band == 0:
                self.band_a_cross_type = info.cross_encode
                self.band_a_tone_type = info.getToneType()
            else:
                self.band_b_cross_type = info.cross_encode
                self.band_b_tone_type = info.getToneType()

            if info.getToneType() == 1:
                encode_cbx.setCurrentIndex(info.tone_freq)
            elif info.getToneType() == 2:
                encode_cbx.setCurrentIndex(info.ctcss_freq)
            elif info.getToneType() == 3:
                encode_cbx.setCurrentIndex(info.dcs_freq)
            elif info.getToneType() == 4:
                if info.cross_encode == 0:
                    encode_cbx.setCurrentIndex(info.dcs_freq)
                    decode_cbx.setCurrentIndex(0)
                elif info.cross_encode == 1:
                    encode_cbx.setCurrentIndex(info.tone_freq)
                    decode_cbx.setCurrentIndex(info.dcs_freq)
                elif info.cross_encode == 2:
                    encode_cbx.setCurrentIndex(info.dcs_freq)
                    decode_cbx.setCurrentIndex(info.ctcss_freq)
                elif info.cross_encode == 3:
                    encode_cbx.setCurrentIndex(info.tone_freq)
                    decode_cbx.setCurrentIndex(info.ctcss_freq)

            cross_cbx.setCurrentIndex(info.cross_encode)

            encode_cbx.blockSignals(False)
            decode_cbx.blockSignals(False)
            cross_cbx.blockSignals(False)
    def bandTCodeUpdateUI(self, tone_cbx: QComboBox, encode_cbx: QComboBox, decode_cbx: QComboBox, cross_cbx: QComboBox, info: ChannelFrequency):
        tone_type = tone_cbx.currentIndex()
        info.setToneType(tone_type)
        
        self.bandTCodeUpdate(encode_cbx, decode_cbx, cross_cbx, info)
        
        tone_type = info.getToneType()
        if tone_type == 4:
            info.cross_encode = cross_cbx.currentIndex()

        self.bandTCodeUpdate(encode_cbx, decode_cbx, cross_cbx, info)

        if tone_type == 1:
            info.tone_freq = encode_cbx.currentIndex()
        elif tone_type == 2:
            info.ctcss_freq = encode_cbx.currentIndex()
        elif tone_type == 3:
            info.dcs_freq = encode_cbx.currentIndex()
        elif tone_type == 4:
            if info.cross_encode == 0:
                info.dcs_freq = encode_cbx.currentIndex()
            elif info.cross_encode == 1:
                info.tone_freq = encode_cbx.currentIndex()
                info.dcs_freq = decode_cbx.currentIndex()
            elif info.cross_encode == 2:
                info.dcs_freq = encode_cbx.currentIndex()
                info.ctcss_freq = decode_cbx.currentIndex()
            elif info.cross_encode == 3:
                info.tone_freq = encode_cbx.currentIndex()
                info.ctcss_freq = decode_cbx.currentIndex()

    def updateFrequencyInfoUIA(self):
        if self.band_a_current_channel_frequency_info != None:
            info = self.band_a_current_channel_frequency_info
            self.bandTCodeUpdateUI(self.ui.bandAToneCbx, self.ui.bandAEncodeCbx, self.ui.bandADecodeCbx, self.ui.bandACrossCbx, info)
            self.updateFrequencyInfo(info)
            self.setFrequencyInfo(info)
    def updateFrequencyInfoUIB(self):
        if self.band_b_current_channel_frequency_info != None:
            info = self.band_b_current_channel_frequency_info
            self.bandTCodeUpdateUI(self.ui.bandBToneCbx, self.ui.bandBEncodeCbx, self.ui.bandBDecodeCbx, self.ui.bandBCrossCbx, info)
            self.updateFrequencyInfo(info)
            self.setFrequencyInfo(info)
    def updateFrequencyInfo(self, info: ChannelFrequency):
        if info.band == 0:
            self.band_a_current_channel_frequency_info = info
            self.ui.bandAFreqText.blockSignals(True)
            self.ui.bandAFreqText.setText(info.frequency)
            self.ui.bandAFreqText.blockSignals(False)

            self.ui.bandAToneCbx.blockSignals(True)
            self.ui.bandAToneCbx.setCurrentIndex(info.getToneType())
            self.ui.bandAToneCbx.blockSignals(False)

            
            if info.getToneType() == 0:
                self.ui.bandAEncodeWrapper.setVisible(False)
                self.ui.bandACrossWrapper.setVisible(False)
                self.ui.bandADecodeWrapper.setVisible(False)
            elif info.getToneType() == 4:
                self.ui.bandAEncodeWrapper.setVisible(True)
                self.ui.bandACrossWrapper.setVisible(True)
                self.ui.bandADecodeWrapper.setVisible(True)
            else:
                self.ui.bandAEncodeWrapper.setVisible(True)
                self.ui.bandACrossWrapper.setVisible(False)
                self.ui.bandADecodeWrapper.setVisible(False)

            self.bandTCodeUpdate(self.ui.bandAEncodeCbx, self.ui.bandADecodeCbx, self.ui.bandACrossCbx, info)

        else:
            self.band_b_current_channel_frequency_info = info
            self.ui.bandBFreqText.blockSignals(True)
            self.ui.bandBFreqText.setText(info.frequency)
            self.ui.bandBFreqText.blockSignals(False)

            self.ui.bandBToneCbx.blockSignals(True)
            self.ui.bandBToneCbx.setCurrentIndex(info.getToneType())
            self.ui.bandBToneCbx.blockSignals(False)

            
            if info.getToneType() == 0:
                self.ui.bandBEncodeWrapper.setVisible(False)
                self.ui.bandBCrossWrapper.setVisible(False)
                self.ui.bandBDecodeWrapper.setVisible(False)
            elif info.getToneType() == 4:
                self.ui.bandBEncodeWrapper.setVisible(True)
                self.ui.bandBCrossWrapper.setVisible(True)
                self.ui.bandBDecodeWrapper.setVisible(True)
            else:
                self.ui.bandBEncodeWrapper.setVisible(True)
                self.ui.bandBCrossWrapper.setVisible(False)
                self.ui.bandBDecodeWrapper.setVisible(False)

        self.bandTCodeUpdate(self.ui.bandBEncodeCbx, self.ui.bandBDecodeCbx, self.ui.bandBCrossCbx, info)
    def setFrequencyInfoA(self):
        info = ChannelFrequency()
        self.setFrequencyInfo(0, info)
    def setFrequencyInfoB(self):
        info = ChannelFrequency()
        self.setFrequencyInfo(1, info)
    def setFrequencyInfo(self, info):
        self.device.setBandFrequencyInfo(info)

class AboutDialog(QDialog):

    def __init__(self, parent: MainWindow=None):
        super().__init__(parent)
        
        # Setup UI
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        self.ui.closeBtn.clicked.connect(self.hide)

class ComPortDialog(QDialog):

    parent: MainWindow = None

    def __init__(self, parent: MainWindow=None):
        super().__init__(parent)

        self.parent = parent
        
        # Setup UI
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
        