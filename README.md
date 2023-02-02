# v2ray-ip-scanner
Scan many ip in a vmess ( or other ) config by setting ip and find out ping and speed

## Installation
at the first you must install project dependencies:
`pip3 install requirements.txt`


then you must build ./utils/LiteSpeedTest
more details in:
`https://github.com/xxf098/LiteSpeedTest`

## Run:
you can run project with this command:
`python3 custom_test.py top`
test run on top.csv file and you can change it and put into the file some of vmess(or other) links seperated with enter

OR:
`python3 custom_test.py total`
You can scan a lot of ip exists in "http://bot.sudoer.net/result.cf" Thanks to ([@MortezaBashsiz](https://github.com/MortezaBashsiz)
in a vmess config that grabbed from [Sudoer VPN bot channel](https://t.me/Sudoer_VPN_bot) and check all ips in this vmess config.

## Result
an output+date.csv file generated in root of project that sorted by maximum speed 
