import streamlit as st
import cv2
from PIL import Image, ImageEnhance, ImageOps
import numpy as np


# Define the color adjustment function
def adjust_color(img, color, hue, saturation, luminance):
    # Convert image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a mask with the color range
    mask = cv2.inRange(hsv, color[0], color[1])
    
    # Normalize color adjustment values
    h = color[1][0] - color[0][0]
    s = color[1][1] - color[0][1]
    l = color[1][2] - color[0][2]
    hue = h * hue / 100
    saturation = s * saturation / 100
    luminance = l * luminance / 100

    # Adjust the color with the given Hue, Saturation, and Value
    hsv[:, :, 0] = np.where(mask > 0, hsv[:, :, 0] + hue, hsv[:, :, 0])
    hsv[:, :, 1] = np.where(mask > 0, np.clip(hsv[:, :, 1] + saturation, 0, 255), hsv[:, :, 1])
    hsv[:, :, 2] = np.where(mask > 0, np.clip(hsv[:, :, 2] + luminance, 0, 255), hsv[:, :, 2])

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return img

# Define the Streamlit app
def main():
    st.title('Image HSL Color Adjuster')

    # Upload an image file
    img_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

    # Display placeholder image
    placeholder_img_file = Image.open("placeholder.png")
    placeholder_img = st.empty()
    placeholder_img.image(placeholder_img_file, caption='Adjusted Image', use_column_width=True)

    # BGR values of the colors
    color_sliders = {
        'Red': [(0, 50, 50), (10, 255, 255)],
        'Orange': [(10, 50, 50), (20, 255, 255)],
        'Yellow': [(20, 50, 50), (30, 255, 255)],
        'Green': [(30, 50, 50), (70, 255, 255)],
        'Cyan': [(70, 50, 50), (100, 255, 255)],
        'Blue': [(100, 50, 50), (130, 255, 255)],
        'Violet': [(130, 50, 50), (150, 255, 255)],
        'Magenta': [(150, 50, 50), (170, 255, 255)]
    }

    # color_values = {color: {'Hue': 0, 'Saturation': 0, 'Luminance': 0} for color in color_sliders.keys()}
    img_cv_new = None

    # Display the color buttons and adjust the image on button change
    if img_file is not None:
        img_pil = Image.open(img_file)
        # img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        if 'img_cv' not in st.session_state or not np.array_equal(cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR), st.session_state.img_cv):
            st.session_state.img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        if 'img_output' not in st.session_state:
            st.session_state.img_output = st.session_state.img_cv
        

        if 'color_values' not in st.session_state:
            st.session_state.color_values = {color: {'Hue': 0, 'Saturation': 0, 'Luminance': 0} for color in color_sliders.keys()}

        selected_color = st.sidebar.radio('Select a color:', list(color_sliders.keys()))
        
        st.sidebar.subheader(selected_color)
        color = color_sliders[selected_color]
        
        color_hue = st.sidebar.slider('Hue', -100, 100, st.session_state.color_values[selected_color]['Hue'], key=selected_color+"H")
        color_saturation = st.sidebar.slider('Saturation', -100, 100, st.session_state.color_values[selected_color]['Saturation'], key=selected_color+"S")
        color_luminance = st.sidebar.slider('Luminance', -100, 100, st.session_state.color_values[selected_color]['Luminance'], key=selected_color+"L")

        st.session_state.color_values[selected_color]['Hue'] = color_hue
        st.session_state.color_values[selected_color]['Saturation'] = color_saturation
        st.session_state.color_values[selected_color]['Luminance'] = color_luminance

        if 'selected_color' not in st.session_state or selected_color != st.session_state.selected_color:
            st.session_state.img_cv = st.session_state.img_output
            st.session_state.selected_color = selected_color
        
        st.session_state.img_output = adjust_color(st.session_state.img_cv, color, color_hue, color_saturation, color_luminance)
        img_pil = Image.fromarray(cv2.cvtColor(st.session_state.img_output, cv2.COLOR_BGR2RGB))
        
        placeholder_img.image(img_pil, caption='Adjusted Image', use_column_width=True)


# Run the Streamlit app
if __name__ == '__main__':
    main()


