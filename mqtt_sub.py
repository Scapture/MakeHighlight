import paho.mqtt.client as mqtt
import cutVideo, post_video, remove_output, main, show

mqtt_broker = "192.168.1.11"
topic = "convert"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("arrived: ", message)

    if message == "start":
        print("Start Highlight Detection")
        main.run()
        # show.run()
        print("Cut Highlight Video")
        cutVideo.run()
        print("POST to Server")
        post_video.run()
        print("Clean Directory")
        remove_output.run()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, 1883, 60)
client.loop_forever()

