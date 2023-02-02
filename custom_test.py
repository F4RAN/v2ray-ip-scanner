import base64
import datetime
import json
import sys
from subprocess import Popen, PIPE, CalledProcessError

import requests

from configs.default import default_config

input_file = sys.argv[1]

port = default_config['port'] # Put your selected port here
id = default_config["id"] # Put your v2ray config uuid here
protocol = default_config['protocol'] # Put your v2ray connection protocol here (like:ws,tcp,...)
host = default_config['host'] # Put your Host Address here
sni = default_config['sni'] # Put your sni Here
path = default_config['path'] # Put your path here, if you don't set path set "/"
tls = default_config['tls'] # if set "tls" means you are using tls connection

if input_file != "top":
    input_file = "links"
    ips = requests.get("http://bot.sudoer.net/result.cf")
    ips = ips.text.split("\n")
    ips = ips[1:len(ips) - 1]
    vmess_list = []
    parts = int(len(ips) / 500) + 1
    print(f"Scanning f{len(ips)} ips http://bot.sudoer.net/result.cf")
    print(f"We have ({parts}) parts of ips for scan")
    selected_part = int(input("Please select a part to scan: "))
    if selected_part > parts or selected_part < 0:
        print("not in rage")
        exit()
    for ip in ips[selected_part * 500:(selected_part + 1) * 500]:
        vmess = {
            "v": "2",
            "ps": f"F4RAN-{'-'.join(ip.split('.'))}",
            "add": f"{ip}",
            "port": f"{port}",
            "id": f"{id}",
            "aid": 0,
            "net": f"{protocol}",
            "type": "none",
            "host": f"{host}",
            "sni": f"{sni}",
            "path": f"{path}",
            "tls": f"{tls}"
        }
        vmess = json.dumps(vmess)
        message = str(vmess)
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_vmess = base64_bytes.decode('ascii')
        base64_vmess = "vmess://" + base64_vmess
        vmess_list.append(base64_vmess)
    links = ""

    for vmess in vmess_list:
        links += vmess + '\n'

    file = open('links.csv', 'w')
    file.write(links)
    file.close()
else:
    print("Scanning custom inputs in top.csv")
output_name = "output-" + input_file + "-" + str(datetime.datetime.now())
cmd = ['./utils/LiteSpeedTest/lite', '--config', './utils/LiteSpeedTest/config.json', '--test', f"./{input_file}.csv"]
with Popen(cmd, bufsize=5, stderr=PIPE) as p:
    for line in p.stderr:
        for l in line.decode("utf-8").split("\n"):
            if l.find("servers") != -1:
                ids = "[" + l.split("[")[1].split("]")[0] + "]"
                ids = json.loads(ids)
            if l.find("maxspeed") != -1:
                response = json.loads("{" + l.split("{")[1].split("}")[0] + "}")
                if response['speed'] != "N/A":
                    conf = {}
                    for i in ids:
                        if i['id'] == response['id']:
                            conf = i
                    records = False
                    try:
                        latest = open(f"{output_name}.csv", "r")
                        records = latest.read()
                        latest.close()
                    except:
                        pass
                    file = open(f"{output_name}.csv", "w")
                    printing_record = response['maxspeed'] + " |#| " + conf["remarks"] + " |#| " + conf[
                        'server'] + " |#| " + response['maxspeed'] + \
                                      " |#| " + response['speed'] + "--- " + str(conf["id"])
                    flag = False
                    if records:
                        recs = records.split("\n")
                        for i, r in enumerate(recs):

                            if len(r) > 0 and r.split("--- ")[1] == str(conf['id']):
                                splited = r.split(" |#| ")
                                splited[0] = response['maxspeed']
                                recs[i] = " |#| ".join(splited)
                                records = "\n".join(recs)
                                storing_record = records
                                flag = True
                                break

                    else:
                        flag = True
                        storing_record = printing_record + "\n"
                    if not flag: storing_record = records + printing_record + "\n"
                    print(printing_record)
                    file.write(storing_record)
                    file.close()


def sort_file():
    file = False
    try:
        file = open(f"{output_name}.csv", "r")
    except:pass
    if file:
        nsorted_records = file.read()
        if nsorted_records:
            ns_recs = nsorted_records.split("\n")
            speed_array = []

            for i, r in enumerate(ns_recs[:len(ns_recs) - 1]):
                maxspeed = r.split(" |#| ")[0]
                if maxspeed.find("KB") != -1:
                    maxspeed = float(maxspeed.split("KB")[0]) * 10 ** 3
                elif maxspeed.find("MB") != -1:
                    maxspeed = float(maxspeed.split("MB")[0]) * 10 ** 6
                else:
                    maxspeed = int(maxspeed.split(".")[0])

                speed_array.append((i, maxspeed))
            speed_array = sorted(speed_array, key=lambda x: x[1], reverse=True)
            sorted_file = ""
            for j in speed_array:
                sorted_file += ns_recs[j[0]] + "\n"
            file = open(f"{output_name}.csv", "w")
            file.write(sorted_file)
            file.close()

sort_file()
if p.returncode != 0:
    raise CalledProcessError(p.returncode, p.args)
