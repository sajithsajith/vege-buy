from flask import Flask, request, render_template, Response
app = Flask(__name__)
import os
import tensorflow
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import numpy as np
import webbrowser
import cv2
from time import sleep
import RPi.GPIO as GPIO
from hx711 import HX711
from PIL import Image
from mfrc522 import SimpleMFRC522
from gpiozero import LED

app.config["TEMPLATES_AUTO_RELOAD"] = True
GPIO.setmode(GPIO.BCM)
hx = HX711(dout_pin=21, pd_sck_pin=20)
buzzer = LED(12)
reader = SimpleMFRC522()
values = {'brinjal':0,'cabbage':0,'green_banana':0, 'lemon':0, 'tomato':0}
price = [30,40,45,60,35]
model = load_model('veget.h5')

GPIO.setup(17, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(17, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(17, False)
	pwm.ChangeDutyCycle(0)
    

def capture():
    
    cap = cv2.VideoCapture(cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    hx.zero()
    hx.set_scale_ratio(102.49178082191781)
    
    weight_mean =[]
    temp = 0
    global values
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            frame1 = frame
                    
            text = f"Brinjal : {round(values['brinjal'],2)}kg green_banana : {round(values['green_banana'],2)}kg"
            cv2.putText(frame1,text,(5, 10),cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255),2,cv2.LINE_8)
            text = f"Cabbage : {round(values['cabbage'],2)}kg lemon : {round(values['lemon'],2)}kg tomato : {round(values['tomato'],2)}kg"
            cv2.putText(frame1,text,(5, 50),cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255),2,cv2.LINE_8)
            ret, jpeg = cv2.imencode('.jpg', frame1)
            data = jpeg.tobytes()
            weight = hx.get_weight_mean(1)
            print(weight, 'g')
            if weight > 10:
                weight_mean.append(weight)
                if len(weight_mean) == 15:
                    average = sum(weight_mean)/len(weight_mean)
                    if average - hx.get_weight_mean(1) < abs(2): 
                        print('detected')
                        cv2.imwrite("temp_image/image_buff.jpg",frame)
                        weight_mean = []
                        buzzer.on()
                        SetAngle(0)
                        values[detect()] += (average/1000)
                        buzzer.off()
                        cap.release()
                        cap = cv2.VideoCapture(cv2.CAP_V4L2)
                if len(weight_mean)>15:
                    weight_mean = []
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
    cap.release()

def detect():

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '150'
    global model
    img = image.load_img("temp_image/image_buff.jpg",target_size=(64,64))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    op = ['brinjal','cabbage','green_banana', 'lemon', 'tomato']
    pred = np.argmax(model.predict(x))
    print(op[pred])
    return (op[pred])


@app.route('/', methods =["GET", "POST"])
def first():
    return render_template("index.html")

@app.route('/result.html', methods = ["GET", "POST"])
def fifth():
    price_list = [values['brinjal']*price[0],values['cabbage']*price[1],values['green_banana']*price[2],values['lemon']*price[3],values['tomato']*price[4]]
    return render_template("result.html", brinjal=round(values['brinjal'],2), cabbage=round(values['cabbage'],2), green_banana=round(values['green_banana'],2), lemon=round(values['lemon'],2), tomato=round(values['tomato'],2),total_weight=round(sum(values.values()),2), brinjal_price=round(price_list[0],2), cabbage_price=round(price_list[1],2), green_banana_price=round(price_list[2],2), lemon_price=round(price_list[3],2), tomato_price=round(price_list[4],2),total=round(sum(price_list),2))

@app.route('/success', methods =["GET", "POST"])
def success():
    global values
    price_list = [values['brinjal']*price[0],values['cabbage']*price[1],values['green_banana']*price[2],values['lemon']*price[3],values['tomato']*price[4]]
    buzzer.on()
    reader.write("Cost : " + str(round(sum(price_list),2)))
    buzzer.off()
    values = dict.fromkeys(values, 0)
    return render_template("success.html")

@app.route('/index.html', methods =["GET", "POST"])
def third():
    return render_template("index.html")
@app.route('/app.html', methods =["GET", "POST"])
def third1():
    return render_template("app.html")
@app.route('/video_feed')
def video_feed():
    return Response(capture(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/features.html', methods =["GET", "POST"])
def second():
    return render_template("features.html")

@app.route('/about.html', methods =["GET", "POST"])
def fourth():
    return render_template("about.html")

if __name__ == '__main__':
    chrome = webbrowser.get('chromium-browser')
    chrome.open('http://127.0.0.1:5000')
    app.run()
