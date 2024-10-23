"""
File name memory_name_dump.py:
Project Name: D75 CAT Control
Author: Ben Kozlowski - K7DMG
Created: 2024-10-22
Version: 1.0.0
Description: 
    Dump the memory channel names to JSON format.

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
Dependencies: PySide6==6.7.1, PySide6_Addons==6.7.1, PySide6_Essentials==6.7.1
"""

import serial, json, argparse

mem_arr = []
port = ""
json_file_name = "channel_memory.json"

def waitCommand(ser, cmd):
    ser.write(cmd)
    # print("MCP:", cmd)
    while True:
        d75_data = ser.read_all()
        if len(d75_data) > 0:
            # print("D75:", d75_data)
            return d75_data

def decodeMem(data):
    global mem_arr
    for i in range(0, 256, 16):
        s = data[i:i+16].decode("UTF-8").rstrip('\x00')
        mem_arr.append(s)

def dumpMemory():
    global mem_arr
    page = 256
    d75 = serial.Serial(port, 9600)
    if not waitCommand(d75, "ID\r".encode("UTF-8")) == b'ID TH-D75\r': return
    if not waitCommand(d75, "0M PROGRAM\r".encode("UTF-8")) == b'0M\r': return
    for i in range(63):
        addr = (page + i).to_bytes(2, 'big') + b'\x00\x00'
        data = waitCommand(d75, b'R' + addr)
        if data.startswith(b'W'):
            decodeMem(data[5:])
            waitCommand(d75, b'\x06')
    waitCommand(d75, b'E')

    mem_arr = mem_arr[:-8]

    with open(json_file_name, 'w') as f:
        f.write(json.dumps(mem_arr))



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
                    prog='D75 Memory Name Dump',
                    description='Dump your D75 Memory Names to JSON',
                    epilog='Created by K7DMG')
    parser.add_argument('-p', '--port')
    args = parser.parse_args()

    port = args.port
    try:
        dumpMemory()
    except KeyboardInterrupt:
        pass