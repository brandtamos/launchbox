#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

lcd = Adafruit_CharLCD()

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

lcd.begin(16, 1)


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

while 1:
    lcd.clear()
    ipaddr = run_cmd(cmd)
    lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\2'))
    lcd.message('IP %s\3' % (ipaddr))
    lcd.message('Hey look\4')
    lcd.message('This works')
    sleep(2)
