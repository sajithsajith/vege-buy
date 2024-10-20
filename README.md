# Vege Buy - Smart Vegetable Identification and Billing Machine

Vege Buy is an intelligent system that automates the process of identifying vegetables, weighing them, and generating bills. It's designed to run on a Raspberry Pi and utilizes computer vision, machine learning, and various hardware components to create a seamless vegetable purchasing experience.

## Features

1. Vegetable Detection: Uses a camera and TensorFlow model to identify vegetables.
2. Weight Measurement: Employs a load cell (HX711) to accurately weigh vegetables.
3. Automated Conveyor: Uses a servo motor to move vegetables after detection.
4. RFID Integration: Prints the total cost on an RFID card.
5. User Interface: Web-based UI for real-time monitoring and billing.

## Hardware Requirements

- Raspberry Pi
- Camera module
- Display
- HX711 load cell amplifier
- Servo motor
- RFID reader/writer (MFRC522)
- LED (for buzzer)
- GPIO connections

## Setup

1. Connect the hardware components according to the pin configurations in the code.
2. Download the [model file](https://drive.google.com/file/d/1R5yqtfi8jYrPfnGOiS422fu734BEZCgb/view?usp=sharing) from here
3. Ensure the TensorFlow model file `veget.h5` is in the project directory.
4. Run the application: `python app.py`

## Usage

1. The application will automatically open in the default web browser.
2. Place a vegetable on the weighing scale.
3. The system will detect the vegetable, measure its weight, and update the UI.
4. After all vegetables are processed, view the final bill on the results page.
5. Use the RFID card to store the total cost.

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JavaScript, and image files
- `temp_image/`: Temporary storage for captured images

## Key Components

- Flask web server
- TensorFlow for vegetable classification
- OpenCV for image capture and processing
- HX711 for weight measurement
- Servo motor control for conveyor movement
- MFRC522 for RFID operations

## Future Improvements

- Add more vegetable types to the classification model
- Implement user accounts and purchase history
- Integrate with payment systems
- Enhance the UI for better user experience

## Images

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/f57d3496-ff27-490c-b556-ebffc2d639a1)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/b00d471f-d9f2-4f6f-8995-3fbbb2098f07)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/5e8c5d36-f060-414b-9404-cab0fa8341c7)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/9a40d121-eb93-4298-8be7-ad9fb489d30e)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/ea38e950-5ae7-4bce-a18e-266ae6110217)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/d849fd26-19fb-4f14-be25-899c37c483f2)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/3a27f4d3-06ec-446c-bb1f-eb6f67b2c10d)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/27fc1661-eec6-43d4-8677-9ec5d0e60153)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/d828afa5-237a-4767-b759-e1f1af4daaef)

![image](https://github.com/sajithsajith/vege-buy/assets/112680443/7c2e8163-768f-4eff-99b2-a65803ba36f8)
