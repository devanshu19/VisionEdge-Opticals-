import os
import requests
import json
from models import Order, Prescription, Frame, Lens, Appointment

def get_db_context(message):
    """
    Very basic intent parser to fetch relevant database context based on keywords in the message.
    """
    context = ""
    msg = message.lower()
    
    # Check for order intent
    if 'order' in msg or 'where is' in msg or 'status' in msg:
        # Just grab the last 5 active orders as context
        orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        context += "Recent Orders Context:\n"
        for o in orders:
            context += f"- Order {o.order_number}: Status '{o.status}', Customer ID {o.customer_id}\n"
            
    # Check for inventory/lens intent
    if 'lens' in msg or 'blue cut' in msg or 'anti-glare' in msg or 'stock' in msg:
        lenses = Lens.query.filter(Lens.stock > 0).limit(5).all()
        context += "\nAvailable Lenses Context:\n"
        for l in lenses:
            bname = l.brand.name if l.brand else "Generic"
            context += f"- {l.name} by {bname} ({l.lens_type}): ₹{l.selling_price} (Stock: {l.stock})\n"
            
    # Check for prescription intent
    if 'prescription' in msg or 'mean' in msg or 'explain' in msg:
        context += "\nOptical Prescription Glossary:\n"
        context += "- Sphere (SPH): Controls near/far vision correction. (-) for nearsighted, (+) for farsighted.\n"
        context += "- Cylinder (CYL): Corrects astigmatism (irregular cornea shape).\n"
        context += "- Axis: Direction of cylinder correction (0 to 180 degrees).\n"
        context += "- Add: Additional magnifying power applied to bottom part of multifocal lenses for reading.\n"
        
    # Check for appointment intent
    if 'appointment' in msg or 'eye test' in msg or 'book' in msg:
        context += "\nAppointments Context:\n"
        context += "- Appointments can be booked through the Appointments module.\n"
        context += "- Eye tests are available daily from 10 AM to 6 PM.\n"
        
    return context

def generate_chat_response(message):
    """
    Generates a response using Gemini REST API directly to avoid package dependency issues.
    Falls back to a keyword-matching mock if API fails or key is missing.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    
    # Fetch relevant context from DB based on keywords
    db_context = get_db_context(message)
    
    system_prompt = f"""
You are VisionEdge AI Optical Assistant.
You are an expert optical consultant for VisionEdge Smart Optical Management System.
Help users with:
- Lens recommendations
- Frame selection
- Prescription explanation
- Eye care tips
- Product information
- Appointment guidance
- Order information

Do not provide medical diagnosis. Keep answers concise, professional, and directly address the user's query.
Format with simple text, no markdown headers, but bullet points are fine.

{db_context}
    """
    
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [{
                    "parts": [{"text": message}]
                }]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                answer = data['candidates'][0]['content']['parts'][0]['text']
                return answer
            else:
                print("Gemini API Error:", response.text)
                # Fall back to mock
        except Exception as e:
            print("Gemini API Request Error:", e)
            # Fall back to mock
            
    # --- MOCK FALLBACK LOGIC ---
    msg = message.lower()
    
    if 'lens' in msg and ('computer' in msg or 'office' in msg):
        return "Blue Cut Anti-Glare lens is highly recommended for long screen usage. It reduces digital eye strain by filtering harmful blue light. We have options available from Essilor and Zeiss."
        
    if 'prescription' in msg and 'mean' in msg:
        return "Your prescription consists of a few key parts:\n- Sphere (SPH): Controls near/far vision correction.\n- Cylinder (CYL): Corrects astigmatism.\n- Axis: The direction of the cylinder correction.\n- Add: Extra power for reading."
        
    if 'blue cut' in msg and 'available' in msg:
        return "Yes, Blue Cut lenses are available in stock. We carry brands like Essilor and Titan. The price range is typically between ₹3000 to ₹5000 depending on the index and exact coating."
        
    if 'order' in msg:
        return "Order ID VE-2026-0025 is currently 'Ready for Delivery'. You can view full details in the Orders module."
        
    if 'appointment' in msg or 'eye test' in msg:
        return "We conduct eye test appointments daily from 10 AM to 6 PM. Please navigate to the Appointment Management module to book a slot for the customer."
        
    return "I am the VisionEdge AI Assistant. How can I help you with your optical needs today? (Note: Running in Mock Mode)"
