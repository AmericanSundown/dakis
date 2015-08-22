Development environment
=======================
In Ubuntu terminal execute::

  $ sudo apt-get install python-dev python3-dev python-virtualenv
  $ sudo apt-get install postgresql libpq-dev
  $ sudo -u postgres psql
  # create role <unix_username>;
  # alter role <unix_username> with superuser;
  # alter role <unix_username> with login;
  $ createdb dakis            # Creates Postgresql database with name ``dakis``
  $ make                      # Downloads and configures python packages
  $ bin/django migrate        # Creates tables in the database
  $ make testall              # Checks if everything works properly
  $ make run                  # Run server locally


Project Scope
=============
- Post one experiments task result through REST 
    - Universal python poster script should exist
    - Results can be posted from supercomputer nodes
+ Show experiments list
+ Show experiment tasks results summary
- Compare two experiment summaryies
