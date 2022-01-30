import numpy as np
import cv2
import pyautogui
from PIL import Image

# take screenshot using pyautogui
#image = pyautogui.screenshot()
image = Image.open('./image1.png')
   
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
radiant_2 = image.crop((3320, 359, 3320+90, 359+50))
radiant_2_im = cv2.cvtColor(np.array(radiant_2), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_2.png", radiant_2_im)
radiant_3 = image.crop((3320, 529, 3320+90, 529+50))
radiant_3_im = cv2.cvtColor(np.array(radiant_3), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_3.png", radiant_3_im)
radiant_4 = image.crop((3320, 584, 3320+90, 584+50))
radiant_4_im = cv2.cvtColor(np.array(radiant_4), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_4.png", radiant_4_im)
radiant_5 = image.crop((3320, 719, 3320+90, 719+50))
radiant_5_im = cv2.cvtColor(np.array(radiant_5), cv2.COLOR_RGB2BGR)
cv2.imwrite("radiant_5.png", radiant_5_im)

#dire_1 = 
#dire_2 = 
#dire_3 = 
#dire_4 = 
#dire_5 = 
