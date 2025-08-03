import torch
from torch import nn
from transformers import BertModel
from QA.modules import MultiHeadSelfAttention


class BertBiLSTMClassifier(nn.Module):
    def __init__(self, dropout=0.5, num_layers=1, embedding_dim=768, hidden_dim=512):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.bert = BertModel.from_pretrained('bert-base-chinese')
        self.dropout = nn.Dropout(dropout)
        self.biLstm = nn.LSTM(input_size=self.embedding_dim, hidden_size=self.hidden_dim // 2,
                              num_layers=self.num_layers, batch_first=True, bidirectional=True)
        self.linear = nn.Linear(self.hidden_dim, 11)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        embeddings, _ = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
        bi_lstm_output, _ = self.biLstm(embeddings)
        dropout_output = self.dropout(bi_lstm_output)
        linear_output = self.linear(dropout_output[:, -1, :])
        final_layer = self.softmax(linear_output)
        return final_layer


class BertBiLSTMMixClassifier(nn.Module):
    def __init__(self, dropout=0.5, num_layers=1, embedding_dim=768, hidden_dim=512):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.bert = BertModel.from_pretrained('bert-base-chinese')
        self.biLstm = nn.LSTM(input_size=self.embedding_dim, hidden_size=self.hidden_dim // 2,
                              num_layers=self.num_layers, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(self.hidden_dim + self.embedding_dim, 11)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            embeddings, pooled_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
        bi_lstm_output, _ = self.biLstm(embeddings)

        mix_output = torch.cat((bi_lstm_output[:, -1, :], pooled_output), dim=-1)
        dropout_output = self.dropout(mix_output)

        linear_output = self.linear(dropout_output)
        final_layer = self.softmax(linear_output)
        return final_layer


class BertBiLSTMMixMSAClassifier(nn.Module):
    def __init__(self, dropout=0.5, num_layers=1, embedding_dim=768, hidden_dim=512):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.dense_dim = self.hidden_dim * self.hidden_dim

        self.bert = BertModel.from_pretrained('bert-base-chinese')
        self.biLstm = nn.LSTM(input_size=self.embedding_dim, hidden_size=self.hidden_dim // 2,
                              num_layers=self.num_layers, batch_first=True, bidirectional=True)
        self.multi_attention = MultiHeadSelfAttention(self.hidden_dim, self.hidden_dim, self.hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(self.dense_dim + self.embedding_dim, 11)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        batch, _ = input_ids.shape
        # print(input_ids.shape)

        embeddings, pooled_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
        bi_lstm_output, _ = self.biLstm(embeddings)

        ma_output = self.multi_attention(bi_lstm_output)
        # print(ma_output.shape)
        mix_output = torch.cat((ma_output.reshape(batch, self.dense_dim), pooled_output), dim=-1)
        dropout_output = self.dropout(mix_output)
        # print(dropout_output.shape)

        linear_output = self.linear(dropout_output)
        final_layer = self.softmax(linear_output)
        return final_layer
