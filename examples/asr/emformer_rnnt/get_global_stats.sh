. /home/gs534/rds/hpc-work/work/espnet/tools/anaconda/etc/profile.d/conda.sh && conda deactivate && conda activate cuda113
export LD_PRELOAD=/lib64/libgsm.so
python global_stats.py --model-typ 'librispeech' --dataset-path /home/gs534/rds/hpc-work/data/Librispeech/
