from torch.utils.data import Dataset
from tools.file_help.file_with_json import open_file
from transformers import BertTokenizer


class QICDataSet(Dataset):
    def __init__(self, path):
        super().__init__()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.data = open_file(path)

    def __getitem__(self, idx):
        data = self.data[idx]['query']
        label = self.data[idx]['label']
        return self.tokenizer(data, padding='max_length', truncation=True, return_tensors="pt"), label

    def __len__(self):
        return len(self.data)
