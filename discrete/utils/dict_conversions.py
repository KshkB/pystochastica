"""
convert bare dict arguments to arguments to initialise classes
    - e.g., RandVar, RandVec, etc.
"""
from ..samples import Sample

def rvdict_to_samples(rvdict) -> list[Sample]:
    """
    convert randvar data dict to list[Sample] object
        - list[Sample] is a list of all samples of the random variable to be initialised
    pass rvdict as {name: 'name', 'pspace': {'value': probability}}
        - Note, probability value is not used in generating Sample objects
    """
    pspace = rvdict['pspace']
    return [Sample(**{'name': rvdict['name'], 'value': float(v)}) for v in pspace.keys()]

def rvdict_to_pspace(rvdict) -> dict:
    """
    convert rvdict to dict to pspace for RandVar object
        - RandVar pspace are dicts {Sample: probability}
    see rvdict_to_samples for presentation of rvdict
    """
    rv_samples = rvdict_to_samples(rvdict)
    return dict(zip(rv_samples, rvdict['pspace'].values()))
