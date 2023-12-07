import numpy as np
import deepnet
import deepnet.nn.functional as f


def test_add_backward_scalar():
    a = np.random.rand()
    b = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.add(a_tensor, b_tensor)
    result_tensor.backward()
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected = (a + b + h - (a + b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected, rtol=1e-5, atol=1e-5)


def test_add_backward_vector():
    a = np.random.rand(4)
    b = np.random.rand(4)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.add(a_tensor, b_tensor)

    v = deepnet.ones((4,), dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected = (a + b + h - (a + b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected, rtol=1e-5, atol=1e-5)


def test_add_backward_matrix():
    a = np.random.rand(5, 5)
    b = np.random.rand(5, 5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.add(a_tensor, b_tensor)

    m = deepnet.ones((5, 5), dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected = (a + b + h - (a + b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected, rtol=1e-5, atol=1e-5)


def test_sub_backward_scalar():
    a = np.random.rand()
    b = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.sub(a_tensor, b_tensor)

    result_tensor.backward()
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = (a + h - b - (a - b)) / h
    expected_grad_b = (a - (b + h) - (a - b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_sub_backward_vector():
    a = np.random.rand(4)
    b = np.random.rand(4)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.sub(a_tensor, b_tensor)

    v = deepnet.ones((4), dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = (a + h - b - (a - b)) / h
    expected_grad_b = (a - (b + h) - (a - b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_sub_backward_matrix():
    a = np.random.rand(5, 5)
    b = np.random.rand(5, 5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.sub(a_tensor, b_tensor)

    m = deepnet.ones((5, 5), dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = (a + h - b - (a - b)) / h
    expected_grad_b = (a - (b + h) - (a - b)) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_mul_backward_scalar():
    a = np.random.rand()
    b = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.mul(a_tensor, b_tensor)

    result_tensor.backward()
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) * b - a * b) / h
    expected_grad_b = (a * (b + h) - a * b) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_mul_backward_vector():
    a = np.random.rand(4)
    b = np.random.rand(4)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.mul(a_tensor, b_tensor)

    v = deepnet.ones((4,), dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) * b - a * b) / h
    expected_grad_b = (a * (b + h) - a * b) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_mul_backward_matrix():
    a = np.random.rand(5, 5)
    b = np.random.rand(5, 5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.mul(a_tensor, b_tensor)

    m = deepnet.ones((5, 5), dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) * b - a * b) / h
    expected_grad_b = (a * (b + h) - a * b) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_div_backward_scalar():
    a = np.random.rand()
    b = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.div(a_tensor, b_tensor)

    result_tensor.backward()
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) / b - a / b) / h
    expected_grad_b = (a / (b + h) - a / b) / h
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_div_backward_vector():
    a = np.random.rand(4)
    b = np.random.rand(4)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.div(a_tensor, b_tensor)

    v = deepnet.ones((4,), dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) / b - (a - h) / b) / (2 * h)
    expected_grad_b = (a / (b + h) - a / (b - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_div_backward_matrix():
    a = np.random.rand(3, 3)
    b = np.random.rand(3, 3)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.div(a_tensor, b_tensor)

    m = deepnet.ones((3, 3), dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = ((a + h) / b - (a - h) / b) / (2 * h)
    expected_grad_b = (a / (b + h) - a / (b - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)

# Using symbolic differentiaton as numeric differentiation, gives unwanted results


def test_matmul_backward_same_shape():
    a = np.random.rand(2, 2)
    b = np.random.rand(2, 2)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.matmul(a_tensor, b_tensor)

    ones = np.ones((2, 2))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    expected_grad_a = np.matmul(ones, b.T)
    expected_grad_b = np.matmul(a.T, ones)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_matmul_backward_different_shape():
    a = np.random.rand(3, 2)
    b = np.random.rand(2, 4)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.matmul(a_tensor, b_tensor)

    ones = np.ones((3, 4))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    expected_grad_a = np.matmul(ones, b.T)
    expected_grad_b = np.matmul(a.T, ones)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_matmul_backward_rank3_same_shape():
    a = np.random.rand(5, 5, 5)
    b = np.random.rand(5, 5, 5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.matmul(a_tensor, b_tensor)

    ones = np.ones((5, 5, 5))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    expected_grad_a = np.matmul(ones, b.transpose(0, 2, 1))
    expected_grad_b = np.matmul(a.transpose(0, 2, 1), ones)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_matmul_backward_rank3_different_shape():
    a = np.random.rand(3, 4, 5)
    b = np.random.rand(3, 5, 2)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.matmul(a_tensor, b_tensor)

    ones = np.ones((3, 4, 2))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    expected_grad_a = np.matmul(ones, b.transpose(0, 2, 1))
    expected_grad_b = np.matmul(a.transpose(0, 2, 1), ones)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_pow_backward_scalar():
    a = np.random.rand()
    b = 2.

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.pow(a_tensor, b_tensor)
    result_tensor.backward()

    grad_a, grad_b = a_tensor.grad, b_tensor.grad
    h = 1e-8
    expected_grad_a = (
        np.power(a + h, b) - np.power(a - h, b)) / (2 * h)
    expected_grad_b = (
        np.power(a, b + h) - np.power(a, b - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, expected_grad_b, rtol=1e-5, atol=1e-5)


def test_pow_backward_vector():
    a = np.random.rand(5)
    b = 3.

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.pow(a_tensor, b_tensor)

    ones = np.ones(5)
    v = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = (
        np.power(a + h, b) - np.power(a - h, b)) / (2 * h)
    expected_grad_b = (
        np.power(a, b + h) - np.power(a, b - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, np.sum(expected_grad_b, axis=0),
        rtol=1e-5, atol=1e-5)


def test_pow_backward_matrix():
    a = np.random.rand(5, 5)
    b = 4.

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b, use_grad=True)
    result_tensor = f.pow(a_tensor, b_tensor)

    ones = np.ones((5, 5))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a, grad_b = a_tensor.grad, b_tensor.grad

    h = 1e-8
    expected_grad_a = (
        np.power(a + h, b) - np.power(a - h, b)) / (2 * h)
    expected_grad_b = (
        np.power(a, b + h) - np.power(a, b - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(
        grad_b.data, np.sum(expected_grad_b, axis=(0, 1)),
        rtol=1e-5, atol=1e-5)


def test_pow_backward_vector_exp():
    a = np.random.rand(4)
    b = np.full_like(a, 2)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b)
    result_tensor = f.pow(a_tensor, b_tensor)

    ones = np.ones(4)
    v = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (
        np.power(a + h, b) - np.power(a - h, b)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_pow_backward_matrix_exp():
    a = np.random.rand(3, 3)
    b = np.full_like(a, 3)

    a_tensor = deepnet.tensor(a, use_grad=True)
    b_tensor = deepnet.tensor(b)
    result_tensor = f.pow(a_tensor, b_tensor)

    ones = np.ones((3, 3))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (
        np.power(a + h, b) - np.power(a - h, b)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_sine_backward_scalar():
    a = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.sine(a_tensor)
    result_tensor.backward()

    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.sin(a + h) - np.sin(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_sine_backward_vector():
    a = np.random.rand(5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.sine(a_tensor)

    ones = np.ones(5)
    v = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.sin(a + h) - np.sin(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_sine_backward_matrix():
    a = np.random.rand(3, 3)

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.sine(a_tensor)

    ones = np.ones((3, 3))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.sin(a + h) - np.sin(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_cosine_backward_scalar():
    a = np.random.rand()

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.cosine(a_tensor)
    result_tensor.backward()

    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.cos(a + h) - np.cos(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_cosine_backward_vector():
    a = np.random.rand(5)

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.cosine(a_tensor)

    ones = np.ones(5)
    v = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(v)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.cos(a + h) - np.cos(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def test_cosine_backward_matrix():
    a = np.random.rand(3, 3)

    a_tensor = deepnet.tensor(a, use_grad=True)
    result_tensor = f.cosine(a_tensor)

    ones = np.ones((3, 3))
    m = deepnet.tensor(ones, dtype=deepnet.float)
    result_tensor.backward(m)
    grad_a = a_tensor.grad

    h = 1e-8
    expected_grad_a = (np.cos(a + h) - np.cos(a - h)) / (2 * h)
    np.testing.assert_allclose(
        grad_a.data, expected_grad_a, rtol=1e-5, atol=1e-5)


def main():

    with deepnet.use_grad():

        # Add Backward Tests

        test_add_backward_scalar()
        test_add_backward_vector()
        test_add_backward_matrix()

        # Sub Backward Tests

        test_sub_backward_scalar()
        test_sub_backward_vector()
        test_sub_backward_matrix()

        # Mul Backward Tests

        test_mul_backward_scalar()
        test_mul_backward_vector()
        test_sub_backward_matrix()

        # Div Backward Tests

        test_div_backward_scalar()
        test_div_backward_vector()
        test_div_backward_matrix()

        # Matmul Backward Tests

        test_matmul_backward_same_shape()
        test_matmul_backward_different_shape()
        test_matmul_backward_rank3_same_shape()
        test_matmul_backward_rank3_different_shape()

        # Sine Backward Tests

        test_sine_backward_scalar()
        test_sine_backward_vector()
        test_sine_backward_matrix()

        # Cosine Backward Tests

        test_cosine_backward_scalar()
        test_cosine_backward_vector()
        test_cosine_backward_matrix()

        # Pow Backward Tests

        test_pow_backward_scalar()
        test_pow_backward_vector()
        test_pow_backward_matrix()

        # Pow Backward (exponent is not a scalar)

        test_pow_backward_vector_exp()
        test_pow_backward_matrix_exp()

        print("All tests passed")


if __name__ == "__main__":
    main()