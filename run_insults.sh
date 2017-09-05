#!/usr/bin/env bash

python3 utils/train_model.py -t deeppavlov.tasks.insults.agents:FullTeacher \
                             -m deeppavlov.agents.insults.insults_agents:OneEpochAgent \
                             --model_file C:/Users/Dilyara/ParlAI/tmp/insults_log_reg/log_reg \
                             -dt train:ordered \
                             --model_name log_reg \
                             --log-every-n-secs 10 \
                             --log-every-n-epochs 1 \
                             --validation-every-n-epochs 2 \
                             --raw-dataset-path C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data \
                             --batchsize 64 \
                             --display-examples False \
                             --max-train-time -1 \
                             --num-epochs 1

python3 ./utils/train_model.py -t deeppavlov.tasks.insults.agents:FullTeacher \
                               -m deeppavlov.agents.insults.insults_agents:OneEpochAgent \
                               --model_file C:/Users/Dilyara/ParlAI/tmp/insults_svc/svc \
                               -dt train:ordered \
                               --model_name svc \
                               --log-every-n-secs 10 \
                               --log-every-n-epochs 1 \
                               --validation-every-n-epochs 2 \
                               --raw-dataset-path C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data \
                               --batchsize 64 \
                               --display-examples False \
                               --max-train-time -1 \
                               --num-epochs 1

python utils/train_model.py -t deeppavlov.tasks.insults.agents \
                            -m deeppavlov.agents.insults.insults_agents:InsultsAgent \
                            -mf C:/Users/Dilyara/ParlAI/tmp/insults_cnn_word/cnn_word \
                            -dt train:ordered \
                            --model_name cnn_word  \
                            --log-every-n-secs 30 \
                            --raw-dataset-path C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data \
                            --batchsize 64 \
                            --display-examples False \
                            --max-train-time -1 \
                            --num-epochs 1 \
                            --max_sequence_length 100 \
                            --learning_rate 0.01 \
                            --learning_decay 0.1 \
                            --num_filters 128 \
                            --kernel_sizes "3 4 5" \
                            --regul_coef_conv 0.001 \
                            --regul_coef_dense 0.001 \
                            --pool_sizes "2 2 2"  \
                            --dropout_rate 0.5 \
                            --dense_dim 100 \
                            --fasttext_model C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data/reddit_fasttext_model.bin \
                            --fasttext_embeddings_dict C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data/emb_dict.emb \
                            --cross-validation-splits-count 3


python3 ./utils/train_model.py -t deeppavlov.tasks.insults.agents:FullTeacher \
                               -m deeppavlov.agents.insults.insults_agents:EnsembleInsultsAgent \
                               -mf C:/Users/Dilyara/ParlAI/tmp/insults_ensemble \
                               --model_files C:/Users/Dilyara/ParlAI/tmp/insults_cnn_word/cnn_word_0 \
                                             C:/Users/Dilyara/ParlAI/tmp/insults_cnn_word/cnn_word_1 \
                                             C:/Users/Dilyara/ParlAI/tmp/insults_cnn_word/cnn_word_2 \
                                             C:/Users/Dilyara/ParlAI/tmp/insults_log_reg/log_reg \
                                             C:/Users/Dilyara/ParlAI/tmp/insults_svc/svc \
                               --model_names cnn_word cnn_word cnn_word log_reg svc \
                               --model_coefs 0.1 0.1 0.1 0.1 0.6 \
                               --datatype test \
                               --batchsize 64 \
                               --display-examples False \
                               --raw-dataset-path C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data \
                               --max-train-time -1 \
                               --num-epochs 1 \
                               --max_sequence_length 100 \
                               --learning_rate 0.01 \
                               --learning_decay 0.1 \
                               --num_filters 64 \
                               --kernel_sizes "3 4 5" \
                               --regul_coef_conv 0.001 \
                               --regul_coef_dense 0.001 \
                               --pool_sizes "2 2 2"  \
                               --dropout_rate 0.5 \
                               --dense_dim 100 \
                               --fasttext_model C:/Users/Dilyara/Documents/DataScience/Insults_kaggle/data/reddit_fasttext_model.bin
