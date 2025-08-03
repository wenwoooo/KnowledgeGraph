import torch
from torch import nn
from transformers import BertModel


class BertClassifier(nn.Module):
    def __init__(self, dropout=0.5):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-chinese')

        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 11)
        self.relu = nn.ReLU()
        # self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            _, pooled_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        # final_layer = self.softmax(linear_output)
        return final_layer
