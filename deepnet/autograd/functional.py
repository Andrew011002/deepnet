import deepnet
from collections import deque
from .graph import AccumGrad


def grad(tensors, out, outgrad):
    assert out.backfn is not None
    tensormap = _mapify(tensors) 
    backfn = out.backfn
    queue = deque()
    queue.append([backfn, outgrad])

    while queue:
        node, grad = queue.popleft()
        outgrad = backfn.apply(grad) 
        if node.tensor in tensormap:
            tensor = node.tensor
            graddata = outgrad[0].data if _isleaf(node) else grad.data
            tgrad = tensormap[tensor]
            tensormap[tensor] = tgrad.withstate(tgrad.data + graddata)
        if node.nodefns:
            nodefns = node.nodefns
            items = [[n, g] for n, g in zip(nodefns, outgrad)]
            queue.extend(items)
    return tuple(tensormap.values())

def _mapify(tensors):
    if deepnet.istensor(tensors):
        tensors = (tensors,)
    return {t: deepnet.zeros_like(t) for t in tensors}   

def _isleaf(node):
    return isinstance(node.ctx, AccumGrad) 
