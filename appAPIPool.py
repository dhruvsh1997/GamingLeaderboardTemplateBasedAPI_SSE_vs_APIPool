from flask import Flask, Response, render_template, jsonify
import random
import time
import threading
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store leaderboard data
DATA_FILE = 'leaderboard_data.json'

# Initialize data file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "leaderboard": [
                {"id": 1, "name": "DragonSlayer", "score": 1250, "character": "🐉"},
                {"id": 2, "name": "ShadowNinja", "score": 980, "character": "🥷"},
                {"id": 3, "name": "PixelWizard", "score": 750, "character": "🧙"},
                {"id": 4, "name": "CyberPunk", "score": 620, "character": "🤖"},
                {"id": 5, "name": "SpaceRanger", "score": 450, "character": "🚀"},
                {"id": 6, "name": "ForestArcher", "score": 320, "character": "🏹"},
                {"id": 7, "name": "IceQueen", "score": 210, "character": "❄️"},
                {"id": 8, "name": "FireKnight", "score": 150, "character": "🔥"},
            ],
            "events": []
        }
        save_data(initial_data)

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_data():
    """Load data from JSON file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def simulate_gameplay():
    """Simulate players scoring points and update data file"""
    while True:
        # Random delay between events (1-5 seconds)
        time.sleep(random.uniform(1, 5))
        
        # Load current data
        data = load_data()
        leaderboard = data["leaderboard"]
        events = data["events"]
        
        # Select random player
        player = random.choice(leaderboard)
        
        # Random score increase (10-100 points)
        points = random.randint(10, 100)
        player["score"] += points
        
        # Create event message
        event = {
            "player_id": player["id"],
            "player_name": player["name"],
            "points": points,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": f"{player['name']} scored {points} points!"
        }
        
        # Add to events log (keep last 10)
        events.insert(0, event)
        if len(events) > 10:
            events.pop()
        
        # Sort leaderboard by score
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        
        # Save updated data
        save_data(data)
        
        # Print to console for debugging
        print(f"EVENT: {event['message']}")

@app.route('/')
def leaderboard_page():
    """Render the leaderboard page"""
    return render_template('leaderboard_polling.html')

@app.route('/api/leaderboard')
def get_leaderboard():
    """API endpoint to get current leaderboard from file"""
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initialize data file
    initialize_data_file()
    
    # Start gameplay simulation thread
    game_thread = threading.Thread(target=simulate_gameplay, daemon=True)
    game_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)