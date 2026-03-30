# AI-Powered IoT Smart Car

A sophisticated, multi-platform IoT vehicle that integrates real-time computer vision, low-latency communication, and dual-microcontroller logic.

## Project Overview
This project demonstrates a complete ecosystem where hardware meets AI. It features a WiFi-controlled vehicle with live video streaming and autonomous traffic sign detection, controlled via a custom-built Android application.

## System Architecture & Tech Stack

### 1. Hardware & Firmware
* **ESP32-WROVER-DEV:** Handles the high-bandwidth task of live video streaming and web server hosting.
* **Raspberry Pi Pico W:** Manages motor control logic and sensor data for precise movement.
* **L298N & Servos:** Driving the propulsion and steering systems.
* **Language:** C++ (Arduino Framework) / MicroPython.

### 2. Mobile Control (Android)
* **Native App:** Built with **Kotlin** for high performance.
* **Protocol:** **MQTT** for near-instantaneous command transmission (sub-50ms latency).
* **Video Feed:** Integrated WebView for real-time monitoring of the car's perspective.

### 3. Artificial Intelligence (Computer Vision)
* **Model:** **YOLOv8** (You Only Look Once) for real-time object detection.
* **Logic:** The system detects and classifies traffic signs, allowing for semi-autonomous decision-making based on visual input.
* **Backend:** Flask-based Python server for processing heavy AI inference.

## Project Structure
* `/Aplicatie`: Native Kotlin Android source code.
* `/CameraWebServer`: ESP32 firmware for video streaming.
* `/Pico`: Motor control logic for Raspberry Pi Pico W.
* `/Server Flask`: Python scripts for YOLOv8 detection and MQTT bridging.

## Setup & Configuration
1.  **WiFi/MQTT:** Update the placeholders (`YOUR_WIFI_SSID`, `YOUR_MQTT_BROKER_IP`) in the source files.
2.  **Firmware:** Flash the ESP32 and Pico W using the provided code.
3.  **Android:** Build the APK and connect it to your local MQTT broker.
4.  **AI:** Run `detection.py` on a machine with the YOLOv8 weights loaded.
