data_tag='Twitter'
dataset=/home/xiuwen/hashtagGen/data/Twitter/repeatsample/


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

full_data_tag=${data_tag}_src${slt}_conv${clt}_tgt${tl}_vs${vs}_bm25


python -u ../preprocess.py \
    -max_shard_size 52428800 \
    -train_src $dataset/trainnew_post.txt \
    -train_conv $dataset/trainnew_conv.txt \
    -train_tgt $dataset/trainnew_tag.txt \
    -valid_src $dataset/validnew_post.txt \
    -valid_conv $dataset/validnew_conv.txt \
    -valid_tgt $dataset/validnew_tag.txt \
    -save_data ../processed_data/${full_data_tag}  \
    -src_vocab_size ${vs} \
    -src_seq_length ${sl} \
    -conversation_seq_length ${cl} \
    -tgt_seq_length ${tl} \
    -src_seq_length_trunc ${slt} \
    -conversation_seq_length_trunc ${clt} \
    -dynamic_dict \
    -share_vocab


