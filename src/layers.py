import numpy as np
from src.util import sigmoid


class Layer:
    """Layer of a fully connected neural network"""
    def __init__(self, num_neurons, num_inputs, init_fact=0.01):
        self._num_neurons = num_neurons
        self._weights = np.random.randn(num_neurons, num_inputs+1)*init_fact  # biases are last column
        # Gradients of output with respect to input/weights/biases
        self._grad_inputs = np.zeros(num_neurons)
        self._grad_weights = np.zeros(self._weights.shape)
        # Gradients of weights and biases
        self._weight_grad = np.zeros(self._weights.shape)
        self._next_layer = None

    def forward_pass(self, inputs):
        """Pass inputs through the network"""
        pass

    def back_propagate(self, gradient_in):
        """Propagate gradients backward through the layer and save weight/bias gradients
        :param gradient_in: vector of gradients (dLoss/dy) heading into each neuron
        :return grad_inputs: vector of gradients heading out of each neuron (dLoss/dx = dLoss/dy * dy/dx)"""
        grad_inputs = self._grad_inputs.T.dot(gradient_in)
        self._weight_grad[:, :-1] = gradient_in[:, np.newaxis] * self._grad_weights[:, :-1]
        self._weight_grad[:, -1] = self._grad_weights[:, -1].T.dot(gradient_in)
        return grad_inputs

    @property
    def next_layer(self):
        return self._next_layer

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights):
        self._weights = new_weights

    @property
    def grad_weights(self):
        return self._grad_weights

    @property
    def grad_inputs(self):
        return self._grad_inputs

    @property
    def weight_grad(self):
        return self._weight_grad

    @property
    def num_neurons(self):
        return self._num_neurons


class ReLuLayer(Layer):
    """Layer with ReLu activated neurons"""
    def forward_pass(self, inputs):
        """Calculate the output of this layer given the input
        Also save gradients of output wrt input, weights and biases"""
        outputs = np.maximum(0, np.dot(self.weights[:, :-1], inputs) + self.weights[:, -1])
        relu_grad = 1. * (outputs > 0)
        self._grad_inputs = relu_grad[np.newaxis, :].T * self._weights[:, :-1]
        self.grad_weights[:, :-1] = relu_grad[np.newaxis, :].T * (inputs[np.newaxis, :]
                                                                   * np.ones(self._grad_inputs.shape))
        self.grad_weights[:, -1] = np.ones(self._num_neurons) * relu_grad
        return outputs


class LinearLayer(Layer):
    """Linear classifier layer e.g. for output layer"""
    def forward_pass(self, inputs):
        outputs = np.dot(self._weights[:, :-1], inputs) + self._weights[:, -1]
        self._grad_inputs = self._weights[:, :-1]
        self._grad_weights[:, :-1] = inputs[np.newaxis, :] * np.ones(self._weights[:, :-1].shape)
        self._grad_weights[:, -1] = np.ones(self.num_neurons)
        return outputs


class SigmoidLayer(Layer):
    """Sigmoid activated layer"""
    def forward_pass(self, inputs):
        outputs = sigmoid(np.dot(self._weights[:, :-1], inputs) + self._weights[:, -1])
        sigmoid_grad = outputs * (1 - outputs)
        self._grad_inputs = sigmoid_grad[np.newaxis, :].T * self._weights[:, :-1]
        self._grad_weights[:, :-1] = sigmoid_grad[np.newaxis, :].T * (inputs[np.newaxis, :] * np.ones(self._grad_inputs.shape))
        self._grad_weights[:, -1] = np.ones(self._num_neurons) * sigmoid_grad
        return outputs


class TanhLayer(Layer):
    """tanh activated layer"""
    def forward_pass(self, inputs):
        outputs = np.tanh(np.dot(self._weights[:, :-1], inputs) + self._weights[:, -1])
        tanh_grad = 1 - outputs**2
        self._grad_inputs = tanh_grad[np.newaxis, :].T * self._weights[:, :-1]
        self._grad_weights[:, :-1] = tanh_grad[np.newaxis, :].T * (inputs[np.newaxis, :] * np.ones(self._grad_inputs.shape))
        self._grad_weights[:, -1] = np.ones(self._num_neurons) * tanh_grad
        return outputs