# coding=utf-8
# Copyright 2022 The Balloon Learning Environment Authors.
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

"""A collection of evaluation suites."""

import dataclasses
from typing import List, Sequence
from balloon_learning_environment.eval import strata_seeds


@dataclasses.dataclass
class EvaluationSuite:
  """An evaluation suite specification.

  Attributes:
    seeds: A sequence of seeds to evaluate the agent on.
    max_episode_length: The maximum number of steps to evaluate the agent
      on one seed. Must be greater than 0.
  """
  seeds: Sequence[int]
  max_episode_length: int


_eval_suites = dict()


_eval_suites['big_eval'] = EvaluationSuite(list(range(10_000)), 960)
_eval_suites['medium_eval'] = EvaluationSuite(list(range(1_000)), 960)
for i in range(0, 100):
  _eval_suites[f'medium_eval{i}'] = EvaluationSuite(list(range(1000*i, 1000*(i+1))), 960)

for i in range(0, 100):
  _eval_suites[f'train_medium_eval{i}'] = EvaluationSuite(list(range(10_000 + 1000*i, 10_000 + 1000*(i+1))), 960)


_eval_suites['small_eval'] = EvaluationSuite(list(range(100)), 960)
for i in range(0, 100):
  _eval_suites[f'small_eval{i}'] = EvaluationSuite(list(range(100*i , 100*(i+1))), 960)

for i in range(0, 100):
  _eval_suites[f'tiny_eval{i}'] = EvaluationSuite(list(range(10*i , 10*(i+1))), 960)


# _eval_suites['200_seeds'] = EvaluationSuite(list(range(200)), 960)

_eval_suites['crashes'] = EvaluationSuite([15, 112, 230, 336], 960)

_eval_suites['tiny_eval'] = EvaluationSuite(list(range(10)), 960)
_eval_suites['micro_eval'] = EvaluationSuite([0], 960)
_eval_suites['our_eval'] = EvaluationSuite([2, 5, 8], 960)
_eval_suites['new_eval'] = EvaluationSuite([0, 2, 3, 4, 5, 8, 20, 21, 22], 960)
_eval_suites['newer_eval'] = EvaluationSuite(list(range(50)), 960)

_eval_suites['dies'] = EvaluationSuite([4, 11, 19, 39], 960)

_eval_suites['micro_eval_short'] = EvaluationSuite([0], 240)
_eval_suites['new_eval_short'] = EvaluationSuite([0, 2, 3, 4, 5, 8, 20, 21, 22], 240)


# NOTE: this is to compare what q values on a hard seed with bad states / low reward 
# vs a good seed with good states / high reward
# The harder seed is 10092 (twr 0.0), easier is 10035 (twr 1.0)
_eval_suites['test_q_values'] = EvaluationSuite([10092, 10035], 960)

all_strata = []
for strata in ['hardest', 'hard', 'mid', 'easy', 'easiest']:
  _eval_suites[f'{strata}_strata'] = EvaluationSuite(
      strata_seeds.STRATA_SEEDS[strata], 960)
  all_strata += strata_seeds.STRATA_SEEDS[strata]
_eval_suites['all_strata'] = EvaluationSuite(all_strata, 960)


def available_suites() -> List[str]:
  return list(_eval_suites.keys())


def get_eval_suite(name: str) -> EvaluationSuite:
  """Gets a named evaluation suite."""
  if name not in _eval_suites:
    raise ValueError(f'Unknown eval suite {name}')

  # Copy the seeds, rather than returning a mutable object.
  suite = _eval_suites[name]
  return EvaluationSuite(list(suite.seeds), suite.max_episode_length)
