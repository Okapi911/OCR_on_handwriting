## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################


import easyocr
import pyrealsense2 as rs
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from mqtt_publisher import connect_mqtt, publish_prediction

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged

def denoise(image,lower,upper):
    drawing = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i,j] < lower):
                drawing[i,j] = 0
            elif(image[i,j] > upper):
                drawing[i,j] = 255
            else:
                drawing[i,j]=image[i,j]
    return drawing

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Instatiate model
reader = easyocr.Reader(['en', 'fr'])

# Connect to MQQT Broker
client = connect_mqtt()
client.loop_start()
plt.ion()
# Get time estimation data
# data = np.array([55, 60, 45, 70, 80])

# np.save('time_estimation_data.npy', data)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert image to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        results = reader.readtext(color_image)

        words = [res[1] for res in results]
        
        publish_prediction(client, " ".join(words))
        
        plt.clf()
        plt.imshow(color_image)
        
        for res in results:
            # bbox coordinates of the detected text
            xy = res[0]
            xy1, xy2, xy3, xy4 = xy[0], xy[1], xy[2], xy[3]
            # text results and confidence of detection
            det, conf = res[1], res[2]
            # show time :)
            plt.plot([xy1[0], xy2[0], xy3[0], xy4[0], xy1[0]], [xy1[1], xy2[1], xy3[1], xy4[1], xy1[1]], 'r-')
            plt.text(xy1[0], xy1[1], f'{det} [{round(conf, 2)}]')
        
        plt.pause(0.5)
        # time.sleep(1)
        # print(len(regions))

        # Show images

finally:

    # Stop streaming
    pipeline.stop()