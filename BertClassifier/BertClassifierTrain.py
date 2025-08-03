import torch
from BertClassifier import BertClassifier
from QA.DataSets.QICDataSet import QICDataSet
from torch.utils.data import DataLoader
from torch import nn
from torch.optim import Adam
from tqdm import tqdm

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


def train(model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_data = QICDataSet('../data/train/KUAKE-QIC/KUAKE-QIC/KUAKE-QIC_train.json')
    val_data = QICDataSet('../data/train/KUAKE-QIC/KUAKE-QIC/KUAKE-QIC_dev.json')
    dataloader = DataLoader(train_data, batch_size=3, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=3)

    # 定义损失函数和优化器
    # TODO pitfall between nn.CrossEntropyLoss and nn.Softmax leads to overfitting
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=1e-6)

    for epoch in range(5):
        # 定义两个变量，用于存储训练集的准确率和损失
        total_acc_train = 0
        total_loss_train = 0
        # 进度条函数tqdm
        for train_input, train_label in tqdm(dataloader):
            # train_label = train_label.to(device)

            # print(train_input['attention_mask'])

            mask = train_input['attention_mask'].squeeze(1).to(device)
            input_id = train_input['input_ids'].squeeze(1).to(device)
            # 通过模型得到输出
            output = model(input_id, mask)

            # print(output, train_label)

            # 计算损失
            train_label = torch.tensor([labels[item] for item in train_label]).to(device)

            # print(train_label)

            batch_loss = criterion(output, train_label)
            total_loss_train += batch_loss.item()
            # 计算精度
            acc = (output.argmax(dim=1) == train_label).sum().item()
            total_acc_train += acc
            # 模型更新
            model.zero_grad()
            batch_loss.backward()
            optimizer.step()

        if epoch % 10 == 0:
            torch.save(model, '/content/drive/MyDrive/Colab Notebooks/BertBiLSTMMixClassifier-02.pth')

        # ------ 验证模型 -----------
        # 定义两个变量，用于存储验证集的准确率和损失
        total_acc_val = 0
        total_loss_val = 0
        # 不需要计算梯度
        with torch.no_grad():
            # 循环获取数据集，并用训练好的模型进行验证
            for val_input, val_label in val_dataloader:
                # 如果有GPU，则使用GPU，接下来的操作同训练
                mask = val_input['attention_mask'].squeeze(1).to(device)
                input_id = val_input['input_ids'].squeeze(1).to(device)

                output = model(input_id, mask)

                val_label = torch.tensor([labels[item] for item in val_label]).to(device)

                batch_loss = criterion(output, val_label)
                total_loss_val += batch_loss.item()

                acc = (output.argmax(dim=1) == val_label).sum().item()
                total_acc_val += acc

        print(
            f'''Epochs: {epoch + 1} 
                      | Train Loss: {total_loss_train / len(train_data): .3f} 
                      | Train Accuracy: {total_acc_train / len(train_data): .3f} 
                      | Val Loss: {total_loss_val / len(val_data): .3f} 
                      | Val Accuracy: {total_acc_val / len(val_data): .3f}''')


def evaluate(model):
    test_data = QICDataSet('./data/train/KUAKE-QIC/KUAKE-QIC/KUAKE-QIC_test.json')
    test_dataloader = DataLoader(test_data, batch_size=2)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    total_acc_test = 0
    with torch.no_grad():
        for test_input, test_label in test_dataloader:
            mask = test_input['attention_mask'].squeeze(1).to(device)
            input_id = test_input['input_ids'].squeeze(1).to(device)
            output = model(input_id, mask)
            test_label = torch.tensor([labels[item] for item in test_label]).to(device)
            acc = (output.argmax(dim=1) == test_label).sum().item()
            total_acc_test += acc
    print(f'Test Accuracy: {total_acc_test / len(test_data): .3f}')


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BertClassifier()
    model.to(device)
    train(model)
    model.save('bertclassifier-m.pth')

    # evaluate(model)
