import os
import pathlib
from argparse import ArgumentParser

import sentencepiece as spm

from lightning import ConformerRNNTModule
from pytorch_lightning import seed_everything, Trainer
from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint, Callback
from pytorch_lightning.strategies import DDPStrategy
from transforms import get_data_module
from config import load_config, update_config, save_config


class MyTrainStartCallback(Callback):
    def on_train_start(self, trainer, pl_module):
        if pl_module.global_rank == 0:
            print("Training is starting ...")

            print("----------------- Training Configuration -------------------")
            print(pl_module.config)
            print("------------------------------------------------------------")

            config_file = pathlib.Path(pl_module.config["training_config"]["exp_dir"]) / "train_config.yaml"
            config_file = config_file.absolute()
            print(f"Saving config to: {config_file}")
            save_config(pl_module.config, config_file)
    
    def on_train_epoch_start(self, trainer, pl_module):
        # https://github.com/Lightning-AI/lightning/discussions/13060
        
        # print(f"pl_module.current_epoch = {pl_module.current_epoch}")
        trainer.datamodule.set_epoch(trainer.current_epoch)


def run_train(args, config):
    seed_everything(config["training_config"]["seed"])
    checkpoint_dir = pathlib.Path(config["training_config"]["exp_dir"]) / "checkpoints"
    checkpoint = ModelCheckpoint(
        checkpoint_dir,
        monitor="Losses/val_loss",
        mode="min",
        save_top_k=config["training_config"]["save_top_k"],
        save_weights_only=False,
        verbose=True,
        every_n_epochs=10,
    )
    train_checkpoint = ModelCheckpoint(
        checkpoint_dir,
        monitor="Losses/train_loss",
        mode="min",
        save_top_k=config["training_config"]["save_top_k"],
        save_weights_only=False,
        verbose=True,
    )
    lr_monitor = LearningRateMonitor(logging_interval="step")
    callbacks = [
        checkpoint,
        train_checkpoint,
        lr_monitor,
        MyTrainStartCallback(),
    ]
    if os.path.exists(args.resume) and args.resume != "":
        trainer = Trainer(
            default_root_dir=pathlib.Path(config["training_config"]["exp_dir"]),
            max_epochs=config["training_config"]["epochs"],
            num_nodes=config["training_config"]["nodes"],
            devices=config["training_config"]["gpus"],
            accelerator="gpu",
            strategy=DDPStrategy(find_unused_parameters=False),
            callbacks=callbacks,
            reload_dataloaders_every_n_epochs=1,
            gradient_clip_val=config["training_config"]["gradient_clip_val"],
            # limit_train_batches=10,
            # limit_val_batches=10,
        )
        ckpt_path = config["training_config"]["resume"]
    else:
        trainer = Trainer(
            default_root_dir=pathlib.Path(config["training_config"]["exp_dir"]),
            max_epochs=config["training_config"]["epochs"],
            num_nodes=config["training_config"]["nodes"],
            devices=config["training_config"]["gpus"],
            accelerator="gpu",
            strategy=DDPStrategy(find_unused_parameters=False),
            callbacks=callbacks,
            reload_dataloaders_every_n_epochs=1,
            gradient_clip_val=config["training_config"]["gradient_clip_val"],
            # limit_train_batches=10,
            # limit_val_batches=10,
        )
        ckpt_path = None

    sp_model = spm.SentencePieceProcessor(model_file=str(args.sp_model_path))
    model = ConformerRNNTModule(sp_model, config, args.biasing)
    data_module = get_data_module(
        str(args.librispeech_path),
        str(args.global_stats_path),
        str(args.sp_model_path),
        config,
        subset=args.subset,
        biasinglist=args.biasing_list,
        droprate=args.droprate,
        maxsize=args.maxsize,
    )
    trainer.fit(model, data_module, ckpt_path=ckpt_path)


def cli_main():
    parser = ArgumentParser()
    parser.add_argument(
        "--checkpoint-path",
        default=None,
        type=pathlib.Path,
        help="Path to checkpoint to use for evaluation.",
    )
    parser.add_argument(
        "--exp-dir",
        default=pathlib.Path("./exp"),
        type=pathlib.Path,
        help="Directory to save checkpoints and logs to. (Default: './exp')",
    )
    parser.add_argument(
        "--global-stats-path",
        default=pathlib.Path("global_stats_100.json"),
        type=pathlib.Path,
        help="Path to JSON file containing feature means and stddevs.",
    )
    parser.add_argument(
        "--librispeech-path",
        type=pathlib.Path,
        help="Path to LibriSpeech datasets.",
        required=True,
    )
    parser.add_argument(
        "--sp-model-path",
        type=pathlib.Path,
        help="Path to SentencePiece model.",
        required=True,
    )
    parser.add_argument(
        "--nodes",
        default=1,
        type=int,
        help="Number of nodes to use for training. (Default: 4)",
    )
    parser.add_argument(
        "--gpus",
        default=1,
        type=int,
        help="Number of GPUs per node to use for training. (Default: 8)",
    )
    parser.add_argument(
        "--epochs",
        default=120,
        type=int,
        help="Number of epochs to train for. (Default: 120)",
    )
    parser.add_argument(
        "--subset",
        default=None,
        type=str,
        help="Train on subset of librispeech.",
    )
    parser.add_argument(
        "--biasing",
        action="store_true",
        help="Use biasing",
    )
    parser.add_argument(
        "--biasing-list",
        type=pathlib.Path,
        help="Path to the biasing list.",
    )
    parser.add_argument("--maxsize", default=1000, type=int, help="Size of biasing lists")
    parser.add_argument("--droprate", default=0.0, type=float, help="Biasing component regularisation drop rate")
    parser.add_argument(
        "--resume",
        default="",
        type=str,
        help="Path to resume model.",
    )
    parser.add_argument(
        "--train-config",
        default=None,
        type=pathlib.Path,
        help="Path to config file.",
    )
    args = parser.parse_args()

    config = load_config(args.train_config)
    config = update_config(config, args)

    run_train(args, config)


if __name__ == "__main__":
    cli_main()
