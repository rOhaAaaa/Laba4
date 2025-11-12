from flask import request, jsonify
from app import create_app

app = create_app()

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/heavy")
def heavy():
    try:
        seconds = float(request.args.get("seconds", 10))
        if seconds <= 0 or seconds > 120:
            seconds = 10.0
    except Exception:
        seconds = 10.0

    import time, math
    end = time.perf_counter() + seconds
    x = 0.0
    while time.perf_counter() < end:
        x += math.sqrt(12345.6789)

    return jsonify(done=True, seconds=seconds, junk=x), 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
