import random

import numpy as np
from pytest import raises, fixture

from discopy.quantum.gates import CRz, CRx, CU1
from discopy.quantum.zx import *
from discopy import frobenius


@fixture
def random_had_cnot_diagram():
    def _random_had_cnot_diagram(qubits, depth, p_had=0.5):
        random.seed(0)
        c = Ket(*(qubits * [0]))
        for _ in range(depth):
            r = random.random()
            if r > p_had:
                c = c.H(random.randrange(qubits))
            else:
                tgt = random.randrange(qubits)
                while True:
                    ctrl = random.randrange(qubits)
                    if ctrl != tgt:
                        break
                c = c.CX(tgt, ctrl)
        return c
    return _random_had_cnot_diagram


def test_Diagram():
    bialgebra = Z(1, 2) @ Z(1, 2) >> PRO(1) @ SWAP @ PRO(1) >> X(2, 1) @ X(2, 1)
    assert str(bialgebra) == "Z(1, 2) @ PRO(1) >> PRO(2) @ Z(1, 2) " \
                             ">> PRO(1) @ SWAP @ PRO(1) " \
                             ">> X(2, 1) @ PRO(2) >> PRO(1) @ X(2, 1)"


def test_Spider():
    assert str(Z(1, 2, 3)) == "Z(1, 2, 3)"
    assert str(Y(1, 2, 3)) == "Y(1, 2, 3)"
    assert str(X(1, 2, 3)) == "X(1, 2, 3)"
    for spider in [Z, Y, X]:
        assert spider(1, 2, 3).phase == 3
        assert spider(1, 2, 3j).dagger() == spider(2, 1, -3j)


def test_H():
    assert str(H) == "H"
    assert H[::-1] == H


def test_Sum():
    assert Z(1, 1) + Z(1, 1) >> Z(1, 1) == sum(2 * [Z(1, 1) >> Z(1, 1)])


def test_scalar():
    assert scalar(1j)[::-1] == scalar(-1j)


def test_Functor():
    x = frobenius.Ty('x')
    f = frobenius.Box('f', x, x)
    F = frobenius.Functor(
        ob=lambda _: PRO(1),
        ar=lambda f: Z(len(f.dom), len(f.cod)),
        cod=frobenius.Category(PRO, Diagram))
    assert F(f) == Z(1, 1)
    assert F(frobenius.Swap(x, x)) == Diagram.permutation([1, 0]) == SWAP
    assert F(frobenius.Cup(x.l, x)) == Z(2, 0)
    assert F(frobenius.Cap(x.r, x)) == Z(0, 2)
    assert F(f + f) == Z(1, 1) + Z(1, 1)


def test_subs():
    from sympy.abc import phi, psi
    assert Z(3, 2, phi).subs(phi, 1) == Z(3, 2, 1)
    assert scalar(phi).subs(phi, psi) == scalar(psi)


def test_grad():
    from sympy.abc import phi, psi
    from math import pi
    assert not scalar(phi).grad(psi) and scalar(phi).grad(phi) == scalar(1)
    assert not Z(1, 1, phi).grad(psi)
    assert Z(1, 1, phi).grad(phi) == scalar(pi) @ Z(1, 1, phi + .5)
    assert (Z(1, 1, phi / 2) >> Z(1, 1, phi + 1)).grad(phi)\
        == (scalar(pi / 2) @ Z(1, 1, phi / 2 + .5) >> Z(1, 1, phi + 1))\
           + (Z(1, 1, phi / 2) >> scalar(pi) @ PRO(1) >> Z(1, 1, phi + 1.5))


def test_to_pyzx_errors():
    with raises(NotImplementedError):
        Diagram.to_pyzx(quantum.H)


def test_to_pyzx():
    assert Diagram.from_pyzx(Z(0, 2).to_pyzx()) == Z(0, 2) >> SWAP


def test_to_pyzx_scalar():
    # Test that a scalar is translated to the corresponding pyzx object.
    k = np.exp(np.pi / 4 * 1j)
    m = (scalar(k) @ scalar(k) @ PRO(1)).to_pyzx().to_matrix()
    m = np.linalg.norm(m / 1j - np.eye(2))
    assert np.isclose(m, 0)


def test_from_pyzx_errors():
    bialgebra = Z(1, 2) @ Z(1, 2) >> PRO(1) @ SWAP @ PRO(1) >> X(2, 1) @ X(2, 1)
    graph = bialgebra.to_pyzx()
    graph.set_inputs(())
    graph.set_outputs(())
    with raises(ValueError):  # missing_boundary
        Diagram.from_pyzx(graph)
    graph.auto_detect_io()
    graph.set_inputs(graph.inputs() + graph.outputs())
    with raises(ValueError):  # duplicate_boundary
        Diagram.from_pyzx(graph)


def test_backnforth_pyzx_1():
    from pyzx import Graph
    path = 'test/utils/zx-graph.json'
    graph = Graph.from_json(open(path).read())
    diagram = Diagram.from_pyzx(graph)
    backnforth = lambda diagram: Diagram.from_pyzx(diagram.to_pyzx())
    assert backnforth(diagram) == diagram


def test_backnforth_pyzx_2(random_had_cnot_diagram):
    from pyzx import compare_tensors
    backnforth = lambda diagram: Diagram.from_pyzx(diagram.to_pyzx())
    c = random_had_cnot_diagram(3, 25)
    diagram = circuit2zx(c)
    new_diagram = backnforth(diagram)
    assert compare_tensors(
        new_diagram.to_pyzx(), diagram.to_pyzx(), preserve_scalar=False
    )


def _std_basis_v(*c):
    v = np.zeros(2**len(c), dtype=complex)
    v[np.sum((np.array(c) != 0) * 2**np.arange(len(c)))] = 1
    return np.expand_dims(v, -1)


def test_circuit2zx():
    circuit = Ket(0, 0) >> quantum.H @ Rx(0) >> CRz(0) >> CRx(0) >> CU1(0)
    assert circuit2zx(circuit) == Diagram.decode(
        dom=PRO(0), boxes_and_offsets=zip([
            X(0, 1), X(0, 1), scalar(0.5), H, X(1, 1),
            Z(1, 2), Z(1, 2), X(2, 1), Z(1, 0), scalar(2 ** 0.5),
            X(1, 2), X(1, 2), Z(2, 1), X(1, 0), scalar(2 ** 0.5),
            Z(1, 2), Z(1, 2), X(2, 1), Z(1, 0)],
            [0, 1, 2, 0, 1, 0, 2, 1, 1, 2, 0, 2, 1, 1, 2, 0, 2, 1, 1]))

    # Verify XYZ=iI
    t = circuit2zx(quantum.Z >> quantum.Y >> quantum.X)
    t = t.to_pyzx().to_matrix() - 1j * np.eye(2)
    assert np.isclose(np.linalg.norm(t), 0)

    # Check scalar translation
    t = circuit2zx(
        quantum.X >> quantum.X @ quantum.scalar(1j)).to_pyzx().to_matrix()
    assert np.isclose(np.linalg.norm(t - 1j * np.eye(2)), 0)

    with raises(NotImplementedError):
        circuit2zx(quantum.scalar(1, is_mixed=True))

    t = circuit2zx(Ket(0)).to_pyzx().to_matrix() - _std_basis_v(0)
    assert np.isclose(np.linalg.norm(t), 0)
    t = circuit2zx(Ket(0, 0)).to_pyzx().to_matrix() - _std_basis_v(0, 0)
    assert np.isclose(np.linalg.norm(t), 0)

    assert (circuit2zx(quantum.Id(3).CX(0, 2))
            == Diagram.decode(
                dom=PRO(3),
                boxes_and_offsets=zip(
                    [SWAP, Z(1, 2), X(2, 1), scalar(2 ** 0.5), SWAP],
                    [1, 0, 1, 2, 1])))
