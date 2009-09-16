#!/usr/bin/python

def main():
  from command_line import command_line

  if command_line.do_help:
    command_line.usage()

  if command_line.do_version:
    from version import version
    print version
    return

  if command_line.do_preprocess:
    from preprocessed_text import preprocessed_text
    for filename,text in preprocessed_text:
      if filename in command_line.preprocessed:
        for line in text:
          print line.text
    return

  from init import init
  if command_line.do_init:
    init()
  if not command_line.do_run:
    return

  init()
  import irp_stack
  irp_stack.create()

  import makefile
  makefile.create()

  from modules import modules, write_module
  for m in modules.keys():
    write_module(modules[m])

  makefile.run()

  import touches
  touches.create()

  import create_man
  create_man.run()

main()
