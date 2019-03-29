# !/usr/bin/env python3
import os
import time

start_time = time.time()
timecounter = 0
FLAG = False
htsvoice_path = "/root/HTS-demo_NIT-ATR503-M001/voices/qst001/ver1/nitech_jp_atr503_m001.htsvoice"
model_log_path = "/root/HTS-demo_NIT-ATR503-M001/log"


while True:
    if os.path.exists(htsvoice_path):
        print("htsvoice file generated!")
        break

    timecounter = int(time.time() - start_time)
    if timecounter % 10 == 0:
        if FLAG is True:
            os.system("echo " +"'waiting for model generation : '" + str(timecounter) +"'s passed.'" )
            FLAG = False
        else:
            continue
    else:
        FLAG = True

print("program terminated")





