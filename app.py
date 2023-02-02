import subprocess
import threading
from dns import resolver

import requests

import asyncio
from requests import Session, HTTPError
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE, DEFAULT_RETRIES, DEFAULT_POOLBLOCK

"""Problem is here"""
# def myResolver(host, dnssrv):
#     res = resolver.Resolver()
#     res.nameservers = dnssrv
#
#     answers = res.resolve(host)
#
#     for rdata in answers:
#         print(rdata.address)
#
# myResolver("scan.sudoer.net",["104.16.209.12"])

# def background(f):
#     def wrapped(*args, **kwargs):
#         return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
#
#     return wrapped
#
# @background
# def run_script(ip):
#
#     script = "timeMil=$(gtimeout 2 curl -s -w \"TIME: %{time_total}\n\" --tlsv1.2 -servername scan.sudoer.net -H " \
#                  "'Host: scan.sudoer.net' --resolve scan.sudoer.net:443:\"" + ip + "\" https://scan.sudoer.net | grep " \
#                                                                                    "\"TIME\" | tail -n 1 | awk '{print $2}' |" \
#                                                                                    " xargs -I {} echo \"{} * 1000 /1\" | bc ) " \
#                                                                                    "&& echo $timeMil "
#     proc = subprocess.Popen(['bash', '-c', script], stdout=subprocess.PIPE)
#     if proc.stdout.read().decode() != "\n":
#         print("OK " + ip)
#         print("----------------")
#     else:
#         print("failed "+ip)

results = []
file = open("top.csv", "r")
inputs = file.read().split(',\n')
for url in inputs:
    result = subprocess.run(['ping', url, '-c', '1'], stdout=subprocess.PIPE)
    try:
        resolved_ip = result.stdout.decode("utf-8").split('\n')[0].split("(")[1].split(")")[0]
        results.append({'provider':url,'ip':resolved_ip})
    except:
        pass


for r in results:
    print(f"{r['provider']}: {r['ip']}")
    print("---------------------------")

res = requests.get("http://bot.sudoer.net/result.cf")
ips = res.text.split("\n")[1:len(res.text.split("\n")) - 1]
#
#
# for ip in ips:
#     run_script(ip)




