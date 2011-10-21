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
    p = subprocess.Popen(["gcc","-O2",filename,"-c","-o","irp_rdtsc.o"])
    p.communicate()
    os.remove(filename)

  threading.Thread(target=t).start()

def build_module():
  data = """
module irp_timer
 double precision :: irp_profile(3,%(n)d) 
 integer          :: irp_order(%(n)d) 
 character*(64)   :: irp_profile_label(%(n)d)
 double precision :: irp_rdtsc_shift

 contains

   subroutine profile_sort ()
    implicit none
    character*(64)         :: xtmp
    integer                :: i, i0, j, jmax

    do i=1,size(irp_profile_label)
     irp_order(i)=i
    enddo
    do i=1,size(irp_profile_label)
     xtmp = irp_profile_label(i)
     i0 = irp_order(i)
     j = i-1
     do j=i-1,1,-1
      if ( irp_profile_label(j) > xtmp ) then
       irp_profile_label(j+1) = irp_profile_label(j)
       irp_order(j+1) = irp_order(j)
      else
       exit
      endif
     enddo
     irp_profile_label(j+1) = xtmp
     irp_order(j+1) = i0
    enddo
   end subroutine profile_sort

end module

subroutine irp_init_timer
 use irp_timer
 implicit none
 integer :: i
 double precision :: irp_rdtsc, t0
 irp_profile = 0.d0
 irp_rdtsc_shift = 0.d0
 do i=1,1000
   t0 = irp_rdtsc()
   irp_rdtsc_shift = irp_rdtsc_shift + (irp_rdtsc()-t0)
 enddo
 irp_rdtsc_shift = 1.d-3*irp_rdtsc_shift
%(text)s
end

subroutine irp_set_timer(i,value)
 use irp_timer
 implicit none
 integer, intent(in) :: i
 double precision, intent(inout) :: value
 value = value - irp_rdtsc_shift
 irp_profile(1,i) = irp_profile(1,i) + value
 irp_profile(2,i) = irp_profile(2,i) + value*value
 irp_profile(3,i) = irp_profile(3,i) + 1.d0
end

subroutine irp_print_timer()
 use irp_timer
 implicit none
 integer :: i, ii
 double precision :: error, sigma2, average, average2, frequency, t0
 double precision :: irp_rdtsc
 t0 = irp_rdtsc()
 call sleep(1)
 frequency = (irp_rdtsc()-t0-irp_rdtsc_shift)

 call profile_sort()
 print '(A24,A8,A17,A20,A13,A20)', '', 'N.Calls', 'Tot Cycles', 'Avg Cycles', &
                          'Tot Secs', 'Avg Secs'
   print '(A)', '----------------------------------------------'// &
                '----------------------------------------------'
 do ii=1,%(n)d
  i = irp_order(ii)
  if (irp_profile(3,i) > 0.) then
   error = 0.d0
   average  = irp_profile(1,i)/irp_profile(3,i)
   if (irp_profile(3,i) > 1.d0) then
     average2 = irp_profile(2,i)/irp_profile(3,i)
     sigma2   = (average2 - average*average)
     error = sqrt(sigma2/(irp_profile(3,i)+1.d0))
   endif
   print '(A24 , F8.0 , X,F12.0 , X,F12.0,A3,F8.0, X,F12.8, X,F8.5,A3,F8.5 )', &
     irp_profile_label(ii), &
     irp_profile(3,i), &
     irp_profile(1,i), &
     average, '+/-', error, &
     irp_profile(1,i)/frequency, &
     average/frequency, '+/-', error/frequency
  endif
 enddo
 print *, 'Frequency     :', frequency*1.d-9, ' GHz'
 print *, 'rdtsc latency :', irp_rdtsc_shift, ' cycles'
end
  """
  label = {}
  for i in variables:
    vi = variables[i]
    label[vi.label] = vi.same_as
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
