import urequests
import network
import os
import secrets


def do_connect(wifi_num):
    network_choice = wifi_num
    wifis = secrets.wifis
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(*wifis[network_choice])


def do_test():
    # target = "https://github.com/f3db02a9-553a-4ee3-bb16-f48c78f182f4"
    target = "https://introcs.cs.princeton.edu/python/14array/sample.py"

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


def do_update_all():
    # Get the name of every file in the directory, and update them all
    # Currently risky. UNTESTED
    REMOTE_ACCESS = "http://url.for.remote.repo"
    if REMOTE_ACCESS[-1] != "/":
        REMOTE_ACCESS = REMOTE_ACCESS + "/"

    for file in os.listdir(""):
        r = urequests.get(REMOTE_ACCESS + file)
        if r.status_code == 200:
            with open(file, "w") as f:
                f.write(r.text)


do_connect(0)
do_test()
