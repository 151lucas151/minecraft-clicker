#!/usr/bin/env python3
"""
Enhanced Game API for Minecraft Click
Handles game state persistence for cross-platform play (Web + React Native)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import os
import json
from datetime import datetime
import secrets
import re

# Try to import stripe, but allow API to run without it
try:
    import stripe
    STRIPE_AVAILABLE = True
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_YOUR_SECRET_KEY_HERE')
except ImportError:
    STRIPE_AVAILABLE = False
    print("Warning: Stripe not installed. Payment features will be disabled. Install with: pip3 install stripe")

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Database setup
DB_PATH = 'minecraft_click.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table for username/password authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            email TEXT UNIQUE,
            profile_picture TEXT DEFAULT 'default.svg',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Game states table for cross-platform save data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_data TEXT NOT NULL,  -- JSON string of complete game state
            last_saved TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            platform TEXT DEFAULT 'web',  -- 'web', 'android', 'ios'
            version TEXT DEFAULT '1.0',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # High scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            blocks INTEGER NOT NULL,
            total_mined INTEGER NOT NULL,
            total_clicks INTEGER NOT NULL,
            upgrades_owned INTEGER NOT NULL,
            play_time INTEGER NOT NULL,
            score_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Password reset tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Purchases table for tracking real money transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stripe_session_id TEXT UNIQUE,
            item_type TEXT NOT NULL,
            price_in_cents INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    """Hash a password with a salt"""
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return password_hash.hex(), salt

def verify_password(password, password_hash, salt):
    """Verify a password against its hash"""
    test_hash, _ = hash_password(password, salt)
    return test_hash == password_hash

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def authenticate_user(username, password):
    """Authenticate user and return user_id if valid"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, salt FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return None
        
        user_id, password_hash, salt = user
        
        if not verify_password(password, password_hash, salt):
            conn.close()
            return None
        
        conn.close()
        return user_id
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

# ===== GAME STATE API ENDPOINTS =====

@app.route('/api/game/save', methods=['POST'])
def save_game_state():
    """Save complete game state for cross-platform sync"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        game_data = data.get('gameState', {})
        platform = data.get('platform', 'web')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        if not game_data:
            return jsonify({'success': False, 'message': 'Game state data is required'}), 400
        
        # Authenticate user
        user_id = authenticate_user(username, password)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Validate and clean game data
        if not isinstance(game_data, dict):
            return jsonify({'success': False, 'message': 'Invalid game state format'}), 400
        
        # Add metadata
        game_data['lastSaved'] = datetime.now().isoformat()
        game_data['platform'] = platform
        game_data['version'] = '1.0'
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Save or update game state
        cursor.execute('''
            INSERT OR REPLACE INTO game_states (user_id, game_data, platform, version)
            VALUES (?, ?, ?, ?)
        ''', (user_id, json.dumps(game_data), platform, '1.0'))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Game state saved successfully',
            'timestamp': game_data['lastSaved']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to save game state: {str(e)}'}), 500

@app.route('/api/game/load', methods=['POST'])
def load_game_state():
    """Load complete game state for cross-platform sync"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        # Authenticate user
        user_id = authenticate_user(username, password)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get most recent game state
        cursor.execute('''
            SELECT game_data, last_saved, platform 
            FROM game_states 
            WHERE user_id = ? 
            ORDER BY last_saved DESC 
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'success': False, 'message': 'No saved game found'}), 404
        
        game_data_str, last_saved, platform = result
        
        try:
            game_data = json.loads(game_data_str)
            return jsonify({
                'success': True,
                'gameState': game_data,
                'lastSaved': last_saved,
                'platform': platform
            }), 200
        except json.JSONDecodeError:
            return jsonify({'success': False, 'message': 'Corrupted save data'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to load game state: {str(e)}'}), 500

@app.route('/api/game/sync', methods=['POST'])
def sync_game_state():
    """Sync game state - save if newer, load if server has newer"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        client_game_data = data.get('gameState', {})
        platform = data.get('platform', 'web')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        # Authenticate user
        user_id = authenticate_user(username, password)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get server's most recent game state
        cursor.execute('''
            SELECT game_data, last_saved 
            FROM game_states 
            WHERE user_id = ? 
            ORDER BY last_saved DESC 
            LIMIT 1
        ''', (user_id,))
        
        server_result = cursor.fetchone()
        
        if not server_result:
            # No server data, save client data
            client_game_data['lastSaved'] = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO game_states (user_id, game_data, platform, version)
                VALUES (?, ?, ?, ?)
            ''', (user_id, json.dumps(client_game_data), platform, '1.0'))
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'action': 'saved',
                'message': 'Game state saved (new player)'
            }), 200
        
        server_game_data_str, server_last_saved = server_result
        
        try:
            server_game_data = json.loads(server_game_data_str)
            server_time = datetime.fromisoformat(server_last_saved.replace('Z', '+00:00'))
        except (json.JSONDecodeError, ValueError):
            conn.close()
            return jsonify({'success': False, 'message': 'Corrupted server save data'}), 500
        
        # Compare timestamps
        client_last_saved = client_game_data.get('lastSaved')
        if client_last_saved:
            try:
                client_time = datetime.fromisoformat(client_last_saved.replace('Z', '+00:00'))
                if client_time > server_time:
                    # Client is newer, save to server
                    client_game_data['lastSaved'] = datetime.now().isoformat()
                    cursor.execute('''
                        INSERT OR REPLACE INTO game_states (user_id, game_data, platform, version)
                        VALUES (?, ?, ?, ?)
                    ''', (user_id, json.dumps(client_game_data), platform, '1.0'))
                    conn.commit()
                    conn.close()
                    
                    return jsonify({
                        'success': True,
                        'action': 'saved',
                        'message': 'Client data saved to server'
                    }), 200
            except ValueError:
                pass  # Invalid client timestamp, use server data
        
        # Server is newer or client timestamp invalid, return server data
        conn.close()
        return jsonify({
            'success': True,
            'action': 'loaded',
            'gameState': server_game_data,
            'lastSaved': server_last_saved,
            'message': 'Server data loaded'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to sync game state: {str(e)}'}), 500

# ===== EXISTING API ENDPOINTS (from highscores.py) =====

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({'success': False, 'message': 'Username must be 3-20 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        if email and not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username already taken'}), 409
        
        # Check if email already exists (if provided)
        if email:
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return jsonify({'success': False, 'message': 'Email already registered'}), 409
        
        # Create new user
        password_hash, salt = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash, salt, email) VALUES (?, ?, ?, ?)', 
                      (username, password_hash, salt, email))
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Registration successful'}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login a user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, salt, email, profile_picture FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        
        user_id, password_hash, salt, email, profile_picture = user
        
        if not verify_password(password, password_hash, salt):
            conn.close()
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        
        # Update last login time
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Login successful', 
            'user_id': user_id,
            'username': username,
            'email': email,
            'profile_picture': profile_picture
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login failed: {str(e)}'}), 500

@app.route('/api/check-username', methods=['POST'])
def check_username():
    """Check if a username is available"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'success': False, 'message': 'Username is required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        
        return jsonify({'success': True, 'available': not exists}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to check username: {str(e)}'}), 500

@app.route('/api/highscores', methods=['GET'])
def get_high_scores():
    """Get top 10 high scores"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT h.username, h.blocks, h.total_mined, h.total_clicks, h.upgrades_owned, h.play_time, h.score_date,
                   u.profile_picture
            FROM high_scores h
            LEFT JOIN users u ON h.user_id = u.id
            ORDER BY h.total_mined DESC, h.blocks DESC 
            LIMIT 10
        ''')
        
        scores = []
        for row in cursor.fetchall():
            scores.append({
                'username': row[0],
                'blocks': row[1],
                'totalMined': row[2],
                'totalClicks': row[3],
                'upgradesOwned': row[4],
                'playTime': row[5],
                'date': row[6],
                'profilePicture': row[7] or 'default.svg'
            })
        
        conn.close()
        return jsonify({'success': True, 'scores': scores}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to get high scores: {str(e)}'}), 500

@app.route('/api/highscores', methods=['POST'])
def save_high_score():
    """Save a new high score"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        blocks = data.get('blocks', 0)
        total_mined = data.get('totalMined', 0)
        total_clicks = data.get('totalClicks', 0)
        upgrades_owned = data.get('upgradesOwned', 0)
        play_time = data.get('playTime', 0)
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        # Authenticate user
        user_id = authenticate_user(username, password)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Save the high score
        cursor.execute('''
            INSERT INTO high_scores (user_id, username, blocks, total_mined, total_clicks, upgrades_owned, play_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, blocks, total_mined, total_clicks, upgrades_owned, play_time))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'High score saved successfully'}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to save high score: {str(e)}'}), 500

@app.route('/api/purchase/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create a Stripe Checkout session for a purchase"""
    if not STRIPE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Payment system not available. Stripe not installed.'}), 503
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        item_type = data.get('itemType', '')
        price_in_cents = data.get('priceInCents', 0)
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        if not item_type or not price_in_cents:
            return jsonify({'success': False, 'message': 'Item type and price are required'}), 400
        
        # Authenticate user
        user_id = authenticate_user(username, password)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Get item name for display
        item_names = {
            'blocks-small': '10,000,000 Blocks',
            'blocks-medium': '50,000,000 Blocks',
            'blocks-large': '150,000,000 Blocks',
            'hour-blocks': '1 Hour Passive Income',
            'multiplier-short': 'x2 Blocks (30 min)',
            'multiplier-long': 'x3 Blocks (1 hour)',
            'blocks-huge': '500,000,000 Blocks',
            'blocks-extreme': '2,000,000,000 Blocks',
            'speed-boost': '2x Mining Speed (1 hour)',
            'all-tools': 'All Basic Tools',
            'premium-tools': 'Premium Tools Pack',
            'permanent-multiplier': 'Permanent +25% Boost',
            'auto-clicker': 'Auto-Clicker (24 hours)'
        }
        
        item_name = item_names.get(item_type, 'Shop Item')
        
        # Create Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item_name,
                        'description': f'Minecraft Clicker - {item_name}',
                    },
                    'unit_amount': price_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/purchase-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/purchase-cancelled',
            client_reference_id=str(user_id),
            metadata={
                'username': username,
                'item_type': item_type,
                'price_in_cents': str(price_in_cents)
            }
        )
        
        # Store purchase record in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO purchases (user_id, stripe_session_id, item_type, price_in_cents, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, checkout_session.id, item_type, price_in_cents, 'pending'))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'sessionId': checkout_session.id
        }), 200
        
    except Exception as e:
        print(f"Checkout error: {e}")
        return jsonify({'success': False, 'message': f'Failed to create checkout session: {str(e)}'}), 500

@app.route('/api/purchase/fulfill', methods=['POST'])
def fulfill_purchase():
    """Fulfill a purchase after successful payment"""
    if not STRIPE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Payment system not available. Stripe not installed.'}), 503
    try:
        data = request.get_json()
        session_id = data.get('sessionId', '')
        
        if not session_id:
            return jsonify({'success': False, 'message': 'Session ID required'}), 400
        
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status != 'paid':
            return jsonify({'success': False, 'message': 'Payment not completed'}), 400
        
        # Update purchase status in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE purchases SET status = 'completed' WHERE stripe_session_id = ?
        ''', (session_id,))
        conn.commit()
        conn.close()
        
        # Return success
        return jsonify({
            'success': True,
            'itemType': session.metadata.get('item_type'),
            'message': 'Purchase fulfilled successfully'
        }), 200
        
    except Exception as e:
        print(f"Fulfillment error: {e}")
        return jsonify({'success': False, 'message': f'Failed to fulfill purchase: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'success': True, 'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    init_db()
    print("Enhanced Minecraft Click API initialized. Database created at:", DB_PATH)
    print("API Endpoints:")
    print("  POST /api/game/save - Save game state")
    print("  POST /api/game/load - Load game state") 
    print("  POST /api/game/sync - Sync game state")
    print("  POST /api/register - Register user")
    print("  POST /api/login - Login user")
    print("  POST /api/check-username - Check username availability")
    print("  GET /api/highscores - Get high scores")
    print("  POST /api/highscores - Save high score")
    print("  POST /api/purchase/create-checkout-session - Create Stripe checkout")
    print("  POST /api/purchase/fulfill - Fulfill purchase")
    print("  GET /api/health - Health check")
    app.run(host='0.0.0.0', port=5002, debug=True)
