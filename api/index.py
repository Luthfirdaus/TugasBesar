from flask import Flask, render_template, jsonify, request

# Atur lokasi folder template karena index.py ada di dalam /api
app = Flask(__name__, static_url_path='/static', template_folder='../templates')

# Penyimpanan data sementara (RAM)
data_sensor = []
max_data = 20

# Status mode sistem
mode = {
    "auto": False,
    "manual": False
}

# ==================== Halaman utama ====================
@app.route('/')
def index():
    return render_template('index.html')

# ==================== Endpoint kirim dan baca data sensor ====================
@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global data_sensor
    if request.method == 'POST':
        try:
            json_data = request.get_json(force=True)  # Force ambil JSON
            if not json_data or 'moisture' not in json_data:
                return jsonify({"status": "error", "msg": "moisture missing"}), 400

            nilai = int(json_data['moisture'])
            data_sensor.append(nilai)
            if len(data_sensor) > max_data:
                data_sensor.pop(0)

            return jsonify({"status": "ok"}), 200
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500

    # GET request
    return jsonify({"data": data_sensor})

# ==================== Endpoint ambil/kirim mode auto/manual ====================
@app.route('/api/status', methods=['GET', 'POST'])
def api_status():
    global mode
    if request.method == 'POST':
        try:
            json_data = request.get_json(force=True)
            if not json_data:
                return jsonify({"status": "error", "msg": "no JSON"}), 400

            mode['auto'] = json_data.get('auto', False)
            mode['manual'] = json_data.get('manual', False)
            return jsonify({"status": "updated"}), 200
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500

    # GET request
    return jsonify(mode)

# ==================== WAJIB UNTUK VERCEL ====================
# Vercel akan mencari variabel 'handler'
handler = app
