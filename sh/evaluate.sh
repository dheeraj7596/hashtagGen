tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/home/xiuwen/hashtagGen/data/modified/withbm25

if [[ $1 =~ 'Twitter' ]]
then
    dataset=${tw_dataset}
    cmd='-filter_chinese 0'
elif [[ $1 =~ 'Weibo' ]]
then
    dataset=${wb_dataset}
    cmd=''
else
    echo 'the model name should contain dataset name'
fi

python -u ../evaluate.py \
    -tgt ${data_prefix}/test_tag.txt \
    -pred prediction/${1/%pt/txt}  \
    >> log/translate_${1%.pt}.log &
