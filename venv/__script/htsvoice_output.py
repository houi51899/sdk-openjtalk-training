# !/usr/bin/env python3
import os
import time

start_time = time.time()
timecounter = 0
FLAG = False
htsvoice_path = "/root/tools/HTS-demo_NIT-ATR503-M001/voices/qst001/ver1/nitech_jp_atr503_m001.htsvoice"
model_log_path = "/root/tools/HTS-demo_NIT-ATR503-M001/log"


while True:
    time.sleep(20)
    if os.path.exists(htsvoice_path):
        os.system("echo " + "htsvoice file generated!")
        break

    timecounter = int(time.time() - start_time)
    os.system("echo " + " waiting for model generation : " + str(timecounter) + "s passed.")








