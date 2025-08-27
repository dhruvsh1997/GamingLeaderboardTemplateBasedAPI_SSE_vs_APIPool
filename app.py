from flask import Flask, Response, render_template, jsonify
import random
import time
import threading
import json
from datetime import datetime

app = Flask(__name__)

# Initial leaderboard data
leaderboard = [
    {"id": 1, "name": "DragonSlayer", "score": 1250, "character": "🐉"},
    {"id": 2, "name": "ShadowNinja", "score": 980, "character": "🥷"},
    {"id": 3, "name": "PixelWizard", "score": 750, "character": "🧙"},
    {"id": 4, "name": "CyberPunk", "score": 620, "character": "🤖"},
    {"id": 5, "name": "SpaceRanger", "score": 450, "character": "🚀"},
    {"id": 6, "name": "ForestArcher", "score": 320, "character": "🏹"},
    {"id": 7, "name": "IceQueen", "score": 210, "character": "❄️"},
    {"id": 8, "name": "FireKnight", "score": 150, "character": "🔥"},
]

# Game events log
game_events = []

def simulate_gameplay():
    """Simulate players scoring points"""
    while True:
        # Random delay between events (1-5 seconds)
        time.sleep(random.uniform(1, 5))
        
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
        game_events.insert(0, event)
        if len(game_events) > 10:
            game_events.pop()
        
        # Sort leaderboard by score
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        
        # Print to console for debugging
        print(f"EVENT: {event['message']}")

@app.route('/')
def leaderboard_page():
    """Render the leaderboard page"""
    return render_template('leaderboard.html')

@app.route('/api/leaderboard')
def get_leaderboard():
    """API endpoint to get current leaderboard"""
    return jsonify({
        "leaderboard": leaderboard,
        "events": game_events
    })

@app.route('/leaderboard-updates')
def leaderboard_updates():
    """SSE endpoint for real-time leaderboard updates"""
    def event_stream():
        last_event_count = 0
        
        while True:
            # Check if there are new events
            if len(game_events) > last_event_count:
                # Get new events
                new_events = game_events[:len(game_events) - last_event_count]
                last_event_count = len(game_events)
                
                # Create SSE message
                data = {
                    "leaderboard": leaderboard,
                    "new_events": new_events
                }
                
                # Format as SSE message
                message = f"data: {json.dumps(data)}\n\n"
                yield message
            
            # Small delay to prevent busy waiting
            time.sleep(0.5)
    
    return Response(
        event_stream(),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    # Start gameplay simulation thread
    game_thread = threading.Thread(target=simulate_gameplay, daemon=True)
    game_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)