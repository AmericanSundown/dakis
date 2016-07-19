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
- Login
- Read instructions how to implement and test your optimization algorithm
- Add new algorithm by posting repository URL of algorithm, which implements the interface
- Choose optimization problem and result visualisation techniques for algorithm and run the experiment
- See single experiment results (algorithm + problem)
- See all experiment results for an algorithm (summary of an algorithm)
- Add optimization problem and its visualization technique (operators and ploting scripts should be uploaded)
- Compare one or more algorithm results for an arbitrary problem
- See a list of algorithms and their modifications
