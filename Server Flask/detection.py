from flask import Flask, Response
import cv2
import numpy as np
import requests
from ultralytics import YOLO
import paho.mqtt.client as mqtt

app = Flask(__name__)
model = YOLO("best.pt")
snapshot_url = "http://YOUR_ESP32_CAM_IP/capture"
last_labels = set()
model.model.names = [
    'accesul_interzis',
    'interzis_la_stanga',
    'depasirea_interzisa',
    'interzis_la_dreapta',
    'limita_viteza_peste_10_km/h',
    'limita_viteza_peste_100_km/h',
    'limita_viteza_peste_130_km/h',
    'limita_viteza_peste_20_km/h',
    'limita_viteza_peste_30_km/h',
    'limita_viteza_peste_40_km/h',
    'limita_viteza_peste_5_km/h',
    'limita_viteza_peste_50_km/h',
    'limita_viteza_peste_60_km/h',
    'limita_viteza_peste_70_km/h',
    'limita_viteza_peste_80_km/h',
    'limita_viteza_peste_90_km/h',
    'oprirea_interzisa',
    'acces_interzis_camioanelor',
    'intoarcerea_interzisa',
    'interzis_vehiculelor_peste_3.5_tone',
    'interzis_vehiculelor_peste_7.5_tone',
    'statie_de_autobuz',
    'trecere_pentru_pietoni',
    'autostrada',
    'sens_unic',
    'parcare',
    'parcare_taxi',
    'pista_pentru_biciclete_obligatorie',
    'viraj_obligatoriu_la_stanga',
    'viraj_obligatoriu_la_stanga_sau_la_dreapta',
    'depasire_obligatorie_pe_stanga',
    'depasire_obligatorie_pe_stanga_sau_pe_dreapta',
    'depasire_obligatorie_pe_dreapta',
    'viraj_obligatoriu_la_dreapta',
    'sens_giratoriu_obligatoriu',
    'inainte_sau_la_stanga_obligatoriu',
    'mers_inainte_obligatoriu',
    'inainte_sau_la_dreapta_obligatoriu',
    'cedeaza_trecerea',
    'drum_prioritar',
    'STOP',
    'atentie_copii',
    'lucrari_pe_drum',
    'trecere_pietoni',
    'atentie_biciclisti',
    'atentie_animale_domestice',
    'atentie_alte_pericole',
    'drum_denivelat',
    'atentie_sens_giratoriu',
    'drum_alunecos',
    'denivelare',
    'semafor',
    'atentie_tramvai',
    'trafic_in_ambele_sensuri',
    'atentie_animale_salbatice'
]

mqtt_client = mqtt.Client()
mqtt_client.connect("YOUR_MQTT_BROKER_IP", 1883)

def generate_stream():
    global last_labels
    while True:
        try:
            resp = requests.get(snapshot_url, timeout=5)
            img = cv2.imdecode(np.frombuffer(resp.content, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                continue

            results = model(img)[0]
            frame = results.plot()

            detected_labels = set()
            for box in results.boxes:
                class_id = int(box.cls[0].item())
                label = model.model.names[class_id]
                detected_labels.add(label)

            new_labels = detected_labels - last_labels
            for label in new_labels:
                print(f"[+] Semn nou detectat: {label}")
                mqtt_client.publish("detectie_masina", label)

            last_labels = detected_labels

            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print("Eroare în stream:", e)
            continue

@app.route("/stream")
def stream():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
