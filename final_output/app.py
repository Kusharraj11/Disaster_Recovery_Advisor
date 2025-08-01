from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import os
import pickle
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # Corrected import

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  

# Database functions
def get_db_path():
    return os.path.join(os.path.dirname(__file__), './users.json')

def load_users():
    try:
        with open(get_db_path(), 'r') as f:
            return json.load(f)['users']
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(get_db_path(), 'w') as f:
        json.dump({'users': users}, f, indent=2)

def find_user(username):
    users = load_users()
    return next((u for u in users if u['username'] == username), None)

import ollama  # Add this import at the top

# Function to generate recovery plan using Ollama
def generate_recovery_plan(disaster_type, magnitude, location):
    prompt = f"""Generate a detailed disaster recovery plan for a **{disaster_type}** (Magnitude: {magnitude}) in **{location}**.
    The plan should be structured with:
    1. **Immediate Response** (First 24 hours)
    2. **Short-Term Recovery** (First 72 hours)
    3. **Medium-Term Actions** (1 week - 1 month)
    4. **Long-Term Rehabilitation** (1+ months)
    5. **Required Resources** (Equipment, personnel, funding)
    6. **Safety Precautions** (Risks to avoid)

    Provide clear, actionable steps in bullet points. Be concise but detailed."""
    
    try:
        response = ollama.generate(
            model="tinyllama",  #
            prompt=prompt,
            options={
                "temperature": 0.7,
                "max_tokens": 1500,
            }
        )
        return response["response"]
    except Exception as e:
        print(f"Ollama Error: {e}")
        return "⚠️ Recovery plan could not be generated. Please try again later."


# Models and mappings
DISASTER_MAPPING = {
    'Animal accident': 0,
    'Drought': 1,
    'Earthquake': 2,
    'Epidemic': 3,
    'Extreme temperature ': 4,
    'Flood': 5,
    'Fog': 6,
    'Glacial lake outburst': 7,
    'Impact': 8,
    'Insect infestation': 9,
    'Landslide': 10,
    'Mass movement (dry)': 11,
    'Storm': 12,
    'Volcanic activity': 13,
    'Wildfire': 14
}
REVERSE_DISASTER_MAPPING = {v: k for k, v in DISASTER_MAPPING.items()}

# Resource planner data
CALCULATIONS_FILE = 'D:\final_year_project\final_year_project\final_output\calculations.json'

def load_calculations():
    try:
        with open(CALCULATIONS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_calculations(calculations):
    with open(CALCULATIONS_FILE, 'w') as file:
        json.dump(calculations, file, indent=2)

# Load models
try:
    with open(r"D:\final_year_project\final_year_project\final_output\disaster_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open(r"D:\final_year_project\final_year_project\final_output\more_info.pkl", "rb") as f:
        additional_model = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    additional_model = None

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('predict'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('predict'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        user = find_user(username)
        if user and check_password_hash(user['password'], password) and user['type'] == user_type:
            session['username'] = username
            session['user_type'] = user_type
            return redirect(url_for('predict'))
        error = "Invalid credentials or user type"
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('predict'))
    
    error = None
    success = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        organization = request.form.get('organization', '')
        
        if not all([username, password, email, user_type]):
            error = "All fields are required"
        elif find_user(username):
            error = "Username already exists"
        elif user_type == 'ngo_gov' and not organization:
            error = "Organization name is required for NGO/Government"
        else:
            new_user = {
                'username': username,
                'password': password,
                'email': email,
                'type': user_type
            }
            if user_type == 'ngo_gov':
                new_user['organization'] = organization
                
            users = load_users()
            users.append(new_user)
            save_users(users)
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
    
    return render_template('signup.html', error=error, success=success)

@app.route('/login/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    prediction = None
    recovery_plan = None

    if request.method == 'POST' and model:
        try:
            features = {
                'Year': int(request.form['year']),
                'Dis Mag scale': float(request.form['mag_scale']),
                'Dis Mag Value': float(request.form['mag_value']),
                'Country': int(request.form['country']),
                'Longitude': float(request.form['longitude']),
                'Latitude': float(request.form['latitude'])
            }

            input_data = pd.DataFrame([features])
            predicted_disaster_num = model.predict(input_data)[0]
            predicted_disaster_name = REVERSE_DISASTER_MAPPING.get(predicted_disaster_num, f"Unknown (Code: {predicted_disaster_num})")

            recovery_plan = generate_recovery_plan(
                predicted_disaster_name,
                features['Dis Mag Value'],
                f"Lat: {features['Latitude']}, Long: {features['Longitude']}"
            )

            prediction = {
                'text': predicted_disaster_name,  # Correct key for template
                'num': predicted_disaster_num,
                'features': features,
                'recovery_plan': recovery_plan,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            flash(f"Prediction error: {str(e)}", 'error')

    return render_template('front.html',
                         prediction=prediction,
                         user_type=session.get('user_type'),
                         username=session.get('username'))

@app.route('/more_info', methods=['POST'])
def more_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        features = {
            'Year': int(request.form['year']),
            'Dis Mag Scale': float(request.form['mag_scale']),
            'Dis Mag Value': float(request.form['mag_value']),
            'Country': int(request.form['country']),
            'Longitude': float(request.form['longitude']),
            'Latitude': float(request.form['latitude']),
            'Disaster Type': int(request.form['disaster_type_num'])
        }

        disaster_type_name = REVERSE_DISASTER_MAPPING.get(features['Disaster Type'], 
                                                         f"Unknown ({features['Disaster Type']})")

        prediction = {
            'text': disaster_type_name,
            'num': features['Disaster Type'],
            'features': features
        }

        if additional_model:
            input_data = pd.DataFrame([features])
            additional_prediction = additional_model.predict(input_data).flatten().tolist()
        else:
            additional_prediction = []

        return render_template('1.html', 
                             prediction=prediction, 
                             additional_prediction=additional_prediction,
                             user_type=session.get('user_type'),
                             username=session.get('username'))

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect(url_for('predict'))

@app.route('/resource_planner')
def resource_planner():
    if 'username' not in session or session.get('user_type') != 'ngo_gov':
        flash('Access restricted to NGO/Government users', 'error')
        return redirect(url_for('predict'))
    
    return render_template('cal_index.html',
                         username=session.get('username'),
                         user_type=session.get('user_type'))

@app.route('/calculate_aid', methods=['POST'])
def calculate_aid():
    if 'username' not in session or session.get('user_type') != 'ngo_gov':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Simplified calculation for example purposes
        resources = sum(int(r['quantity']) for r in data.get('resources', []))
        personnel = sum(int(p['number']) for p in data.get('personnel', []))
        transport = sum(int(t['capacity']) for t in data.get('transportation', []))
        
        success_score = min(100, (resources * 0.4 + personnel * 0.3 + transport * 0.3))
        
        return jsonify({
            'disaster_name': data.get('name', 'Unnamed Disaster'),
            'success_score': round(success_score, 2),
            'estimated_cost': round(success_score * 1000),
            'resources_needed': max(0, 100 - resources),
            'personnel_needed': max(0, 50 - personnel)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_calculation', methods=['POST'])
def save_calculation():
    if 'username' not in session or session.get('user_type') != 'ngo_gov':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'calculation' not in data:
            return jsonify({'error': 'Invalid data'}), 400
            
        calculations = load_calculations()
        
        # Ensure calculations is always a dictionary
        if not isinstance(calculations, dict):
            calculations = {}

        save_name = data['name']
        
        # Handle duplicate names
        if save_name in calculations:
            counter = 1
            while f"{save_name} ({counter})" in calculations:
                counter += 1
            save_name = f"{save_name} ({counter})"
        
        calculations[save_name] = data['calculation']
        save_calculations(calculations)
        return jsonify({'status': 'success', 'saved_name': save_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_calculations', methods=['GET'])
def load_calculations_route():
    if 'username' not in session or session.get('user_type') != 'ngo_gov':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        calculations = load_calculations()
        # Ensure we're returning a dictionary
        if not isinstance(calculations, dict):
            return jsonify({'error': 'Invalid calculations format'}), 500
        return jsonify(calculations)
    except Exception as e:
        return jsonify({
            'error': 'Failed to load calculations',
            'details': str(e)
        }), 500

def load_calculations():
    try:
        if not os.path.exists(CALCULATIONS_FILE):
            return {}
            
        with open(CALCULATIONS_FILE, 'r') as file:
            content = file.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in calculations file: {str(e)}")
        return {}
    except Exception as e:
        print(f"Error loading calculations: {str(e)}")
        return {}
    
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Extract disaster info
        disaster_info = {
            'name': data.get('name', 'Unnamed Disaster'),
            'type': data.get('type', 'Unknown'),
            'location': data.get('location', 'Unknown'),
            'affected_population': int(data.get('affected_population', 0)),
            'duration_days': int(data.get('duration_days', 0))
        }

        # Validate and parse resources
        total_resources = 0
        resource_weight = 0
        for res in data.get('resources', []):
            try:
                quantity = int(res.get('quantity', 0))
                total_resources += quantity
                resource_weight += float(res.get('weight', 0)) * quantity
            except (ValueError) as e:
                return jsonify({'error': f'Invalid resource data: {str(e)}'}), 400

        # Validate and parse personnel
        total_personnel = 0
        personnel_cost = 0
        for pers in data.get('personnel', []):
            try:
                number = int(pers.get('number', 0))
                total_personnel += number
                if not bool(pers.get('volunteer', False)):
                    personnel_cost += float(pers.get('pay_rate', 0)) * number * disaster_info['duration_days']
            except (ValueError) as e:
                return jsonify({'error': f'Invalid personnel data: {str(e)}'}), 400

        # Validate and parse transportation
        total_transport = 0
        transport_cost = 0
        for trans in data.get('transportation', []):
            try:
                capacity = float(trans.get('capacity', 0))
                total_transport += capacity
                transport_cost += float(trans.get('cost_per_km', 0)) * 100  # assuming 100km average distance
            except (ValueError) as e:
                return jsonify({'error': f'Invalid transportation data: {str(e)}'}), 400

        # Calculate results
        population_coverage = min(100, (total_resources / max(1, disaster_info['affected_population'])) * 100)
        personnel_coverage = min(100, (total_personnel / max(1, disaster_info['affected_population'] / 100)) * 10)  # 1 personnel per 100 people
        transport_coverage = min(100, (total_transport / max(1, resource_weight)) * 100)
        
        success_score = min(100, (
            population_coverage * 0.4 +
            personnel_coverage * 0.3 +
            transport_coverage * 0.3
        ))
        
        total_cost = personnel_cost + transport_cost

        return jsonify({
            'disaster_info': disaster_info,
            'success_score': round(success_score, 2),
            'estimated_cost': round(total_cost, 2),
            'population_coverage': round(population_coverage, 2),
            'personnel_coverage': round(personnel_coverage, 2),
            'transport_coverage': round(transport_coverage, 2),
            'resources_needed': max(0, disaster_info['affected_population'] - total_resources),
            'personnel_needed': max(0, (disaster_info['affected_population'] // 100) - total_personnel)
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
# Initialize database if not exists
if not os.path.exists(get_db_path()):
    save_users([])

if __name__ == '__main__':
    app.run(port=5001)