import os
import tarfile
from tqdm import tqdm
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import torch
import torch.optim as optim
from torchsummaryX import summary

from mltu.torch.model import Model
from mltu.torch.losses import CTCLoss
from mltu.torch.dataProvider import DataProvider
from mltu.torch.metrics import CERMetric, WERMetric
from mltu.torch.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, Model2onnx, ReduceLROnPlateau

from mltu.preprocessors import ImageReader
from mltu.transformers import ImageResizer, LabelIndexer, LabelPadding
from mltu.augmentors import RandomBrightness, RandomRotate, RandomErodeDilate, RandomSharpen

from model import Network
from configs import ModelConfigs

def download_dataset_IAM(url, extract_to="Datasets", chunk_size=1024*1024):
    http_response = urlopen(url)

    data = b""
    iterations = http_response.length // chunk_size + 1
    for _ in tqdm(range(iterations)):
        data += http_response.read(chunk_size)

    #The next lines are to extract the downloaded file. They operate better in linux since they use the tar command
    zipfile = ZipFile(BytesIO(data))
    zipfile.extractall(path=extract_to)

dataset_path = os.path.join("Data", "IAM_Words")
print(os.path.exists(dataset_path))
if not os.path.exists(dataset_path):
    download_dataset_IAM("https://git.io/J0fjL", extract_to="Data")

    file = tarfile.open(os.path.join(dataset_path, "words.tgz"))
    file.extractall(os.path.join(dataset_path, "words"))

dataset, vocab, max_len = [], set(), 0

# Preprocess the dataset by taking into account the specific IAM_Words dataset file structure
words = open(os.path.join(dataset_path, "words.txt"), "r").readlines()
for line in tqdm(words):
    if line.startswith("#"):
        continue

    line_split = line.split(" ")
    if line_split[1] == "err":
        continue

    folder1 = line_split[0][:3]
    folder2 = "-".join(line_split[0].split("-")[:2])
    file_name = line_split[0] + ".png" #Beware, only png from this point, adapt if necesary to have a better experience when testing
    label = line_split[-1].rstrip("\n")

    rel_path = os.path.join(dataset_path, "words", folder1, folder2, file_name)
    if not os.path.exists(rel_path):
        print(f"File not found: {rel_path}")
        continue

    dataset.append([rel_path, label])
    vocab.update(list(label))
    max_len = max(max_len, len(label))

configs = ModelConfigs()

# Save vocab and maximum text length to configs
configs.vocab = "".join(sorted(vocab))
configs.max_text_length = max_len
configs.save()

# Create a data provider to store transformed data
data_provider = DataProvider(
    dataset=dataset,
    skip_validation=True,
    batch_size=configs.batch_size,
    data_preprocessors=[ImageReader()],
    transformers=[
        # ImageShowCV2(), # uncomment to show images when iterating over the data provider
        ImageResizer(configs.width, configs.height, keep_aspect_ratio=False),
        LabelIndexer(configs.vocab),
        LabelPadding(max_word_length=configs.max_text_length, padding_value=len(configs.vocab))
        ],
    use_cache=True,
)

# Split the dataset into training and validation sets
train_dataProvider, test_dataProvider = data_provider.split(split = 0.9)

# Augment training data with random brightness, rotation and erode/dilate
train_dataProvider.augmentors = [
    RandomBrightness(), 
    RandomErodeDilate(),
    RandomSharpen(),
    RandomRotate(angle=10), 
    ]

network = Network(len(configs.vocab), activation="leaky_relu", dropout=0.3)
loss = CTCLoss(blank=len(configs.vocab))
optimizer = optim.Adam(network.parameters(), lr=configs.learning_rate)

# put on cuda GPU device if any is available
if torch.cuda.is_available():
    network = network.cuda()

# create callbacks at the end of each epoch to update data or the neural network (especially useful to decrease the learning rate or save copies of the model as a failsafe)
earlyStopping = EarlyStopping(monitor="val_CER", patience=10, mode="min", verbose=1)
modelCheckpoint = ModelCheckpoint(configs.model_path + "/model.pt", monitor="val_CER", mode="min", save_best_only=True, verbose=1)
tb_callback = TensorBoard(configs.model_path + "/logs")
reduce_lr = ReduceLROnPlateau(monitor="val_CER", factor=0.9, patience=10, verbose=1, mode="min", min_lr=1e-6)
model2onnx = Model2onnx(
    saved_model_path=configs.model_path + "/model.pt",
    input_shape=(1, configs.height, configs.width, 3), 
    verbose=1,
    metadata={"vocab": configs.vocab}
    )

# create model (beware, this is not simply a pytorch model with the usual properties) object that will handle training and testing of the network
model = Model(network, optimizer, loss, metrics=[CERMetric(configs.vocab), WERMetric(configs.vocab)])
model.fit(
    train_dataProvider, 
    test_dataProvider, 
    epochs=200, 
    callbacks=[earlyStopping, modelCheckpoint, tb_callback, reduce_lr, model2onnx]
    )

# Save training and validation datasets as csv files
train_dataProvider.to_csv(os.path.join(configs.model_path, "train.csv"))
test_dataProvider.to_csv(os.path.join(configs.model_path, "val.csv"))