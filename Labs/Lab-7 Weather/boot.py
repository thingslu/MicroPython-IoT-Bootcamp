# This file is executed on every boot (including wake-boot from deepsleep)
#-----------------------------------------------------
# .) Init Display
# 1) connect to the network details stored in myconfig 
#    beep if no network connection
# 2) if connect , get the network time
# 3) load utility functions from upysh 
#
# x) start ftp server 
#-----------------------------------------------------
# add path to library folder in flash
try:
    import sys
    sys.path[1] = '/flash/lib'
    mkdir('/flash/lib')
except:
    pass 
#helper functions    
import m5stack
from windows import *
borders(clear=False)
header('boot.py')
mainwindow(clear=False)
home()

def beepHappy():
    #Happy 
    m5stack.tone(4200, 80)
    m5stack.tone(2800, 100)
    m5stack.tone(4200, 60)

def beepSad():
    #Sad
    m5stack.tone(1200, duration=100)
    m5stack.tone(700, duration=120)
    m5stack.tone(300, duration=100)

def log(text):
    print(text)
    writeln(text)

# Connect to WiFi 
def connectWifi():
    "Connect to WiFi"
    import network, time
    #read network info from : myconfig.py
    try:
        from myconfig import wifi_ssid , wifi_psk
    except:
        print('No Network configuration file found')
        #todo: show help how to create one 
        return False
    wlan = network.WLAN(network.STA_IF)
    tmo = 80
    if not wlan.isconnected():
        print('connecting to network : {}'.format(wifi_ssid))
        wlan.active(True)
        wlan.connect(wifi_ssid, wifi_psk)
        #Wait for WiFi connection 
        while not wlan.isconnected():
            if tmo == 0:
                break
            print(".", end="")
            tmo -= 1
            time.sleep_ms(200)
        print()
    try: 
        log( 'IP: {}'.format( wlan.ifconfig()[0]  ))
        return True
    except:
        pass
    if not wlan.isconnected():
        beepSad()
        return False

def getNetworkTime(timezone = "CET-1CEST"):
    "get time via NTP for Central Europe"
    # Lobo Specific 
    import machine
    rtc = machine.RTC()
    rtc.init((2018, 01, 01, 12, 12, 12))
    rtc.ntp_sync(server= "", tz=timezone, update_period=3600)
    #need to wait a bit 
    tmo = 100
    while not rtc.synced():
        tmo=tmo-1
        if tmo==0:
            break
        time.sleep_ms(10)

#simplify filesystem access from the prompt
from upysh import *

# Connect to WiFi 
log('Connect to WiFi...')
connected = connectWifi()
if connected:
    #log('Get network Time...')
    getNetworkTime()
    fmt="%d-%m-%Y, %T %Z" #Europe
    #fmt="%b %d %Y, %r %Z" #US
    log(time.strftime(fmt,time.localtime()))
#----------
# Start FTP Server
#-----------
StartFTP = False
if StartFTP:
    log('Start FTP Server...')
    from network import ftp,telnet
    ftp.start(user="micro", password="python")
    telnet.start(user="micro", password="python")
    time.sleep(1)
    log("FTP server: {}".format(ftp.status()[2]))
    log("Telnet server: {}".format(telnet.status()[2]))
 
import gc;gc.collect()
