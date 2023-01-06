. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_clean100_suffix600_tcpgen200_sche30_drop0.1_smooth"
mkdir -p $expdir
python train.py \
    --exp-dir $expdir \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --global-stats-path ./global_stats_100.json \
    --sp-model-path ./spm_unigram_600_100suffix.model \
    --biasing true \
    --biasinglist ./blists/rareword_f15.txt \
    --droprate 0.1 \
    --maxsize 200 \
    --epochs 90 \
    --resume $expdir/checkpoints/epoch=50-step=99603.ckpt \
