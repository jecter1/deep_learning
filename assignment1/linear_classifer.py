import numpy as np
from tqdm import tqdm


def softmax(predictions):
    '''
    Computes probabilities from scores

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output

    Returns:
      probs, np array of the same shape as predictions - 
        probability for every class, 0..1
    '''
    is_batch = predictions.ndim == 2
    max_pred_in_row = np.max(predictions, axis=1)[:, np.newaxis] if is_batch else np.max(predictions)
    pred_norm = predictions - max_pred_in_row
    pred_exp = np.exp(pred_norm)
    sum_pred_exp = np.sum(pred_exp, axis=1)[:, np.newaxis] if is_batch else np.sum(pred_exp)
    probs = pred_exp / sum_pred_exp
    return probs


def cross_entropy_loss(probs, target_index):
    '''
    Computes cross-entropy loss

    Arguments:
      probs, np array, shape is either (N) or (batch_size, N) -
        probabilities for every class
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss: single value
    '''
    is_batch = probs.ndim == 2
    target_probs = probs[np.arange(target_index.size), target_index] if is_batch else probs[target_index]
    loss = -np.mean(np.log(target_probs))
    return loss


def softmax_with_cross_entropy(predictions, target_index):
    '''
    Computes softmax and cross-entropy loss for model predictions,
    including the gradient

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss, single value - cross-entropy loss
      dprediction, np array same shape as predictions - gradient of predictions by loss value
    '''
    probs = softmax(predictions)
    loss = cross_entropy_loss(probs, target_index)
    
    is_batch = probs.ndim == 2
    dprediction = probs
    
    if is_batch:
        dprediction[np.arange(target_index.size), target_index] -= 1
        dprediction /= target_index.size
    else:
        dprediction[target_index] -= 1
        
    return loss, dprediction


def l2_regularization(W, reg_strength):
    '''
    Computes L2 regularization loss on weights and its gradient

    Arguments:
      W, np array - weights
      reg_strength - float value

    Returns:
      loss, single value - l2 regularization loss
      gradient, np.array same shape as W - gradient of weight by l2 loss
    '''
    loss = reg_strength * np.sum(W ** 2)
    grad = 2 * reg_strength * W
    return loss, grad
    

def linear_softmax(X, W, target_index):
    '''
    Performs linear classification and returns loss and gradient over W

    Arguments:
      X, np array, shape (num_batch, num_features) - batch of images
      W, np array, shape (num_features, classes) - weights
      target_index, np array, shape (num_batch) - index of target classes

    Returns:
      loss, single value - cross-entropy loss
      gradient, np.array same shape as W - gradient of weight by loss

    '''
    predictions = np.dot(X, W)
    loss, dprediction = softmax_with_cross_entropy(predictions, target_index)
    dW = np.dot(X.T, dprediction)
    return loss, dW


class LinearSoftmaxClassifier():
    def __init__(self):
        self.W = None

    def fit(self, X, y, batch_size=100, learning_rate=1e-7, reg=1e-5,
            epochs=1):
        '''
        Trains linear classifier
        
        Arguments:
          X, np array (num_samples, num_features) - training data
          y, np array of int (num_samples) - labels
          batch_size, int - batch size to use
          learning_rate, float - learning rate for gradient descent
          reg, float - L2 regularization strength
          epochs, int - number of epochs
        '''

        num_train = X.shape[0]
        num_features = X.shape[1]
        num_classes = np.max(y)+1
        if self.W is None:
            self.W = 0.001 * np.random.randn(num_features, num_classes)

        loss_history = []
        for epoch in tqdm(range(epochs)):
            shuffled_indices = np.arange(num_train)
            np.random.shuffle(shuffled_indices)
            sections = np.arange(batch_size, num_train, batch_size)
            batches_indices = np.array_split(shuffled_indices, sections)

            loss = 0
            cnt = 0
            for batch_indices in batches_indices:
                batch_X = X[batch_indices]
                batch_y = y[batch_indices]
                loss1, dW1 = linear_softmax(batch_X, self.W, batch_y)
                loss2, dW2 = l2_regularization(self.W, reg)
                loss += loss1 + loss2
                dW = dW1 + dW2
                self.W -= learning_rate * dW
                cnt += 1
                
            loss_history.append(loss / cnt)

        return loss_history

    def predict(self, X):
        '''
        Produces classifier predictions on the set
       
        Arguments:
          X, np array (test_samples, num_features)

        Returns:
          y_pred, np.array of int (test_samples)
        '''
        y = np.dot(X, self.W)
        y_pred = np.argmax(y, axis=1)
        return y_pred



                
                                                          

            

                
