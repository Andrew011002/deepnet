import numpy as np
import nura
from nura.tensors import Tensor
from typing import Dict, Generator, Tuple, Optional, Callable, Any, Union
from collections import deque


def backward(out: Tensor, grad: Optional[Tensor] = None) -> None:
    if err := _backwarderr(out, grad):
        raise err
    if grad is None:
        grad = nura.oneslike(out)
    _backward(out, grad)


def _backward(out: Tensor, grad: Optional[Tensor] = None) -> None:
    queue = deque()
    queue.append((out.backfn, grad))

    while queue:
        node, grad = queue.popleft()
        nodes = node.children()
        tensor = node.tensor
        if tensor.leaf:
            assert isinstance(grad, Tensor)
            accumgrad = sumgrad(tensor, grad) if mismatch(tensor, grad) else grad
            oldgrad = (
                tensor.grad
                if isinstance(tensor.grad, Tensor)
                else nura.zeroslike(tensor)
            )
            newgrad = oldgrad + accumgrad
            tensor.mutate(grad=newgrad.to(tensor.dtype))
        elif nodes:
            items = [(n, g) for n, g in zip(nodes, node.apply(grad, backward=True))]
            queue.extend(items)


def _backwarderr(
    out: Tensor, grad: Optional[Tensor] = None
) -> Optional[Union[RuntimeError, ValueError]]:
    if out.backfn is None:
        return RuntimeError(
            "Cannot backpropagate gradients for Tensor with no backward function"
        )
    if grad is None and out.nelem != 1:
        return RuntimeError(
            f"A gradient (grad) must be passed if the Tensor has more than one elements, received Tensor with {out.nelem}"
        )
    elif grad is not None and not grad.gradtensor:
        return ValueError(
            f"Expected grad argument to a floating-point type, received {grad.dtype.name()}"
        )
    return None


def grad(
    inpt: Union[Tensor, Tuple[Tensor, ...]], out: Tensor, grad: Optional[Tensor] = None
) -> Tuple[Tensor, ...]:
    inpt = tupify(inpt)
    if err := _graderr(inpt, out, grad):
        raise err
    if grad is None:
        grad = nura.oneslike(out)
    inptmap = _grad(inpt, out, grad)
    return tuple(inptmap.values())


def _grad(
    inpt: Tuple[Tensor, ...], out: Tensor, grad: Optional[Tensor] = None
) -> Dict[Tensor, Tensor]:
    grads = tuple(nura.zeroslike(t) for t in inpt)
    inptmap = mapify(inpt, grads)
    queue = deque()
    queue.append((out.backfn, grad))

    while queue:
        node, grad = queue.popleft()
        nodes = node.children()
        tensor = node.tensor
        if tensor in inptmap:
            assert isinstance(grad, Tensor)
            accumgrad = sumgrad(tensor, grad) if mismatch(tensor, grad) else grad
            oldgrad = inptmap[tensor]
            newgrad = oldgrad + accumgrad
            inptmap[tensor] = newgrad.to(tensor.dtype)
        if nodes:
            items = [[n, g] for n, g in zip(nodes, node.apply(grad, backward=True))]
            queue.extend(items)
    return inptmap


def _graderr(
    inpt: Tuple[Tensor, ...], out: Tensor, grad: Optional[Tensor] = None
) -> Optional[Union[ValueError, RuntimeError]]:
    if not all(t.gradtensor for t in inpt):
        return ValueError(
            "One or more Tensors passed to argument 'inpt' cannot have their gradients computed because they're not differentiable types"
        )
    if out.backfn is None:
        return ValueError(
            "Cannot backpropagate gradients for Tensor with no backward function"
        )
    if grad is None and out.nelem != 1:
        return RuntimeError(
            f"A gradient (grad) must be passed if the output Tensor (out) has more than one elements, received Tensor with {out.nelem}"
        )
    elif grad is not None and not grad.gradtensor:
        return ValueError(
            f"Expected grad argument to a floating-point type, received {grad.dtype.name()}"
        )
    return None


def mapify(keys, values) -> Dict[Tensor, Any]:
    return {k: v for k, v in zip(keys, values)}


def mismatch(tensor: Tensor, grad: Tensor) -> bool:
    return tensor.dim != grad.dim and tensor.ndim <= grad.ndim


def sumgrad(tensor: Tensor, grad: Tensor) -> Tensor:
    dim = sumdims(tensor.dim, grad.dim, tensor.ndim, grad.ndim)
    keepdims = tensor.ndim == grad.ndim
    return grad.sum(dim=dim, keepdims=keepdims)


def sumdims(tdim, gdim, tndim, gndim) -> Tuple[int, ...]:
    paddim = np.pad(tdim, (gndim - tndim, 0), constant_values=0)
    mask = paddim != np.array(gdim)
    return tuple(np.where(mask)[0])


def tupify(inpt) -> Tuple[Tensor, ...]:
    if isinstance(inpt, Tensor):
        return (inpt,)
    return inpt


def vjp(
    inpt: Union[Tuple[Tensor, ...], Tensor],
    vec: Tensor,
    f: Callable[..., Tensor],
    *args,
    **kwargs,
) -> Tuple[Tensor, Tuple[Tensor, ...]]:

    inpt = tupify(inpt)
    if err := _vjperr(inpt, vec):
        raise err
    inpt = tuple(t.mutated(usegrad=True, grad=None, leaf=True) for t in inpt)
    vec = vec.mutated(usegrad=False, grad=None)
    out, grads = _vjp(inpt, vec, f, *args, **kwargs)
    return out.mutated(usegrad=False, backfn=None, leaf=True), grads


def _vjp(
    inpt: Tuple[Tensor, ...],
    vec: Tensor,
    f: Callable[..., Tensor],
    *args,
    **kwargs,
) -> Tuple[Tensor, Tuple[Tensor, ...]]:
    if err := _vjperr(inpt, vec):
        raise err
    with nura.autograd(enabled=True, reverse=True, forward=False):
        out = f(*inpt, *args, **kwargs)
    inptmap = _grad(inpt, out, vec)
    return out, tuple(inptmap.values())


def _vjperr(inpt: Tuple[Tensor, ...], vec: Tensor) -> Optional[ValueError]:
    if not all(t.gradtensor for t in inpt):
        return ValueError(
            "One or more Tensors passed to argument 'inpt' cannot have their gradients computed because they're not differentiable types"
        )
    if not vec.gradtensor:
        return ValueError(
            f"Expected Tensor passed to 'vec' to be a floating-point type, received {vec.dtype.name()}"
        )
    return None


def jvp(
    inpt: Union[Tuple[Tensor, ...], Tensor],
    vec: Union[Tuple[Tensor, ...], Tensor],
    f: Callable[..., Tensor],
    *args,
    **kwargs,
) -> Tuple[Tensor, Tensor]:

    inpt = tupify(inpt)
    vec = tupify(vec)
    if err := _jvperr(inpt, vec):
        raise err
    gen = (v for v in vec)
    inpt = tuple(t.mutated(usegrad=True, grad=next(gen)) for t in inpt)
    out, grad = _jvp(inpt, f, *args, **kwargs)
    return out.mutated(usegrad=False, leaf=True), grad


def _jvp(
    inpt: Tuple[Tensor, ...],
    f: Callable[..., Tensor],
    *args,
    **kwargs,
) -> Tuple[Tensor, Tensor]:
    with nura.autograd(enabled=True, reverse=False, forward=True):
        out = f(*inpt, *args, **kwargs)
    assert out.grad is not None
    return out, out.grad


def _jvperr(inpt: Tuple[Tensor, ...], vec: Tuple[Tensor, ...]) -> Optional[ValueError]:
    if not all(t.gradtensor for t in inpt):
        return ValueError(
            "One or more Tensors passed to argument 'inpt' cannot have their gradients computed because they're not differentiable types"
        )
    if not all(v.gradtensor for v in vec):
        return ValueError(
            "One or more Tensors passed to argument 'vec' cannot be used to compute jvp() because they're not a floating-point type"
        )
    return None


def jacrev(
    inpt: Union[Tuple[Tensor, ...], Tensor],
    f: Callable[..., Tensor],
    pos=0,
    *args,
    **kwargs,
) -> Tuple[Tensor, Tensor]:

    inpt = tupify(inpt)
    if err := _jacerr(inpt):
        raise err
    inpt = tuple(t.mutated(usegrad=True, grad=None, leaf=True) for t in inpt)
    with nura.autograd(enabled=True, reverse=True, forward=False):
        out = f(*inpt, *args, **kwargs)
    tensor = inpt[pos]
    jac = getjac(tensor, out)
    perts = getperts(out)

    for row, pert in zip(np.ndindex(out.dim), perts):
        _, grads = _vjp(inpt, pert, f, *args, **kwargs)
        jacrow = grads[pos]
        slc = row + (...,)
        jac[slc] = jacrow
    return out, jac


def jacfwd(
    inpt: Union[Tuple[Tensor, ...], Tensor],
    f: Callable[..., Tensor],
    pos=0,
    *args,
    **kwargs,
) -> Tuple[Tensor, Tensor]:

    inpt = tupify(inpt)
    if err := _jacerr(inpt):
        raise err
    with nura.autograd(enabled=False):
        out = f(*inpt, *args, **kwargs)
    tensor = inpt[pos]
    perts = getperts(tensor)
    jac = getjac(tensor, out)
    colinpt = [
        t.mutated(usegrad=True, grad=nura.zeroslike(t)) if i != pos else t
        for i, t in enumerate(inpt)
    ]
    for col, pert in zip(np.ndindex(tensor.dim), perts):
        colinpt[pos] = colinpt[pos].mutated(usegrad=True, grad=pert)
        _, jaccol = _jvp(tuple(colinpt), f, *args, **kwargs)
        slc = (...,) + col
        jac[slc] = jaccol
    return out, jac


def _jacerr(inpt: Tuple[Tensor, ...]) -> Optional[ValueError]:
    if not all(t.gradtensor for t in inpt):
        return ValueError(
            "Cannot compute Jacobian because one or more Tensors passed to 'inpt' are not a floating-point type"
        )
    return None


def getperts(tensor: Tensor) -> Generator[Tensor, None, None]:
    nelem, dim, dtype = tensor.nelem, tensor.dim, tensor.dtype
    perts = nura.zeros((nelem,) + dim).to(dtype)
    arange = np.arange(nelem)
    indices = np.unravel_index(arange, dim)
    slc = (arange,) + indices
    perts[slc] = 1.0
    return (perts[i] for i in range(nelem))


def getjac(tensor: Tensor, out: Tensor) -> Tensor:
    dim = out.dim + tensor.dim
    jac = nura.zeros(dim).to(out.dtype)
    return jac
