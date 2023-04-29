from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import os
import tempfile
import io

import slideio




from PIL import Image 
Image.MAX_IMAGE_PIXELS = 1000000000 



directory = os.getcwd()


pathtempDir = os.path.join(directory + r'//tempDir/')





"""
# Liver Cancer Detection Application

Upload your SVS Whole slide image file and click the button Diagnostic !

The preview display the first layer of the svs file.


"""

st.button("Diagnostic", key=None, help=None, on_click=None, args=None, kwargs=None,  type="secondary", disabled=True, use_container_width=False)


uploaded_file = st.file_uploader("Choose a file")


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    with open(os.path.join(pathtempDir,uploaded_file.name),"wb") as f:
      f.write(uploaded_file.getbuffer())
        

    slide = slideio.open_slide(os.path.join(pathtempDir,uploaded_file.name),"SVS")
   
    num_scenes = slide.num_scenes
    scene = slide.get_scene(0)   


    st.write(num_scenes, scene.name, scene.rect, scene.num_channels)


    # A code snippet bellow. retrieves the whole image and scales it to 500 pixels width picture
    myimage = scene.read_block(size=(1500,0))



    """
    # Preview
    #  

    """

    st.image(myimage, caption='Image uploaded')

    os.remove(os.path.join(pathtempDir,uploaded_file.name))


   


