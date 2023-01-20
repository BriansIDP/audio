. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_clean100_suffix600_tcpgen200_deep_sche30_drop0.1_smooth"
decode_dir=$expdir/decode_test_clean_b10
mkdir -p $decode_dir
ckptpath=$expdir/checkpoints/epoch=89-step=175770.ckpt  
python eval.py \
    --checkpoint-path $ckptpath \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --sp-model-path ./spm_unigram_600_100suffix.model \
    --expdir $decode_dir \
    --use-cuda \
    --biasing true \
    --biasinglist ./blists/all_rare_words.txt \
    --droprate 0.0 \
    --maxsize 1000 \
