#!/usr/bin/python
#   IRPF90 is a Fortran90 preprocessor written in Python for programming using
#   the Implicit Reference to Parameters (IRP) method.
#   Copyright (C) 2009 Anthony SCEMAMA 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr 


import util 
from command_line import command_line

do_assert = command_line.do_assert
do_debug = command_line.do_debug

import irpf90_t

FILENAME = irpf90_t.irpdir+"irp_stack.irp.F90"

def create():

  txt = """
module irp_stack_mod
  integer, parameter            :: STACKMAX=1000
  character*(128),allocatable   :: irp_stack(:,:)
  double precision,allocatable  :: irp_cpu(:,:)
  integer,allocatable           :: stack_index(:)
  logical                       :: alloc = .False.
  character*(128)               :: white = ''
end module

subroutine irp_enter(irp_where)
 use irp_stack_mod
 integer       :: ithread
 integer       :: nthread
 character*(*) :: irp_where
 ithread = 0
 nthread = 1
$1
$2
end subroutine

subroutine irp_leave (irp_where)
 use irp_stack_mod
  character*(*) :: irp_where
  integer       :: ithread
  double precision :: cpu
  ithread = 0
$3
$4
end subroutine
"""

  # $1
  if do_assert or do_debug:
    txt = txt.replace("$1","""
!$OMP CRITICAL
 if (.not.alloc) then
   allocate(irp_stack(STACKMAX,nthread))
   allocate(irp_cpu(STACKMAX,nthread))
   allocate(stack_index(nthread))
   alloc = .True.
 endif
!$OMP END CRITICAL
 stack_index(ithread+1) = stack_index(ithread+1)+1
 irp_stack(stack_index(ithread+1),ithread+1) = irp_where""")
  else:
    txt = txt.replace("$1","")

  # $2
  if do_debug:
    txt = txt.replace("$2","""
  print *, ithread, ':', white(1:stack_index(ithread+1))//'-> ', trim(irp_where)
  call cpu_time(irp_cpu(stack_index(ithread+1),ithread+1))""")
  else:
    txt = txt.replace("$2","")

  # $3
  if do_debug:
    txt = txt.replace("$3","""
  call cpu_time(cpu)
  print *, ithread, ':', white(1:stack_index(ithread+1))//'<- ', &
    trim(irp_stack(stack_index(ithread+1),ithread+1)), &
    cpu-irp_cpu(stack_index(ithread+1),ithread+1)""")
  else:
    txt = txt.replace("$3","")

  # $4
  if do_debug or do_assert:
    txt = txt.replace("$4","""
  stack_index(ithread+1) = stack_index(ithread+1)-1""")
  else:
    txt = txt.replace("$4","")

  if do_debug or do_assert:
    txt += """
subroutine irp_trace
 use irp_stack_mod
 integer :: ithread
 integer :: i
 ithread = 0
 if (.not.alloc) return
 print *, 'Stack trace: ', ithread
 print *, '-------------------------'
 do i=1,stack_index(ithread+1)
  print *, trim(irp_stack(i,ithread+1))
 enddo
 print *, '-------------------------'
end subroutine
"""

  txt = txt.split('\n')
  txt = map(lambda x: x+"\n",txt)
  if not util.same_file(FILENAME, txt):
    file = open(FILENAME,'w')
    file.writelines(txt)
    file.close()


