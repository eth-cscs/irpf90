BEGIN_PROVIDER [ integer, t ]
  t = u1+v+4
END_PROVIDER

BEGIN_PROVIDER [integer,w]
  w = d5+3
END_PROVIDER

BEGIN_PROVIDER [ integer, v ]
  v = u2+w+2
END_PROVIDER

BEGIN_PROVIDER [ integer, u1 ]
  integer :: fu
! u1 = fu(d1,d2)
  u1 = d1+d2+1
END_PROVIDER

BEGIN_PROVIDER [ integer, u2 ]
  integer :: fu
! u2 = fu(d3,d4)
  u2 = d3+d4+1
  ASSERT (u2 > d3)
END_PROVIDER

integer function fu(x,y)
  integer :: x,y
  fu = x+y+1
end function
