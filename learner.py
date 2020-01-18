# -*- coding: utf-8 -*-
"""
Implements the PRO of functions on vectors with cartesian product as tensor.

Projections and the copy map witness the categorical product.

>>> discard = lambda n: Box('discard', n, 0, lambda x: np.array([]))
>>> assert (COPY >> discard(1) @ Id(1))([46]) == Id(1)([46])\\
...     == (COPY >> Id(1) @ discard(1))([46])

We can check the axioms for symmetry on specific inputs.

>>> assert np.all((SWAP >> SWAP)([1, 2]) == Id(2)([1, 2]))
>>> assert np.all((Id(1) @ SWAP >> SWAP @ Id(1) >> Id(1) @ SWAP)([0, 1, 2])
...            == (SWAP @ Id(1) >> Id(1) @ SWAP >> SWAP @ Id(1))([0, 1, 2]))

As an example, we show that copy and add satisfy the bimonoid law.

>>> assert np.all(ADD([1, 2]) == np.array([3]))
>>> assert np.all((COPY @ COPY >> Id(1) @ SWAP @ Id(1)
...                >> ADD @ ADD)([123, 25]) == (ADD >> COPY)([123, 25]))
"""

from discopy import messages, moncat
from discopy.cat import AxiomError, Quiver
from discopy.matrix import np
from discopy.moncat import Ty, MonoidalFunctor
from discopy.circuit import PRO
from discopy.function import Function, CartesianFunctor


class Diagram(moncat.Diagram):
    """
    Implements learners as diagrams of functions.
    """
    def __init__(self, dom, cod, boxes, offsets, _fast=False):
        super().__init__(PRO(dom), PRO(cod), boxes, offsets, _fast=_fast)

    def then(self, other):
        """
        >>> assert isinstance(ADD >> COPY, Diagram)
        """
        result = super().then(other)
        return Diagram(len(result.dom), len(result.cod),
                       result.boxes, result.offsets, _fast=True)

    def tensor(self, other):
        """
        >>> assert (ADD @ ADD >> Id(1) @ COPY).offsets == [0, 1, 1]
        """
        result = super().tensor(other)
        return Diagram(len(result.dom), len(result.cod),
                       result.boxes, result.offsets, _fast=True)

    def interchange(self, i, j, left=False):
        """
        >>> id = Id(1)
        >>> assert (COPY @ ADD).interchange(0, 1) == id @ ADD >> COPY @ id
        """
        result = super().interchange(i, j, left=left)
        return Diagram(len(result.dom), len(result.cod),
                       result.boxes, result.offsets, _fast=True)

    def normal_form(self, left=False):
        """
        >>> assert (COPY @ COPY >> ADD @ ADD).normal_form()\\
        ...        == (COPY >> ADD) @ (COPY >> ADD)
        """
        result = super().normal_form(left=left)
        return Diagram(len(result.dom), len(result.cod),
                       result.boxes, result.offsets, _fast=True)

    @staticmethod
    def id(x):
        """
        >>> Diagram.id(2)
        Id(2)
        """
        return Id(x)

    def __call__(self, value):
        """
        >>> assert np.all(SWAP([1, 2]) == np.array([2, 1]))
        >>> assert np.all((COPY @ COPY)([1, 2]) == Id(4)([1, 1, 2, 2]))
        """
        ob = Quiver(lambda t: t)
        ar = Quiver(lambda f:
                    Function(f.name, f.dom, f.cod, f.function))
        return CartesianFunctor(ob, ar)(self)(value)


class Id(Diagram):
    """ Implements identity diagrams on n inputs.

    >>> c =  SWAP >> ADD >> COPY
    >>> assert Id(2) >> c == c == c >> Id(2)
    """
    def __init__(self, dim):
        """
        >>> assert Diagram.id(42) == Id(42) == Diagram(42, 42, [], [])
        """
        if isinstance(dim, PRO):
            dim = len(dim)
        super().__init__(dim, dim, [], [], _fast=True)

    def __repr__(self):
        """
        >>> Id(42)
        Id(42)
        """
        return "Id({})".format(len(self.dom))

    def __str__(self):
        """
        >>> print(Id(42))
        Id(42)
        """
        return repr(self)


class Box(moncat.Box, Diagram):
    """
    Implements Python functions as boxes in a learner.Diagram.

    >>> Swap = Box('Swap', 2, 2, lambda x: x[::-1])
    """
    def __init__(self, name, dom, cod, function=None, data=None):
        """
        >>> copy = Copy(2, 3)
        >>> assert copy.dom == PRO(2)
        >>> assert copy.cod == PRO(6)
        """
        if function is not None:
            self._function = function
        moncat.Box.__init__(self, name, PRO(dom), PRO(cod), data=data)
        Diagram.__init__(self, dom, cod, [self], [0], _fast=True)

    @property
    def function(self):
        return self._function

    def __repr__(self):
        return "Box({}, {}, {}{}{})".format(
            repr(self.name), len(self.dom), len(self.cod),
            ', function=' + repr(self.function) if self.function else '',
            ', data=' + repr(self.data) if self.data else '')


class Copy(Box):
    """
    Implements the copy function with domain 'dom' and codomain 'dom * copies'.

    >>> assert np.all(Copy(3, 2)([1, 2, 3]) == np.array([1, 2, 3, 1, 2, 3]))
    >>> assert np.all(Copy(2, 3)([1, 2]) == np.array([1, 2, 1, 2, 1, 2]))
    >>> assert np.all(Copy(1, 2)([34]) == COPY([34]))

    Parameters
    ----------
    dom : int
        Domain dimension.
    copies : int
        Number of copies.
    """
    def __init__(self, dom, copies=2):
        """
        >>> assert Copy(2, 3).dom == PRO(2)
        >>> assert Copy(2, 3).cod == PRO(6)
        """
        name = 'Copy({}, {})'.format(dom, copies)

        def func(val):
            return np.concatenate([val for i in range(copies)])
        super().__init__(name, dom, copies * dom, func)


class Sum(Box):
    """
    Implements the sum function with codomain 'cod' and domain 'cod * copies'.

    >>> assert np.all(Sum(2, 3)([1, 2, 3, 4, 5, 6]) == np.array([9, 12]))

    Parameters
    ----------
    cod : int
        Codomain dimension.
    copies : int
        Number of copies.
    """
    def __init__(self, cod, copies=2):
        """
        >>> assert Sum(3, 2).cod == PRO(3)
        >>> assert Sum(2, 3).cod == PRO(2)
        """
        name = 'Sum({}, {})'.format(cod, copies)

        def func(val):
            return np.array([np.sum([val[i + cod * j] for j in range(copies)])
                             for i in range(cod)])
        super().__init__(name, copies * cod, cod, func)


class Mults(Diagram):
    """
    Implements scalar multiplication by a list of weights.

    >>> assert np.all(Mults(2, [2., 3.])([1, 1]) == np.array([2, 3]))

    Parameters
    ----------
    dom : int
        Domain dimension.
    weights : any
        List of weights of length 'dom'.
    """
    def __init__(self, dom, weights):
        """
        >>> m = Mults(3, [1, 2, 3])
        >>> assert m.dom == PRO(3) == m.cod
        """
        super().__init__(dom, dom, [MULT(weight) for weight in weights],
                         list(range(len(weights))))


class Neuron(Diagram):
    """
    Implements a neuron with domain 'dom' and codomain 1,
    given a list of weights of length 'dom + 1', and an activation function.

    >>> assert Neuron(3, [1.3, 0.5, 2.1, 0.4])([1, 2, 3])\\
    ...             == np.array([0.99987662])
    >>> disconnect = Neuron(4, [0., 0., 0., 0., 0.])
    >>> assert disconnect([13, 2, 3, 4]) == disconnect([1, 2, 3, 4])

    Parameters
    ----------
    dom : int
        Domain dimension.
    weights : list
        List of weights of length 'dom + 1'.
    """
    def __init__(self, dom, weights):
        """
        >>> neuron = Neuron(4, [0.1, 0.4, 3., 2., 0.7])
        >>> assert neuron.dom == PRO(4)
        >>> assert neuron.cod == PRO(1)
        """
        neuron = Mults(dom, weights[:-1]) @ BIAS(weights[-1])
        neuron = neuron >> Sum(1, dom + 1) >> sigmoid
        super().__init__(dom, 1, neuron.boxes, neuron.offsets, _fast=True)


class Layer(Diagram):
    """
    Implements a neural network layer as a diagram of neurons.

    >>> params = np.array([[0.1, 0.2, 0.3], [1, 2, 3], [0.3, 0.2, 0.1]])
    >>> layer = Layer(2, 3, params)
    >>> assert np.all(layer([1., 1.]) ==\\
    ...               np.array([0.64565629, 0.99752742, 0.64565629]))

    Parameters
    ----------
    dom : int
        Number of inputs.
    cod : int
        Number of outputs.
    params: array
        Array of weigths with shape '(cod, dom + 1)'
    """
    def __init__(self, dom, cod, params):
        """
        >>> layer = Layer(1, 2, np.array([[0., 0.1], [1.2, 1.3]]))
        >>> assert (layer.dom == PRO(1)) and (layer.cod == PRO(2))
        """
        neurons = Id(0)
        for i in range(cod):
            neurons = neurons @ Neuron(dom, params[i])
        layer = Copy(dom, cod) >> neurons
        super().__init__(dom, cod, layer.boxes, layer.offsets, _fast=True)


class LearnerFunctor(MonoidalFunctor):
    """
    Implements functors into the category of learners.

    >>> x, y = Ty('x'), Ty('y')
    >>> f = moncat.Box('f', x, y)
    >>> g = moncat.Box('g', y, x)
    >>> F = LearnerFunctor({x: PRO(1), y: PRO(2)}, {f: COPY >> SWAP, g: ADD})
    >>> assert F(f >> g)([1]) == np.array([2])
    >>> ob = lambda n: Quiver(lambda x: PRO(n * len(x)))
    >>> M = lambda n: LearnerFunctor(ob(n), {COPY: Copy(n), ADD: Sum(n)})
    >>> assert np.all(M(3)(COPY >> ADD)([1, 2, 3]) == np.array([2, 4, 6]))
    """
    def __init__(self, ob, ar):
        super().__init__(ob, ar, ob_cls=PRO, ar_cls=Diagram)


SWAP = Box('SWAP', 2, 2, lambda x: x[::-1])
COPY = Box('COPY', 1, 2, lambda x: np.concatenate((x, x)))
ADD = Box('ADD', 2, 1, lambda x: np.array([x[0] + x[1]]))
sigmoid = Box('sigmoid', 1, 1, lambda x: 1/(1 + np.exp(-x)))


def BIAS(scalar):
    return Box('{}'.format(scalar), 0, 1, lambda x: np.array([scalar]))


def MULT(scalar):
    return Box('{}'.format(scalar), 1, 1, lambda x: scalar * x)
