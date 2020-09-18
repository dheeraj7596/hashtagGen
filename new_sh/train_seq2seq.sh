dataset=Twitter
model=rnn
wb_data_tag=Weibo_src50_conv100_tgt10_v50000
tw_data_tag=Twitter_src35_conv100_tgt10_v30000
is_copyrnn=false
emb_size=200
seed=23
special=''

if [[ $dataset =~ 'Weibo' ]]
then
    data_tag=$wb_data_tag
elif [[ $dataset =~ 'Twitter' ]]
then
    data_tag=$tw_data_tag
else
    echo 'Wrong dataset name'
fi

if $is_copyrnn
then
    copy_cmd='-copy_attn -reuse_copy_attn'
    model_tag='copyrnn'
else
    copy_tag=''
    model_tag='rnn'
fi


model_name=${dataset}_${model}_${model_tag}_${emb_size}emb_seed${seed}${special}

onmt_train \
    -word_vec_size ${emb_size} \
    -share_embeddings \
    -model_type text \
    -encoder_type rnn  \
    -decoder_type rnn \
    -enc_layers 2  \
    -dec_layers 1 \
    -rnn_size 300 \
    -rnn_type GRU \
    -save_model saved_models/${model_name} \
    -seed ${seed} \
    -data ../processed_data/${data_tag} \
    -batch_size 64 \
    -train_steps 3000 \
    -optim adam \
    -max_grad_norm 1 \
    -dropout 0.1 \
    -learning_rate 0.001 \
    -learning_rate_decay 0.5 \
    -gpu_ranks 0
    > log/train_${model_name}.log &
