from easyvvuq.sampling import ReplicaSampler
from easyvvuq.sampling import BasicSweep
from easyvvuq.sampling import EmptySampler
import pytest


@pytest.fixture
def replica_sampler():
    return ReplicaSampler(BasicSweep({'a': [1, 2], 'b': [3, 4]}))


def test_infite_exception():
    with pytest.raises(RuntimeError):
        ReplicaSampler(EmptySampler())


def test_is_finite(replica_sampler):
    assert(not replica_sampler.is_finite())


def test_element_version(replica_sampler):
    assert(replica_sampler.element_version() == '0.1')


def test_n_samples(replica_sampler):
    with pytest.raises(RuntimeError):
        replica_sampler.n_samples()


def test_replica_sampler(replica_sampler):
    for _ in range(18):
        params = next(replica_sampler)
    assert(params['a'] == 1)
    assert(params['b'] == 4)
    assert(params['ensemble'] == 4)