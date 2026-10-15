from app import create_app
from models import db, Frame

app = create_app()
with app.app_context():
    # Clear existing frames
    db.session.query(Frame).delete()
    db.session.commit()
    
    # Add diverse frames with stock > 0 and distinct image URLs
    frames = [
        Frame(
            name="Classic Aviator Sunglasses", 
            brand="Ray-Ban", 
            frame_code="RB3025", 
            price=1200.00, 
            selling_price=999.00,
            stock=45,
            status="Available",
            shape="Aviator",
            material="Metal",
            color="Gold",
            image="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&q=80"
        ),
        Frame(
            name="Wayfarer Classic Eyeglasses", 
            brand="Ray-Ban", 
            frame_code="RB2140", 
            price=1500.00, 
            selling_price=1299.00,
            stock=30,
            status="Available",
            shape="Wayfarer",
            material="Acetate",
            color="Black",
            image="https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&q=80"
        ),
        Frame(
            name="Clubmaster Rectangle Eyeglasses", 
            brand="Ray-Ban", 
            frame_code="RB3016", 
            price=1800.00, 
            selling_price=1499.00,
            stock=25,
            status="Available",
            shape="Rectangle",
            material="Titanium",
            color="Bronze",
            image="https://images.unsplash.com/photo-1577803645773-f96470509666?w=600&q=80"
        ),
        Frame(
            name="Round Metal Sunglasses", 
            brand="Ray-Ban", 
            frame_code="RB3447", 
            price=2100.00, 
            selling_price=1699.00,
            stock=50,
            status="Available",
            shape="Round",
            material="Metal",
            color="Silver",
            image="https://images.unsplash.com/photo-1591076482161-42ce6da69f67?w=600&q=80"
        ),
        Frame(
            name="Kids Durable Rectangle Glasses", 
            brand="FlexiKids", 
            frame_code="FK100", 
            price=800.00, 
            selling_price=599.00,
            stock=40,
            status="Available",
            shape="Rectangle",
            material="TR90",
            color="Blue",
            image="https://images.unsplash.com/photo-1508296695146-257a814070b4?w=600&q=80"
        ),
        Frame(
            name="Kids Round Play Eyeglasses", 
            brand="FlexiKids", 
            frame_code="FK101", 
            price=850.00, 
            selling_price=649.00,
            stock=35,
            status="Available",
            shape="Round",
            material="TR90",
            color="Red",
            image="https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=600&q=80"
        ),
        Frame(
            name="Computer Blue-Light Rectangle", 
            brand="VisionEdge", 
            frame_code="VE-C1", 
            price=1400.00, 
            selling_price=999.00,
            stock=60,
            status="Available",
            shape="Rectangle",
            material="Acetate",
            color="Transparent",
            image="https://images.unsplash.com/photo-1582142407894-ec85a1260a46?w=600&q=80"
        ),
        Frame(
            name="Premium Aviator Eyeglasses", 
            brand="Oakley", 
            frame_code="OK10", 
            price=2500.00, 
            selling_price=1999.00,
            stock=20,
            status="Available",
            shape="Aviator",
            material="Titanium",
            color="Silver",
            image="https://images.unsplash.com/photo-1513672174276-14149029410d?w=600&q=80"
        ),
        Frame(
            name="Clear Round Crystal Eyeglasses", 
            brand="VisionEdge", 
            frame_code="VE-R2", 
            price=1600.00, 
            selling_price=1199.00,
            stock=15,
            status="Available",
            shape="Round",
            material="Acetate",
            color="Clear",
            image="https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?w=600&q=80"
        ),
        Frame(
            name="Sport Wayfarer Sunglasses", 
            brand="Oakley", 
            frame_code="OK15", 
            price=1900.00, 
            selling_price=1499.00,
            stock=28,
            status="Available",
            shape="Wayfarer",
            material="TR90",
            color="Matte Black",
            image="https://images.unsplash.com/photo-1509695507497-903c140c43b0?w=600&q=80"
        )
    ]
    
    db.session.add_all(frames)
    db.session.commit()
    print(f"Successfully re-seeded {len(frames)} frames with stock and distinct images!")
