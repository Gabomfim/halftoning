import numpy as np
import cv2
import sys
import copy

# HELPER FUNCTIONS

def find_closest_color(color):
    return round(color/255) * 255

# SETTING UP

input = cv2.imread(sys.argv[1],1).astype("float64")
height, width, channels = input.shape
output = np.empty((6, height, width, channels), dtype="float64")

# DEFINING KERNELS

#Floyd and Steinberg
h1 = np.array([[   0,    0, 7/16],
               [3/16, 5/16, 1/16]])
               
#Stevenson and Arce               
h2 = np.array([[      0,      0,      0,      0,      0, 32/200,      0],
               [ 12/200,      0, 26/200,      0, 30/200,      0, 16/200],
               [      0, 12/200,      0, 26/200,      0, 12/200,      0],
               [  5/200,      0, 12/200,      0, 12/200,      0,  5/200]])

#Burkes
h3 = np.array([[    0,    0,    0, 8/32, 4/32],
               [ 2/32, 4/32, 8/32, 4/32, 2/32]])

#Sierra
h4 = np.array([[    0,    0,    0, 5/32, 3/32],
               [ 2/32, 4/32, 5/32, 4/32, 2/32],
               [    0, 2/32, 3/32, 2/32,    0]])

#Stucki
h5 = np.array([[    0,    0,    0, 8/42, 4/42],
               [ 2/42, 4/42, 8/42, 4/42, 2/42],
               [ 1/42, 2/42, 4/42, 2/42, 1/42]])


#Jarvis, Judice and Ninke
h6 = np.array([[    0,    0,    0, 7/48, 5/48],
               [ 3/48, 5/48, 7/48, 5/48, 3/48],
               [ 1/48, 3/48, 5/48, 3/48, 1/48]])

                
kernel = [h1,h2,h3,h4,h5,h6]



# IMPLEMENTATION

for k in range(len(kernel)):
	output[k] = copy.deepcopy(input)
	kHeight, kWidth = kernel[k].shape 

	for line in range(height):

		#what direction should I go?
		if(line%2 == 0): #RIGHT
			column=0
		else:
			column=width-1 #LEFT

		while (0<=column and column<width):

			newColor = [find_closest_color(output[k][line][column][i]) for i in range(channels)]

			error = output[k][line][column] - newColor

			output[k][line][column] = newColor

			#distributing error

			lowerInterval = round(column-((kWidth-1)/2))
			higherInterval = round(column+((kWidth-1)/2)+1)
				

			if(line%2 == 0): #Going to the right
				
				try:
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 0] += error[0] * kernel[k]
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 1] += error[1] * kernel[k]
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 2] += error[2] * kernel[k]
				except:
					pass
				
				column+=1

			else: #Going to the left

				try:
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 0] += error[0] * cv2.flip(kernel[k], 1)
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 1] += error[1] * cv2.flip(kernel[k], 1)
					output[k][line:(line+kHeight), lowerInterval:higherInterval, 2] += error[2] * cv2.flip(kernel[k], 1)
				except:
					pass

				column-=1

#storing results

cv2.imwrite('./outputs/Floyd and Steinberg.png', output[0].astype("uint8"))
cv2.imwrite('./outputs/Stevenson and Arce.png', output[1].astype("uint8"))
cv2.imwrite('./outputs/Burkes.png', output[2].astype("uint8"))
cv2.imwrite('./outputs/Sierra.png', output[3].astype("uint8"))
cv2.imwrite('./outputs/Stucki.png', output[4].astype("uint8"))
cv2.imwrite('./outputs/Jarvis, Judice and Ninke.png', output[5].astype("uint8"))
