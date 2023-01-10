import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
UID = os.getenv('UID')
SERVERS = ["localhost"]

"""
{
    "connection":%s
    "Id": %s,
    "ip": %s,
    "uptime": %s,
    "load": %s,
    "total_ram(GB)": %s,
    "used_ram(%)": %s,
}
"""


def send_alert(text: str, uid: str = UID):
    try:
        link = 'https://api.telegram.org/bot'+BOT_TOKEN + \
            '/sendMessage?chat_id='+str(uid)+'&test='+text
        requests.get(link)
    except:
        time.sleep(1)
        send_alert(text)

def create_json(*var):
    template = """
            {
                "connection": "%s",
                "Id": "%s",
                "ip": "%s",
                "uptime": "%s",
                "load": "%s",
                "total_ram_GB": "%s",
                "used_ram_percent": "%s",
            }""" % (
        var[0],
        var[1],
        var[2],
        var[3],
        var[4],
        var[5],
        var[6],
    )
    return template

def main():
    data = ""
    for idx, ip in enumerate(SERVERS):
        if ip == "localhost":
            temp_uptime = os.popen("uptime").read().split(",")[
                0].split("up")[1].strip()
            temp_load = os.popen("uptime").read().split("load average:")[1]
            temp_total_ram = ' '.join(
                os.popen("free -m").read().split("\n")[1].split()).split()[1]
            temp_used_ram = ' '.join(
                os.popen("free -m").read().split("\n")[1].split()).split()[2]
            temp_used_ram_percent = round(
                (int(temp_used_ram) / int(temp_total_ram)) * 100, 2)
            temp_ram_used_GB = round(int(temp_total_ram)/1000, 2)
            data += f'id:{idx+1} -ip:{ip} -uptime:{temp_uptime} -load:{temp_load} -total_ram(GB):{temp_ram_used_GB} -used_ram(%):{temp_used_ram_percent}\n'
        else:
            # TODO
            # data += os.popen(f'ssh -o StrictHostKeyChecking=no USERS@{ip} uptime').read()
            pass
    print(create_json("True",idx+1,ip,temp_uptime,temp_load,temp_ram_used_GB,temp_used_ram_percent))
    # send_alert(data)


if __name__ == "__main__":
    main()
    print("done!")
