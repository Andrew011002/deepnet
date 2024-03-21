import nura
import nura.nn as nn
import numpy as np
import torch
import torch.nn as tnn


def main():

    class Model(nn.Module):

        def __init__(self) -> None:
            super().__init__()
            self.linear = nn.Linear(3, 8)

        def forward(self, x):
            return self.linear(x)

    model = Model()

    batch, seqlen, dmodel, dim = 1, 3, 2, 0
    q = nura.randn(batch, seqlen, dmodel)
    k = q.clone()
    v = nura.randn(batch, seqlen, dmodel + 1)

    mask = nura.tri(seqlen, seqlen, dtype=nura.bool).unsqueeze()
    # context, attn = nn.selfattention(q, k, v, dim=1, mask=mask)
    simscore = nura.matmul(q, k.transpose(-2, -1)) / dmodel**0.5
    print(f"simscore pre masked:\n{simscore}")
    simscore = nura.where(mask == True, simscore, -1e9)
    print(f"simscore post masked:\n{simscore}")
    attn = nn.softmax(simscore, dim=dim)
    print(f"attn:\n{attn}")
    context = nura.matmul(attn, v)
    print(context)

    q = torch.from_numpy(q.data)
    k = q.clone()
    v = torch.from_numpy(v.data)

    mask = torch.tril(torch.ones(seqlen, seqlen)).bool()
    simscore = torch.matmul(q, k.transpose(-2, -1)) / dmodel**0.5
    print(f"simscore pre masked:\n{simscore}")
    simscore = simscore.masked_fill(mask == False, -1e9)
    print(f"simscore post masked:\n{simscore}")
    attn = tnn.Softmax(dim=dim)(simscore)
    print(f"attn:\n{attn}")
    context = torch.matmul(attn, v)
    print(context)


if __name__ == "__main__":
    main()
