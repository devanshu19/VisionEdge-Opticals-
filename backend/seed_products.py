from app import create_app
from models import db, Frame, Lens
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE frame ADD COLUMN category VARCHAR(50)"))
        db.session.commit()
    except:
        db.session.rollback()
        
    try:
        db.session.execute(text("ALTER TABLE lens ADD COLUMN category VARCHAR(50)"))
        db.session.commit()
    except:
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE frame MODIFY COLUMN image TEXT"))
        db.session.commit()
    except:
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE lens MODIFY COLUMN image TEXT"))
        db.session.commit()
    except:
        db.session.rollback()

    db.create_all()

    # Clear old data
    db.session.query(Frame).delete()
    db.session.query(Lens).delete()
    db.session.commit()

    # CATEGORY 1: Eyeglasses (5 Local Optical Products)
    eyeglasses = [
        Frame(
            name="Classic Black Wayfarer Eyeglasses", brand="Ray-Ban", frame_code="EYE-001",
            category="Eyeglasses", price=1499.00, selling_price=1299.00, stock=45, status="Available",
            shape="Wayfarer", material="Acetate", color="Black",
            image="assets/images/products/real_eye1.png"
        ),
        Frame(
            name="Vintage Round Metal Specs", brand="Oakley", frame_code="EYE-002",
            category="Eyeglasses", price=1899.00, selling_price=1599.00, stock=35, status="Available",
            shape="Round", material="Metal", color="Gold",
            image="assets/images/products/real_eye2.png"
        ),
        Frame(
            name="Browline Clubmaster Frame", brand="Vogue Eyewear", frame_code="EYE-003",
            category="Eyeglasses", price=2199.00, selling_price=1799.00, stock=25, status="Available",
            shape="Clubmaster", material="Titanium", color="Tortoise Shell",
            image="assets/images/products/real_eye3.png"
        ),
        Frame(
            name="Crystal Clear Oval Eyeglasses", brand="VisionEdge", frame_code="EYE-004",
            category="Eyeglasses", price=1299.00, selling_price=999.00, stock=50, status="Available",
            shape="Oval", material="TR90", color="Transparent Clear",
            image="assets/images/products/real_eye4.png"
        ),
        Frame(
            name="Titanium Ultra-Light Square Specs", brand="Titan Eye Plus", frame_code="EYE-005",
            category="Eyeglasses", price=2499.00, selling_price=2099.00, stock=30, status="Available",
            shape="Square", material="Titanium", color="Matte Silver",
            image="assets/images/products/real_eye5.png"
        )
    ]

    # CATEGORY 2: Sunglasses (5 Local Optical Products)
    sunglasses = [
        Frame(
            name="Gold Classic Aviator Sunglasses", brand="Ray-Ban", frame_code="SUN-001",
            category="Sunglasses", price=2999.00, selling_price=2499.00, stock=40, status="Available",
            shape="Aviator", material="Metal", color="Gold / Green Lens",
            image="assets/images/products/real_sun1.png"
        ),
        Frame(
            name="Matte Black Sport Wayfarer Shades", brand="Oakley", frame_code="SUN-002",
            category="Sunglasses", price=2799.00, selling_price=2299.00, stock=30, status="Available",
            shape="Wayfarer", material="TR90", color="Matte Black",
            image="assets/images/products/real_sun2.png"
        ),
        Frame(
            name="Retro Dark Lens Round Sunglasses", brand="Prada", frame_code="SUN-003",
            category="Sunglasses", price=3499.00, selling_price=2999.00, stock=20, status="Available",
            shape="Round", material="Acetate", color="Dark Gunmetal",
            image="assets/images/products/real_sun3.png"
        ),
        Frame(
            name="Glamour Cat-Eye Polarized Sunglasses", brand="Gucci", frame_code="SUN-004",
            category="Sunglasses", price=3899.00, selling_price=3299.00, stock=15, status="Available",
            shape="Cat-Eye", material="Acetate", color="Rose Gold / Tinted",
            image="assets/images/products/real_sun4.png"
        ),
        Frame(
            name="Hexagonal Metal Frame Sunglasses", brand="Ray-Ban", frame_code="SUN-005",
            category="Sunglasses", price=3199.00, selling_price=2699.00, stock=38, status="Available",
            shape="Hexagonal", material="Metal", color="Copper / Brown Tint",
            image="assets/images/products/real_sun5.png"
        )
    ]

    # CATEGORY 3: Computer Glasses (5 Local Optical Products)
    computer_glasses = [
        Frame(
            name="Blue-Light Block Shield Transparent", brand="VisionEdge", frame_code="CMP-001",
            category="Computer Glasses", price=1599.00, selling_price=1199.00, stock=60, status="Available",
            shape="Rectangle", material="Polycarbonate", color="Transparent Crystal",
            image="assets/images/products/real_11.jpg"
        ),
        Frame(
            name="Anti-Glare Screen Reader Matte Black", brand="Lenskart Air", frame_code="CMP-002",
            category="Computer Glasses", price=1699.00, selling_price=1299.00, stock=50, status="Available",
            shape="Wayfarer", material="TR90 Ultra Lightweight", color="Matte Black",
            image="assets/images/products/real_12.jpg"
        ),
        Frame(
            name="Digital Ray Cut Minimalist Frame", brand="ZeroScreen", frame_code="CMP-003",
            category="Computer Glasses", price=1899.00, selling_price=1499.00, stock=40, status="Available",
            shape="Round", material="Beta Titanium", color="Sleek Grey",
            image="assets/images/products/real_13.jpg"
        ),
        Frame(
            name="Pro Gamer Amber Blue Block Glasses", brand="Gunnar Optics", frame_code="CMP-004",
            category="Computer Glasses", price=2499.00, selling_price=1999.00, stock=25, status="Available",
            shape="Rectangle", material="Alloy Metal", color="Onyx Black",
            image="assets/images/products/real_14.jpg"
        ),
        Frame(
            name="Executive Workstation Blue-Ray Specs", brand="VisionEdge", frame_code="CMP-005",
            category="Computer Glasses", price=1999.00, selling_price=1599.00, stock=35, status="Available",
            shape="Clubmaster", material="Acetate & Metal", color="Navy Blue / Silver",
            image="assets/images/products/real_15.jpg"
        )
    ]

    # CATEGORY 4: Kids Glasses (5 Local Optical Products)
    kids_glasses = [
        Frame(
            name="Kids Flexible Blue TR90 Specs", brand="FlexiKids", frame_code="KID-001",
            category="Kids Glasses", price=999.00, selling_price=699.00, stock=40, status="Available",
            shape="Rectangle", material="Flexible TR90 Rubber", color="Electric Blue",
            image="assets/images/products/real_16.jpg"
        ),
        Frame(
            name="Kids Dark Blue Oval TR90 Eyeglasses", brand="FlexiKids", frame_code="KID-006",
            category="Kids Glasses", price=1099.00, selling_price=749.00, stock=40, status="Available",
            shape="Oval", material="Flexible TR90", color="Dark Blue / Cyan",
            image="assets/images/products/real_26.webp"
        ),
        Frame(
            name="Junior Red Black Rectangle Specs", brand="LittleVision", frame_code="KID-007",
            category="Kids Glasses", price=1149.00, selling_price=799.00, stock=35, status="Available",
            shape="Rectangle", material="Flexible Silicone", color="Red / Black",
            image="assets/images/products/real_27.webp"
        ),
        Frame(
            name="Kids Teal Blue Sporty Eyeglasses", brand="FlexiKids", frame_code="KID-008",
            category="Kids Glasses", price=1099.00, selling_price=749.00, stock=38, status="Available",
            shape="Rectangle", material="TR90 Soft Bend", color="Teal / Black",
            image="assets/images/products/real_28.webp"
        ),
        Frame(
            name="Junior Coral Pink Oval Kids Glasses", brand="LittleVision", frame_code="KID-009",
            category="Kids Glasses", price=1199.00, selling_price=849.00, stock=42, status="Available",
            shape="Oval", material="Lightweight Acetate", color="Coral Pink / Brown",
            image="assets/images/products/real_29.webp"
        )
    ]

    # CATEGORY 5: Contact & Optical Lenses (5 Local Optical Products)
    lenses = [
        Lens(
            name="Acuvue Moist Daily Contact Lenses (30 Pack)", brand="Acuvue", lens_code="LNS-001",
            category="Contact & Optical Lenses", type="Daily Contact Lens", coating="HydraClear Ultra Moisture",
            price=1899.00, selling_price=1499.00, stock=100, status="Available",
            image="assets/images/products/real_21.jpg"
        ),
        Lens(
            name="FreshLook ColorEnhance Hazel Contact Lenses", brand="Alcon", lens_code="LNS-002",
            category="Contact & Optical Lenses", type="Monthly Color Lens", coating="ColorBlend Breathable Matrix",
            price=1699.00, selling_price=1299.00, stock=80, status="Available",
            image="assets/images/products/real_22.jpg"
        ),
        Lens(
            name="UltraClear HD Progressive Precision Lens", brand="Essilor", lens_code="LNS-003",
            category="Contact & Optical Lenses", type="Progressive Optical Lens", coating="Crizal Sapphire Anti-Reflective",
            price=3499.00, selling_price=2899.00, stock=60, status="Available",
            image="assets/images/products/real_23.jpg"
        ),
        Lens(
            name="Biofinity Toric Astigmatism Monthly Lenses", brand="CooperVision", lens_code="LNS-004",
            category="Contact & Optical Lenses", type="Toric Contact Lens", coating="Aquaform Comfort Tech",
            price=2299.00, selling_price=1899.00, stock=75, status="Available",
            image="assets/images/products/real_24.jpg"
        ),
        Lens(
            name="Transitions Gen8 Photochromic Smart Lens", brand="Zeiss", lens_code="LNS-005",
            category="Contact & Optical Lenses", type="Photochromic Optical Lens", coating="DuraVision Platinum Anti-Scratch",
            price=2999.00, selling_price=2499.00, stock=50, status="Available",
            image="assets/images/products/real_25.jpg"
        )
    ]

    db.session.add_all(eyeglasses + sunglasses + computer_glasses + kids_glasses + lenses)
    db.session.commit()
    print("Successfully seeded database with 25 LOCAL HIGH-DEFINITION OPTICAL GLASSES & LENSES IMAGES!")
