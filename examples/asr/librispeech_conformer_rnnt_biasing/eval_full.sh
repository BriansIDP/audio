. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_full960_suffix600_standard"
decode_dir=$expdir/decode_test_clean_b10_cuda
mkdir -p $decode_dir
ckptpath=$expdir/checkpoints/epoch=169-step=621609.ckpt
python eval.py \
    --checkpoint-path $ckptpath \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --sp-model-path ./spm_unigram_600_suffix_full.model \
    --global-stats-path ./global_stats_full.json \
    --expdir $decode_dir \
    --use-cuda \
    # --biasing \
    # --biasing-list ./blists/all_rare_words.txt \
    # --droprate 0.0 \
    # --maxsize 1000 \
