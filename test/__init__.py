import torch
from torch import nn

if __name__ == '__main__':
    # st = ['fa']
    # print('-', '.'.join(st[:-1]), '-', sep='')
    st = set()
    st.update({'fafa'})
    print('--', '\n'.join(st), '--', sep='')
    print('--', '\n'.join(st).strip(), '--', sep='')

    # Example of target with class indices
    loss = nn.CrossEntropyLoss()
    inp = torch.randn(3, 5, requires_grad=True)
    target = torch.empty(3, dtype=torch.long).random_(5)
    output = loss(inp, target)
    output.backward()
    # Example of target with class probabilities
    inp = torch.randn(3, 5, requires_grad=True)
    target = torch.randn(3, 5).softmax(dim=1)
    output = loss(inp, target)
    output.backward()

    # s = {'name': {'f', 'f2', '3'}, 'label': 1}
    # print(s.get('fff'))
    # print(len(s))

    # tensor = torch.randn(3, 5, 4)
    # tensor1 = torch.randn(3, 5, 4)
    # sm = nn.Softmax(-1)
    # linear = nn.Linear(5, 1)
    # print(tensor)
    # print(tensor1)
    # print(tensor.transpose(0, 1))
    # print(torch.cat((tensor, tensor1), dim=-1))
    # print(tensor[:, -1, :])
    # print(sm(tensor))
    # print(linear(tensor)[0])
    # print(linear(tensor).reshape(3, 5))

    pass
