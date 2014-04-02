 BEGIN_PROVIDER [ integer, d1 ]
&BEGIN_PROVIDER [ integer, d2 ]
&BEGIN_PROVIDER [ integer, d3 ]
&BEGIN_PROVIDER [ integer, d4 ]
&BEGIN_PROVIDER [ integer, d5 ]

 print *,  'd1'
 read(*,*) d1

 BEGIN_TEMPLATE
  print *,  '$X'
  read(*,*) $X
  ASSERT ( $X > $Y )

  SUBST [ X, Y ]
   d2; d1;;
   d3; d2;;
   d4; d3;;
   d5; d4;;
 END_TEMPLATE
END_PROVIDER

