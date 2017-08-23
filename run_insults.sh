#!/usr/bin/env bash

python3 ./train_model.py -t parlai_tasks.insults.agents \
                         -m parlai_agents.insults.insults_agents:InsultsAgent \
                         -mf C:/Users/Dilyara/ParlAI/tmp/insults_2 \
                         --log-every-n-secs 5 \
                         --raw-dataset-path C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data \
                         --batchsize 64 \
                         --display-examples True \
                         --max-train-time 100 \
                         --models cnn_word \
                         --num-epochs 5 \
                         --max_sequence_length 200 \
                         --learning_rate 0.1 \
                         --learning_decay 0.1 \
                         --num_filters 64 \
                         --kernel_sizes "3 4 5" \
                         --regul_coef_conv 0.01 \
                         --regul_coef_dense 0.01 \
                         --pool_sizes "2 2 2" \
                         --dropout_rate 0.5 \
                         --dense_dim 100