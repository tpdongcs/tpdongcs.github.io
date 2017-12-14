import paho.mqtt.client as mqtt
import time
import numpy as np
from threading import Lock
from keras.models import load_model
client = mqtt.Client(client_id="clientId-069fOnLO9B")
client.username_pw_set("chvnbmzq", "nE_X6pIBl1kx")
model = load_model("cnn_model_final.h5")
my_model = load_model("cnn_mymodel.h5")
lock = Lock()
window_length = 5000
cacheECG = []
# for i in range(10):
#     client.publish("iotsystem/heartcare", str([i]*100))
def z_norm(result):
    result_mean = result.mean()
    result_std = result.std()
    result -= result_mean
    result /= result_std
    return result, result_mean

def genTestData(idata):
    input = []
    output = []
    ifrom = 0
    for i in range(len(idata) - 200):
        index = i

        raw_input = idata[index:index + 200]
        ecg = np.asarray(raw_input, dtype=np.float32)
        ecg, mean = z_norm(ecg)
        input.append(ecg[:-1])
        output.append(ecg[-1])

    input = np.reshape(input, (len(input), 199, 1))
    output = np.asarray(output, dtype=np.float32)

    return input, output
def mad(se, median_padding):
    back_pad = []
    front_pad = se[1:median_padding + 1]
    mad = []
    for i in range(len(se)):
        median_range = np.asarray(back_pad + [se[i]] + front_pad)
        median = np.median(median_range)
        medians = [abs(j - median) for j in median_range]
        medians = np.asarray(medians)
        mad.append(np.median(medians))
        # next loop
        if len(back_pad) > median_padding:
            del back_pad[0]
        back_pad.append(se[i])
        if i + median_padding + 1 < len(se):
            front_pad.append(se[i + median_padding + 1])
        if len(front_pad) > 0:
            del front_pad[0]
    return mad


def on_message(client, userdata, message):
    print("message received...")
    if "iotsystem/heartcare/ecg/physionet/" == message.topic:
        f = message.payload.decode()
        data = f.split(",")
        x, y = genTestData(data)
        start_predict = time.time()
        predicted = model.predict(x)
        print(str(len(predicted)) + " - " + str(time.time() - start_predict))
        padding = 100
        threshold = 0.05  # 0.0025
        square_error = [(p - r) ** 2 for p, r in zip(predicted, y)]
        median_absolute_deviation = mad(square_error, padding)
        client.publish("iotsystem/heartcare/warning/display/", ",".join(["1" if i >threshold else "0" for i in median_absolute_deviation]))
    else:
        f = message.payload.decode()
        data = [ord(f[i])*94 + ord(f[i + 1]) for i in range(0, len(f), 2)]
        x, y = genTestData(data)
        start_predict = time.time()
        predicted = my_model.predict(x)
        print(str(len(predicted)) + " - " + str(time.time() - start_predict))
        padding = 100
        threshold = 0.05  # 0.0025
        square_error = [(p - r) ** 2 for p, r in zip(predicted, y)]
        median_absolute_deviation = mad(square_error, padding)
        client.publish("iotsystem/heartcare/warning/display/",
                       ",".join(["1" if i > threshold else "0" for i in median_absolute_deviation]))


client.on_message = on_message
client.connect(host="m14.cloudmqtt.com", port=16649)
client.subscribe("iotsystem/heartcare/ecg/physionet/")
client.subscribe("iotsystem/heartcare/ecg/")
print("Server Started ...")
client.loop_forever()

# time.sleep(4)
# client.loop_stop()