from io import StringIO
import cv2
import numpy as np
import sys

template = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
h, w = np.shape(template)[:2]
print(h, w)

# Load the target image, big image
target = cv2.imread(sys.argv[2], cv2.IMREAD_COLOR)

# Perform match template
result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
#print(result)

# Locate the position of the template in the target image
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(min_loc, max_loc)
# Create a rectangle around the match
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(target, top_left, bottom_right, 255, 2)

# Show the images
cv2.imshow("Template", template)
cv2.imshow("Target", target)
cv2.waitKey(0)
#cv2.destroyAllWindows()
