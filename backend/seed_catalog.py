"""
VisionEdge Catalog & Admin Initialization
Guarantees Admin account (Dev@7272) and rich initial inventory catalog across all categories.
"""

from werkzeug.security import generate_password_hash

def seed_initial_catalog_and_admin(app=None):
    from models import db, User, Frame, Lens, Brand, Category

    try:
        # 1. Guarantee admin account exists with password: Dev@7272
        admin_user = User.query.filter((User.role == 'admin') | (User.username == 'admin')).first()
        if not admin_user:
            admin_user = User(
                username="admin",
                first_name="Admin",
                last_name="VisionEdge",
                email="admin@visionedge.com",
                role="admin",
                password_hash=generate_password_hash("Dev@7272"),
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("[VisionEdge] Admin user created with password Dev@7272")
        else:
            admin_user.role = "admin"
            admin_user.password_hash = generate_password_hash("Dev@7272")
            db.session.commit()

        # 2. Seed Brands if empty
        if Brand.query.count() == 0:
            brands = [
                Brand(name="Ray-Ban", status="Active"),
                Brand(name="Oakley", status="Active"),
                Brand(name="Gucci", status="Active"),
                Brand(name="Prada", status="Active"),
                Brand(name="Titan Eye Plus", status="Active"),
                Brand(name="Vogue Eyewear", status="Active"),
                Brand(name="VisionEdge", status="Active"),
                Brand(name="FlexiKids", status="Active"),
                Brand(name="Acuvue", status="Active"),
                Brand(name="Essilor", status="Active"),
                Brand(name="Zeiss", status="Active"),
            ]
            db.session.add_all(brands)
            db.session.commit()

        # 3. Seed Categories if empty
        if Category.query.count() == 0:
            cats = [
                Category(name="Eyeglasses", type="Frame"),
                Category(name="Sunglasses", type="Frame"),
                Category(name="Computer Glasses", type="Frame"),
                Category(name="Kids Glasses", type="Frame"),
                Category(name="Contact & Optical Lenses", type="Lens"),
            ]
            db.session.add_all(cats)
            db.session.commit()

        # 4. Seed Products if catalog has fewer than 10 products
        if Frame.query.count() < 10:
            items = [
                # Eyeglasses (5 items)
                Frame(
                    name="Classic Black Wayfarer Eyeglasses", brand="Ray-Ban", model="RB-WAY-01", frame_code="EYE-001",
                    category="Eyeglasses", price=1499.00, selling_price=1299.00, stock=45, status="Available",
                    shape="Wayfarer", material="Acetate", color="Black", size="Medium", gender="Unisex",
                    image="assets/images/products/real_eye1.png"
                ),
                Frame(
                    name="Vintage Round Metal Specs", brand="Oakley", model="OK-RND-02", frame_code="EYE-002",
                    category="Eyeglasses", price=1899.00, selling_price=1599.00, stock=35, status="Available",
                    shape="Round", material="Metal", color="Gold", size="Medium", gender="Unisex",
                    image="assets/images/products/real_eye2.png"
                ),
                Frame(
                    name="Browline Clubmaster Frame", brand="Vogue Eyewear", model="VG-CLM-03", frame_code="EYE-003",
                    category="Eyeglasses", price=2199.00, selling_price=1799.00, stock=25, status="Available",
                    shape="Clubmaster", material="Titanium", color="Tortoise Shell", size="Medium", gender="Unisex",
                    image="assets/images/products/real_eye3.png"
                ),
                Frame(
                    name="Crystal Clear Oval Eyeglasses", brand="VisionEdge", model="VE-OVL-04", frame_code="EYE-004",
                    category="Eyeglasses", price=1299.00, selling_price=999.00, stock=50, status="Available",
                    shape="Oval", material="TR90", color="Transparent Clear", size="Medium", gender="Unisex",
                    image="assets/images/products/real_eye4.png"
                ),
                Frame(
                    name="Titanium Ultra-Light Square Specs", brand="Titan Eye Plus", model="TT-SQR-05", frame_code="EYE-005",
                    category="Eyeglasses", price=2499.00, selling_price=2099.00, stock=30, status="Available",
                    shape="Square", material="Titanium", color="Matte Silver", size="Medium", gender="Unisex",
                    image="assets/images/products/real_eye5.png"
                ),
                # Sunglasses (5 items)
                Frame(
                    name="Gold Classic Aviator Sunglasses", brand="Ray-Ban", model="RB-AVI-01", frame_code="SUN-001",
                    category="Sunglasses", price=2999.00, selling_price=2499.00, stock=40, status="Available",
                    shape="Aviator", material="Metal", color="Gold / Green Lens", size="Large", gender="Unisex",
                    image="assets/images/products/real_sun1.png"
                ),
                Frame(
                    name="Matte Black Sport Wayfarer Shades", brand="Oakley", model="OK-SPT-02", frame_code="SUN-002",
                    category="Sunglasses", price=2799.00, selling_price=2299.00, stock=30, status="Available",
                    shape="Wayfarer", material="TR90", color="Matte Black", size="Large", gender="Men",
                    image="assets/images/products/real_sun2.png"
                ),
                Frame(
                    name="Retro Dark Lens Round Sunglasses", brand="Prada", model="PR-RND-03", frame_code="SUN-003",
                    category="Sunglasses", price=3499.00, selling_price=2999.00, stock=20, status="Available",
                    shape="Round", material="Acetate", color="Dark Gunmetal", size="Medium", gender="Unisex",
                    image="assets/images/products/real_sun3.png"
                ),
                Frame(
                    name="Glamour Cat-Eye Polarized Sunglasses", brand="Gucci", model="GC-CAT-04", frame_code="SUN-004",
                    category="Sunglasses", price=3899.00, selling_price=3299.00, stock=15, status="Available",
                    shape="Cat-Eye", material="Acetate", color="Rose Gold / Tinted", size="Medium", gender="Women",
                    image="assets/images/products/real_sun4.png"
                ),
                Frame(
                    name="Hexagonal Metal Frame Sunglasses", brand="Ray-Ban", model="RB-HEX-05", frame_code="SUN-005",
                    category="Sunglasses", price=3199.00, selling_price=2699.00, stock=38, status="Available",
                    shape="Hexagonal", material="Metal", color="Copper / Brown Tint", size="Medium", gender="Unisex",
                    image="assets/images/products/real_sun5.png"
                ),
                # Computer Glasses (5 items)
                Frame(
                    name="Blue-Light Block Shield Transparent", brand="VisionEdge", model="VE-BLU-01", frame_code="CMP-001",
                    category="Computer Glasses", price=1599.00, selling_price=1199.00, stock=60, status="Available",
                    shape="Rectangle", material="Polycarbonate", color="Transparent Crystal", size="Medium", gender="Unisex",
                    image="assets/images/products/real_11.jpg"
                ),
                Frame(
                    name="Anti-Glare Screen Reader Matte Black", brand="Titan Eye Plus", model="TT-AGR-02", frame_code="CMP-002",
                    category="Computer Glasses", price=1699.00, selling_price=1299.00, stock=50, status="Available",
                    shape="Wayfarer", material="TR90 Ultra Lightweight", color="Matte Black", size="Medium", gender="Unisex",
                    image="assets/images/products/real_12.jpg"
                ),
                Frame(
                    name="Digital Ray Cut Minimalist Frame", brand="VisionEdge", model="VE-DIG-03", frame_code="CMP-003",
                    category="Computer Glasses", price=1899.00, selling_price=1499.00, stock=40, status="Available",
                    shape="Round", material="Beta Titanium", color="Sleek Grey", size="Medium", gender="Unisex",
                    image="assets/images/products/real_13.jpg"
                ),
                Frame(
                    name="Pro Gamer Amber Blue Block Glasses", brand="Oakley", model="OK-GMR-04", frame_code="CMP-004",
                    category="Computer Glasses", price=2499.00, selling_price=1999.00, stock=25, status="Available",
                    shape="Rectangle", material="Alloy Metal", color="Onyx Black", size="Large", gender="Unisex",
                    image="assets/images/products/real_14.jpg"
                ),
                Frame(
                    name="Executive Workstation Blue-Ray Specs", brand="VisionEdge", model="VE-EXC-05", frame_code="CMP-005",
                    category="Computer Glasses", price=1999.00, selling_price=1599.00, stock=35, status="Available",
                    shape="Clubmaster", material="Acetate & Metal", color="Navy Blue / Silver", size="Medium", gender="Unisex",
                    image="assets/images/products/real_15.jpg"
                ),
                # Kids Glasses (5 items)
                Frame(
                    name="Kids Flexible Blue TR90 Specs", brand="FlexiKids", model="FK-BLU-01", frame_code="KID-001",
                    category="Kids Glasses", price=999.00, selling_price=699.00, stock=40, status="Available",
                    shape="Rectangle", material="Flexible TR90 Rubber", color="Electric Blue", size="Small", gender="Kids",
                    image="assets/images/products/real_16.jpg"
                ),
                Frame(
                    name="Kids Dark Blue Oval TR90 Eyeglasses", brand="FlexiKids", model="FK-OVL-06", frame_code="KID-006",
                    category="Kids Glasses", price=1099.00, selling_price=749.00, stock=40, status="Available",
                    shape="Oval", material="Flexible TR90", color="Dark Blue / Cyan", size="Small", gender="Kids",
                    image="assets/images/products/real_26.webp"
                ),
                Frame(
                    name="Junior Red Black Rectangle Specs", brand="FlexiKids", model="FK-RED-07", frame_code="KID-007",
                    category="Kids Glasses", price=1149.00, selling_price=799.00, stock=35, status="Available",
                    shape="Rectangle", material="Flexible Silicone", color="Red / Black", size="Small", gender="Kids",
                    image="assets/images/products/real_27.webp"
                ),
                Frame(
                    name="Kids Teal Blue Sporty Eyeglasses", brand="FlexiKids", model="FK-TEL-08", frame_code="KID-008",
                    category="Kids Glasses", price=1099.00, selling_price=749.00, stock=38, status="Available",
                    shape="Rectangle", material="TR90 Soft Bend", color="Teal / Black", size="Small", gender="Kids",
                    image="assets/images/products/real_28.webp"
                ),
                Frame(
                    name="Junior Coral Pink Oval Kids Glasses", brand="FlexiKids", model="FK-PNK-09", frame_code="KID-009",
                    category="Kids Glasses", price=1199.00, selling_price=849.00, stock=42, status="Available",
                    shape="Oval", material="Lightweight Acetate", color="Coral Pink / Brown", size="Small", gender="Kids",
                    image="assets/images/products/real_29.webp"
                ),
            ]
            for itm in items:
                if not Frame.query.filter_by(frame_code=itm.frame_code).first():
                    db.session.add(itm)
            db.session.commit()
            print("[VisionEdge] Successfully seeded 20 high-quality frames across categories!")

        # 5. Seed Lenses if fewer than 5 lenses
        if Lens.query.count() < 5:
            lens_items = [
                Lens(
                    name="Acuvue Moist Daily Contact Lenses (30 Pack)", brand="Acuvue", lens_code="LNS-001",
                    category="Contact & Optical Lenses", type="Daily Contact Lens", lens_type="Daily Contact Lens",
                    coating="HydraClear Ultra Moisture", price=1899.00, selling_price=1499.00, stock=100, status="Available",
                    image="assets/images/products/real_21.jpg"
                ),
                Lens(
                    name="FreshLook ColorEnhance Hazel Contact Lenses", brand="Acuvue", lens_code="LNS-002",
                    category="Contact & Optical Lenses", type="Monthly Color Lens", lens_type="Monthly Color Lens",
                    coating="ColorBlend Breathable Matrix", price=1699.00, selling_price=1299.00, stock=80, status="Available",
                    image="assets/images/products/real_22.jpg"
                ),
                Lens(
                    name="UltraClear HD Progressive Precision Lens", brand="Essilor", lens_code="LNS-003",
                    category="Contact & Optical Lenses", type="Progressive Optical Lens", lens_type="Progressive Optical Lens",
                    coating="Crizal Sapphire Anti-Reflective", price=3499.00, selling_price=2899.00, stock=60, status="Available",
                    image="assets/images/products/real_23.jpg"
                ),
                Lens(
                    name="Biofinity Toric Astigmatism Monthly Lenses", brand="Essilor", lens_code="LNS-004",
                    category="Contact & Optical Lenses", type="Toric Contact Lens", lens_type="Toric Contact Lens",
                    coating="Aquaform Comfort Tech", price=2299.00, selling_price=1899.00, stock=75, status="Available",
                    image="assets/images/products/real_24.jpg"
                ),
                Lens(
                    name="Transitions Gen8 Photochromic Smart Lens", brand="Zeiss", lens_code="LNS-005",
                    category="Contact & Optical Lenses", type="Photochromic Optical Lens", lens_type="Photochromic Optical Lens",
                    coating="DuraVision Platinum Anti-Scratch", price=2999.00, selling_price=2499.00, stock=50, status="Available",
                    image="assets/images/products/real_25.jpg"
                )
            ]
            for l in lens_items:
                if not Lens.query.filter_by(lens_code=l.lens_code).first():
                    db.session.add(l)
            db.session.commit()
            print("[VisionEdge] Successfully seeded 5 optical & contact lenses!")

    except Exception as e:
        db.session.rollback()
        print(f"[VisionEdge Seed Notice] {e}")
