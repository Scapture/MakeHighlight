import paho.mqtt.client as mqtt

def run(game_number):
    # 변경
    broker_ip = "192.168.1.11" # 현재 이 컴퓨터를 브로커로 설정
    client = mqtt.Client()
    client.connect(broker_ip, 1883, 60)
    client.publish("post", f"{game_number}", qos=0)
    client.disconnect()


