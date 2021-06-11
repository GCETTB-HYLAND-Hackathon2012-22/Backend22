import pathlib
import numpy
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image as TF_IMAGE
from fastapi import UploadFile
from PIL import Image as PIL_IMAGE
import numpy as np
import io

model: models.Model = models.load_model(pathlib.Path(__file__).parent/'model'/'X-ray_Checker.h5')
class_list = ["BacterialPneumonia", "Covid", "Normal", "ViralPneumonia"]

ext_class = ["Normal"]

async def load_image_from_file(file: UploadFile, target_size=None):
    f = await file.read()
    img = PIL_IMAGE.open(io.BytesIO(f))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if target_size is not None:
            width_height_tuple = (target_size[1], target_size[0])
            if img.size != width_height_tuple:
                img = img.resize(width_height_tuple, resample=PIL_IMAGE.NEAREST)
    return TF_IMAGE.img_to_array(img)

async def predict(file: UploadFile) -> list:
    image = await load_image_from_file(file, target_size=(256,256))
    image = np.expand_dims(image, axis=0)
    return list(model.predict(image).squeeze())
