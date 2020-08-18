tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/data1/xiuwen/twitter/match-using-words/tweet-conv-8days-no-time-usingwords/news/
path=match-using-words

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

python3.6 -u ../evaluate.py \
    -tgt ${data_prefix}/test_tag.txt \
    -pred ./prediction/${path}/$1 \
    ${cmd}
