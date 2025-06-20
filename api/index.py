from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_url_path='/static', template_folder='../templates')

data_sensor = []
max_data = 20
mode = {"auto": False, "manual": False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global data_sensor
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            nilai = int(json_data['moisture'])
            data_sensor.append(nilai)
            if len(data_sensor) > max_data:
                data_sensor.pop(0)
            return jsonify({"status": "ok"}), 200
        except:
            return jsonify({"status": "error"}), 400
    return jsonify({"data": data_sensor})

@app.route('/api/status', methods=['GET', 'POST'])
def api_status():
    global mode
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            mode['auto'] = json_data.get('auto', False)
            mode['manual'] = json_data.get('manual', False)
            return jsonify({"status": "updated"}), 200
        except:
            return jsonify({"status": "error"}), 400
    return jsonify(mode)

# Untuk Vercel
handler = app
