from .. import RandWalk
import pytest

def test_rwalk():
    rw = RandWalk(time_steps=18)
    rw.run()
    print(rw.out)
    assert len(rw.out) == 18

@pytest.fixture(scope='function') # comment out decorator to show plot
def test_rwalk_plot():
    rw = RandWalk(time_steps=18)
    rw.plt()
    assert True