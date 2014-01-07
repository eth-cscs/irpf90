#!/usr/bin/python
from command_line import command_line
import irpf90_t

def run():
  template = """
program codelet_%(name)s
  implicit none
  integer :: i
  double precision :: ticks_0, ticks_1, cpu_0, cpu_1
  integer, parameter :: irp_imax = %(NMAX)d

  %(precondition)s

  call provide_%(name)s

  double precision :: irp_rdtsc

  call cpu_time(cpu_0)
  ticks_0 = irp_rdtsc()
  do i=1,irp_imax
    call bld_%(name)s
  enddo
  ticks_1 = irp_rdtsc()
  call cpu_time(cpu_1)
  print *, '%(name)s'
  print *, '-----------'
  print *, 'Cycles:'
  print *,  (ticks_1-ticks_0)/dble(irp_imax)
  print *, 'Seconds:'
  print *,  (cpu_1-cpu_0)/dble(irp_imax)
end

  """

  name, NMAX, precondition, filename = command_line.codelet
  if precondition is None:
    precondition = ""
  else:
    precondition = "PROVIDE "+precondition
  file = open(filename,'w')
  file.write(template%locals())
  file.close()


