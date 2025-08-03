import torch
from transformers import BertTokenizer
from QA.BertClassifier.BertBiLSTMClassifier import BertBiLSTMMixClassifier

# bert = BertModel.from_pretrained('bert-base-chinese')
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
text = ("你好，我想，去够。买一个玩。具", "我爱中国")
# tokens = tokenizer(text, padding=True, truncation=True,
#                    return_tensors="pt")
#
# with torch.no_grad():
#     features = bert(tokens.input_ids)
# print(features)
# softmax = nn.Softmax(dim=1)
# t = softmax(features['pooler_output'])
# print(t.argmax(dim=1))
#
# print(tokens)
# print(tokenizer.decode(tokens.input_ids[0]))

# bert_ = Bert_BiLSTM_CRF({'faf': 0, 'faa': 1})
# print('initiate success')
# print(bert_)
model = BertBiLSTMMixClassifier()
# model = bert_lstm('bert-base-chinese', 256, 11, 2)
embedding = tokenizer(text, padding='max_length', truncation=True, return_tensors="pt")
# print(embedding['input_ids'][0], embedding['attention_mask'][0])

with torch.no_grad():
    input_ids = embedding['input_ids']
    attention_mask = embedding['attention_mask']
    output = model(input_ids, attention_mask)

    print('--->', output)
    print(output.softmax(dim=1))
    # softmax(output)

# def softmax(tensor, dim=-1):

# test = [[[0.1, 0.2, 0.3], [1.1, 1.2, 1.3]], [[0.01, 0.02, 0.03], [0.11, 0.12, 0.13]],
#         [[0.001, 0.002, 0.003], [0.111, 0.222, 0.333]]]
# print(np.array(test)[:, -1, :])
