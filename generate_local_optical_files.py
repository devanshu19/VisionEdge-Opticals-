import os

output_dir = r"c:\projects\VisionEdge\frontend\assets\images\products"
os.makedirs(output_dir, exist_ok=True)

products = [
    # Eyeglasses (1 - 5)
    {"file": "opt_1.svg", "title": "Classic Black Wayfarer Eyeglasses", "cat": "EYEGLASSES", "shape": "wayfarer", "frame_col": "#0f172a", "lens_col": "#e2e8f0", "op": "0.15"},
    {"file": "opt_2.svg", "title": "Vintage Round Metal Specs", "cat": "EYEGLASSES", "shape": "round", "frame_col": "#d97706", "lens_col": "#fef3c7", "op": "0.15"},
    {"file": "opt_3.svg", "title": "Browline Clubmaster Frame", "cat": "EYEGLASSES", "shape": "clubmaster", "frame_col": "#78350f", "lens_col": "#e2e8f0", "op": "0.15"},
    {"file": "opt_4.svg", "title": "Crystal Clear Oval Eyeglasses", "cat": "EYEGLASSES", "shape": "oval", "frame_col": "#06b6d4", "lens_col": "#cff4fc", "op": "0.2"},
    {"file": "opt_5.svg", "title": "Titanium Ultra-Light Square Specs", "cat": "EYEGLASSES", "shape": "square", "frame_col": "#475569", "lens_col": "#e2e8f0", "op": "0.15"},
    
    # Sunglasses (6 - 10)
    {"file": "opt_6.svg", "title": "Gold Classic Aviator Sunglasses", "cat": "SUNGLASSES", "shape": "aviator", "frame_col": "#b45309", "lens_col": "#064e3b", "op": "0.85"},
    {"file": "opt_7.svg", "title": "Matte Black Sport Wayfarer Shades", "cat": "SUNGLASSES", "shape": "wayfarer", "frame_col": "#020617", "lens_col": "#0f172a", "op": "0.9"},
    {"file": "opt_8.svg", "title": "Retro Dark Lens Round Sunglasses", "cat": "SUNGLASSES", "shape": "round", "frame_col": "#334155", "lens_col": "#1e293b", "op": "0.88"},
    {"file": "opt_9.svg", "title": "Glamour Cat-Eye Polarized Sunglasses", "cat": "SUNGLASSES", "shape": "cat-eye", "frame_col": "#be185d", "lens_col": "#831843", "op": "0.8"},
    {"file": "opt_10.svg", "title": "Hexagonal Metal Frame Sunglasses", "cat": "SUNGLASSES", "shape": "hexagonal", "frame_col": "#92400e", "lens_col": "#78350f", "op": "0.8"},

    # Computer Glasses (11 - 15)
    {"file": "opt_11.svg", "title": "Blue-Light Block Shield Transparent", "cat": "COMPUTER GLASSES", "shape": "rectangle", "frame_col": "#0284c7", "lens_col": "#38bdf8", "op": "0.3"},
    {"file": "opt_12.svg", "title": "Anti-Glare Screen Reader Matte Black", "cat": "COMPUTER GLASSES", "shape": "wayfarer", "frame_col": "#0f172a", "lens_col": "#0284c7", "op": "0.3"},
    {"file": "opt_13.svg", "title": "Digital Ray Cut Minimalist Frame", "cat": "COMPUTER GLASSES", "shape": "round", "frame_col": "#64748b", "lens_col": "#38bdf8", "op": "0.25"},
    {"file": "opt_14.svg", "title": "Pro Gamer Amber Blue Block Glasses", "cat": "COMPUTER GLASSES", "shape": "rectangle", "frame_col": "#1e293b", "lens_col": "#f59e0b", "op": "0.4"},
    {"file": "opt_15.svg", "title": "Executive Workstation Blue-Ray Specs", "cat": "COMPUTER GLASSES", "shape": "clubmaster", "frame_col": "#1e3a8a", "lens_col": "#60a5fa", "op": "0.3"},

    # Kids Glasses (16 - 20)
    {"file": "opt_16.svg", "title": "Kids Flexible Blue TR90 Specs", "cat": "KIDS GLASSES", "shape": "rectangle", "frame_col": "#2563eb", "lens_col": "#93c5fd", "op": "0.2"},
    {"file": "opt_17.svg", "title": "Kids Bright Red Playtime Glasses", "cat": "KIDS GLASSES", "shape": "round", "frame_col": "#dc2626", "lens_col": "#fca5a5", "op": "0.2"},
    {"file": "opt_18.svg", "title": "Junior Pastel Pink Oval Glasses", "cat": "KIDS GLASSES", "shape": "cat-eye", "frame_col": "#db2777", "lens_col": "#fbcfe8", "op": "0.2"},
    {"file": "opt_19.svg", "title": "Comfy Flex Yellow Round Specs", "cat": "KIDS GLASSES", "shape": "round", "frame_col": "#d97706", "lens_col": "#fef08a", "op": "0.2"},
    {"file": "opt_20.svg", "title": "Smart Junior Wayfarer Eyeglasses", "cat": "KIDS GLASSES", "shape": "wayfarer", "frame_col": "#1e3a8a", "lens_col": "#93c5fd", "op": "0.2"},

    # Contact & Optical Lenses (21 - 25)
    {"file": "opt_21.svg", "title": "Acuvue Moist Daily Contact Lenses", "cat": "CONTACT & OPTICAL LENSES", "shape": "lens_pack", "frame_col": "#0284c7", "lens_col": "#38bdf8", "op": "0.7"},
    {"file": "opt_22.svg", "title": "FreshLook ColorEnhance Hazel Lens", "cat": "CONTACT & OPTICAL LENSES", "shape": "lens_pack", "frame_col": "#059669", "lens_col": "#34d399", "op": "0.7"},
    {"file": "opt_23.svg", "title": "UltraClear HD Progressive Precision", "cat": "CONTACT & OPTICAL LENSES", "shape": "lens_pack", "frame_col": "#7c3aed", "lens_col": "#c084fc", "op": "0.7"},
    {"file": "opt_24.svg", "title": "Biofinity Toric Astigmatism Monthly", "cat": "CONTACT & OPTICAL LENSES", "shape": "lens_pack", "frame_col": "#0891b2", "lens_col": "#67e8f9", "op": "0.7"},
    {"file": "opt_25.svg", "title": "Transitions Gen8 Photochromic Lens", "cat": "CONTACT & OPTICAL LENSES", "shape": "lens_pack", "frame_col": "#475569", "lens_col": "#94a3b8", "op": "0.7"},
]

for p in products:
    file_path = os.path.join(output_dir, p["file"])
    
    if p["shape"] == "lens_pack":
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="lensGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['frame_col']}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{p['lens_col']}" stop-opacity="0.5"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="600" height="400" fill="url(#bg)"/>
  <g filter="url(#shadow)" transform="translate(300, 180)">
    <rect x="-120" y="-85" width="240" height="160" rx="20" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect x="-120" y="-85" width="240" height="50" rx="20" fill="{p['frame_col']}"/>
    <rect x="-120" y="-55" width="240" height="20" fill="{p['frame_col']}"/>
    <text x="0" y="-54" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1">VISIONEDGE OPTICAL LENS</text>
    <circle cx="0" cy="22" r="44" fill="url(#lensGrad)" stroke="{p['frame_col']}" stroke-width="3"/>
    <ellipse cx="-14" cy="8" rx="16" ry="9" fill="#ffffff" opacity="0.6" transform="rotate(-30 -14 8)"/>
    <text x="0" y="92" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">{p['title'][:28]}</text>
  </g>
</svg>'''
    else:
        stroke_w = "8" if "KIDS" in p["cat"] else "6"
        s = p["shape"]
        
        if s == "aviator":
            lens_l = '<path d="M -130,-35 C -75,-35 -65,-30 -65,5 C -65,45 -85,60 -105,60 C -135,60 -145,35 -145,5 C -145,-30 -140,-35 -130,-35 Z" />'
            lens_r = '<path d="M 130,-35 C 75,-35 65,-30 65,5 C 65,45 85,60 105,60 C 135,60 145,35 145,5 C 145,-30 140,-35 130,-35 Z" />'
        elif s == "round":
            lens_l = '<circle cx="-100" cy="5" r="48" />'
            lens_r = '<circle cx="100" cy="5" r="48" />'
        elif s == "wayfarer":
            lens_l = '<rect x="-145" y="-35" width="90" height="75" rx="16" />'
            lens_r = '<rect x="55" y="-35" width="90" height="75" rx="16" />'
        elif s == "cat-eye":
            lens_l = '<path d="M -155,-40 Q -100,-45 -60,-25 Q -60,40 -100,50 Q -150,45 -155,-40 Z" />'
            lens_r = '<path d="M 155,-40 Q 100,-45 60,-25 Q 60,40 100,50 Q 150,45 155,-40 Z" />'
        elif s == "clubmaster":
            lens_l = '<path d="M -145,-35 L -55,-35 L -60,35 Q -100,50 -140,35 Z" />'
            lens_r = '<path d="M 145,-35 L 55,-35 L 60,35 Q 100,50 140,35 Z" />'
        else: # rectangle / square / oval / hexagonal
            lens_l = '<rect x="-145" y="-30" width="92" height="65" rx="14" />'
            lens_r = '<rect x="53" y="-30" width="92" height="65" rx="14" />'

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="lensTint" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['lens_col']}" stop-opacity="{p['op']}"/>
      <stop offset="100%" stop-color="{p['lens_col']}" stop-opacity="0.85"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#0f172a" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="600" height="400" fill="url(#bg)"/>
  <ellipse cx="300" cy="305" rx="180" ry="18" fill="#0f172a" opacity="0.06"/>
  
  <g filter="url(#shadow)" transform="translate(300, 185)">
    <g fill="url(#lensTint)" stroke="none">
      {lens_l}
      {lens_r}
    </g>
    <path d="M -135,-15 L -100,25" stroke="#ffffff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>
    <path d="M 65,-15 L 100,25" stroke="#ffffff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>

    <g fill="none" stroke="{p['frame_col']}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round">
      {lens_l}
      {lens_r}
      <path d="M -55,-10 C -25,-25 25,-25 55,-10" stroke-width="{int(stroke_w)+2}"/>
      <path d="M -145,-15 C -170,-20 -200,-5 -220,10"/>
      <path d="M 145,-15 C 170,-20 200,-5 220,10"/>
    </g>
  </g>
  <rect x="30" y="30" width="160" height="32" rx="16" fill="{p['frame_col']}"/>
  <text x="110" y="51" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{p['cat']}</text>
</svg>'''

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

print(f"Generated {len(products)} local optical SVG product files in {output_dir}")
