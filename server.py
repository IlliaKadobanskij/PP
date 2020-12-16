from waitress import serve
from Lab4 import app

serve(app, host='0.0.0.0', port=8080)