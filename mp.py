import streamlit as st
import random
import markovify
from streamlit_option_menu import option_menu 
from PIL import Image, ImageDraw, ImageFont
from datasets import load_dataset

def generate_image_for_quote(quote, image_paths, font_colors, save_path="quote_image.png"):
    image_path = random.choice(image_paths)
    background = Image.open(image_path)
    target_width = 1200
    wpercent = (target_width / float(background.size[0]))
    hsize = int((float(background.size[1]) * float(wpercent)))
    background = background.resize((target_width, hsize), Image.ANTIALIAS)
    draw = ImageDraw.Draw(background)
    font_path = "arial.ttf" 
    max_font_size = 100
    font_size = background.height // 10
    font_color = random.choice(font_colors)
    font = ImageFont.truetype(font_path, font_size)

    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.textsize(quote, font=font)
        if text_width <= background.width and text_height <= background.height:
            break
        font_size -= 1
        if font_size <= 10:
            break
    text_x = (background.width - text_width) / 2
    text_y = (background.height - text_height) / 2
    draw.text((text_x, text_y), quote, fill=font_color, font=font)
    background.save(save_path)
    st.image(background, use_column_width=True)
    
def generate_markov_quote(quotes):
    text_model = markovify.Text(quotes)
    new_quote = text_model.make_sentence() 
    return new_quote if new_quote else "Failed to generate a new quote"

st.set_page_config(page_title="Quotify", page_icon="🖼️")
    
selected=option_menu(
    menu_title=None,
    options= ["Home", "Generate Image", "Contact Us"],
    icons=["house","patch-plus","envelope"],
    orientation="horizontal"            
)    

if selected == "Home":
    st.header("Welcome to Quotify")
    st.code('''
            Turn your favorite words into visual masterpieces! 
            Our quote image generator lets you transform quotes, thoughts, 
            and inspirations into captivating visuals. 
            Random variety of fonts, colors and backgrounds to create images. 
            Whether it's for social media, presentations, or personal inspiration boards,
            our generator makes it easy to bring your words to life. 
            Start creating and sharing your unique quotes today!''',language=None)


if selected == "Generate Image": 
    @st.cache_data()
    def fetch_dataset():
        dataset = load_dataset("asuender/motivational-quotes", "quotes")  
        return dataset["train"]["quote"] 

    dataset_text = fetch_dataset()

    if dataset_text:
        image_paths = ["C:/Users/Mohini/Desktop/mp/background1.jpeg", "C:/Users/Mohini/Desktop/mp/background4.jpeg", "C:/Users/Mohini/Desktop/mp/background2.jpeg", "C:/Users/Mohini/Desktop/mp/background3.jpeg"]  
        font_colors = ["black", "red", "blue", "green"] 

        if st.button("Generate Quote"):
            new_quote = generate_markov_quote(dataset_text)
            generate_image_for_quote(new_quote, image_paths, font_colors)
    
if selected == "Contact Us":    
    st.header("Contact Us:")
    st.markdown("""---""")
    st.subheader("Atharva Durgvale")
    st.caption("16010122816")
    st.markdown("""---""")
    st.subheader("Om Walke")
    st.caption("16010122819")
    st.markdown("""---""")
    st.subheader("Nikhil Deokar")
    st.caption("16010122825")