from .. import RandWalk
import pytest

def test_rwalk():
    rw = RandWalk(time_steps=18)
    rw.generate_process()
    print(rw.process)
    assert len(rw.process) == 18

@pytest.fixture(scope='function') # comment out decorator to show plot
def test_rwalk_plot():
    rw = RandWalk(time_steps=18)
    rw.plt()
    assert True

@pytest.fixture(scope='function') 
def test_rwalk_walkplot():
    rw = RandWalk(time_steps=18)
    rw.plt_walk(100)

@pytest.fixture(scope='function') 
def test_rwalk_walkplots():
    rw = RandWalk(time_steps=10)
    rw.plt_walks(1000)