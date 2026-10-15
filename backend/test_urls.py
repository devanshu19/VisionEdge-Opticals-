import urllib.request

urls = [
    # Eyeglasses
    "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&q=80",
    "https://images.unsplash.com/photo-1591076482161-42ce6da69f67?w=600&q=80",
    "https://images.unsplash.com/photo-1577803645773-f96470509666?w=600&q=80",
    "https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?w=600&q=80",
    "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=600&q=80",
    
    # Sunglasses
    "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&q=80",
    "https://images.unsplash.com/photo-1509695507497-903c140c43b0?w=600&q=80",
    "https://images.unsplash.com/photo-1589782182703-2aaa69037b5b?w=600&q=80",
    "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=600&q=80",
    "https://images.unsplash.com/photo-1582142407894-ec85a1260a46?w=600&q=80",

    # Computer Glasses
    "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=600&q=80",
    "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80",
    "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&q=80",
    "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=600&q=80",
    "https://images.unsplash.com/photo-1506169894395-36397e4aaee4?w=600&q=80",

    # Kids Glasses
    "https://images.unsplash.com/photo-1544717305-2782549b5136?w=600&q=80",
    "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=600&q=80",
    "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=600&q=80",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=600&q=80",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=600&q=80",

    # Contact & Optical Lenses
    "https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=600&q=80",
    "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=600&q=80",
    "https://images.unsplash.com/photo-1585435557343-3b092031a831?w=600&q=80",
    "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80",
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80"
]

print(f"Testing {len(urls)} URLs...")
success_count = 0
for idx, u in enumerate(urls, 1):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status == 200:
                success_count += 1
                print(f"[{idx}] 200 OK")
            else:
                print(f"[{idx}] STATUS {res.status}")
    except Exception as e:
        print(f"[{idx}] ERROR: {e}")

print(f"\nResult: {success_count}/{len(urls)} URLs working 200 OK.")
