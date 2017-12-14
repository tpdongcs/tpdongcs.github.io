import paho.mqtt.client as mqtt
import re
import numpy as np
import time
def getData(ecg_file_name, ann_file_name):
    with open(ecg_file_name, "rb") as f:
        f = f.read()
        sdata = f.decode().split()
        arange = int(round(len(sdata) / 3))
        data = [sdata[i * 3 + 1] for i in range(arange)]
        annMap = dict()
        with open(ann_file_name, "rb") as fa:
            fa = fa.read()
            adata = fa.decode().split('\n')
            for i in range(len(adata)):
                match = re.search("[[](.*)[]][ ]+([0-9]*)[ ]+(.)", adata[i])
                if match != None:
                    atime, idx, ann = match.groups()
                    if ann == 'N':
                        annMap[int(idx)] = 1
        return data, annMap



data, annMap = getData("31.txt", "31_a.txt")
data = data[:]
client = mqtt.Client(client_id="clientId-069fOnLOBB")
client.username_pw_set("chvnbmzq", "nE_X6pIBl1kx")
client.connect(host="m14.cloudmqtt.com", port=16649)
client.loop()
for i in range(0, len(data), 100):
    start_time = time.time()
    msg = [data[j] for j in range(i, i + 100)]
    msg = np.reshape(msg, (100,))
    msg = ",".join(msg.tolist())
    client.publish("iotsystem/heartcare/ecg/physionet/display/", msg)
    if i % 1200 == 0 and i > 0:
        msg = [data[j] for j in range(i - 1100, i + 150)]
        msg = np.reshape(msg, (1250,))
        msg = ",".join(msg.tolist())
        client.publish("iotsystem/heartcare/ecg/physionet/", msg)
    time.sleep(0.5)
client.loop_stop()
client.disconnect()