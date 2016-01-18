
Muffin-SqlAlchemy
#################

.. _description:

Muffin-SqlAlchemy -- A simple sqlalchemy helper plugin for muffin_ framework.

.. _badges:

.. image:: http://img.shields.io/travis/drgarcia1986/muffin-sqlalchemy.svg?style=flat-square
    :target: http://travis-ci.org/drgarcia1986/muffin-sqlalchemy
    :alt: Build Status

.. _requirements:

Requirements
=============

- python >= 3.4
- muffin >= 0.5.5

.. _installation:

Installation
=============

**Muffin-SqlAlchemy** should be installed using pip: ::

    pip install muffin-sqlalchemy

.. _usage:

Usage
=====

Add *muffin-sqlalchemy* to muffin plugin list:

.. code-block:: python

    import muffin


    app = muffin.Application(
        'example',

        PLUGINS=(
            'muffin_sqlalchemy',
        )
    )

And use *sqlalchemy* session in request object:

.. code-block:: python

    @app.register('/foo')
    class Example(muffin.Handler):

        @asyncio.coroutine
        def post(self, request):
            foo = FooModel(name='foo')
            session = request.sqlalchemy_session
            session.add(foo)
            session.commit()
            return 'Ok'

.. _options:

Options
-------

========================== ==============================================================
 *SQLALCHEMY_DATABASE_URI* URI of database (``sqlite:///muffin.db``)
========================== ==============================================================

Commands
========

The plugin adds some commands to your Muffin_ application.

Create Databse
--------------

Create all tables in database according to you engine: ::

    $ muffin app_module create_databse

to work fine inherit from *muffin_sqalchemy.SqlAlchemyDeclarativeBase* to create yours sqlalchemy models

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/drgarcia1986/muffin-sqlalchemy/issues

.. _contributing:

Contributing
============

Development of Muffin-SqlAlchemy happens at: https://github.com/drgarcia1986/muffin-sqlalchemy


Contributors
=============

* drgarcia1986_ (Diego Garcia)

.. _license:

License
=======

Licensed under a `MIT license`_.

.. _links:


.. _muffin: https://github.com/klen/muffin
.. _drgarcia1986: https://github.com/drgarcia1986
.. _MIT license: http://opensource.org/licenses/MIT
