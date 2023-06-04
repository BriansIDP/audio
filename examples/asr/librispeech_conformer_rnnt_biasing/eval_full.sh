. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_full960_suffix600_noam_highlr"
decode_dir=$expdir/decode_test_clean_b10_cuda
mkdir -p $decode_dir
ckptpath=$expdir/checkpoints/epoch=75-step=178220.ckpt
python eval.py \
    --checkpoint-path $ckptpath \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --sp-model-path ./spm_unigram_600_suffix_full.model \
    --global-stats-path ./global_stats_full.json \
    --expdir $decode_dir \
    --use-cuda \
    --biasing \
    --biasing-list ./blists/all_rare_words.txt \
    --droprate 0.0 \
    --maxsize 1000 \


ckpt='/fsx/users/huangruizhe/audio_guangzhi/examples/asr/librispeech_conformer_rnnt_biasing/experiments_biasing1/checkpoints/epoch=143-step=526752.ckpt'
exp_dir=./experiments_biasing1
srun -p scavenge --cpus-per-task=12 --gpus-per-node=1 --nodes 1 --ntasks-per-node=1 \
  python eval.py \
  --librispeech-path /fsx/users/huangruizhe/datasets \
  --global-stats-path ./global_stats_full.json \
  --sp-model-path ./spm_unigram_600_suffix_full.model \
  --use-cuda \
  --train-config $exp_dir/train_config.yaml \
  --checkpoint-path $ckpt \
  --expdir $exp_dir \
  --biasing \
  --biasing-list ./blists/all_rare_words.txt \
  --droprate 0.0 \
  --maxsize 1000 