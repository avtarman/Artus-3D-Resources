import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI

xg = 'c176p[+40,+20,+20,+30,+10,+00,+00,+10,+00,+00,+10,+00,+00,+10,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end\n'
ag = 'c176p[+40,+20,+20,+30,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end\n'
bg = 'c176p[+40,+20,+20,+30,+40,-20,+35,+40,-05,+40,+35,+05,+40,+30,+05,+35]v[+99,+99,+99,+99,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95]end\n'

cg = 'c176p[+30,+20,+00,+00,+00,-05,+00,+10,-05,+00,+10,+05,+00,+10,+05,+00]v[+99,+99,+99,+99,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95]end\n'
dg = 'c176p[+00,+35,+00,+00,+00,+00,+00,+10,-05,+00,+10,+05,+00,+50,+20,+40]v[+99,+99,+99,+99,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95]end\n'
eg = 'c176p[+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end\n'

aa = 'c176p[+40,+20,+30,+30,+35,-15,+35,+40,-05,+40,+35,+05,+40,+30,+05,+35]v[+99,+99,+99,+99,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95,+95]end'

artus3d = Artus3DAPI(target_ssid='ArtusMK6RH',port='COM11',communication_method=UART,hand='left')
artus3d.start_connection()

# artus3d.send_target_command(xg)
input("grab")
artus3d.send_target_command(ag)
t = time.perf_counter()
while True:
    if time.perf_counter() - t > 0.35:
        break
artus3d.send_target_command(bg)

input("drop")
artus3d.send_target_command(ag)
input("drop2")
artus3d.send_target_command(eg)
