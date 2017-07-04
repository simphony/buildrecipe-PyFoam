Build Recipe: PyFoam
--------------------

This recipe builds the Enthought egg for the PyFoam package

Provisioning
------------

Machine supported: CentOS 6.5.
To create the egg::

    python edmsetup.py egg

The resulting egg will be in the `dist` directory

To upload, perform::
    
    python edmsetup.py upload_egg

