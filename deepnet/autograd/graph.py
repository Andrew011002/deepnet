import numpy as np
import deepnet
from deepnet.autograd.mode import Grad


class Node:

    def __init__(self, context, next_functions=None):
        self.context = context
        self.next_functions = next_functions

    def apply(self, grad):
        next_grads = self.context.apply(grad)
        if self.next_functions:
            self._apply_next_functions(
                self.next_functions, next_grads)

    def _apply_next_functions(self, next_functions, next_grads):
        for next_function, grad in zip(next_functions, next_grads):
            if next_function is not None:
                next_function.apply(grad)

    @classmethod
    def with_context(cls, context, next_functions):
        return cls(context, next_functions)

    def __repr__(self) -> str:
        return str(self.context.__class__.__name__)


class AccumulateGrad:

    def __init__(self, tensor) -> None:
        self._tensor = tensor

    def apply(self, grad):
        if self._tensor.grad is None:
            self._tensor.grad = deepnet.tensor(
                np.zeros_like(self._tensor.data))
        self._tensor.grad.data += grad.data

    def tensor(self):
        return self._tensor

    @classmethod
    def with_tensor(cls, tensor):
        return cls(tensor)


def pass_to_graph(context, output):
    if Grad.enabled() and any(
            tensor.use_grad for tensor in context.saved_tensors()):
        next_functions = _get_next_functions(context)
        node = Node.with_context(context, next_functions)
        _set_tensor_grad_state(output, True, node, False)


def _get_next_functions(context):
    if hasattr(context, "saved_tensors"):
        next_functions = []
        for tensor in context.saved_tensors():
            next_function = _get_next_functions_helper(
                tensor)
            next_functions.append(next_function)
        return tuple(next_functions)


def _get_next_functions_helper(tensor):
    if tensor.is_leaf and tensor.use_grad:
        context = AccumulateGrad.with_tensor(tensor)
        return Node.with_context(context, next_functions=None)
    return tensor.grad_fn


def _set_tensor_grad_state(tensor, use_grad, grad_fn, is_leaf):
    tensor.use_grad = use_grad
    tensor.grad_fn = grad_fn
    tensor.is_leaf = is_leaf
