import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw

img = Image.new('RGB', (100, 100), 'black')
draw = ImageDraw.Draw(img)
draw.text((0,0), 'abc', font=ImageFont.truetype("../resources/msyh.ttc", 30), textColor=(255,255,255))
img = np.asarray(img)/255

sr1 = Image.new('RGB', (100, 100), 'black')
sr1 = np.asarray(sr1)

dst = sr1*(1-img)+(img)*(200,0,200)
print(dst.shape)
cv2.imshow('a', sr1)
cv2.imshow('b', img)
cv2.imshow('f', dst.astype(np.uint8))
cv2.waitKey(100)
input()



