dataset=Twitter
model=PostEncoder  # PostEncoder | BiAttEncoder
wb_data_tag=Weibo_src50_conv100_tgt10_v50000
tw_data_tag=Twitter_src35_conv100_tgt10_vs30000_modifiedbm25_notshare
is_copyrnn=true
emb_size=300
seed=23
special='bm25'
rnn=300
lr=0.001

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


model_name=${dataset}_${model}_${lr}_${rnn}rnn_${emb_size}emb_seed${seed}${special}_notshare

nohup \
python -u ../train.py \
    -max_src_len 50 \
    -max_conv_len 100 \
    -word_vec_size ${emb_size} \
    -model_type text \
    -encoder_type ${model}  \
    -decoder_type rnn \
    -enc_layers 2  \
    -dec_layers 1 \
    -rnn_size ${rnn} \
    -rnn_type GRU \
    -global_attention general ${copy_cmd} \
    -save_model saved_models/modifiedbm25/${model_name} \
    -seed ${seed} \
    -data ../processed_data/${data_tag} \
    -batch_size 64 \
    -epochs 15 \
    -optim adam \
    -max_grad_norm 1 \
    -dropout 0.1 \
    -learning_rate ${lr} \
    -learning_rate_decay 0.5 \
    -gpuid 6 \
    > log/train_${model_name}.log &
# -share_embeddings for share_vocab
