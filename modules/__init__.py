from math import sqrt

import torch
import torch.nn as nn
from torch.nn import Parameter


class Linear(nn.Module):
    def __init__(self, in_features, out_features, device=None, dtype=None):
        super().__init__()
        factory_kwargs = {'device': device, 'dtype': dtype}
        self.weight = Parameter(torch.tensor((out_features, in_features), **factory_kwargs))

    def forward(self, x):
        pass


class MultiHeadSelfAttention(nn.Module):
    # dim_in: int  # input dimension
    # dim_k: int  # key and query dimension
    # dim_v: int  # value dimension
    # num_heads: int  # number of heads, for each head, dim_* = dim_* // num_heads

    def __init__(self, dim_in, dim_k, dim_v, num_heads=8):
        super(MultiHeadSelfAttention, self).__init__()
        assert dim_k % num_heads == 0 and dim_v % num_heads == 0, "dim_k and dim_v must be multiple of num_heads"
        self.dim_in = dim_in
        self.dim_k = dim_k
        self.dim_v = dim_v
        self.num_heads = num_heads

        self.dk = self.dim_k // self.num_heads  # dim_k of each head
        self.dv = self.dim_v // self.num_heads  # dim_v of each head

        self.w_q = nn.Linear(self.dim_in, self.dim_k, bias=False)
        self.w_k = nn.Linear(self.dim_in, self.dim_k, bias=False)
        self.w_v = nn.Linear(self.dim_in, self.dim_v, bias=False)
        self._norm_fact = 1 / sqrt(self.dim_k // self.num_heads)

    def forward(self, x):
        # x: (batch, n, dim_in)
        batch, n, dim_in = x.shape
        assert dim_in == self.dim_in

        q = self.w_q(x).reshape(batch, n, self.num_heads, self.dk).transpose(1, 2)  # (batch, nh, n, dk)
        k = self.w_k(x).reshape(batch, n, self.num_heads, self.dk).transpose(1, 2)  # (batch, nh, n, dk)
        v = self.w_v(x).reshape(batch, n, self.num_heads, self.dv).transpose(1, 2)  # (batch, nh, n, dv)

        dist = torch.matmul(q, k.transpose(2, 3)) * self._norm_fact  # batch, nh, n, n
        dist = torch.softmax(dist, dim=-1)  # batch, nh, n, n

        att = torch.matmul(dist, v)  # batch, nh, n, dv
        att = att.transpose(1, 2).reshape(batch, n, self.dim_v)  # batch, n, dim_v
        return att
