import torch
from transformers import BertTokenizer

from QA.BertClassifier.BertBiLSTMClassifier import BertBiLSTMMixClassifier, BertBiLSTMClassifier, \
    BertBiLSTMMixMSAClassifier
from QA.BertClassifier.BertClassifier import BertClassifier
from configurations.key_label_match import rev_labels


class IntentionRecognition:
    def __init__(self, model_path='classificier-relu-08.pth', device=None):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cup") if device is None else device
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.model = torch.load(self.model_path, map_location=self.device)

        self.model.eval()
        print('Intention Recognition Model Loaded')

    def predict(self, text) -> (int, str):
        with torch.no_grad():
            embedding = self.tokenizer(text, padding='max_length', truncation=True, return_tensors="pt")
            input_ids = embedding['input_ids'].to(self.device)
            attention_mask = embedding['attention_mask'].to(self.device)
            output = self.model(input_ids, attention_mask)

        # print(output)
        res_idx = output.argmax(dim=1).item()
        return res_idx, rev_labels[res_idx]


if __name__ == '__main__':
    # model = IntentionRecognition()
    #
    # print(model)
    model = BertBiLSTMMixMSAClassifier()
    print(model)

    text = '你好啊'
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    embedding = tokenizer(text, padding='max_length', truncation=True, return_tensors="pt")

    input_ids = embedding['input_ids']
    attention_mask = embedding['attention_mask']
    output = model(input_ids, attention_mask)
    print(output.argmax(dim=-1))
