import subprocess
from time import sleep
f = open("top.csv", "r")
links = f.read()
p = subprocess.Popen(['./utils/LiteSpeedTest/lite','--config','./utils/LiteSpeedTest/config.json','--test',links], stdout=subprocess.PIPE)