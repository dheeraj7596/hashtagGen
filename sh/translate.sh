tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/data1/xiuwen/twitter/tweet2018/match-using-entity/modifiedbm25
path=match-using-entity/modifiedbm25
if [[ $1 =~ 'Twitter' ]]
then
    dataset=${tw_dataset}
elif [[ $1 =~ 'Weibo' ]]
then
    dataset=${wb_dataset}
else
    echo 'the model name should contain dataset name'
fi


nohup \
python -u ../translate.py \
    -model saved_models/${path}/$1  \
    -output prediction/${path}/${1/%pt/txt} \
    -src ${data_prefix}/test_post.txt \
    -conversation ${data_prefix}/test_conv.txt \
    -beam_size 30 \
    -max_length 10 \
    -n_best 20 \
    -batch_size 64 \
    -gpu 2 > log/${path}/translate_${1%.pt}.log  \
&& python -u ../evaluate.py \
    -tgt ${data_prefix}/test_tag.txt \
    -pred prediction/${path}/${1/%pt/txt}  \
    >> log/${path}/translate_${1%.pt}.log &
