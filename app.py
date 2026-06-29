from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route('/')
def home():
    start = time.time()
    REQUEST_COUNT.labels(endpoint='/', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return jsonify({'message': 'Secure pipeline demo app', 'status': 'running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/slow')
def slow():
    start = time.time()
    time.sleep(2)
    REQUEST_COUNT.labels(endpoint='/slow', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/slow').observe(time.time() - start)
    return jsonify({'message': 'This endpoint is intentionally slow'})

@app.route('/error')
def error():
    REQUEST_COUNT.labels(endpoint='/error', status='500').inc()
    return jsonify({'error': 'Intentional error for testing alerts'}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
