import cv2
import numpy as np
import sys
import os

num = sys.argv[1]

for i in range(1,6):
  for directory_type in ['input', 'static']:
    round_directory = os.path.join(
      directory_type,
      f'round_{i}')
    
    os.makedirs(round_directory, exist_ok=True)

# Get image filter
filter_path = os.path.join(
  'input',
  f'round_{num}.png')

filter_overlay = cv2.imread(filter_path, -1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

images_path = os.path.join(
  'input',
  f'round_{num}')

images_dir = os.listdir(images_path)

for image_name in images_dir:
  image_path = os.path.join(
    images_path,
    image_name)

  image = cv2.imread(image_path)
  (input_height, input_width) = image.shape[:2]

  image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Detect faces on image, mn=6 to try and avoid false positives
  detected_faces = face_cascade.detectMultiScale(image_grayscale, minNeighbors = 6)

  for (column, row, width, height) in detected_faces:
    # Resize filter to fit the face
    filter_resized = cv2.resize(filter_overlay, (height, width))

    # Blank image with the same dimensions as input image
    foreground_image = np.zeros((input_height, input_width, 4), np.uint8)

    # Filter in location of detected face, but on the blank image
    foreground_image[row:row+height, column:column+width] = filter_resized

    # Alpha layers
    alpha_s = foreground_image[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    # Overlay filter image w/ filter on input image, taking into account the transparent pixels
    for c in range(0, 3):
        image[:, :, c] = (alpha_s * foreground_image[:, :, c] + alpha_l * image[:, :, c])

  cv2.imwrite(f'static/round_{num}/{image_name}', image)