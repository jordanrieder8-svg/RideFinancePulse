"""
Web server for RideFinance Pulse
Serves the static dashboard and runs scheduled news fetching
"""
import os
import threading
import time
from flask import Flask, send_from_directory
from fetch_news import fetch_news

app = Flask(__name__, static_folder='.')

# Run fetch_news every hour in a background thread
def scheduled_fetch():
    """Run fetch_news every hour"""
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fetching news...")
            fetch_news()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] News fetch completed")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error fetching news: {e}")
        
        # Wait 1 hour (3600 seconds) before next fetch
        time.sleep(3600)

# Start background thread for scheduled fetching
if os.environ.get("NEWSAPI_KEY"):
    # Run initial fetch immediately
    try:
        fetch_news()
    except Exception as e:
        print(f"Initial fetch error: {e}")
    
    # Start scheduled fetching in background
    thread = threading.Thread(target=scheduled_fetch, daemon=True)
    thread.start()
    print("Scheduled news fetching started (runs every hour)")
else:
    print("WARNING: NEWSAPI_KEY not set. News fetching disabled.")

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JSON, TXT)"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
