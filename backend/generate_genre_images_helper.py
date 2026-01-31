#!/usr/bin/env python3
"""
Script to generate placeholder genre images or help with AI generation workflow
"""

import os
from pathlib import Path
from genre_mapping import GENRE_IMAGE_MAP

GENRE_IMAGES_DIR = Path(__file__).parent.parent / "public" / "genre-images"
PROMPTS_FILE = Path(__file__).parent.parent / "GENRE_IMAGE_GENERATION_GUIDE.md"

# AI Generation prompts mapping
AI_PROMPTS = {
    "martial-arts": "martial arts anime battle arena, dynamic action scene, fighters in traditional dojo, energy effects, cinematic lighting",
    "vampires": "dark vampire gothic anime night, elegant vampire character, moonlight castle background, red and black color scheme, mysterious atmosphere",
    "harem": "romantic harem anime group sunset, multiple anime characters around protagonist, warm colors, cherry blossoms, sunset background",
    "demons": "demon war anime hell landscape, epic demon battles, fire and brimstone, dark fantasy atmosphere, red and black tones",
    "detective": "noir anime detective city rain, mysterious detective silhouette, urban night scene, neon lights reflecting on wet streets",
    "josei": "mature josei emotional anime drama, sophisticated adult characters, coffee shop or office setting, realistic emotions, soft colors",
    "drama": "dramatic emotional anime scene, intense character expressions, rain and tears, melancholic atmosphere, cinematic composition",
    "games": "virtual game anime cyber arena, gaming interface elements, VR headsets, digital world, neon colors, futuristic setting",
    "isekai": "fantasy portal anime world, magical gate between worlds, epic fantasy landscape, otherworldly atmosphere, vibrant colors",
    "historical": "historical samurai anime era, feudal Japan setting, samurai warriors, traditional architecture, cherry blossoms, period accurate",
    "cyberpunk": "cyberpunk neon anime megacity, futuristic cityscape, neon signs, rain-soaked streets, high-tech low-life aesthetic",
    "comedy": "colorful comedy anime chaos, exaggerated facial expressions, slapstick action, bright cheerful colors, humorous situation",
    "magic": "magic fantasy anime spell world, magical circles and runes, spell casting effects, fantasy wizards, mystical atmosphere",
    "mecha": "giant mech anime battlefield, massive robots fighting, epic scale, explosions and energy beams, sci-fi warfare",
    "mystery": "mysterious supernatural anime fog, eerie atmosphere, shadowy figures, moonlit night, supernatural elements",
    "music": "music concert anime stage lights, idol performers, musical instruments, stage performance, colorful lights, energetic atmosphere",
    "parody": "parody exaggerated anime chaos, over-the-top comedic scene, anime trope references, satirical humor, bright colors",
    "slice-of-life": "cozy slice of life anime town, peaceful everyday scene, school or neighborhood setting, warm comfortable atmosphere",
    "adventure": "epic adventure anime landscape, vast fantasy world, adventurers on journey, mountains and forests, sense of exploration",
    "psychological": "psychological mind anime abstract, surreal mental imagery, fractured reality, dark thoughts visualization, unsettling atmosphere",
    "romance": "romantic anime sunset couple, two characters in romantic moment, cherry blossoms, warm sunset colors, emotional connection",
    "supernatural": "supernatural spirit anime realm, ghosts and yokai, spiritual energy effects, mystical Japanese setting, ethereal atmosphere",
    "shoujo": "shoujo pastel anime romance, sparkles and flowers, romantic shoujo aesthetic, soft pastel colors, dreamy atmosphere",
    "shoujo-ai": "soft yuri anime emotional scene, two female characters, tender moment, gentle colors, emotional intimacy",
    "seinen": "dark seinen mature anime tone, gritty realistic style, mature themes, sophisticated storytelling, darker color palette",
    "shonen": "energetic shonen anime battle, young heroes fighting, power-up effects, dynamic action poses, vibrant colors",
    "sports": "sports anime stadium action, athletic competition, sports equipment, energetic movement, competitive atmosphere",
    "superpower": "superpower anime explosion, characters with superpowers, energy effects, power manifestation, heroic poses",
    "thriller": "thriller suspense anime shadows, tense atmosphere, dramatic lighting, mysterious danger, suspenseful moment",
    "horror": "horror nightmare anime darkness, terrifying creatures, eerie shadows, psychological horror, disturbing atmosphere",
    "sci-fi": "sci-fi anime galaxy future, space stations, futuristic technology, distant planets, advanced civilization",
    "fantasy": "fantasy kingdom anime world, magical castles, dragons and magic, epic fantasy setting, enchanted atmosphere",
    "school": "anime school life classroom, high school setting, students in uniforms, cherry blossoms outside window, nostalgic atmosphere",
    "action": "action anime explosion fight, intense combat scene, dynamic movement, explosions and special effects, adrenaline-filled",
    "ecchi": "playful ecchi anime stylized, suggestive but tasteful anime art, beach or school setting, fan service moments, colorful style",
}


def check_existing_images():
    """Check which genre images already exist"""
    print("🔍 Checking for existing genre images...\n")
    
    existing = []
    missing = []
    
    for genre_name, filename in GENRE_IMAGE_MAP.items():
        found = False
        for ext in ['.webp', '.jpg', '.jpeg', '.png']:
            image_path = GENRE_IMAGES_DIR / f"{filename}{ext}"
            if image_path.exists():
                existing.append((genre_name, filename, ext))
                found = True
                break
        
        if not found:
            missing.append((genre_name, filename))
    
    print(f"✅ Found: {len(existing)} genre images")
    for genre, filename, ext in existing:
        print(f"   • {genre}: {filename}{ext}")
    
    print(f"\n❌ Missing: {len(missing)} genre images")
    for genre, filename in missing:
        print(f"   • {genre}: {filename}")
    
    return existing, missing


def generate_curl_commands(missing_genres):
    """Generate curl commands to download placeholder images"""
    print("\n" + "="*80)
    print("📥 Placeholder Image Download Commands")
    print("="*80)
    print("\nYou can use these curl commands to download placeholder images:")
    print("(These will download generic anime-style images as placeholders)\n")
    
    # Placeholder image service (using placeholder.com or similar)
    for genre, filename in missing_genres[:5]:  # Show first 5 as example
        url = f"https://via.placeholder.com/1024x576/1a1a2e/eee?text={genre.replace(' ', '+')}"
        output_path = GENRE_IMAGES_DIR / f"{filename}.jpg"
        print(f'curl -o "{output_path}" "{url}"')
    
    print("\n... (showing first 5 as example)")


def generate_python_script(missing_genres):
    """Generate a Python script to create simple placeholder images"""
    print("\n" + "="*80)
    print("🐍 Python Script to Generate Placeholder Images")
    print("="*80)
    print("""
To generate placeholder images with Python, install Pillow:
    pip install Pillow

Then run this script:
""")
    
    script = '''#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

GENRE_IMAGES_DIR = Path(__file__).parent / "public" / "genre-images"
GENRE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

genres = [
'''
    
    for genre, filename in missing_genres:
        script += f'    ("{genre}", "{filename}"),\n'
    
    script += ''']

for genre_name, filename in genres:
    # Create 1024x576 image with gradient
    img = Image.new('RGB', (1024, 576), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for i in range(576):
        color = int(26 + (100 * i / 576))
        draw.line([(0, i), (1024, i)], fill=(color, color, color + 30))
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), genre_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (1024 - text_width) // 2
    y = (576 - text_height) // 2
    
    draw.text((x, y), genre_name, fill='white', font=font)
    
    # Save as WebP
    output_path = GENRE_IMAGES_DIR / f"{filename}.webp"
    img.save(output_path, 'WEBP', quality=85)
    print(f"✅ Created: {output_path}")

print(f"\\n✅ Generated {len(genres)} placeholder images!")
'''
    
    # Save script
    script_path = Path(__file__).parent.parent / "generate_placeholder_images.py"
    with open(script_path, 'w') as f:
        f.write(script)
    
    print(f"✅ Script saved to: {script_path}")
    print(f"\nRun it with: python3 {script_path}")


def show_ai_generation_guide():
    """Show AI generation guide"""
    print("\n" + "="*80)
    print("🎨 AI Image Generation Guide")
    print("="*80)
    print(f"""
For best results, use AI image generators like:
• DALL-E 3 (via ChatGPT Plus or API)
• Midjourney (Discord bot)
• Stable Diffusion (local or online)
• Leonardo.ai (web-based)

Full guide with all prompts: {PROMPTS_FILE}

Example workflow with DALL-E 3:
1. Open ChatGPT (with Plus subscription)
2. Copy prompt from the guide
3. Ask: "Generate an image with this prompt: [paste prompt]"
4. Download the generated image
5. Save it as the correct filename in: {GENRE_IMAGES_DIR}

Example prompt for "Боевые искусства":
"{AI_PROMPTS.get('martial-arts')}"
""")


def main():
    """Main function"""
    print("="*80)
    print("🎨 Genre Image Generator Helper")
    print("="*80)
    
    # Create directory if it doesn't exist
    GENRE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Genre images directory: {GENRE_IMAGES_DIR}")
    
    # Check existing images
    existing, missing = check_existing_images()
    
    if not missing:
        print("\n🎉 All genre images are present!")
        return
    
    # Show options
    print("\n" + "="*80)
    print("📋 Options to Get Genre Images")
    print("="*80)
    print("""
1. 🎨 Use AI Image Generators (RECOMMENDED)
   - Best quality and most relevant to genre
   - See full guide: GENRE_IMAGE_GENERATION_GUIDE.md
   
2. 🐍 Generate Simple Placeholders with Python
   - Quick solution for testing
   - Simple colored images with text
   
3. 📥 Download Generic Placeholders
   - Fastest solution
   - Basic placeholder images
""")
    
    # Show AI generation guide
    show_ai_generation_guide()
    
    # Generate Python script for placeholders
    generate_python_script(missing)
    
    # Generate curl commands
    generate_curl_commands(missing)
    
    print("\n" + "="*80)
    print("✅ Helper complete! Choose one of the methods above.")
    print("="*80)


if __name__ == "__main__":
    main()
