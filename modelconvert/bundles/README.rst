**************************
The Output Template System
**************************

**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


========
Overview
========

This is the root of the prepackaged
content template bundels.

plain
metadata
fullsize
etc.

They are to be distinguised form the
application templates (layout, etc.)
for the CIF application itself.

Files and directories in the _shared folder
are copied over to each of the templates
in addtion to the resources provided with the
template. 

Use this simplify delivery of assets that are 
common to all tempaltes (e.g. X3DOM files, readme
etc.)

The resources within the template folder
take precedence. If you need to provide a customized
resource of a shared one, just put it in the respective
template directory. eg.g

_shared/static/x3dom.js
_shared/static/x3dom.css

plain/static/x3dom.css

Resulting in

output/static/x3dom.js    (from _shared/static/x3dom.js)
output/static/x3dom.css   (from plain/static/x3dom.css)

The system is using the `Jinja`_ Template engine. You can use all the
default features of this system.



.. _Jinja: http://jinja.pocoo.org/