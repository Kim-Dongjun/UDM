# coding=utf-8
# Copyright 2020 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modified at 2021 by anonymous authors of "Score Matching Model for Unbounded Data Score"
# submitted on NeurIPS 2021 conference.

# Lint as: python3
"""Training UNCSN on Church with RVE-SDE."""

from configs.default_lsun_configs import get_default_configs
import ml_collections

def get_config():
  config = get_default_configs()
  # training
  training = config.training
  training.sde = 'rve-sde'
  training.continuous = True

  # sampling
  sampling = config.sampling
  sampling.method = 'pc'
  sampling.predictor = 'reverse_diffusion'
  sampling.corrector = 'langevin'

  # data
  data = config.data
  data.category = 'church_outdoor'

  # model
  model = config.model
  model.name = 'ncsnpp'
  model.sigma_max = 380
  model.scale_by_sigma = True
  model.ema_rate = 0.999
  model.normalization = 'GroupNorm'
  model.nonlinearity = 'swish'
  model.nf = 128
  model.ch_mult = (1, 1, 2, 2, 2, 2, 2)
  model.num_res_blocks = 2
  model.attn_resolutions = (16,)
  model.resamp_with_conv = True
  model.conditional = True
  model.fir = True
  model.fir_kernel = [1, 3, 3, 1]
  model.skip_rescale = True
  model.resblock_type = 'biggan'
  model.progressive = 'output_skip'
  model.progressive_input = 'input_skip'
  model.progressive_combine = 'sum'
  model.attention_type = 'ddpm'
  model.init_scale = 0.
  model.fourier_scale = 16
  model.conv_size = 3

  # DJ
  config.add = add = ml_collections.ConfigDict()
  add.model_mode = 'reciprocal'
  model.sigma_min = 1e-3
  add.eta = 1e-3
  add.transform = 'ver3'
  add.begin_time = 'initial'
  add.loss = False
  add.random_t = True
  sampling.probability_flow = False

  return config