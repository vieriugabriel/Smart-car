import network
from umqtt.simple import MQTTClient
from machine import Pin,PWM,time_pulse_us
import time

ssid = "YOUR_WIFI_SSID"
password = "YOUR_WIFI_PASSWORD"

mqtt_server = "YOUR_MQTT_BROKER_IP"
topic_masina = b"comanda_masina"
topic_camera = b"control_camera"
topic_detectie = b"detectie_masina"

led = Pin("LED", Pin.OUT)

In1 = Pin(2, Pin.OUT)
In2 = Pin(3, Pin.OUT)
In3 = Pin(4, Pin.OUT)
In4 = Pin(5, Pin.OUT)

In1_2 = Pin(8, Pin.OUT)
In2_2 = Pin(9, Pin.OUT)
In3_2 = Pin(10, Pin.OUT)
In4_2 = Pin(11, Pin.OUT)

EN_AB = PWM(Pin(6))
EN_AB2 = PWM(Pin(7))
EN_AB.freq(1000)      
EN_AB2.freq(1000)

servo1 = PWM(Pin(16))
servo2 = PWM(Pin(17))
servo1.freq(50)
servo2.freq(50)

trig = Pin(18, Pin.OUT)
echo=Pin(19, Pin.IN, machine.Pin.PULL_UP)
trig.value(0)

def distance_cm():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    
    duration = time_pulse_us(echo, 1, 30000)  
    if duration < 0:
        return None
   
    distance = (duration / 2) * 0.0343
    return distance

def obstacol():
    dist = distance_cm()
    if dist is not None:
        print("Distanță:", dist, "cm")
        if dist < 20:
            print("Obstacol detectat! STOP")
            stop()
        
    time.sleep(0.2)
    

    
def move_forward():
    EN_AB.duty_u16(65535)
    EN_AB2.duty_u16(65535)
    In1.high()
    In2.low()
    In3.low()
    In4.high()
    In1_2.low()
    In2_2.high()
    In3_2.high()
    In4_2.low()

def move_backward():
    EN_AB.duty_u16(65535)
    EN_AB2.duty_u16(65535)
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    In1_2.high()
    In2_2.low()
    In3_2.low()
    In4_2.high()

def turn_right():
    EN_AB.duty_u16(50000)
    EN_AB2.duty_u16(50000)
    In1.high()
    In2.low()
    In3.low()
    In4.high()
    In1_2.high()
    In2_2.low()
    In3_2.low()
    In4_2.high()

def turn_left():
    EN_AB.duty_u16(50000)
    EN_AB2.duty_u16(50000)
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    In1_2.low()
    In2_2.high()
    In3_2.high()
    In4_2.low()

def stop():
    EN_AB.duty_u16(0)
    EN_AB2.duty_u16(0)
    In1.low()
    In2.low()
    In3.low()
    In4.low()
    In1_2.low()
    In2_2.low()
    In3_2.low()
    In4_2.low()
    
def set_speed(servo, speed):
    duty = int((speed / 180) * 8000 + 1000)
    servo.duty_u16(duty)
    
def move_up():
    set_speed(servo2, 75)

def move_down():
    set_speed(servo2, 95)

def move_left():
    set_speed(servo1, 95)

def move_right():
    set_speed(servo1, 75)

def stop_camera():
   set_speed(servo1, 85)
   set_speed(servo2, 85)
    
def conectare_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Conectare WiFi...")
        led.value(1)
        time.sleep(1)
    print("Conectat la WiFi:", wlan.ifconfig())
    led.value(0)

def on_message(topic, msg):
    print("Mesaj primit:", msg)
  
    comanda = msg.decode().upper()
    
    if topic == topic_masina:
        if comanda == "FORWARD":
            dist = distance_cm()
            if dist < 20:
                print("Obstacol detectat la", dist, "cm — comanda ignorată")
                stop()
            else:
                move_forward()
        elif comanda == "BACKWARD":
            move_backward()
        elif comanda == "LEFT":
            turn_left()
        elif comanda == "RIGHT":
            turn_right()
        elif comanda == "STOP":
            stop()
            
    elif topic == topic_camera:
        if comanda == "UP":
            move_up()
        elif comanda == "DOWN":
            move_down()
        elif comanda == "LEFT":
            move_left()
        elif comanda == "RIGHT":
            move_right()
        elif comanda == "STOP":
            stop_camera()
 
    elif topic == topic_detectie:
        if comanda == "STOP":
            stop()


conectare_wifi()
client = MQTTClient("pico_client", mqtt_server)
client.set_callback(on_message)
client.connect()
client.subscribe(topic_masina)
client.subscribe(topic_camera)
client.subscribe(topic_detectie)
print("Conectat la broker MQTT și ascult pe topicele:")
print("-", topic_masina)
print("-", topic_camera)
print("-", topic_detectie)
led.value(1)
time.sleep(0.5)
led.value(0)

try:
    while True:
        obstacol()
        client.check_msg()
        time.sleep(0.1)
    
except KeyboardInterrupt:
    client.disconnect()
    print("Deconectat de la MQTT")
