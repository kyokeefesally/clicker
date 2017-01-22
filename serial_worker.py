#!/usr/bin/env python

import time
import multiprocessing

import serial
import paho.mqtt.client as mqtt

# serial variables
serial_config = serial.Serial(
        port='/dev/usb_serial',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)

# MQTT variables
MQTT_BROKER = "10.0.1.134"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_CLIENT_ID = "clicker_client"
SUBSCRIBE_TOPIC = 'ww/command'
PUBLISH_TOPIC = 'ww/response'

CUR_VALUE = None

'''
base_topic = "ww/readers/"
multi_level_wildcard = "#"
single_level_wildcard = "/+"
'''

class SerialProcess(multiprocessing.Process):
 
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.ser = serial.Serial(
            port='/dev/usb_serial',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.ser.isOpen()
 
    def close(self):
        self.ser.close()
 
    def writeSerial(self, data):
        self.ser.write(data + '\r\n')
        time.sleep(2)
        
    def readSerial(self):
        return self.ser.readline()
        #return self.ser.read(1)

    def mqtt_client_connect(self, topic):
        # Define on_connect event Handler
        def on_connect(mosq, obj, rc):
            #Subscribe to a the Topic
            self.mqttc.subscribe(topic, 0)
            self.mqttc.publish(PUBLISH_TOPIC, "clicker_client connected")

        # Define on_subscribe event Handler
        def on_subscribe(mosq, obj, mid, granted_qos):
            print "Subscribed to MQTT Topic"

        # Define on_publish event Handler
        def on_publish(client, userdata, mid):
            #print "Message Published..."
            pass

        # Define on_message event Handler
        def on_message(mosq, obj, msg):
            global CUR_VALUE

            self.ser.isOpen()
            self.ser.flushInput()

            # get MQTT message
            _payload = msg.payload
            mqtt_message = _payload

            # send it to the serial device
            self.writeSerial(mqtt_message)

            #print "serial command: " + mqtt_message

            # look for incoming serial data
            if (self.ser.inWaiting() > 0):
                #line = self.ser.readline()
                #print(line)
                serial_response = ''
                if self.ser.inWaiting() > 0:
                    serial_response = self.readSerial()
                '''    
                while self.ser.inWaiting() > 0:
                    serial_response += self.readSerial()
                '''
                
                # check to see if serial response has changed
                if serial_response != CUR_VALUE:
                    print "serial command: " + mqtt_message
                    print "serial response: " + serial_response
                    # update current value
                    CUR_VALUE = serial_response

                # publish to MQTT
                self.mqttc.publish(PUBLISH_TOPIC, serial_response)
            else:
                print("no incoming serial data")
            


        # Initiate MQTT Client
        self.mqttc = mqtt.Client(client_id=MQTT_CLIENT_ID)

        # Register Event Handlers
        self.mqttc.on_message = on_message
        self.mqttc.on_connect = on_connect
        self.mqttc.on_subscribe = on_subscribe
        self.mqttc.on_publish = on_publish

        # Uncomment to connect to Broker w/auth mqttc.username_pw_set('username', 'password')
        #mqttc.username_pw_set('5e8cd9c3', '87bfb9a8dbdd4038')

        # Connect with MQTT Broker
        self.mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )

        # Continue the network loop
        self.mqttc.loop_forever()

def main():
    _thread = SerialProcess()
    _thread.mqtt_client_connect(SUBSCRIBE_TOPIC)

if __name__ == "__main__":
    main()

 




