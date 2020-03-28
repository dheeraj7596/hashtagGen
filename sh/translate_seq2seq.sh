tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/data4/dheeraj/hashtag/notinline/

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
onmt_translate \
    -model saved_models/$1  \
    -output prediction/${1/%pt/txt} \
    -src ${data_prefix}/${dataset}/test_post.txt \
    -beam_size 30 \
    -max_length 10 \
    -n_best 1 \
    -batch_size 64 \
    -gpu 0 > log/translate_${1%.pt}.log  \
&& python3.6 -u ../evaluate.py \
    -tgt ${data_prefix}/${dataset}/test_tag.txt \
    -pred prediction/${1/%pt/txt}  \
    >> log/translate_${1%.pt}.log &

onmt_translate \
    -model saved_models/$1  \
    -output prediction/${1/%pt/txt} \
    -src ${data_prefix}/${dataset}/test_post.txt \
    -beam_size 30 \
    -max_length 10 \
    -n_best 1 \
    -batch_size 64 \
    -gpu 0 \
&& python3.6 -u ../evaluate.py \
    -tgt ${data_prefix}/${dataset}/test_tag.txt \
    -pred prediction/${1/%pt/txt}
