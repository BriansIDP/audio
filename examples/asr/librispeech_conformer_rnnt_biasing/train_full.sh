. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_full960_suffix600_newsetup"
mkdir -p $expdir
python train.py \
    --exp-dir $expdir \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --global-stats-path ./global_stats_full.json \
    --sp-model-path ./spm_unigram_600_suffix_full.model \
    --epochs 200 \
    --resume experiments/librispeech_full960_suffix600_standard/checkpoints/epoch\=169-step\=621609.ckpt \
    --biasing \
    --biasing-list ./blists/rareword_f120.txt \
    --droprate 0.0 \
    --maxsize 500 \
    # --resume experiments/librispeech_full960_suffix600/checkpoints/epoch=24-step=59600.ckpt \
