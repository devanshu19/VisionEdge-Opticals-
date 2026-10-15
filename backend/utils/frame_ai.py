import json
import os
import random

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Hardcoded rules from the prompt
RULES = {
    'Oval': {'recommended': ['Rectangle', 'Square', 'Geometric'], 'avoid': ['Round']},
    'Round': {'recommended': ['Rectangle', 'Angular'], 'avoid': ['Round']},
    'Square': {'recommended': ['Round', 'Oval'], 'avoid': ['Square', 'Geometric']},
    'Heart': {'recommended': ['Oval', 'Light'], 'avoid': ['Heavy', 'Oversized']},
    'Diamond': {'recommended': ['Oval', 'Cat-Eye'], 'avoid': ['Narrow', 'Square']},
    'Long': {'recommended': ['Tall', 'Oversized'], 'avoid': ['Narrow', 'Rectangular']}
}

def recommend_frames_ai(customer_data, face_shape, inventory_frames):
    """
    Simulates calling Gemini AI to filter and recommend frames based on rules.
    If the API key is not present or library not installed, uses deterministic mocking.
    """
    
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if GEMINI_AVAILABLE and api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert optical frame consultant.
        Customer: Age {customer_data.get('age', 'Unknown')}, Gender {customer_data.get('gender', 'Unknown')}.
        Face shape: {face_shape}.
        Budget: {customer_data.get('budget', 'Any')}.
        Lifestyle/Usage: {customer_data.get('usage', 'Any')}.
        
        Available frames in stock (JSON):
        {json.dumps([{ 'id': f['id'], 'name': f['name'], 'brand': f['brand'], 'shape': f['shape'], 'color': f['color'], 'price': f['price'] } for f in inventory_frames])}
        
        Recommend 2-3 suitable frames from the available stock based on the face shape.
        
        Return ONLY valid JSON matching this schema:
        {{
            "frame_type": "Rectangle",
            "reason": "Balances round face structure",
            "color": "Black or dark blue",
            "recommended_brands": ["RayBan"],
            "selected_inventory_ids": [1, 5] // array of integer IDs from the available frames that match
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            raw = response.text.strip()
            if raw.startswith("```json"):
                raw = raw[7:-3]
            elif raw.startswith("```"):
                raw = raw[3:-3]
            
            data = json.loads(raw)
            return {
                "success": True,
                "data": data,
                "is_mock": False
            }
        except Exception as e:
            print("Gemini API Error:", e)
            # Fall back to mock
            pass
            
    # --- MOCK LOGIC (Fallback) ---
    shape_rules = RULES.get(face_shape, RULES['Oval'])
    
    # Filter inventory based on recommended shapes and budget
    filtered_frames = []
    
    budget_range = customer_data.get('budget', 'Any')
    min_b, max_b = 0, 999999
    if '1000-3000' in budget_range:
        min_b, max_b = 1000, 3000
    elif '3000-7000' in budget_range:
        min_b, max_b = 3000, 7000
    elif '7000+' in budget_range:
        min_b, max_b = 7000, 999999
        
    for frame in inventory_frames:
        f_shape = frame.get('shape', '').lower()
        
        # Avoid banned shapes
        avoid = False
        for bad in shape_rules['avoid']:
            if bad.lower() in f_shape:
                avoid = True
        
        if avoid:
            continue
            
        # Check budget
        if not (min_b <= frame['price'] <= max_b):
            continue
            
        filtered_frames.append(frame)
        
    if not filtered_frames:
        # If too restrictive, just pick randomly from inventory to ensure the UI works
        filtered_frames = inventory_frames
        
    # Pick 2-3 random ones from the filtered list
    num_to_pick = min(3, len(filtered_frames))
    if num_to_pick > 0:
        selected = random.sample(filtered_frames, num_to_pick)
        selected_ids = [f['id'] for f in selected]
        brands = list(set([f['brand'] for f in selected]))
        frame_type = selected[0]['shape'] or shape_rules['recommended'][0]
    else:
        selected_ids = []
        brands = []
        frame_type = shape_rules['recommended'][0]
        
    return {
        "success": True,
        "is_mock": True,
        "data": {
            "frame_type": frame_type,
            "reason": f"A {frame_type} frame perfectly balances a {face_shape} face shape according to optical styling principles.",
            "color": "Classic Black / Tortoise",
            "recommended_brands": brands,
            "selected_inventory_ids": selected_ids
        }
    }
