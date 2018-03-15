# numberwon

A package with Song Fingerprinting and Facial Recognition and clustering capabilities (CogWorks 2017)

`number` was created as the backbone for an autonomous cognitive assistant at the [Beaver Works Summer Institute at MIT](https://beaverworks.ll.mit.edu/CMS/bw/bwsi). It was developed by [AJ Federici](https://github.com/AFederici), [Michael Huang](https://github.com/myh1000), [Megan Kaye](https://github.com/mkaye5), and by [Christine Zhao](https://github.com/czhao028)). 

## Installation Instructions
Clone numberwon, navigate to the resulting directory, and run

```shell
python setup.py develop
```

In the numberwon directory, you can install the database class, the Face_Recognition class and the FingerPrint class:
```shell
import Database, import Face_Recognition, import FingerPrint
```

We will need to install OpenCV with the Python bindings so that we can access laptop cameras via our Python code (aka the camera import).

### Windows Instructions (Python 3.{2-6})
Requires: Anaconda + Python 3.{2-6}, numpy, python-opencv

#### For Windows OS
```shell
conda install -c conda-forge opencv
```
