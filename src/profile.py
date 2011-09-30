#!/usr/bin/python

rdtsc = """
#ifdef __i386
double irp_rdtsc_(void) {
  unsigned long long x;
  __asm__ volatile ("rdtsc" : "=A" (x));
  return (double) x;
}
#elif __amd64
double irp_rdtsc_(void) {
  unsigned long long a, d;
  __asm__ volatile ("rdtsc" : "=a" (a), "=d" (d));
  return (double)((d<<32) | a);
}
#endif
"""

import subprocess
import tempfile
import os
import threading
from variables import variables

def build_rdtsc():
  file,filename = tempfile.mkstemp()
  filename += ".c"
  file = open(filename,'w')
  file.write(rdtsc)
  file.close()
  def t():
    p = subprocess.Popen(["gcc","-O2",filename,"-c","-o","IRPF90_temp/irp_rdtsc.o"])

    p.communicate()
    os.remove(filename)

  threading.Thread(target=t).start()

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
 double precision, intent(in) :: value
 irp_profile(1,i) = irp_profile(1,i) + value
 irp_profile(2,i) = irp_profile(2,i) + 1.d0
end

subroutine irp_print_timer()
 use irp_timer
 implicit none
 integer :: i
 print '(A24,A8,4(X,A14))', 'Calls', 'Tot Cycles', 'Avge Cycles', &
                          'Tot Secs(1GHz)', 'Avge Secs(1GHz)'
   print '(A)', '----------------------------------------------'// &
                '----------------------------------------------'
 do i=1,%(n)d
  if (irp_profile(2,i) > 0.) then
   print '(A24,F8.0,2(X,F14.0),2(X,F14.8))', &
     irp_profile_label(i), irp_profile(2,i), &
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
  lmax = 0
  for l in label:
    text.append(" irp_profile_label(%d) = '%s'"%(l,label[l]))
    lmax = max(lmax,l)
  text.sort()
  text = '\n'.join(text)
  data = data%{'text': text, 'n':lmax}
  file = open("IRPF90_temp/irp_profile.irp.F90",'w')
  file.write(data)
  file.close()

def run():
  build_module()
  build_rdtsc()

if __name__ == "__main__":
  build_rdtsc()
