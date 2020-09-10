data_tag='Twitter'
dataset=/data1/xiuwen/twitter/tweet2020/
path=match-using-words/withscore

if [[ $data_tag =~ 'Twitter' ]]
then
    vs=30000
    sl=35
    slt=35
    cl=200
    clt=100
    tl=10
elif [[ $data_tag =~ 'Weibo' ]]
then
    vs=50000
    sl=100
    slt=50
    cl=200
    clt=100
    tl=10
else
    echo 'Wrong dataset name!!'
fi


if [[ ! -e ../processed_data ]]
then
    mkdir ../processed_data
fi

full_data_tag=${data_tag}_src${slt}_conv${clt}_tgt${tl}_vs${vs}_notshare


python -u ../preprocess.py \
    -max_shard_size 52428800 \
    -train_src $dataset$path/train_repeat_post.txt \
    -train_conv $dataset$path/train_repeat_conv.txt \
    -train_score $dataset$path/train_repeat_score.txt \
    -train_tgt $dataset$path/train_repeat_tag.txt \
    -valid_src $dataset$path/valid_repeat_post.txt \
    -valid_conv $dataset$path/valid_repeat_conv.txt \
    -valid_score $dataset$path/valid_repeat_score.txt \
    -valid_tgt $dataset$path/valid_repeat_tag.txt \
    -save_data ../new_processed_data/words/${full_data_tag} \
    -src_vocab_size ${vs} \
    -src_seq_length ${sl} \
    -conversation_seq_length ${cl} \
    -tgt_seq_length ${tl} \
    -src_seq_length_trunc ${slt} \
    -conversation_seq_length_trunc ${clt} \
    -dynamic_dict \
    # -share_vocab


