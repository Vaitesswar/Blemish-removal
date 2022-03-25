import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

coordinates = []
patches = []


def RemoveBlemish(action, x, y, flags, userdata):
    
    # Referencing global variables 
    global coordinates,patches,image
    
    # Action to be taken when left mouse button is pressed
    if action == cv2.EVENT_LBUTTONDOWN:
        coordinates = [(x,y)]
        patch = image[y-15:y+15, x-15:x+15]
        patches = [patch]
    
    elif action == cv2.EVENT_LBUTTONUP:
        patch1 = image[y-45:y-15, x-15:x+15] # Top patch
        patch2 = image[y+15:y+45, x-15:x+15] # Bottom patch
        patch3 = image[y-15:y+15, x-45:x-15] # Left patch
        patch4 = image[y-15:y+15, x+15:x+45] # Right patch
        patch5 = image[y-45:y-15, x-45:x-15] # Top left patch
        patch6 = image[y-45:y-15, x+15:x+45] # Top right patch
        patch7 = image[y+15:y+45, x-45:x-15] # Bottom left patch
        patch8 = image[y+15:y+45, x+15:x+45] # Bottom right patch
        
        patch_list = [patch1,patch2,patch3,patch4,patch5,patch6,patch7,patch8]
        ind = -1
        total = math.inf

        for i in range(len(patch_list)):
            patch_ctr = patches[0].copy()
            patch_ctr = cv2.cvtColor(patch_ctr,cv2.COLOR_RGB2GRAY)
            patch_nbr = patch_list[i].copy()
            patch_nbr = cv2.cvtColor(patch_nbr,cv2.COLOR_RGB2GRAY)
            patch_ctr[5:25,5:25] = 0
            patch_nbr[5:25,5:25] = 0
            patch_diff_val = np.sum(np.abs(patch_ctr - patch_nbr)) # Minimum change on borders of the patch
            patch_nbr = patch_list[i].copy()
            patch_nbr = cv2.cvtColor(patch_nbr,cv2.COLOR_RGB2GRAY)
            img1 = cv2.GaussianBlur(patch_nbr,(5,5),10,10)
            smoothness_val = np.sum(np.abs(cv2.Laplacian(img1, cv2.CV_32F, ksize = 5, scale = 1, delta = 0))) # Maximum smoothness within the patch
                  
            if (smoothness_val + patch_diff_val < total):
                ind = i
                total = smoothness_val + patch_diff_val
        
        source = patch_list[ind]
        src_mask = np.ones_like(source)*255
        x,y = coordinates[0]
        image = cv2.seamlessClone(source, image, src_mask, (x,y), cv2.NORMAL_CLONE)
        cv2.imshow("Window",image)


image = cv2.imread('blemish.png',cv2.IMREAD_UNCHANGED)
B,G,R = cv2.split(image)
image = cv2.merge((R,G,B))
imageCopy = image.copy()
cv2.namedWindow("Window")
cv2.setMouseCallback("Window", RemoveBlemish)
k = 0

while k != 27:
    cv2.imshow("Window",image[:,:,[2,1,0]])
    k = cv2.waitKey(20) & 0xFF
    
    if k == 99:
        source= dummy.copy()
    
cv2.destroyAllWindows()