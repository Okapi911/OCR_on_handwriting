import cv2
import typing
import numpy as np

from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer

class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])

        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = ctc_decoder(preds, self.vocab)[0]

        return text

if __name__ == "__main__":
    import pandas as pd
    from tqdm import tqdm

    model = ImageToWordModel(model_path="AI/202402061519/model.onnx") #Change the path to test another model

    prediction_text = model.predict(cv2.imread("AI/C.png")) #Repeat this syntax to test images that weren't in the original dataset 
    try:
            cer = get_cer(prediction_text, "logo") #Certitude per character, can be seemed as cross_entropy_loss on charcater classification on the alphabet normalized to the size of the word
            print(f"Image: AI/C.png, Label: logo, Prediction: {prediction_text}, CER: {cer}")
    except:
            print("oups")

    df = pd.read_csv("AI/202402061519/val.csv").values.tolist() #Get results of the last validation step in the training at the end of the last epoch (the model didn't learn since). It would be better to write a true test databasis unused before

    x=0
    accum_cer = []
    for image_path, label in tqdm(df):
        image = cv2.imread(image_path)

        prediction_text = model.predict(image)

        try:
            cer = get_cer(prediction_text, label)
            if(x%100==0):
                 print(f"Image: {image_path}, Label: {label}, Prediction: {prediction_text}, CER: {cer}")
            accum_cer.append(cer)
        except:
            print(image_path, label)
        
        x+=1



    print(f"Average CER: {np.average(accum_cer)}")