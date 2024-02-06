import os as os
from datetime import datetime

print(os.getcwd())
print(os.path.exists(os.path.join("Interactive_Systems/OCR_on_handwriting/Data")))

from mltu.configs import BaseModelConfigs
class ModelConfigs(BaseModelConfigs):
    def __init__(self):
        super().__init__()
        self.model_path = os.path.join("Interactive_Systems/OCR_on_handwriting/AI", datetime.strftime(datetime.now(), "%Y%m%d%H%M"))
        self.vocab = ""
        self.height = 32
        self.width = 128
        self.max_text_length = 0
        self.batch_size = 64
        self.learning_rate = 0.004
        self.train_epochs = 2