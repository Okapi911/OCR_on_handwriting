import cv2
import typing
import numpy as np
import matplotlib.pyplot as plt

from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer

class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, image: np.ndarray):
        print(image.shape)
        image = cv2.resize(image, self.input_shape[:2][::-1])
        print(image.shape)
        cv2.imwrite("img/image.jpg", image)
        # cv2.imshow("image", image)
        
        # plt.imshow(ima
        # ge)
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = ctc_decoder(preds, self.vocab)[0]

        return text



