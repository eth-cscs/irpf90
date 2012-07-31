program irp_example1
! integer :: x(W)
  BEGIN_SHELL [ /bin/bash ]
    echo print *, \'Compiled by `whoami` on `date`\'
    echo print *, \'$FC $FCFLAGS\'
    echo print *, \'$IRPF90\'
  END_SHELL
  print *, 't = ', t

  print *,  'v=', v
! print *,  u2
end
