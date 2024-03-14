import numpy as np
import nura
from nura.types import dtype, dim, dimlike
from nura.tensors import Tensor, tensor
from typing import Optional, Type, Any, Tuple, Union


def empty(dim: dimlike, dtype: Optional[Type[dtype]] = None):
    if dtype is None:
        dtype = nura.float
    empty_arr = np.empty(dim)
    return tensor(empty_arr, dtype=dtype)


def emptylike(a: Tensor, dtype: Optional[Type[dtype]] = None):
    if dtype is None:
        dtype = nura.float if dtype is nura.bool else a.dtype
    data = a.data
    empty_arr = np.empty_like(data)
    return tensor(empty_arr, dtype=dtype)


def zeros(dim: dimlike, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = nura.float
    dim = todim(dim)
    zero_arr = np.zeros(dim)
    return tensor(zero_arr, usegrad, dtype)


def zeroslike(a: Tensor, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = nura.float if dtype is nura.bool else a.dtype
    data = a.data
    zero_arr = np.zeros_like(data)
    return tensor(zero_arr, usegrad, dtype)


def ones(dim: dimlike, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = nura.float
    dim = todim(dim)
    ones_arr = np.ones(dim)
    return tensor(ones_arr, usegrad, dtype)


def oneslike(a: Tensor, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = nura.float if dtype is nura.bool else a.dtype
    data = a.data
    ones_arr = np.ones_like(data)
    return tensor(ones_arr, usegrad, dtype)


def randn(
    dim: Optional[dimlike] = None,
    usegrad=False,
    dtype: Optional[Type[dtype]] = None,
) -> Tensor:
    if dtype is None:
        dtype = nura.float
    dim = todim(dim)
    randn_arr = np.random.randn(*dim)
    return tensor(randn_arr, usegrad, dtype)


def randnlike(a: Tensor, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = (
            nura.float
            if a.dtype not in (nura.half, nura.float, nura.double)
            else a.dtype
        )
    dim = a.dim
    return randn(dim, usegrad, dtype)


def rand(
    dim: Optional[dimlike] = None,
    usegrad=False,
    dtype: Optional[Type[dtype]] = None,
) -> Tensor:
    if dtype is None:
        dtype = nura.float
    dim = todim(dim)
    rand_arr = np.random.rand(*dim)
    return tensor(rand_arr, usegrad, dtype)


def randlike(a: Tensor, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = (
            nura.float
            if a.dtype not in (nura.half, nura.float, nura.double)
            else a.dtype
        )
    dim = a.dim
    return rand(dim, usegrad, dtype)


def randint(
    low: int, high: int, dim: dimlike, dtype: Optional[Type[dtype]] = None
) -> Tensor:
    if dtype is None:
        dtype = nura.int
    dim = todim(dim)
    randint_arr = np.random.randint(low, high, dim)
    return tensor(randint_arr, dtype=dtype)


def randintlike(
    low: int, high: int, a: Tensor, dtype: Optional[Type[dtype]] = None
) -> Tensor:
    if dtype is None:
        dtype = (
            nura.int
            if dtype in (nura.half, nura.float, nura.double, nura.bool)
            else a.dtype
        )
    dim = a.dim
    return randint(low, high, dim, dtype)


def identity(n: int, usegrad=False, dtype: Optional[Type[dtype]] = None) -> Tensor:
    if dtype is None:
        dtype = nura.float
    data = np.identity(n)
    return tensor(data, usegrad, dtype)


def full(
    dim: dimlike,
    num: float,
    usegrad=False,
    dtype: Optional[Type[dtype]] = None,
) -> Tensor:
    if dtype is None:
        dtype = nura.float
    dim = todim(dim)
    data = np.full(dim, num)
    return tensor(data, usegrad, dtype)


def eye(
    n: int,
    m: Optional[int] = None,
    k=0,
    dtype: Optional[Type[dtype]] = None,
) -> Tensor:
    if dtype is None:
        dtype = nura.float
    data = np.eye(n, m, k)
    return tensor(data, dtype=dtype)


def where(
    logical: Union[Tensor, bool],
    x: Union[Tensor, float, int, bool],
    y: Union[Tensor, float, int, bool],
) -> Tensor:
    data = logical.data if isinstance(logical, Tensor) else logical
    xdata = x.data if isinstance(x, Tensor) else x
    ydata = y.data if isinstance(y, Tensor) else y
    return tensor(np.where(data, xdata, ydata))


def poswhere(logical: Union[Tensor, bool]) -> Tensor:
    data = logical.data if isinstance(logical, Tensor) else logical
    return tensor(np.where(data)[0])


def nonzero(a: Tensor):
    data = np.nonzero(a.data)
    return tensor(data)


def argmax(a: Tensor, pos: Optional[int] = None, keepdims=False):
    data = np.argmax(a.data, axis=pos, keepdims=keepdims)
    return tensor(data)


def argmin(a: Tensor, pos: Optional[int] = None, keepdims=False):
    data = np.argmin(a.data, axis=pos, keepdims=keepdims)
    return tensor(data)


def tensorany(a: Tensor, dim: Optional[dimlike] = None, keepdims=False):
    return tensor(np.any(a.data, axis=dim, keepdims=keepdims))


def tensorall(a: Tensor, dim: Optional[dimlike] = None, keepdims=False):
    return tensor(np.all(a.data, axis=dim, keepdims=keepdims))


def hashtensor(a: Tensor) -> int:
    return hash(id(a))


def equal(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = nura.atot(a, b)
    return tensor(np.equal(a.data, b.data))


def less(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(np.less(a.data, b.data))


def lesseq(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(np.less_equal(a.data, b.data))


def greater(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(np.greater(a.data, b.data))


def greatereq(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(np.greater_equal(a.data, b.data))


def notequal(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(np.not_equal(a.data, b.data))


def tensorand(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(a.data and b.data)


def tensoror(a: Union[Tensor, Any], b: Union[Tensor, Any]) -> Tensor:
    a, b = atot(a, b)
    return tensor(a.data or b.data)


def tensornot(a: Union[Tensor, Any]) -> Tensor:
    b = atot(a)[0]
    return tensor(not b.data)


def atot(*args: Any) -> Union[Tuple[Tensor, ...], Tensor]:
    return tuple(a if istensor(a) else tensor(a) for a in args)


def typesmatch(*tensors: Tensor) -> bool:
    return len(set(t.dtype for t in tensors)) == 1


def to(a: Tensor, dtype: Type[dtype]):
    if not istensor(a):
        raise ValueError(f"Expected Tensor, received {a.__class__.__name__}")
    data = dtype.numpy(a.data)
    return tensor(data, a.usegrad, dtype)


def todim(dim: Any) -> dim:
    if dim is None:
        return tuple()
    if isinstance(dim, int):
        return (dim,)
    return dim


def iscontig(a: Tensor) -> bool:
    return a.data.flags["C_CONTIGUOUS"]


def istensor(obj: Any) -> bool:
    return isinstance(obj, Tensor)


def typename(a: Tensor) -> str:
    return f"{a.dtype.name().capitalize()}{a.__class__.__name__}"
