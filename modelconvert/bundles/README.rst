**************************
The Output Template System
**************************

**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


======
Basics
======

This is the root of the prepackaged
content template bundels.

  * basic
  * metadata
  * fullsize
  * etc.

-----------
Customizing
-----------

The basic template can be used to create your own template. It also
contains all settings and comments you can use. 


-------------
Shared assets
-------------
Files and directories in the ``_shared`` folder
are copied over to each of the templates output directory in addtion 
to the resources provided with in the template bundle.

Use this simplify delivery of assets that are common to all tempaltes 
(e.g. X3DOM files)

Resources within the template folder take precedence over the shared
version. If you need to provide a customized resource of a shared one,
just put it in the respective template directory. For exmaple:

.. code-block::

    _shared/static/x3dom.js
    _shared/static/x3dom.css
    _shared/static/x3dom.swf

If you want to override the ``x3dom.css`` file in your template just put
the new file in your ``template/static`` directory:

.. code-block::

    yourtemplate/static/x3dom.css


Resulting in the following generated output:

.. code-block::

    output/static/x3dom.js    (from _shared/static/x3dom.js)
    output/static/x3dom.css   (from yourtemplate/static/x3dom.css)


-----------------
Template Language
-----------------
The system is using the `Jinja`_ Template engine. You can use all the
default features of this system, including template inheritance. For 
a basic example please see the ``basic`` template. You can use this 
as blueprint for your own work.


.. _Jinja: http://jinja.pocoo.org/