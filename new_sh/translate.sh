tw_dataset=Twitter
wb_dataset=Weibo
<<<<<<< HEAD
data_prefix=/data1/xiuwen/twitter/tweet2020/
path=match-using-words/withscore
=======
data_prefix=/data1/xiuwen/twitter/tweet2018/
path=match-using-entity/modifiedbm25
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
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
<<<<<<< HEAD
    -model saved_models/words/$1  \
    -output prediction/${1/%pt/txt} \
    -src ${data_prefix}${path}/test_post.txt \
    -conversation ${data_prefix}${path}/test_conv.txt \
    -score ${data_prefix}${path}/test_score.txt \
=======
    -model saved_models/${path}/$1  \
    -output prediction/${path}/${1/%pt/txt} \
    -src ${data_prefix}${path}/test_post.txt \
    -conversation ${data_prefix}${path}/test_conv.txt \
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
    -beam_size 30 \
    -max_length 10 \
    -n_best 20 \
    -batch_size 64 \
<<<<<<< HEAD
    -gpu 0 > log/translate_${1%.pt}.log  \
&& python -u ../evaluate.py \
    -tgt ${data_prefix}${path}/test_tag.txt \
    -pred prediction/${1/%pt/txt}  \
    >> log/translate_${1%.pt}.log &
=======
    -gpu 2 > log/${path}/translate_${1%.pt}.log  \
&& python -u ../evaluate.py \
    -tgt ${data_prefix}${path}/test_tag.txt \
    -pred prediction/${path}/${1/%pt/txt}  \
    >> log/${path}/translate_${1%.pt}.log &
>>>>>>> 22aa72c86f916fe03c6b6134eb6b97032e77dd41
