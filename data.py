import os
import shutil
import torch
import faiss
import numpy as np
from PIL import Image
import requests
from transformers import AutoProcessor, CLIPModel
from IPython.display import display

# Iterate over all files in 'Mountains_and_Beaches' and copy to 'data'
os.makedirs('data', exist_ok=True)
for root, dirs, files in os.walk('Mountains_and_Beaches'):
    for file in files:
        source_path = os.path.join(root, file)
        destination_path = 'data'
        shutil.copy(source_path, destination_path)

shutil.rmtree('Mountains_and_Beaches')

filenames = []
for item in os.listdir('data'):
  filenames.append(item)

filenames.sort()

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

all_images = []
for i in filenames:
  image = Image.open('data/'+i)
  inputs = processor(images=image, return_tensors="pt")
  image_features = model.get_image_features(**inputs)
  all_images.append(image_features[0].detach().numpy())
  
all_images = np.array([embedding for embedding in all_images]).astype("float32")

index = faiss.IndexFlatL2(image_features.shape[1])
index = faiss.IndexIDMap(index)

index.add_with_ids(all_images, range(0, len(all_images)))