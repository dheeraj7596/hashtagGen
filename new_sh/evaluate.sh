tw_dataset=Twitter
wb_dataset=Weibo
data_prefix=/data1/xiuwen/twitter/tweet2020/
path=match-using-entity/modifiedbm25

python -u ../evaluate.py \
    -tgt ${data_prefix}${path}/test_tag.txt \
    -pred prediction/${1/%pt/txt}  \
    >> log/translate_${1%.pt}.log &
