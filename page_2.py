from PIL import Image, ImageDraw, ImageFont

#Text 2 max 240 char

def draw_text_with_letter_spacing(draw, position, text, font, fill, letter_spacing):
    x, y = position
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        char_width = draw.textlength(char, font=font)
        x += char_width + letter_spacing

def wrap_text(text, font, max_width, draw, letter_spacing):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        
        width = sum(draw.textlength(c, font=font) + letter_spacing for c in test_line[:-1]) + draw.textlength(test_line[-1], font=font) if test_line else 0
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def gen_page2(template,text1,text2,text3,save):

   
    bg_path = template  
    font_bold_path = './assets/timesbd.ttf'      
    font_regular_path = './assets/times.ttf'        

    
    img = Image.open(bg_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    
    
    pos1 = (108, 300)
    font1 = ImageFont.truetype(font_bold_path, 100)
    letter_spacing1 = 7

    
    draw_text_with_letter_spacing(draw, pos1, text1, font1, "black", letter_spacing1)

    
    pos2 = (108, 459)
    font2 = ImageFont.truetype(font_regular_path, 36)
    letter_spacing2 = 2
    max_width2 = 864
    color2 = "black"

    
    lines2 = wrap_text(text2, font2, max_width2, draw, letter_spacing2)
    y2 = pos2[1]
    line_height = font2.getbbox("Ay")[3] - font2.getbbox("Ay")[1]  # More accurate than font2.size

    for line in lines2:
        draw_text_with_letter_spacing(draw, (pos2[0], y2), line, font2, color2, letter_spacing2)
        y2 += line_height + 10  


    pos3 = (108, 559)
    font3 = ImageFont.truetype(font_regular_path, 36)
    letter_spacing3 = 2
    max_width3 = 864
    color3 = "black"

    
    lines3 = wrap_text(text3, font3, max_width3, draw, letter_spacing3)
    y3 = pos3[1]
    line_height = font3.getbbox("Ay")[3] - font3.getbbox("Ay")[1]  

    for line in lines3:
        draw_text_with_letter_spacing(draw, (pos3[0], y3), line, font3, color3, letter_spacing3)
        y3 += line_height + 10 

    
    img.save("./"+save)



#gen_page2(template,text1,text2,text3,save)



