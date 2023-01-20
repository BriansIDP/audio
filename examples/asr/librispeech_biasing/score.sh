dir=experiments/librispeech_clean100_suffix600_tcpgen200_deep_sche30_drop0.1_smooth/decode_test_clean_b10
/home/gs534/rds/hpc-work/work/espnet-mm/tools/sctk-2.4.10/bin/sclite -r ${dir}/ref.trn.txt trn -h ${dir}/hyp.trn.txt trn -i rm -o all stdout > ${dir}/result.wrd.txt
