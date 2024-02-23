import pytest
import numpy as np
from online_and_reinforcement_learning.markov_decision_process import DummyEnv
from online_and_reinforcement_learning.value_iteration import value_iteration

env = DummyEnv()

def test_value_iteration():
    result = value_iteration(env, gamma=0.90, epsilon=(10 ** -6))

    # Check the validity of the output
    assert isinstance(result, np.ndarray), "Output should be a numpy array."
    assert result.shape[0] == env.nS, "Output shape should match number of states."


# Run the test with `pytest -v your_test_module.py`
