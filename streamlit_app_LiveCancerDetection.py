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



from torchvision import models
from torchvision import transforms
import torch
 
#dir(models)
#st.write(dir(models))

directory = os.getcwd()


pathtempDir = os.path.join(directory + r'//tempDir/')



st.markdown(f'<h1 style="color:#ffffff;padding:5px;margin:5px;background-color:#Eaa7a6;font-size:40px;">{"  Liver Cancer Detection Application"}</h1>', unsafe_allow_html=True)


"""
# 

Upload your SVS Whole slide image file and click the button Diagnostic !

The preview display all the layers of the svs file.


"""

st.button("Diagnostic", key=None, help=None, on_click=None, args=None, kwargs=None,  type="secondary", disabled=True, use_container_width=False)


uploaded_file = st.file_uploader("Choose a .svs file", type=['svs'])


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    with open(os.path.join(pathtempDir,uploaded_file.name),"wb") as f:
      f.write(uploaded_file.getbuffer())
        

    slide = slideio.open_slide(os.path.join(pathtempDir,uploaded_file.name),"SVS")
   
    ########################
    num_scenes = slide.num_scenes


    st.write("Number of scenes in the file : ", num_scenes)

    """
    # Preview
    #  

    """

    num_scenes = slide.num_scenes
    for index in range(0, num_scenes):
      scene = slide.get_scene(index)   
      st.write("Scene Number ", index+1)
      #  retrieves the image of the layerand scales it to 1500 pixels width picture

      myimage = scene.read_block(size=(1500,0))
      mycaption = "Scene " + str(index + 1)
      st.image(myimage, caption=mycaption)

      #print(slide.get_scene(index).name)



    os.remove(os.path.join(pathtempDir,uploaded_file.name))


    ### TO DO call the model ont the button click on a specific image
    alexnet = models.alexnet(pretrained=True)
    st.write("details Alexnet models")
    st.write(alexnet)


    transform = transforms.Compose([            #[1]
       transforms.Resize(256),                    #[2]
       transforms.CenterCrop(224),                #[3]
       transforms.ToTensor(),                     #[4]
       transforms.Normalize(                      #[5]
       mean=[0.485, 0.456, 0.406],                #[6]
       std=[0.229, 0.224, 0.225]                  #[7]
       )])

    # open test image 
    img = Image.open("dog.jpg")


    # image transformation ,pre-process the image and prepare a batch to be passed through the network.
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)

    # before inference, we need to put the model in eval mode

    alexnet.eval()

    # inference prediction

    out = alexnet(batch_t)
    st.write(out.shape)

    #**************************
    #for archive
    #scene = slide.get_scene(0)   

    #st.write(num_scenes, scene.name, scene.rect, scene.num_channels)
    #st.image(myimage, caption='Image uploaded')