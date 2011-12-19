#!/usr/bin/python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

to_remove = """cython_setup.py command_line.py""".split()
ext_modules = []

files = os.listdir('.')
for file in to_remove:
  files.remove(file)

for file in files:
  if file.endswith(".py"):
   module = file.split('.')[0]
   ext_modules += [ Extension(module,[file]) ]

setup(
  name = 'IRPF90 extensions',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)




