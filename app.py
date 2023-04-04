from io import BytesIO
import streamlit as st          # for creating the web app
import cv2                      # for image processing
from PIL import Image
import numpy as np

def colorize_image(image):
    image_input_arr = np.asarray(image)

    # TO DO: image colorization implementation
    image_output_arr = cv2.cvtColor(image_input_arr, cv2.COLOR_BGR2GRAY)
    image_output = Image.fromarray(image_output_arr)

    return image_output

def img_to_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="jpeg")
    image_output_bytes = buffer.getvalue()

    return image_output_bytes

def main():
    st.title("Image Colorization")
    st.text("sumthing text to add")

    # add file uploader for input
    uploaded_file = st.file_uploader("Upload", type=['jpg','png','jpeg'])

    if uploaded_file is not None:
        image_input = Image.open(uploaded_file)
        filename = uploaded_file.name.split(".")

        col1, col2 = st.columns([0.5, 0.5])
        btn_colorize = ""
        placeholder_img_file = Image.open("placeholder.png").resize((image_input.width, image_input.height))
        placeholder_img = ""
        placeholder_btn  = ""

        # Before Column
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image_input, width=300)
            btn_colorize = st.button('Colorize')

        # After Column
        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            placeholder_img = st.empty()          
            placeholder_img.image(placeholder_img_file, width=300)
            placeholder_btn = st.empty()
            placeholder_btn.button(label='Download Image', disabled=True)

        # Colorize Button
        if btn_colorize:
            image_output = colorize_image(image_input)
            placeholder_img.image(image_output, width=300)
            placeholder_btn.download_button(label='Download Image', 
                                            data=img_to_bytes(image_output),
                                            file_name=filename[0]+"-colored.jpg",
                                            mime="image/jpeg", 
                                            disabled=False)
                

if __name__ == "__main__":
    main()

