Development environment
=======================
In Ubuntu terminal execute::

  $ createdb dakis
  $ make
  $ bin/django migrate
  $ make testall
  $ make run

Project Scope
=============
- Post one experiments task result through REST 
    - Universal python poster script should exist
    - Results can be posted from supercomputer nodes
- Show experiments list
- Show experiment tasks results summary
- Compare two experiment summaryies
