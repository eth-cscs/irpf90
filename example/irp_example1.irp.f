program irp_example1
  BEGIN_SHELL [ /bin/bash ]
    echo print *, \'Compiled by `whoami` on `date`\'
    echo print *, \'$FC $FCFLAGS\'
    echo print *, \'$IRPF90\'
  END_SHELL
  call run

end

subroutine run
  print *, 't = ', t
end
