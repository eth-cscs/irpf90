 BEGIN_PROVIDER [ integer, d1 ]
&BEGIN_PROVIDER [ integer, d2 ]
&BEGIN_PROVIDER [ integer, d3 ]
&BEGIN_PROVIDER [ integer, d4 ]
&BEGIN_PROVIDER [ integer, d5 ]

 BEGIN_SHELL [ /usr/bin/python ]
for i in range(1,6):
  print "  print *,  'd%d'"%(i,)
  print "  read(*,*) d%d"%(i,)
  if i > 1:
    print "  ASSERT ( d%d > d%d )"%(i,i-1)
 END_SHELL

END_PROVIDER

