import codecs
import json
import os
import tensorflow as tf

# logger = logging.getLogger(__name__) check correctness


class HyParams:
    def __init__(self, model_dir):
	"""
	Hyperparameter class.

	Args:
		model_dir: Location of the model.
		
	Returns:
		None

	Raises:
		None
	"""
        self.hyparams = self.load_hyparams(model_dir)

    @staticmethod
    def load_hyparams(model_dir):
        """Load hyperparameters from an existing directory.

		Args:
			model_dir: Location of the model.
			
		Returns:
			Hyperparameters loaded if no errors are raised and None if a ValueError is raised.

		Raises:
			ValueError: Raises an exception if the hyperparameter file was not read correctly.
		"""
        hyparams_file = os.path.join(model_dir, "hyparams.json")
        if tf.gfile.Exists(hyparams_file):
            print("# Loading hyparams from {} ...".format(hyparams_file))
			#logger.info("[+] Loading hyparams from {} ...".format(hyparams_file))(
            with codecs.getreader("utf-8")(tf.gfile.GFile(hyparams_file, "rb")) as hpf:
                try:
                    hyparams_values = json.load(hpf)
                    hparams = tf.contrib.training.HParams(**hyparams_values)
                except ValueError:
                    print("[-] Error loading data from hyparams.json.")
					#logger.error("[-] Error loading data from hyparams.json.")
                    return None
            return hyparams
        else:
            return None