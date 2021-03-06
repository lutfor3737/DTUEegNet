### This file implements training operations
# calcLoss       - to calculate the cross-entropy
# calcAccuracy   - to calculate the accuracy
# trainNetwork   - to backpropagate the error through the network (1 training step)
import tensorflow as tf
import numpy as np

# 1) Define cross entropy loss
def calcLoss(predictions, labels):
    with tf.variable_scope("Loss"):
        #One hot labels
        labels_resized = tf.reshape(labels,[tf.size(labels)])
        #Calculate entropy
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels_resized, logits=predictions)
   	    # Average over batch samples
   	    # Averaging makes the loss invariant to batch size, which is very nice.
        cross_entropy = tf.reduce_mean(cross_entropy)
        return cross_entropy

# 2) Define accuracy
def calcAccuracy(predictions, labels):
    with tf.variable_scope("Accuracy"):
        # Reshape
        labels_resized = tf.reshape(labels,[tf.size(labels)])
        # Calculate the number of pixels with the same value in pred and lab
        predictions = tf.cast(predictions, tf.int32)
        equal_elements = tf.equal(predictions, labels_resized)
        num_equal_elements = tf.reduce_sum(tf.cast(equal_elements, tf.int32))
        #Calculate global accuracy as fraction of matching pixels
        accuracy = num_equal_elements/tf.size(labels_resized)
        labels_size = tf.shape(labels_resized)
        predictions_size = tf.shape(predictions)
        return accuracy

# 3) Define the training op
def trainNetwork(loss):
    with tf.variable_scope("TrainOp"):
        #Add bn to training ops
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            optimizer = tf.train.AdamOptimizer(learning_rate=0.0001)
            # Computing our gradients
            grads_and_vars = optimizer.compute_gradients(loss)
            # Applying the gradients
            train_op = optimizer.apply_gradients(grads_and_vars)
            return train_op