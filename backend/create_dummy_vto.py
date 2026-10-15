from PIL import Image, ImageDraw
import os

# Create media dirs if they don't exist
os.makedirs('media/frames', exist_ok=True)

# Create a 400x150 transparent image
img = Image.new('RGBA', (400, 150), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw left lens
draw.rounded_rectangle([20, 20, 180, 130], radius=15, outline=(50, 50, 50, 255), width=8)
# Draw right lens
draw.rounded_rectangle([220, 20, 380, 130], radius=15, outline=(50, 50, 50, 255), width=8)
# Draw bridge
draw.line([(180, 75), (220, 75)], fill=(50, 50, 50, 255), width=8)
# Draw arms (just a little bit)
draw.line([(20, 40), (0, 30)], fill=(50, 50, 50, 255), width=6)
draw.line([(380, 40), (400, 30)], fill=(50, 50, 50, 255), width=6)

img.save('media/frames/rayban_vto.png')
print("Dummy glasses created")
