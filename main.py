#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json

switches = ["zigbee2mqtt/large_remote"]
lights = [
    "zigbee2mqtt/ceiling_light",
    "zigbee2mqtt/bed_light",
    "zigbee2mqtt/desk_light",
]

# TODO: Publish current light as a home assistant sensor
# https://github.com/hjelev/rpi-mqtt-monitor/blob/master/src/rpi-cpu2mqtt.py

# TODO: Allow brightness up/down


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for switch in switches:
        client.subscribe(switch)


def on_message(client, userdata, msg):
    cur_light = userdata["cur_light"]
    print(f"Current light: {cur_light}")
    light = lights[cur_light]

    if msg.topic in switches:
        payload = json.loads(msg.payload)
        match payload["action"]:
            case "on":
                client.publish(f"{light}/set", json.dumps({"state": "ON"}))
            case "off":
                client.publish(f"{light}/set", json.dumps({"state": "OFF"}))
            case "arrow_right_click":
                client.user_data_set({"cur_light": (cur_light + 1) % len(lights)})
            case "arrow_left_click":
                cur_light = (cur_light - 1 + len(lights)) % len(lights)
                client.user_data_set({"cur_light": cur_light})


client = mqtt.Client(userdata={"cur_light": 0})
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
