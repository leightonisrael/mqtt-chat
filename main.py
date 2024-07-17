import threading
import time
import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
THE_TOPIC = "ufrn/group-chating"
CLIENT_ID = ""

person = ""

def on_connect(client, userdata, flags, rc):
    client.subscribe(THE_TOPIC, qos=0)

def on_message(client, userdata, msg):
    global person
    payload = msg.payload.decode('utf-8')
    sender_name, message = payload.split(': ', 1)
    if sender_name != person:
        print(f"{payload}")

def start_subscriber():
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(None, password=None)
    client.connect(THE_BROKER, port=1883, keepalive=60)
    client.loop_forever()

def start_publisher():
    global person
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.username_pw_set(None, password=None)
    client.connect(THE_BROKER, port=1883, keepalive=60)
    client.loop_start()

    person = input("Type your name: ")
    while True:
        msg_to_be_sent = input("")
        client.publish(THE_TOPIC, payload=f"{person}: {msg_to_be_sent}".encode('utf-8'), qos=0, retain=False)

    client.loop_stop()

if __name__ == '__main__':
    subscriber_thread = threading.Thread(target=start_subscriber)
    publisher_thread = threading.Thread(target=start_publisher)

    subscriber_thread.start()
    publisher_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber_thread.join()
        publisher_thread.join()