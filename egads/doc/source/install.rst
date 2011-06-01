
=============
Installation
=============
The latest version of EGADS can be obtained from http://eufar-egads.googlecode.com

Prerequisites
**************
Building EGADS requires the following packages:

* Python 2.5 or newer. Available at http://www.python.org/
* numpy 1.3.0 or newer. Available at http://numpy.scipy.org/
* scipy 0.6.0 or newer. Available at http://www.scipy.org/
* Python netCDF4 libraries 0.8.2. Available at http://code.google.com/p/netcdf4-python/

Optional Packages
*****************

The following are useful when using or compiling EGADS:

* IPython - An optional package which simplifies Python command line usage (http://ipython.scipy.org). IPython is an enhanced interactive Python shell which supports tab-completion, debugging, command history, etc. 

Installation
************
Since EGADS is a pure Python distribution, it does not need to be built. However, to use it, it must 
be installed to a location on the Python path. To install EGADS, type ``python setup.py install`` 
from the command line. To install to a user-specified location, type ``python setup.py install --prefix=$MYDIR``.

Testing
********
To test EGADS after it is installed, run the following commands in Python:

   >>> import egads
   >>> egads.test()
