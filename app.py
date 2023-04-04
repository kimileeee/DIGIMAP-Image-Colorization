from io import StringIO
import streamlit as st          # for creating the web app
import cv2                      # for image processing
from PIL import Image, ImageEnhance
import numpy as np
import os

def colorize_image(image):
    image_input_arr = np.asarray(image)

    # TO DO: image colorization implementation
    image_output_arr = cv2.cvtColor(image_input_arr, cv2.COLOR_BGR2GRAY)
    image_output = Image.fromarray(image_output_arr)

    return image_output

def main():
    st.title("Image Colorization")
    st.text("sumthing text to add")

    # add file uploader for input
    uploaded_file = st.file_uploader("Upload", type=['jpg','png','jpeg'])

    # add BEFORE and AFTER columns
    if uploaded_file is not None:
        image_input = Image.open(uploaded_file)

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image_input, width=300)

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)

        cola, colb, colc = st.columns([0.33, 0.34, 0.33])
        if colb.button('Colorize'):
            image_output = colorize_image(image_input)
            with col2:
                st.image(image_output, width=300)

        # TO DO: output image downloadable

if __name__ == "__main__":
    main()

