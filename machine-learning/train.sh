#!/bin/sh
python3 generate_training_set.py && \
rm -rf output && python3 neural_network.py && \
$(which tensorflowjs_converter) --input_format=tf_saved_model --saved_model_tags=serve ./output ../model