************************************
How to Install Word2Vec Dependencies
************************************

This document will help you install the requirements need to run the word2vec model created by the TensorFlow team.
Word2vec is used as part of the TensorFlow connector and in the example bot using this connector.

g++
###

`Windows <http://mingw-w64.org/doku.php/download/mingw-builds): Installing instructions for Windows.>`_


`Mac <http://cs.millersville.edu/~gzoppetti/InstallingGccMac.html): Installation instructions for Mac.>`_


`Linux (resource 1) <https://help.ubuntu.com/community/InstallingCompilers>`_: Installation instructions
for Linux.

`Linux (resource 2) <https://gcc.gnu.org/wiki/InstallingGCC)>`_: Another resource that might be useful.


word2vec_ops.so
###############
The C files to create this ops file are part of a zipped file in the Microsoft Azure portal.

1. If you haven't done so already, clone the pybotframework repo.

2. Download the zipped file from `here <https://odsc2017.blob.core.windows.net/models/tensorflow_tutorial_data.zip>`_

3. Unzip the file and place the contents in `pybotframework/examples/tf_bot/data` in the cloned repo.

4. Enter this `data` directory and proceed with the following steps.


Before executing these commands, make sure that TensorFlow has been installed on your system.::

    `TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')`

    `g++ -std=c++11 -shared word2vec_ops.cc word2vec_kernels.cc -o word2vec_ops.so -fPIC -I $TF_INC -O2 -D_GLIBCXX_USE_CXX11_ABI=0`

On a Mac, add `-undefined dynamic_lookup` to the g++ command.

After running these commands, the file `word2vec_ops.so` will be created. This file needs to be placed in the
`pybotframework/word2vec/` directory in order to be able to run the tf_bot sample bot.


Once this ops file has been created, it needs to be moved into your installation of pybotframework.

1. Open a terminal and start python::

    `> python`
2. In path, load the pybotframework package::

    `> import pybotframework`
3. Retrieve the location of the package::

    `> pybotframework.__path__`

4. In the pybotframework-0.1-py3.5.egg directory, there is an `examples/tf_bot/word2vec` directory. Copy
`word2vec_ops.so` into that directory.
