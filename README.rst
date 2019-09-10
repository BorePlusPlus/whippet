Whippet - like husky, but leaner
################################
Use `make <https://www.gnu.org/software/make/>`_ targets to execute git hooks. Inspired by `husky <https://github.com/typicode/husky#readme>`_.

Rationale
*********
I liked the simplicity of setting up git hooks using husky, and since I failed to find a similar tool in python ecosystem, I decided to write one myself.

As far as I know, there is no standard equivalent to `npm scripts <https://docs.npmjs.com/misc/scripts>`_ in python, so I chose to rely on make which seems to be a popular way to organise project-related tasks in the python world.

Installation
************
Whippet is available as a `PyPI package <https://pypi.org/project/whippet/>`_. Use a tool that can install packages from it, like for instance `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    $ pip install requests

Usage
*****

Install hooks
-------------
Once whippet is installed, it is used by invoking ``whippet`` executable in the directory where you wish to install hooks. Whippet checks if that directory (or its ancestor) contains a ``.git`` directory and offer to install hooks into it.

.. code-block:: bash

    $ cd demo
    $ whippet
    whippet - Are you sure you want to install hooks in /home/bpp/demo/.git? [Y/n] y

Setup target
------------
Whippet hooks are scripts that check for the existence of make targets with the same name as git hooks. If such a target exists, the script executes it. Let's take ``pre-commit`` as an example. Once whippet hooks are installed, we simply add ``pre-commit`` target to the Makefile like so:

.. code-block:: make

    pre-commit:
        @echo "Whippet says: Woof!"


Then the target will be executed on ``pre-commit``:

.. code-block:: bash

    $ git ci -m 'Testing whippet'
    pre-commit
    Whippet says: Woof!
    [master d654d33] Bar
    1 file changed, 12 insertions(+)
    create mode 100644 Makefile
    $


Non-interactive
---------------
To avoid the prompt pass the ``--assume-yes`` argument to whippet. This can be useful when adding whippet to initialisation target in Makefile. Example:

.. code-block:: make

    init:
        poetry install
        whippet --assume-yes


