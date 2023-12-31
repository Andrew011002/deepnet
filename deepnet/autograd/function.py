import deepnet
from .graph import _pass_to_graph
from deepnet import Tensor
from typing import Tuple, Union


class Context:

    def __init__(self) -> None:
        self._saved_tensors = None

    def save_tensors(self, *tensors):
        assert deepnet.is_all_tensor(*tensors)
        self._saved_tensors = tensors

    def saved_tensors(self) -> Tuple[Tensor, ...]:
        return self._saved_tensors


class BackwardFunction(Context):

    def apply(self, *args):
        backward_fn = self._forward_cls.backward
        return backward_fn(self, *args)

    def apply_jvp(self):
        jvp_fn = self._forward_cls.jvp
        return jvp_fn(self)


class FunctionMeta(type):

    def __init__(cls, name, bases, attrs):
        backward_cls = type(
            name + "Backward", (BackwardFunction,),
            {"_forward_cls": cls})
        cls._backward_cls = backward_cls
        super().__init__(name, bases, attrs)


class Function(metaclass=FunctionMeta):

    @staticmethod
    def forward(context, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def backward(context, grad):
        raise NotImplementedError

    @staticmethod
    def jvp(context):
        raise NotImplementedError

    @classmethod
    def apply(cls, *args, **
              kwargs) -> Union[Tensor, Tuple[Tensor, ...]]:
        context = cls._backward_cls()
        output = cls.forward(context, *args, **kwargs)
        output = _pass_to_graph(context, output)
        return output
