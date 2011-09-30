#!/usr/bin/python

rdtsc = """
#define uint64_t unsigned long
#ifdef __i386
uint64_t irp_rdtsc_() {
  uint64_t x;
  __asm__ volatile ("rdtsc" : "=A" (x));
  return x;
}
#elif __amd64
uint64_t irp_rdtsc_() {
  uint64_t a, d;
  __asm__ volatile ("rdtsc" : "=a" (a), "=d" (d));
  return (d<<32) | a;
}
#endif
"""

import subprocess
import tempfile
import os
from variables import variables

def build_rdtsc():
  file,filename = tempfile.mkstemp()
  filename += ".c"
  file = open(filename,'w')
  file.write(rdtsc)
  file.close()
  p = subprocess.Popen(["gcc","-O3",filename,"-c","-o","IRPF90_temp/irp_rdtsc.o"])
  p.communicate()
  os.remove(filename)

def build_module():
  data = """
module irp_timer
 double precision :: irp_profile(2,%(n)d) 
 character*(64)   :: irp_profile_label(%(n)d)
end module

subroutine irp_init_timer
 use irp_timer
 implicit none
 irp_profile = 0.
%(text)s
end

subroutine irp_set_timer(i,value)
 use irp_timer
 implicit none
 integer, intent(in) :: i
 integer*8, intent(in) :: value
 irp_profile(1,i) = dble(value)
 irp_profile(2,i) = irp_profile(2,i)+1.d0
end

subroutine irp_print_timer()
 use irp_timer
 implicit none
 integer :: i
 print '(16X,5(2X,A16))', 'Num Calls', 'Tot Cycles', 'Avge Cycles', &
                          'Tot Secs(1GHz)', 'Avge Secs(1GHz)'
 do i=1,%(n)d
  if (irp_profile(2,i) > 0.) then
   print '(A16,5(2X,F16.4))', irp_profile_label(i), irp_profile(2,i), &
     irp_profile(1,i), irp_profile(1,i)/irp_profile(2,i), &
     irp_profile(1,i)*1.d-9, 1.d-9*irp_profile(1,i)/irp_profile(2,i)
  endif
 enddo
end
  """
  label = {}
  for i in variables:
    vi = variables[i]
    label[vi.label] = vi.name
  text = []
  for l in label:
    text.append(" irp_profile_label(%d) = '%s'"%(l,label[l]))
  text.sort()
  text = '\n'.join(text)
  data = data%{'text': text, 'n':len(label.keys())}
  file = open("IRPF90_temp/irp_profile.irp.F90",'w')
  file.write(data)
  file.close()

def run():
  build_module()
  build_rdtsc()

if __name__ == "__main__":
  build_rdtsc()
