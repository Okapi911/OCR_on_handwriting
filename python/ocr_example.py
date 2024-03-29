import cv2
import easyocr
import matplotlib.pyplot as plt

# This needs to run only once to load the model into memory
reader = easyocr.Reader(['en'])


# reading the image
img = cv2.imread('img/asd.jpeg')

# run OCR
results = reader.readtext(img)

# show the image and plot the results
plt.imshow(img)
for res in results:
    # bbox coordinates of the detected text
    xy = res[0]
    print(xy)
    xy1, xy2, xy3, xy4 = xy[0], xy[1], xy[2], xy[3]
    # text results and confidence of detection
    det, conf = res[1], res[2]
    x, y = xy1
    w = xy3[0] - xy1[0]
    h = xy3[1] - xy1[1]
    print(x, y, w, h)

    # show time :)
    plt.plot([xy1[0], xy2[0], xy3[0], xy4[0], xy1[0]], [xy1[1], xy2[1], xy3[1], xy4[1], xy1[1]], 'r-')
    plt.text(xy1[0], xy1[1], f'{det} [{round(conf, 2)}]')
    # print(det)