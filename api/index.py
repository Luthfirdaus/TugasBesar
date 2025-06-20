from flask import Flask, render_template, jsonify, request

# Penting: template_folder disesuaikan karena index.py di /api
app = Flask(__name__, static_url_path="/static", template_folder="../templates")

# Data kelembapan disimpan sementara di memori
data_sensor = []
mode = {"auto": False, "manual": False}
max_data = 20

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET", "POST"])
def api_data():
    global data_sensor
    if request.method == "POST":
        try:
            json_data = request.get_json(force=True)
            nilai = int(json_data.get("moisture", 0))
            data_sensor.append(nilai)
            if len(data_sensor) > max_data:
                data_sensor.pop(0)
            return jsonify({"status": "ok"})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify({"data": data_sensor})

@app.route("/api/status", methods=["GET", "POST"])
def api_status():
    global mode
    if request.method == "POST":
        try:
            json_data = request.get_json(force=True)
            mode["auto"] = json_data.get("auto", False)
            mode["manual"] = json_data.get("manual", False)
            return jsonify({"status": "updated"})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify(mode)

# Ini WAJIB agar bisa dipanggil sebagai serverless function di Vercel
handler = app
