from typing import Any
import yaml
import pathlib


class config_dict(dict):
    # https://stackoverflow.com/questions/2328235/pythonextend-the-dict-class
    def __getitem__(self, __key: Any) -> Any:
        return super().__getitem__(__key)
    

default_config = {
    # model:
    "spm_vocab_size": 600,

    # # Xiaohui's
    # "rnnt_config": {
    #     "input_dim": 80,
    #     "encoding_dim": 512,
    #     "time_reduction_stride": 4,
    #     "conformer_input_dim": 512,
    #     "conformer_ffn_dim": 2048,
    #     "conformer_num_layers": 12,
    #     "conformer_num_heads": 8,
    #     "conformer_depthwise_conv_kernel_size": 31,
    #     "conformer_dropout": 0.1,
    #     "num_symbols": 1024,
    #     "symbol_embedding_dim": 1024,
    #     "num_lstm_layers": 2,
    #     "lstm_hidden_dim": 512,
    #     "lstm_layer_norm": True,
    #     "lstm_layer_norm_epsilon": 1e-5,
    #     "lstm_dropout": 0.3,
    #     "joiner_activation": "tanh",
    # },

    # Default
    "rnnt_config": {
        "input_dim": 80,
        "encoding_dim": 512,
        "time_reduction_stride": 4,
        "conformer_input_dim": 512,
        "conformer_ffn_dim": 2048,
        "conformer_num_layers": 12,
        "conformer_num_heads": 8,
        "conformer_depthwise_conv_kernel_size": 31,
        "conformer_dropout": 0.1,
        "num_symbols": 601,
        "symbol_embedding_dim": 1024,
        "num_lstm_layers": 2,
        "lstm_hidden_dim": 512,
        "lstm_layer_norm": True,
        "lstm_layer_norm_epsilon": 1e-5,
        "lstm_dropout": 0.3,
        "joiner_activation": "tanh",
        "biasing_attndim": 256,
        "deepbiasing": True,
        "tcpgen_start_epoch": 0,
        "deepbiasing_average": False,
    },

    # training:
    "training_config": {
        "seed": 1,
        "save_top_k": 5,
        "checkpoint_path": None,
        "exp_dir": "./exp",
        "nodes": 1,
        "gpus": 1,
        "epochs": 200,
        "gradient_clip_val": 10.0,
    },
    
    "optim_config": {
        "warmup_steps": 80000,
        "force_anneal_step": 320000, 
        "anneal_factor": 0.99999,
        "lr": 8e-4,
        "batch_size": 20,
        "max_tokens": 3600,
        "train_num_buckets": 50,
        "reduction": "sum",
        "weight_decay": 0,
    },
    # "optim_config": {
    #     "warmup_steps": 80,
    #     "lr": 5,
    #     "batch_size": 25,
    #     "max_tokens": 5400,
    #     "train_num_buckets": 50,
    #     "reduction": "sum",
    #     "weight_decay": 0,
    # },
    # # Xiaohui's:
    # "specaug_conf": {
    #     "new_spec_aug_api": False,
    #     "n_time_masks": 10,
    #     "time_mask_param": 30,
    #     "p": 0.2,
    #     "n_freq_masks": 2,
    #     "freq_mask_param": 27,
    #     "iid_masks": True,
    #     "zero_masking": True,
    # },

    # Default:
    "specaug_conf": {
        "new_spec_aug_api": False,
        "n_time_masks": 2,
        "time_mask_param": 100,
        "p": 0.2,
        "n_freq_masks": 2,
        "freq_mask_param": 27,
        "iid_masks": True,
        "zero_masking": True,
    },

    # # Espnet's:
    # "specaug_conf": {
    #     "new_spec_aug_api": False,
    #     "n_time_masks": 0,
    #     "time_mask_param": 40,
    #     "p": 0.2,
    #     "n_freq_masks": 2,
    #     "freq_mask_param": 30,
    #     "iid_masks": True,
    #     "zero_masking": True,
    # },

    # # inference:
    # "inference_config": {
    #     "temperature": 1.0,
    #     "step_max_tokens": 100,
    #     "beam_width": 20,  # espnet: 10  # https://github.com/espnet/espnet/blob/master/egs2/librispeech/asr1/conf/tuning/transducer/decode.yaml
    # },
}


# https://python.land/data-processing/python-yaml
def load_config(config_file):
    if config_file is None or not pathlib.Path(config_file).exists():
        return default_config
    
    with open(config_file, 'r') as fin:
        config = yaml.safe_load(fin)
    return config


def my_stringify_dict(d):
    str_d = dict()

    for k, v in d.items():
        if type(v) is pathlib.Path:
            str_d[k] = str(v.absolute())
        elif type(v) is dict:
            str_d[k] = my_stringify_dict(v)
        else:
            str_d[k] = v
    return str_d


def save_config(config, config_file):
    _str_config = my_stringify_dict(config)

    if not pathlib.Path(config_file).exists():
        with open(config_file, 'w') as fout:
            yaml.dump(_str_config, fout)
    else:
        print(f"Skipped saving config file. Existed: {config_file}")


def update_config(config, args):
    if args.checkpoint_path is not None:
        config["training_config"]["checkpoint_path"] = args.checkpoint_path
    if args.exp_dir is not None:
        config["training_config"]["exp_dir"] = args.exp_dir
    if args.nodes is not None:
        config["training_config"]["nodes"] = args.nodes
    if args.gpus is not None:
        config["training_config"]["gpus"] = args.gpus
    if args.epochs is not None:
        config["training_config"]["epochs"] = args.epochs
    if args.resume is not None:
        config["training_config"]["resume"] = args.resume
    return config
