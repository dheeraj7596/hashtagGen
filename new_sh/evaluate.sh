tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/data1/xiuwen/twitter/tweet2020/
path=match-using-entity/modifiedbm25
<<<<<<< HEAD

python -u ../evaluate.py \
    -tgt ${data_prefix}${path}/test_tag.txt \
    -pred prediction/${1/%pt/txt}  \
    >> log/translate_${1%.pt}.log &
=======
pred_path=~/tweetAnalyze/OpenNMT-py/new_sh/prediction/modifiedbm25

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
    -tgt ${data_prefix}${path}/test_tag.txt \
    -pred ${pred_path}/${1/%pt/txt} \
    >> ${pred_path}/translate_${1%.pt}.log &
    # -pred prediction/${path}/${1/%pt/txt}  \
    # >> log/${path}/translate_${1%.pt}.log &
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
