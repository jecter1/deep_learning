import numpy as np

from layers import FullyConnectedLayer, ReLULayer, softmax_with_cross_entropy, l2_regularization


class TwoLayerNet:
    """ Neural network with two fully connected layers """

    def __init__(self, n_input, n_output, hidden_layer_size, reg):
        """
        Initializes the neural network

        Arguments:
        n_input, int - dimension of the model input
        n_output, int - number of classes to predict
        hidden_layer_size, int - number of neurons in the hidden layer
        reg, float - L2 regularization strength
        """
        self.reg = reg
        self.layers = []
        self.layers.append(FullyConnectedLayer(n_input, hidden_layer_size))
        self.layers.append(ReLULayer())
        self.layers.append(FullyConnectedLayer(hidden_layer_size, n_output))

    def compute_loss_and_gradients(self, X, y):
        """
        Computes total loss and updates parameter gradients
        on a batch of training examples

        Arguments:
        X, np array (batch_size, input_features) - input data
        y, np array of int (batch_size) - classes
        """
        for param in self.params().values():
            param.grad = np.zeros_like(param.value)
        
        res = X.copy()
        
        for layer in self.layers:
            res = layer.forward(res)
   
        loss, dres = softmax_with_cross_entropy(res, y)
   
        for layer in reversed(self.layers):
            W = layer.params().get('W')
            if W is not None:
                loss_reg, dW_reg = l2_regularization(W.value, self.reg)
                loss += loss_reg
                W.grad += dW_reg
            dres = layer.backward(dres)
        
        return loss

    def predict(self, X):
        """
        Produces classifier predictions on the set

        Arguments:
          X, np array (test_samples, num_features)

        Returns:
          y_pred, np.array of int (test_samples)
        """
        res = X.copy()
        
        for layer in self.layers:
            res = layer.forward(res)
        
        y_pred = np.argmax(res, axis=1)
        return y_pred

    def params(self):
        result = {}

        for layer_num, layer in enumerate(self.layers):    
            for param_name, param in layer.params().items():
                result[param_name + '_' + str(layer_num)] = param
                
        return result
