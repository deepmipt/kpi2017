#!/usr/bin/env bash

# Build custom kernels.
#TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')

# Linux (pip)
#g++ -std=c++11 -shared coref_kernels.cc -o coref_kernels.so -I $TF_INC -fPIC -D_GLIBCXX_USE_CXX11_ABI=0

# Linux (build from source)
#g++ -std=c++11 -shared coref_kernels.cc -o coref_kernels.so -I $TF_INC -fPIC

# Mac
#g++ -std=c++11 -shared coref_kernels.cc -o coref_kernels.so -I $TF_INC -fPIC -D_GLIBCXX_USE_CXX11_ABI=0  -undefined dynamic_lookup

#parlai.agents.repeat_label.repeat_label
export CUDA_VISIBLE_DEVICES=1; python3 ./utils/train_model.py -t deeppavlov.tasks.coreference.agents:BaseTeacher \
                         -m deeppavlov.agents.coreference.agents:CoreferenceAgent \
                         -mf ./build/coreference/ \
		         --language russian \
			 --name main \
                         --rep_iter 100 \
			 --pretrained_model False \
                         --split 0.2 \
                         --random-seed None \
                         -dt train:ordered \
                         --batchsize 1 \
                         --display-examples True \
                         --max-train-time -1 \
                         --validation-every-n-epochs 10 \
                         --log-every-n-epochs 10 \
                         --log-every-n-secs -1 \
                         --chosen-metric conll-F-1 \

