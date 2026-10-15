from app import create_app
from models import Frame, Lens

app = create_app()
with app.app_context():
    frames = Frame.query.all()
    lenses = Lens.query.all()
    
    print(f"Total Frames: {len(frames)}")
    print(f"Total Lenses: {len(lenses)}")
    
    cat_counts = {}
    all_images = set()
    
    for f in frames:
        cat = f.category or "Unknown"
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        all_images.add(f.image)
        
    for l in lenses:
        cat = l.category or "Unknown"
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        all_images.add(l.image)
        
    print("\nProduct Count per Category:")
    for cat, count in cat_counts.items():
        print(f" - {cat}: {count} products")
        
    total_products = len(frames) + len(lenses)
    print(f"\nTotal Products: {total_products}")
    print(f"Unique Images Count: {len(all_images)}")
    
    if total_products == len(all_images):
        print("SUCCESS: Every single product has a completely UNIQUE image! No duplicate goggles images.")
    else:
        print(f"WARNING: {total_products - len(all_images)} duplicate images detected.")
