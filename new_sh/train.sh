dataset=Twitter
model=BiAttEncoder  # PostEncoder | BiAttEncoder
wb_data_tag=Weibo_src50_conv100_tgt10_v50000
<<<<<<< HEAD
tw_data_tag=Twitter_src35_conv100_tgt10_vs30000_notshare
is_copyrnn=false
emb_size=300
seed=23
special='bm25'
rnn=400
lr=0.0006
=======
tw_data_tag=Twitter_src35_conv100_tgt10_vs30000_nonshare
path=incorpscore
is_copyrnn=false
emb_size=300
seed=23
special='raw_news'
rnn=400
lr=0.0008
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41

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


<<<<<<< HEAD
model_name=${dataset}_${model}_${lr}_${rnn}rnn_${emb_size}emb_seed${seed}${special}_notshare
=======
model_name=${dataset}_${model}_${lr}_${rnn}rnn_${emb_size}emb_seed${seed}_notshare
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41

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
<<<<<<< HEAD
    -save_model saved_models/words/${model_name} \
    -seed ${seed} \
    -data ../new_processed_data/words/${data_tag} \
=======
    -save_model ./saved_models/${path}/${model_name} \
    -seed ${seed} \
    -data ../new_processed_data/${path}/${data_tag} \
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
    -batch_size 64 \
    -epochs 15 \
    -optim adam \
    -max_grad_norm 1 \
    -dropout 0.1 \
    -learning_rate ${lr} \
    -learning_rate_decay 0.5 \
<<<<<<< HEAD
    -gpuid 1 \
    > log/words/train_${model_name}.log &
# -share_embeddings for share_vocab
=======
    -gpuid 5 \
    > ./log/${path}/train_${model_name}.log &
# -share_embeddings for share_vocab

>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
