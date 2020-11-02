import paho.mqtt.client as mqtt
import json

class MqttMessageService:
    def __init__(self):
        with open('config.json') as file:
            self._config = json.load(file)
        
        self._client = mqtt.Client(clean_session=self._config['CleanSession'])
        self._client.username_pw_set(self._config['Username'], self._config['Password'])
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if self._config['SSL_TLS']:
            self._client.tls_set()
        self._client.connect(self._config['ServerUri'], self._config['Port'], 60)
        self._listeners = { }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        return True

    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic in self._config['Topics']:
            self._client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, client, userdata, msg):
        print('Message received ('+msg.topic+'): ' + str(msg.payload))

        if msg.topic in self._listeners:
            for handler in self._listeners[msg.topic]:
                try:
                    handler(msg)
                except Exception as e:
                    print('An exception occured in message handler for topic: ' + msg.topic + ". Exception: " + e)    


    def start(self):
        self._client.loop_start()

    def stop(self):
        self._client.loop_stop()

    def add_listener(self, topic, listener):
        if topic not in self._listeners:
            self._listeners[topic] = []
        self._listeners[topic].append(listener)
    
    def remove_listener(self, topic, listener):
        if topic in self._listeners:
            self._listeners[topic].remove(listener)


if __name__ == "__main__":
    def on_test(data):
        kvps = json.loads(data.payload)    
        print(kvps)

    with MqttMessageService() as service:
        service.add_listener("suitceyes/tactile-board/test", on_test)
        while True:
            pass