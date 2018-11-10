import tensorflow as tf
# from itertools import repeat



def get_initializer(init_op, seed=None, init_weight=None):
    """
	Create an initializer [Uniform distribution | Xavier(Normal | Uniform)]. 
	init_weight is only for uniform.

	Args:
		init_op: Type of weight initializer.
		seed: An integer used to seed the random generator.
		init_weight: Scalar (tensor) which will be used to determine 
			the lower and upper bounds of the the random value
			
	Returns:
		Returns an initializer.

	Raises:
		ValueError: Raises an exception if the initializer is not in the listed specifiers.
	"""	
    if init_op == "uniform": # Uniform distribution.
        assert init_weight
        return tf.random_uniform_initializer(-init_weight, init_weight, seed=seed)
    elif init_op == "glorot_normal": # Xavier normal initializer.
        return tf.contrib.keras.initializers.glorot_normal(seed=seed)
    elif init_op == "glorot_uniform": # Xavier uniform initializer.
        return tf.contrib.keras.initializers.glorot_uniform(seed=seed)
    else:
        raise ValueError("Unknown init_op %s" % init_op)


def create_embbeding(vocab_size, embed_size, dtype=tf.float32, scope=None):
    """
	Create embedding matrix for both encoder and decoder.
	
	Args:
		vocab_size: Size of the embedding vector/matrix.
		embed_size: Size of the embedding vector/matrix.
		scope: context of the "embeddings" variable
			
	Returns:
		Returns an embedding matrix (dense vector representations of the characters).

	Raises:
		None
	"""	
    with tf.variable_scope(scope or "embeddings", dtype=dtype):
        embedding = tf.get_variable("embedding", [vocab_size, embed_size], dtype)

    return embedding


def _single_cell(num_units, keep_prob, device_str=None):
    """
	Create an instance of a single RNN cell.	
	
	Args:
		num_units: An integer representing the number of units in the GRU (Gated recurrent unit) cell.
		keep_prob: Input keep probability which will add no input dropout if constant and 1.
		device_str: A device string or function, for passing to tf.device (Device to use for created ops)
			
	Returns:
		Returns a cell (object) with a single scalar output.

	Raises:
		None
	"""	
    single_cell = tf.contrib.rnn.GRUCell(num_units) # An instance of RNN cell (RNNCell)

    if keep_prob < 1.0:
        single_cell = tf.contrib.rnn.DropoutWrapper(cell=single_cell, input_keep_prob=keep_prob)

    # Device Wrapper: tf.device
    if device_str:
        single_cell = tf.contrib.rnn.DeviceWrapper(single_cell, device_str) 

    return single_cell


def create_rnn_cell(num_units, num_layers, keep_prob):
    """
	Create multi-layer RNN cell.
	
	Args:
		num_units: An integer representing the number of units in the GRU (Gated recurrent unit) cell.
		num_layers: An integer representing the number of layers in the network.
		keep_prob: Input keep probability which will add no input dropout if constant and 1.
			
	Returns:
		Returns a RNN.

	Raises:
		None
	"""	
    cell_list = []
    for _ in range(num_layers):
        single_cell = _single_cell(num_units=num_units, keep_prob=keep_prob)
        cell_list.append(single_cell)

    if len(cell_list) == 1:  # Single layer.
        return cell_list[0]
    else:  # Multi layers
        return tf.contrib.rnn.MultiRNNCell(cell_list)


def gradient_clip(gradients, max_gradient_norm):
    """
	Clipping gradients of a model which is capping them to a Threshold value to prevent the gradients from getting too large
	
	Args:
		gradients: Gradient that is needed in the calculation of the weights.
		max_gradient_norm: An integer if exceeded will scale the weight matrix by a factor that reduces the norm to it
			
	Returns:
		Returns clipped gradients and gradiant normalization summary.

	Raises:
		None
	"""	
    clipped_gradients, gradient_norm = tf.clip_by_global_norm(gradients, max_gradient_norm)
    gradient_norm_summary = [tf.summary.scalar("grad_norm", gradient_norm)]
    gradient_norm_summary.append(
        tf.summary.scalar("clipped_gradient", tf.global_norm(clipped_gradients)))

    return clipped_gradients, gradient_norm_summary

