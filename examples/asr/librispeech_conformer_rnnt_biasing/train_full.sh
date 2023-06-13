. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
expdir="./experiments/librispeech_full960_suffix600_newwarmup"
mkdir -p $expdir
python train.py \
    --exp-dir $expdir \
    --librispeech-path /home/gs534/rds/hpc-work/data/Librispeech/ \
    --global-stats-path ./global_stats_full.json \
    --sp-model-path ./spm_unigram_600_suffix_full.model \
    --epochs 200 \
    --nodes 1 \
    --gpus 1 \
    --biasing \
    --biasing-list ./blists/rareword_f120.txt \
    --droprate 0.0 \
    --maxsize 500 \


n_nodes=1
exp_dir=./experiments_biasing2
srun -p train --cpus-per-task=12 --gpus-per-node=8 --nodes $n_nodes --ntasks-per-node=8  \
  python train.py \
  --exp-dir $exp_dir \
  --librispeech-path /fsx/users/huangruizhe/datasets \
  --global-stats-path ./global_stats_full.json \
  --sp-model-path ./spm_unigram_600_suffix_full.model \
  --epochs 200 \
  --nodes 1 \
  --gpus 8 \
  --biasing \
  --biasing-list ./blists/rareword_f120.txt \
  --droprate 0.0 \
  --maxsize 500

# # standard rnnt only
# n_nodes=1
# exp_dir=./experiments_rnnt1
# srun -p train --cpus-per-task=12 --gpus-per-node=8 --nodes $n_nodes --ntasks-per-node=8  \
#   python train.py \
#   --exp-dir $exp_dir \
#   --librispeech-path /fsx/users/huangruizhe/datasets \
#   --global-stats-path ./global_stats_full.json \
#   --sp-model-path ./spm_unigram_600_suffix_full.model \
#   --epochs 200 \
#   --nodes $n_nodes \
#   --gpus 8


# tensorboard
log_dir=experiments_biasing1
tensorboard dev upload --logdir $log_dir --description "$log_dir"
