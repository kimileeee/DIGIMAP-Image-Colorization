from io import BytesIO
import streamlit as st          # for creating the web app
import cv2                      # for image processing
from PIL import Image
import numpy as np

def colorize_image(image):
    # --------Model file paths--------#
    proto_file = 'Model\colorization_deploy_v2.prototxt'
    model_file = 'Model\colorization_release_v2.caffemodel'
    hull_pts = 'Model\pts_in_hull.npy'
    # --------------#--------------#

    # --------Reading the model params--------#
    net = cv2.dnn.readNetFromCaffe(proto_file, model_file)
    kernel = np.load(hull_pts)
    # -----------------------------------#---------------------#

    # -----Reading and preprocessing image--------#
    img = np.asarray(image)
    scaled = img.astype("float32") / 255.0
    lab_img = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    # -----------------------------------#---------------------#

    # add the cluster centers as 1x1 convolutions to the model
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = kernel.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    # -----------------------------------#---------------------#

    # we'll resize the image for the network
    resized = cv2.resize(lab_img, (224, 224))
    # split the L channel
    L = cv2.split(resized)[0]
    # mean subtraction
    L -= 50
    # -----------------------------------#---------------------#

    # predicting the ab channels from the input L channel

    net.setInput(cv2.dnn.blobFromImage(L))
    ab_channel = net.forward()[0, :, :, :].transpose((1, 2, 0))
    # resize the predicted 'ab' volume to the same dimensions as our
    # input image
    ab_channel = cv2.resize(ab_channel, (img.shape[1], img.shape[0]))

    # Take the L channel from the image
    L = cv2.split(lab_img)[0]
    # Join the L channel with predicted ab channel
    colorized = np.concatenate((L[:, :, np.newaxis], ab_channel), axis=2)

    # Then convert the image from Lab to BGR
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    # change the image to 0-255 range and convert it from float32 to int
    colorized = (255 * colorized).astype("uint8")

    return colorized

def img_to_bytes(image):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
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

