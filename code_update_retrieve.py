import urequests
import network
import os
import sys
import time

wifis = [("RET - IOT", "UwolnicMajonez!"), ("pretty-fly-for-a-wifi","ExtrAT3st"), ("Bapunzel","SayUpBig")]
network_choice = 1
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.5)
wlan.active(True)
wlan.connect(wifis[network_choice][0])

last_attempts = 0
max_tries = 22
while wlan.isconnected() is False and last_attempts < max_tries:
    print(f"Waiting for connection... attempts: {last_attempts}")
    time.sleep(1)
    last_attempts += 1

if last_attempts == max_tries:
    print("Connection failed")
    wlan.active(False)
    sys.exit()
    
print(wifis[network_choice][0])
print(wlan.ifconfig())
time.sleep(3)

# target = "https://github.com/f3db02a9-553a-4ee3-bb16-f48c78f182f4"
# target = "https://introcs.cs.princeton.edu/python/14array/sample.py"
target = "https://raw.githubusercontent.com/RoushAH/starlights/main/test_saddle.py"

try:

    r = urequests.get(target)
    print(f"Response status code: {r.status_code}")
    print("GREAT SUCCESS") if r.status_code == 200 else print("Whomp, whomp")
    tgt_file = target.split("/").pop() 
    with open(tgt_file, "w") as results_out:
        results_out.write(r.text)

    print(f"Is {tgt_file} in memory? {tgt_file in os.listdir()}")
    line = f"import {tgt_file[:-3]}"
    print(f"Attempting to execute `{line}`")
    try:
        exec(line)
    except Exception as e:
        print(f"Failed, due to \n {e}")

    print("Donezo")

except Exception as e:
    print("Ruh, roh",e)

finally :
    wlan.disconnect()
    wlan.active(False)
    while wlan.isconnected() or wlan.active():
        time.sleep(1)
        print("Disconnecting")
    print("Disconnected")