IRPF90
======

IRPF90 is a Fortran90 preprocessor written in Python for programming using the Implicit Reference to Parameters (IRP) method. It simplifies the development of large fortran codes in the field of scientific high performance computing.

![IRPF90 Logo](./irpf90.xpm)

Dependencies
------------

- GNU make (>= 3.81 recommended)
- Python > 2.3
- Any Fortran 90 compiler (Intel recommended)

Installing IRPF90
-----------------

``${IRPF90_HOME}`` is the location of your irpf90 directory::

``` bash
  cd ${IRPF90_HOME}
  make
  cat << EOF >> ${HOME}/.bash_profile
  export PYTHONPATH=${IRPF90_HOME}/src:${PYTHONPATH}
  export PATH=${IRPF90_HOME}/bin:${PATH}
  export MANPATH=${IRPF90_HOME}/man:${MANPATH}
  EOF
  . ${HOME}/.bash_profile
```


Using IRPF90
------------

In an empty directory, run:

``` bash
  irpf90 --init
```

This command creates a new Makefile suitable for most irpf90 projects.
Now you can start to program using irpf90.


Web Site
--------

http://irpf90.ups-tlse.fr

