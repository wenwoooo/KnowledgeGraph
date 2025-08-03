import torch
from transformers import BertTokenizer
from BertClassifier.BertClassifier import BertClassifier

model = torch.load('BertClassifier/classificier-relu-08.pth')

labels = {'病情诊断': 0,
          '病因分析': 1,
          '治疗方案': 2,
          '就医建议': 3,
          '指标解读': 4,
          '疾病表述': 5,
          '后果表述': 6,
          '注意事项': 7,
          '功效作用': 8,
          '医疗费用': 9,
          '其他': 10
          }

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

while True:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    text = input("Enter:")
    embedding = tokenizer(text, padding='max_length', truncation=True, return_tensors="pt")
    print(embedding['input_ids'][0], embedding['attention_mask'][0])

    with torch.no_grad():
        input_ids = embedding['input_ids'].to(device)
        attention_mask = embedding['attention_mask'].to(device)
        output = model(input_ids, attention_mask)

        print(output)
        print(output.argmax(dim=1))
