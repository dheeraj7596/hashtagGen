data_tag='Twitter'
dataset=/data4/dheeraj/hashtag/notinline/${data_tag}


if [[ $dataset =~ 'Twitter' ]]
then
    vs=30000
    sl=35
    slt=35
    cl=200
    clt=100
    tl=10
elif [[ $dataset =~ 'Weibo' ]]
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

full_data_tag=${data_tag}_src${slt}_conv${clt}_tgt${tl}_v${vs}


onmt_preprocess \
    -shard_size 52428800 \
    -train_src $dataset/train_post.txt \
    -train_tgt $dataset/train_tag.txt \
    -valid_src $dataset/valid_post.txt \
    -valid_tgt $dataset/valid_tag.txt \
    -save_data ../processed_data/${full_data_tag}  \
    -src_vocab_size ${vs} \
    -src_seq_length ${sl} \
    -tgt_seq_length ${tl} \
    -src_seq_length_trunc ${slt} \
    -dynamic_dict \
    -share_vocab


