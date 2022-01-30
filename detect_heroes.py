import numpy as np
import cv2
import pyautogui
from PIL import Image
import imagehash
import os
import json

# return list of hero portraits
def load_portraits():
    portraits = []
    with open('./portrait_data.json') as port_json:
        portrait_dict = json.load(port_json)

    files = [f for f in os.listdir('./portraits/') if os.path.isfile(os.path.join('./portraits/',f))]
    for portrait in files:
        portraits.append((portrait_dict[portrait],Image.open('./portraits/'+portrait).resize((90,50))))

    return portraits

portraits = load_portraits()

# take screenshot using pyautogui
image = pyautogui.screenshot()
#image = Image.open('./image1.png')

# since the pyautogui takes as a 
# PIL(pillow) and in RGB we need to 
# convert it to numpy array and BGR 
# so we can write it to the disk
im = cv2.cvtColor(np.array(image),
                    cv2.COLOR_RGB2BGR)
   
# writing it to the disk using opencv
cv2.imwrite("image1.png", im)

radiant_1 = image.crop((3320, 302, 3320+90, 302+50))
radiant_1_im = cv2.cvtColor(np.array(radiant_1), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_1.png", radiant_1_im)
radiant_2 = image.crop((3320, 355, 3320+90, 359+50))
radiant_2_im = cv2.cvtColor(np.array(radiant_2), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_2.png", radiant_2_im)
radiant_3 = image.crop((3320, 528, 3320+90, 529+50))
radiant_3_im = cv2.cvtColor(np.array(radiant_3), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_3.png", radiant_3_im)
radiant_4 = image.crop((3320, 582, 3320+90, 584+50))
radiant_4_im = cv2.cvtColor(np.array(radiant_4), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_4.png", radiant_4_im)
radiant_5 = image.crop((3320, 718, 3320+90, 719+50))
radiant_5_im = cv2.cvtColor(np.array(radiant_5), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_5.png", radiant_5_im)

dire_1 = image.crop((3493, 302, 3493+90, 302+50))
dire_1_im = cv2.cvtColor(np.array(dire_1), cv2.COLOR_RGB2BGR)
cv2.imwrite("dire_1.png", dire_1_im)
dire_2 = image.crop((3493, 355, 3493+90, 359+50))
dire_2_im = cv2.cvtColor(np.array(dire_2), cv2.COLOR_RGB2BGR)
cv2.imwrite("dire_2.png", dire_2_im)
dire_3 = image.crop((3493, 528, 3493+90, 529+50))
dire_3_im = cv2.cvtColor(np.array(dire_3), cv2.COLOR_RGB2BGR)
cv2.imwrite("dire_3.png", dire_3_im)
dire_4 = image.crop((3493, 582, 3493+90, 584+50))
dire_4_im = cv2.cvtColor(np.array(dire_4), cv2.COLOR_RGB2BGR)
cv2.imwrite("dire_4.png", dire_4_im)
dire_5 = image.crop((3493, 718, 3493+90, 719+50))
dire_5_im = cv2.cvtColor(np.array(dire_5), cv2.COLOR_RGB2BGR)
cv2.imwrite("dire_5.png", dire_5_im)

min_radiant_1 = ('',9999999999999)
min_radiant_2 = ('',9999999999999)
min_radiant_3 = ('',9999999999999)
min_radiant_4 = ('',9999999999999)
min_radiant_5 = ('',9999999999999)
min_dire_1 = ('',9999999999999)
min_dire_2 = ('',9999999999999)
min_dire_3 = ('',9999999999999)
min_dire_4 = ('',9999999999999)
min_dire_5 = ('',9999999999999)

for hero, portrait in portraits:
    if (new_min := imagehash.phash(radiant_1) - imagehash.phash(portrait)) < min_radiant_1[1]:
        min_radiant_1 = (hero, new_min)
    if (new_min := imagehash.phash(radiant_2) - imagehash.phash(portrait)) < min_radiant_2[1]:
        min_radiant_2 = (hero, new_min)
    if (new_min := imagehash.phash(radiant_3) - imagehash.phash(portrait)) < min_radiant_3[1]:
        min_radiant_3 = (hero, new_min)
    if (new_min := imagehash.phash(radiant_4) - imagehash.phash(portrait)) < min_radiant_4[1]:
        min_radiant_4 = (hero, new_min)
    if (new_min := imagehash.phash(radiant_5) - imagehash.phash(portrait)) < min_radiant_4[1]:
        min_radiant_5 = (hero, new_min)
    if (new_min := imagehash.phash(dire_1) - imagehash.phash(portrait)) < min_dire_1[1]:
        min_dire_1 = (hero, new_min)
    if (new_min := imagehash.phash(dire_2) - imagehash.phash(portrait)) < min_dire_2[1]:
        min_dire_2 = (hero, new_min)
    if (new_min := imagehash.phash(dire_3) - imagehash.phash(portrait)) < min_dire_3[1]:
        min_dire_3 = (hero, new_min)
    if (new_min := imagehash.phash(dire_4) - imagehash.phash(portrait)) < min_dire_4[1]:
        min_dire_4 = (hero, new_min)
    if (new_min := imagehash.phash(dire_5) - imagehash.phash(portrait)) < min_dire_4[1]:
        min_dire_5 = (hero, new_min)
print("The Radiant's draft is: ")
print(min_radiant_1[0],min_radiant_2[0],min_radiant_3[0],min_radiant_4[0],min_radiant_5[0],sep=', ')
print("The Dire's draft is: ")
print(min_dire_1[0],min_dire_2[0],min_dire_3[0],min_dire_4[0],min_dire_5[0],sep=', ')

