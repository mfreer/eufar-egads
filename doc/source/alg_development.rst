

========
Algorithm Development
========

Introduction
*******************

The EGADS framework is designed to facilitate integration of third-party algorithms. This is accomplished
through creation of Python modules containing the algorithm code, and corresponding LaTeX files which 
contain the algorithm documentation. This section will explain the elements necessary to create these files,
 and how to incorporate them into the broader package.

Python module creation
************************

To guide creation of Python modules containing algorithms in EGADS, an algorithm template has been included
in the distribution. It can be found in ./egads/algorithms/algorithm_template.py and is shown below:

.. literalinclude:: algorithm_template.py

The best practice before starting an algorithm is to copy this file and name it following the EGADS algorithm
file naming conventions, which is all lowercase with words separated by underscores. As an example, the file
name for an algorithm calculating the wet bulb temperature contributed by DLR would be called
'temperature_wet_bulb_dlr.py'.

Within the file itself, there are several elements in this template that will need to be modified before this
can be usable as an EGADS algorithm:

# Class name
   The class name is currently 'AlgorithmTemplate', but this must be changed to the actual name of the
   algorithm. The conventions here are the same name as the filename (see above), but using MixedCase. So,
   following the example above, the class name would be TemperatureWetBulbDlr

# Algorithm docstring
   The docstring is everything following the three quote marks just after the class definition. This 
   section describes several essential aspects of the algorithm for easy reference directly from Python. 
   Each field following the word in ALLCAPS should be changed to reflect the properties of the algorithm
   (with the exception of VERSION, which will be changed automatically by Subversion when the file is 
   committed to the server).

# Algorithm and output metadata
   In the __init__ method of the module, two important parameters are defined. The first is the
   'output_metadata', which defines the metadata elements that will be assigned to the variable 
   output by the algorithm. A few recommended elements are included, but a broader list of variable
   metadata parameters can be found in the NetCDF standards document on the N6SP wiki (www.eufar.net/n6sp).
   In the case that there are multiple parameters output by the algorithm, the output_metadata parameter
   can be defined as a list VariableMetadata instances.
   
   Next, the 'metadata' parameter defines metadata concerning the algorithm itself. These information
   include the names of inputs and their units; names of outputs; name, date and version of the
   algorithm; date processed; and a reference to the output parameters.

# Definition of parameters
   In both the run and _algorithm methods, the local names intended for inputs need to be included. There
   are three locations where the same list must be added (marked in bold):
   
   * def run(self, **inputs**)
   * return egads_core.EgadsAlgorithm.run(self, **inputs**)
   * def _algorithm(self, **inputs**)
   
# Implementation of algorithm
   The algorithm itself gets written in the _algorithm module and uses variables passed in by the user.
   The variables which arrive here are simply scalar or arrays, and if the source is an instance of 
   EgadsData, the variables will be converted to the units you specified in the InputUnits of the 
   algorithm metadata. 




