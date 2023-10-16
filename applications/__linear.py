"""
@Author: Conghao Wong
@Date: 2022-07-15 20:13:07
@LastEditors: Conghao Wong
@LastEditTime: 2023-10-16 21:41:31
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

from typing import Union
import torch

from qpid.args import Args
from qpid.base import BaseManager

from ..args import DYNAMIC, Args
from ..model import Model, layers
from ..training import Structure


class LinearArgs(Args):
    def __init__(self, terminal_args: list[str] = None, is_temporary=False) -> None:
        super().__init__(terminal_args, is_temporary)

    @property
    def weights(self) -> float:
        """
        The weights in the calculation of the mean squared error at 
        different moments of observation.
        Set to `0.0` to disable this function.
        """
        return self._arg('weights', default=0.0, argtype=DYNAMIC)


class LinearModel(Model):
    def __init__(self, Args: LinearArgs, structure=None, *args, **kwargs):
        super().__init__(Args, structure, *args, **kwargs)

        self.linear = layers.LinearLayerND(obs_frames=self.args.obs_frames,
                                           pred_frames=self.args.pred_frames,
                                           diff=Args.weights)

    def forward(self, inputs: list[torch.Tensor], training=None, *args, **kwargs):
        trajs = inputs[0]
        return self.linear(trajs)


class Linear(Structure):
    is_trainable = False

    def __init__(self, terminal_args: list[str]):

        self.args = LinearArgs(terminal_args)
        super().__init__(self.args)

    def create_model(self, *args, **kwargs) -> Model:
        return LinearModel(self.args, structure=self)
