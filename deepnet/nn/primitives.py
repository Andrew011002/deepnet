import numpy as np
import deepnet
from deepnet import Tensor
from deepnet.autograd.function import Function, Context
from typing import Any


class Add(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        context.save_tensors(a, b)
        out = deepnet.tensor(a.data + b.data)
        return out

    @staticmethod
    def backward(context: Any, grad: Tensor):
        grad_a = deepnet.tensor(1 * grad.data)
        grad_b = deepnet.tensor(1 * grad.data)
        return grad_a, grad_b


class Sub(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        context.save_tensors(a, b)
        out = deepnet.tensor(a.data - b.data)
        return out

    @staticmethod
    def backward(context: Any, grad: Tensor):
        grad_a = grad
        grad_b = deepnet.tensor(grad.data * -1)
        return grad_a, grad_b


class Mul(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        context.save_tensors(a, b)
        out = deepnet.tensor(a.data * b.data)
        return out

    @staticmethod
    def backward(context: Context, grad: Tensor):
        a, b = context.saved_tensors()
        grad_a = deepnet.tensor(b.data * grad.data)
        grad_b = deepnet.tensor(a.data * grad.data)
        return grad_a, grad_b

    @staticmethod
    def jvp(context: Context, tangent_a: Tensor, tangent_b: Tensor):
        a, b = context.saved_tensors()
        tangent_out = deepnet.tensor(
            tangent_a.data * b.data + tangent_b.data * a.data)
        return tangent_out


class Div(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        context.save_tensors(a, b)
        out = deepnet.tensor(a.data / b.data)
        return out

    @staticmethod
    def backward(context: Context, grad: Tensor):
        a, b = context.saved_tensors()
        grad_a = deepnet.tensor(1 / b.data * grad.data)
        grad_b = deepnet.tensor(-1 * a.data / b.data ** 2 * grad.data)
        return grad_a, grad_b


class Matmul(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        context.save_tensors(a, b)
        out = a.data @ b.data
        return deepnet.tensor(out)

    @staticmethod
    def backward(context: Context, grad: Tensor):
        a, b = context.saved_tensors()
        dim_a, dim_b = np.arange(a.ndim()), np.arange(b.ndim())
        dim_a[-2], dim_a[-1] = dim_a[-1], dim_a[-2]
        dim_b[-2], dim_b[-1] = dim_b[-1], dim_b[-2]
        grad_a = deepnet.tensor(grad.data @ b.data.transpose(dim_b))
        grad_b = deepnet.tensor(a.data.transpose(dim_a) @ grad.data)
        return grad_a, grad_b


class Pow(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, b: Tensor):
        out = deepnet.tensor(np.power(a.data, b.data))
        context.save_tensors(a, b, out)
        return out

    @staticmethod
    def backward(context: Context, grad: Tensor):
        a, b, out = context.saved_tensors()
        grad_a = deepnet.tensor(
            b.data * np.power(a.data, b.data - 1.) * grad.data)
        grad_b = deepnet.tensor(out.data * np.log(a.data) * grad.data)
        return grad_a, grad_b


class Tranpose(Function):

    @staticmethod
    def forward(context: Context, a: Tensor, dim_0: int, dim_1: int):
        size = np.arange(a.ndim())
        size[dim_0], size[dim_1] = size[dim_1], size[dim_0]
        out = deepnet.tensor(a.data.transpose(size))
        context.save_tensors(a)
        context.size = size
        return out

    @staticmethod
    def backward(context: Context, grad: Tensor):
        size = context.size
        grad_data = deepnet.tensor(grad.data.transpose(size))
        return (grad_data,)


class Clone(Function):

    @staticmethod
    def forward(context: Context, a: Tensor):
        context.save_tensors(a)
        out = deepnet.tensor(
            a.data.copy(), use_grad=a.use_grad, dtype=a.dtype())
        return out

    @staticmethod
    def backward(context: Any, grad: Tensor):
        return (grad,)
