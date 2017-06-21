Build Recipe: PyFoam
--------------------

This recipe builds the Enthought egg for the PyFoam package

Provisioning
------------

Machine supported: CentOS 6.5.
To create the egg::

    python builder.py egg

The resulting egg will be in the `dist` directory

To upload, perform::
    
    python builder.py upload_egg

