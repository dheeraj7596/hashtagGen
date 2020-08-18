tw_dataset=Twitter
wb_dataset=Weibo

python -u ../evaluate.py \
    -tgt  /home/xiuwen/hashtagGen/data/modified/withoutbm25/test_tag.txt \
    -pred ./prediction/Twitter_BiAttEncoder_0.001_300rnn_200emb_seed23bm25_notshare_acc_52.82_ppl_30.91_e10.txt \
    >> log/translate_newcode.log &
