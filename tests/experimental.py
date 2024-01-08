import numpy as np
import torch
import torch.autograd.functional as torch_autograd_f
import deepnet
import deepnet.autograd.functional as deepnet_autograd_f


def main():
    
    long_zero_dim = deepnet.tensor(1).long()
    int_tensor = deepnet.ones((2, 3)).int()
    print(int_tensor)

if __name__ == "__main__":
    main()
