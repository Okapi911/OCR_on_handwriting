import os
from tqdm import tqdm
from model import Network
from configs import ModelConfigs

dataset_path = os.path.join("Data", "IAM_Words")

dataset, vocab, max_len = [], set(), 0

words = open(os.path.join(dataset_path, "words.txt"), "r").readlines()
for line in tqdm(words):
    if line.startswith("#"):
        continue

    line_split = line.split(" ")

    folder1 = line_split[0][:3]
    folder2 = "-".join(line_split[0].split("-")[:2])
    file_name = line_split[0] + ".png" 
    label = line_split[-1].rstrip("\n")

    rel_path = os.path.join(dataset_path, "words", folder1, folder2, file_name)
    if not os.path.exists(rel_path):
        print(f"File not found: {rel_path}")
        continue

    vocab.update(list(label))
    max_len = max(max_len, len(label))

configs = ModelConfigs()

# Save vocab and maximum text length to configs
configs.vocab = "".join(sorted(vocab))
configs.max_text_length = max_len
configs.save()

network = Network(len(configs.vocab), activation="leaky_relu", dropout=0.3)

def count_parameters(model): return sum(p.numel() for p in model.parameters() if p.requires_grad) 
print(count_parameters(network))