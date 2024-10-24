<p align="center">
<img src="./icon.png" />
</p>

# D74/75 CAT Control Software

This software is for controlling the Kenwood D74/75 via CAT commands from your PC, Mac, or Linux computer.

## How to use
You can connect to your radio either via USB or through Bluetooth. If you plan on using the internal KISS TNC, make sure to set your Interface opposite of your CAT connection. For example, if you are using USB for CAT control, set your KISS interface to Bluetooth, otherwise CAT Control will disconnect from the radio.

The KISS interface can be changed via Menu [983].

## Memory Channels
Memory channels are defaulted in the CAT control software to just the numbers. If you would like add names to your channels, use the additional <i>mnd.py</i> file with the 
argument -p [COMPORT]. This will dump your memory channel names to <i>channel_memory.json</i> and will load next time you start the CAT Control software.

The file can be located in the D75 CAT Control folder in your HOME directory.

You will need to dump the memory channel names if there is any addition, removal, or name change of the channel.

<i>Note: The way that the radio reports the current channel over serial, it is not possible to preload both bands current channel. Once you switch bands, it will load the current band into the CAT Control software.</i>

## Config
Some additional settings can be set in the config.cfg file. The config file can be located in the D75 CAT Control folder in your HOME directory.

| Section | Variable    | Default      | Description |
|---------|-------------|--------------|-------------|
| SERIAL  | port        | <i>empty</i> | Defines the serial COM port.<br/>Autosaved based on your previous connection. |
| SERIAL  | autoconnect | False        | Can be set to <i>True</i> if you wish to attempt a<br/>connection to your last COM port on startup. |
| GPS     | alt_format  | I            | I = Imperial, M = Metric |
| GPS     | spd_format  | I            | I = Imperial, M = Metric |
| DEBUG   | verbose     | False        | Set to True if you want all data sent and received<br/>to print to console. |
|||||




## Future Development
As this program is in beta stage of development, there is always room for improvement.

Some things that will be coming in future updates.
* Read GPS, APRS, and KISS data
* Open TCP/IP ports for other software to access CAT control, GPS data, and APRS data.

If you come across any issues or wish to have features added, please let me know at <a href="mailto:k7dmg@protonmail.com">k7dmg@protonmail.com</a>.

## License

D75 CAT Control is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

D75 CAT Control is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with D75 CAT Control. If not, see <https://www.gnu.org/licenses/>.