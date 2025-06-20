import sys
import json
from http.server import BaseHTTPRequestHandler

# ⚠️ Pastikan ini class yang kamu definisikan sendiri
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from MyHandler!")


def handler(request):
    """
    Fungsi utama Vercel untuk menangani HTTP request
    """
    try:
        # Kamu bisa ambil class name dari query atau request, misal:
        class_name = "MyHandler"  # bisa kamu ubah dinamis jika mau
        base = globals().get(class_name)

        # ✅ Pastikan base adalah class dan subclass dari BaseHTTPRequestHandler
        if not (isinstance(base, type) and issubclass(base, BaseHTTPRequestHandler)):
            raise TypeError(f"{class_name} is not a valid handler class")

        # Simulasikan penggunaan handler untuk balasan
        response_body = {
            "message": f"Handler {class_name} aktif",
            "status": "success"
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_body)
        }

    except Exception as e:
        # Tangani error dengan log dan respon error
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
