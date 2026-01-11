from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_professional_icon():
    # 1. Canvas Settings
    size = (512, 512)
    bg_color = "#1e272e"  # Dark Corporate Charcoal
    accent_color = "#00d2d3" # Cyan/Teal (Modern Tech)
    text_color = "white"
    
    # 2. Create Image
    img = Image.new('RGBA', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 3. Draw Background Gradient/Shape (Subtle Tech Look)
    # Draw a rounded rectangle container
    margin = 20
    draw.rounded_rectangle(
        [(margin, margin), (size[0]-margin, size[1]-margin)], 
        radius=80, 
        fill="#2f3640", 
        outline=accent_color, 
        width=15
    )

    # 4. Draw "IE" Text (Block Style - No external fonts needed)
    # Drawing 'I'
    draw.rectangle([100, 100, 160, 400], fill=text_color)
    
    # Drawing 'E'
    draw.rectangle([200, 100, 260, 400], fill=text_color) # Vertical
    draw.rectangle([200, 100, 400, 160], fill=text_color) # Top
    draw.rectangle([200, 220, 380, 280], fill=text_color) # Middle
    draw.rectangle([200, 340, 400, 400], fill=text_color) # Bottom

    # 5. Draw "Efficiency" Graph Overlay
    # A rising line graph representing productivity
    points = [
        (50, 450),
        (150, 350),
        (250, 380),
        (350, 150),
        (450, 50)
    ]
    # Draw line
    draw.line(points, fill=accent_color, width=30, joint="curve")
    
    # Draw Dots at points
    for p in points:
        r = 20
        draw.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=accent_color)

    # 6. Save as ICO (Includes multiple sizes for Windows)
    img.save("logo.ico", format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("Success! 'logo.ico' has been generated.")

if __name__ == "__main__":
    try:
        create_professional_icon()
    except ImportError:
        print("Error: Pillow library missing.")
        print("Run: pip install Pillow")