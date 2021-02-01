from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import yaml
import colorsys
import os
import time
import psutil
import time
import subprocess

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

if not checkIfProcessRunning('openrgb'):
    subprocess.Popen(["./openrgb", "--gui", "--startminimized", "--server"], cwd="/home/itsco/Hardware/OpenRGB/")
    time.sleep(5)

client = OpenRGBClient()

mobo = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
ram1 = client.get_devices_by_type(DeviceType.DRAM)[0]
ram2 = client.get_devices_by_type(DeviceType.DRAM)[1]
fans = client.get_devices_by_type(DeviceType.LEDSTRIP)[0]
gpu = client.get_devices_by_type(DeviceType.GPU)[0]
mouse = client.get_devices_by_type(DeviceType.MOUSE)[0]
keyboard = client.get_devices_by_type(DeviceType.KEYBOARD)[0]
led_strip = client.get_devices_by_type(DeviceType.LEDSTRIP)[1]

with open('/home/itsco/.cache/wal/colors.yml') as file:
    colors = yaml.full_load(file)
    hex_color = colors["colors"]["color2"]
    hex_color2 = colors["colors"]["color3"]
    hsv = colorsys.rgb_to_hsv(RGBColor.fromHEX(hex_color).red, RGBColor.fromHEX(hex_color).green, RGBColor.fromHEX(hex_color).blue)
    hsv2 = colorsys.rgb_to_hsv(RGBColor.fromHEX(hex_color2).red, RGBColor.fromHEX(hex_color2).green, RGBColor.fromHEX(hex_color2).blue)
    mobo.set_color(RGBColor.fromHSV(hsv[0] * 360, 100, 100))
    ram1.set_color(RGBColor.fromHSV(hsv[0] * 360, 100, 100))
    ram2.set_color(RGBColor.fromHSV(hsv2[0] * 360, 100, 100))
    fans.set_color(RGBColor.fromHSV(hsv[0] * 360, 100, 100))
    gpu.set_mode('static')
    gpu.set_color(RGBColor.fromHSV(hsv2[0] * 360, 100, 100))
    mouse.set_mode('static')
    mouse.set_color(RGBColor.fromHSV(hsv2[0] * 360, 100, 100), 0, 1)
    mouse.set_color(RGBColor.fromHSV(hsv[0] * 360, 100, 100), 1, 2)
    keyboard.set_color(RGBColor.fromHSV(hsv2[0] * 360, 100, 100))
    led_strip.set_color(RGBColor.fromHSV(hsv[0] * 360, 100, 100))
    os.system("liquidctl --device 2 initialize")
    os.system("liquidctl --device 2 set led color fixed 'hsv(" + str(hsv2[0] * 360) + ",100,100)'") 
