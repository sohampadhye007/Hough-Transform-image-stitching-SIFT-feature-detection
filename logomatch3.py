# -*- coding: utf-8 -*-
"""logoMatch3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SUwJ_PaEgxUHSCBWn8zunU9KQb6LAkHE

#(M22RM007-Soham Padhye)
# Use BRISK to find the featurepoints in the image and using Brute- Force matcher for matching the descriptors
"""

import cv2
from google.colab.patches import cv2_imshow

def brisk_bfmatcher(scene_img,gallery):
    #scene image is the image containing the region of interest only
    #that is it cropped image where logo is located
    #I have defined the region of interest because without region of inrerest it is not giving the satisfactory results

    # Create a BRISK object to find the features in the image
    brisk = cv2.BRISK_create()

    # Detect and extract keypoints and descriptors using BRISK
    scene_keypoints, scene_descriptors = brisk.detectAndCompute(scene_img, None)

    # Loop over the reference logos one by one
    for logo in gallery:
        # Load the logo image and convert it to grayscale
        logo_img = cv2.imread(logo)
        logo_gray = cv2.cvtColor(logo_img, cv2.COLOR_BGR2GRAY)

        # Detect and extract keypoints and descriptors using BRISK
        logo_keypoints, logo_descriptors = brisk.detectAndCompute(logo_gray, None)

        # Perform matching between the descriptors of the scene image and the descriptors of the logo using the brute-force matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(scene_descriptors, logo_descriptors)

        # Compute the ratio of the best match and the second-best match
        matches = sorted(matches, key=lambda x: x.distance)
        best_match = matches[0]
        second_best_match = matches[1]
        ratio = best_match.distance / second_best_match.distance

        # Choose the logo with the highest ratio as the detected logo
        #set thid threshold for the perticular image
        #for each image threshold value will change
        if ratio < 0.75:
            continue
        else:
            detected_logo = logo_img
            matched_keypoints = [scene_keypoints[best_match.queryIdx], logo_keypoints[best_match.trainIdx]]
            break

    # Draw the matched keypoints on the scene image and the detected logo
    matched_img = cv2.drawMatches(scene_img, scene_keypoints, detected_logo, logo_keypoints, [best_match], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    # Display the matched image with the keypoints matching pair
    cv2_imshow(matched_img)

"""# Calling the brisk_bfmatcher function and passing the ROI scene image"""

# Read the scene image
scene_img = cv2.imread("starbucks.jpeg")

#define the region of interest top left coordinates are origin of the image
x, y, w, h = 0, 300, 500, 500  # x, y are the top-left corner coordinates, w and h are the width and height of the ROI

# Crop the image to the ROI
scene_img = scene_img[y:y+h, x:x+w]

gallery =["honda.jpg", "hp.jpg", "lg.jpg", "motorola.jpg", "pepsi.jpg",
                   "puma.jpg", "rolex.jpg", "starbucks.jpg", "toyota.jpg", "warnerbros.jpg"]

#calling the function to check which company logo is present in the given scene
brisk_bfmatcher(scene_img,gallery)

"""# Calling the brisk_bfmatcher function and passing the ROI scene image"""

scene_image = cv2.imread("scene.jpg")

#define the region of interest top left coordinates are origin of the image
x, y, w, h = 0, 100, 600, 300  # x, y are the top-left corner coordinates, w and h are the width and height of the ROI

# Crop the image to the ROI
scene_image = scene_image[y:y+h, x:x+w]

reference_gallery=["hp.jpg", "kfc.jpg", "levis.jpg", "lg.jpg", "nescafe.jpg",
                   "shell.jpg", "spar.jpg", "tacobell.jpg", "tommyhilfiger.jpg", "umbro.jpg"]
#calling the function to check which company logo is present in the given scene
brisk_bfmatcher(scene_image,reference_gallery)

"""# Defining new function that uses BRISK and FLANN for matching the descriptors
#(As BFmatcher is not giving the satisfactory results)
"""

import cv2
from google.colab.patches import cv2_imshow
import numpy as np


def brisk_flann(scene_img,gallery):
    #scene image is the image containing the region of interest only
    #that is it cropped image where logo is located
    #I have defined the region of interest because without region of inrerest it is not giving the satisfactory results
    scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)

    # Create a BRISK object to find the features in the image
    brisk = cv2.BRISK_create()

    # Detect and extract keypoints and descriptors using BRISK method
    scene_keypoints, scene_descriptors = brisk.detectAndCompute(scene_gray, None)

    # Convert descriptors to float32-important
    scene_descriptors = np.float32(scene_descriptors)

    # FLANN parameters set the trees and checks properly to get the good results
    #importance of the papameters is written in the report 
    index_params = dict(algorithm=0, trees=15)
    search_params = dict(checks=50)

    # Create FLANN object for matching the descriptors
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Loop over the reference logos one by one
    for logo in gallery:
        # Load the logo image and convert it to grayscale
        logo_img = cv2.imread(logo)
        

        # Detect and extract keypoints and descriptors using BRISK
        logo_keypoints, logo_descriptors = brisk.detectAndCompute(logo_img, None)

        # Convert descriptors to float32-imp
        logo_descriptors = np.float32(logo_descriptors)

        # Perform matching between the descriptors of the scene image and the descriptors of the logo using FLANN
        matches = flann.knnMatch(scene_descriptors, logo_descriptors, k=2)

        # Apply ratio test to filter out false matches
        #set the threshold properly to get good results
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Choose the logo with the highest number of good matches as the detected logo
        if len(good_matches) < 10:
            continue
        else:
            detected_logo = logo_img
            matched_keypoints = []
            for match in good_matches:
                matched_keypoints.append([scene_keypoints[match.queryIdx], logo_keypoints[match.trainIdx]])
            break

    # Draw the matched keypoints on the scene image and the detected logo
    matched_img = cv2.drawMatches(scene_img, scene_keypoints, detected_logo, logo_keypoints, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    # Display the matched image with the keypoints matching pair
    cv2_imshow(matched_img)

"""#Call the function and passing entire image as parameter to the function
#(Not considering region of interest)
"""

# Read the scene image
scene_img = cv2.imread("starbucks.jpeg")
#logos for matching
gallery =["honda.jpg", "hp.jpg", "lg.jpg", "motorola.jpg", "pepsi.jpg",
                   "puma.jpg", "rolex.jpg", "starbucks.jpg", "toyota.jpg", "warnerbros.jpg"]
brisk_flann(scene_img,gallery)

"""# Call BRISK_FLANN 
#Crop the image as per the Region of Interest and pass this scene image to the function
"""

# Read the scene image
scene_img = cv2.imread("starbucks.jpeg")

#define the region of interest top left coordinates are origin of the image
x, y, w, h = 0, 300, 500, 500  # x, y are the top-left corner coordinates, w and h are the width and height of the ROI

# Crop the image to the ROI
scene_img = scene_img[y:y+h, x:x+w]

gallery =["honda.jpg", "hp.jpg", "lg.jpg", "motorola.jpg", "pepsi.jpg",
                   "puma.jpg", "rolex.jpg", "starbucks.jpg", "toyota.jpg", "warnerbros.jpg"]
brisk_flann(scene_img,gallery)

scene_image = cv2.imread("scene.jpg")

#define the region of interest top left coordinates are origin of the image
x, y, w, h = 0, 100, 600, 300  # x, y are the top-left corner coordinates, w and h are the width and height of the ROI

# Crop the image to the ROI
scene_image = scene_image[y:y+h, x:x+w]
#logos for matching
reference_gallery=["hp.jpg", "kfc.jpg", "levis.jpg", "lg.jpg", "nescafe.jpg",
                   "shell.jpg", "spar.jpg", "tacobell.jpg", "tommyhilfiger.jpg", "umbro.jpg"]
brisk_flann(scene_image,reference_gallery)

