#/usr/bin/python

import os

def install():
  VIM = os.environ["HOME"]+"/.vim"
  try:
    if os.access(VIM+"/syntax/irpf90.vim",os.F_OK):
       return
    if not os.access(VIM,os.F_OK):
      os.mkdir(VIM)
    file = open(VIM+"/filetype.vim","a")
    file.write("au BufRead,BufNewFile *.irp.f setfiletype irpf90")
    file.close()
    if not os.access(VIM+"/syntax",os.F_OK):
      os.mkdir(VIM+"/syntax")
    wd = os.path.abspath(os.path.dirname(__file__))+"/../vim"
    os.symlink(wd+"/irpf90.vim",VIM+"/syntax/irpf90.vim")
  except:
    pass

if __name__ == "__main__":
  install()
