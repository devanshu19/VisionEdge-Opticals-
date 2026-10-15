import urllib.parse

def create_glasses_svg(name, category, shape, primary_color, lens_color, frame_type="glasses"):
    """
    Generates a crisp, studio-quality SVG product illustration for optical eyewear.
    """
    if frame_type == "contact_lens":
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="lensGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="600" height="400" fill="url(#bg)"/>
  <g filter="url(#shadow)" transform="translate(300, 180)">
    <!-- Contact Lens Solution Pack -->
    <rect x="-110" y="-80" width="220" height="150" rx="24" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect x="-110" y="-80" width="220" height="45" rx="24" fill="{primary_color}"/>
    <rect x="-110" y="-55" width="220" height="20" fill="{primary_color}"/>
    <text x="0" y="-52" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1">VISIONEDGE OPTICS</text>
    
    <!-- Blister Lens Cup -->
    <circle cx="0" cy="20" r="42" fill="url(#lensGrad)" stroke="{primary_color}" stroke-width="3"/>
    <ellipse cx="-12" cy="8" rx="15" ry="8" fill="#ffffff" opacity="0.6" transform="rotate(-30 -12 8)"/>
    <text x="0" y="85" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="700" fill="#334155" text-anchor="middle">{name[:28]}</text>
  </g>
</svg>'''
    else:
        # Determine lens opacity & style based on category
        lens_op = "0.7" if "sunglasses" in category.lower() else ("0.25" if "computer" in category.lower() else "0.15")
        stroke_w = "8" if "kids" in category.lower() else "6"
        
        # Shape specific paths
        if shape.lower() == "aviator":
            lens_left = '<path d="M -130,-35 C -75,-35 -65,-30 -65,5 C -65,45 -85,60 -105,60 C -135,60 -145,35 -145,5 C -145,-30 -140,-35 -130,-35 Z" />'
            lens_right = '<path d="M 130,-35 C 75,-35 65,-30 65,5 C 65,45 85,60 105,60 C 135,60 145,35 145,5 C 145,-30 140,-35 130,-35 Z" />'
        elif shape.lower() == "round":
            lens_left = '<circle cx="-100" cy="5" r="48" />'
            lens_right = '<circle cx="100" cy="5" r="48" />'
        elif shape.lower() == "wayfarer":
            lens_left = '<rect x="-145" y="-35" width="90" height="75" rx="16" />'
            lens_right = '<rect x="55" y="-35" width="90" height="75" rx="16" />'
        elif shape.lower() == "cat-eye":
            lens_left = '<path d="M -155,-40 Q -100,-45 -60,-25 Q -60,40 -100,50 Q -150,45 -155,-40 Z" />'
            lens_right = '<path d="M 155,-40 Q 100,-45 60,-25 Q 60,40 100,50 Q 150,45 155,-40 Z" />'
        elif shape.lower() == "clubmaster":
            lens_left = '<path d="M -145,-35 L -55,-35 L -60,35 Q -100,50 -140,35 Z" />'
            lens_right = '<path d="M 145,-35 L 55,-35 L 60,35 Q 100,50 140,35 Z" />'
        else: # Rectangle / Square / Oval default
            lens_left = '<rect x="-145" y="-30" width="92" height="65" rx="14" />'
            lens_right = '<rect x="53" y="-30" width="92" height="65" rx="14" />'

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="lensTint" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{lens_color}" stop-opacity="{lens_op}"/>
      <stop offset="100%" stop-color="{lens_color}" stop-opacity="0.85"/>
    </linearGradient>
    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#0f172a" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="600" height="400" fill="url(#bgGrad)"/>
  
  <!-- Subtle Studio Reflection Ground -->
  <ellipse cx="300" cy="305" rx="180" ry="18" fill="#0f172a" opacity="0.06"/>
  
  <g filter="url(#dropShadow)" transform="translate(300, 185)">
    <!-- Lens Fill -->
    <g fill="url(#lensTint)" stroke="none">
      {lens_left}
      {lens_right}
    </g>

    <!-- Anti-reflective Glare Lines -->
    <path d="M -135,-15 L -100,25" stroke="#ffffff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>
    <path d="M 65,-15 L 100,25" stroke="#ffffff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>

    <!-- Frame Outline -->
    <g fill="none" stroke="{primary_color}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round">
      {lens_left}
      {lens_right}
      <!-- Nose Bridge -->
      <path d="M -55,-10 C -25,-25 25,-25 55,-10" stroke-width="{int(stroke_w)+2}"/>
      <!-- Temples -->
      <path d="M -145,-15 C -170,-20 -200,-5 -220,10"/>
      <path d="M 145,-15 C 170,-20 200,-5 220,10"/>
    </g>
  </g>
  
  <!-- Category Badge Tag -->
  <rect x="30" y="30" width="140" height="32" rx="16" fill="{primary_color}"/>
  <text x="100" y="51" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{category.upper()}</text>
</svg>'''

    encoded = "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg)
    return encoded
