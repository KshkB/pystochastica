discrete.core
=============

The package ``pystochastica.discrete.core`` contains the base class objects for the main classes 
used by ``pystochastica.discrete``. The central obbjective of the base class objects is to facilitate 
the ``__eq__`` and ``__hash__`` methods, in addition to other, generically useful functionality.

Package contents 
----------------

The ``SampleBase`` class  
************************

.. autoclass:: discrete.core.SampleBase
   :special-members: __new__, __init__, __eq__, __hash__
   :members:
   :undoc-members:
   :show-inheritance:


The ``RandVarBase`` class 
*************************

.. autoclass:: discrete.core.RandVarBase
   :special-members: __new__, __init__, __eq__, __hash__
   :members:
   :undoc-members:
   :show-inheritance:


The ``JointDistribution`` class  
*******************************

.. autoclass:: discrete.core.JointDistribution
   :special-members: __new__, __init__, __eq__, __hash__
   :members:
   :undoc-members:
   :show-inheritance:
