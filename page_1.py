from PIL import Image, ImageDraw, ImageFont

# Text 1 len should be less than 11 text 2 <21 char
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory where your script is
ASSET_DIR = os.path.join(BASE_DIR, "assets")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
# Font paths
FONT_BOLD = os.path.join(ASSET_DIR, "timesbd.ttf")
FONT_BOLD_ITALIC = os.path.join(ASSET_DIR, "timesbi.ttf")
FONT_ITALIC = os.path.join(ASSET_DIR, "timesi.ttf")


def gen_page1(template,text1,text2,save):

    def draw_text_with_letter_spacing(draw, position, text, font, fill, letter_spacing):
        x, y = position
        for char in text:
            draw.text((x, y), char, font=font, fill=fill)
            char_width = draw.textlength(char, font=font)  
            x += char_width + letter_spacing
    
    bg_path = template  
    img = Image.open(bg_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    font_path = FONT_BOLD
    font_size = 125
    font = ImageFont.truetype(font_path, font_size)

    text1 = text1
    position1 = (108, 304)
    color1 = "black"
    letter_spacing_px = 7

    draw_text_with_letter_spacing(draw, position1, text1, font, color1, letter_spacing_px)

  
    font_italic_path = FONT_BOLD_ITALIC
    font2 = ImageFont.truetype(font_italic_path, 65)
    text2 = text2
    position2 = (108, 510)
    color2 = "#444444"

    draw_text_with_letter_spacing(draw, position2, text2, font2, color2, letter_spacing_px)

    img.save(os.path.join(CONTENT_DIR, save))




