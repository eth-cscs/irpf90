#!/usr/bin/python

def main():
  from command_line import command_line

  if command_line.do_version:
    from version import version
    print version
    return

  from init import init
  if command_line.do_init:
    init()
  if not command_line.do_run:
    return

  init()
  import irp_stack
  irp_stack.create()

main()
