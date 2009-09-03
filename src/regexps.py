#!/usr/bin/python

import re

re_comment = re.compile(r"^([^'!]*)('[^']*'[^']*)*!")

re_decl    = re.compile( "".join( [ r"^\ *",
 r"(integer[(::)?\* ,]+",
 r"|double *precision[(::)?\* ,]+",
 r"|logical[(::)?\* ,]+",
 r"|character[(::)?\* ,]+",
 r"|real[(::)?\* ,]+",
 r"|dimension *(::)?",
 r"|parameter *(::)?",
 r"|data */",
 r"|allocatable *(::)?",
 r"|common */",
 r"|namelist */",
 r"|save */",
 r"|complex[(::)?\* ,]+",
 r"|intrinsic *(::)?",
 r"|external *(::)?",
 r"|equivalence *(::)?",
 r")[^=(]"
] ) )

re_left  = re.compile(r"\[")
re_right = re.compile(r"\]")

re_test  = re.compile(r"\( *(.*)(\.[a-zA-Z]*\.|[<>]=?|[=/]=)([^=]*)\)")

re_space = re.compile("\s")

re_string = re.compile(r"'.*'")
re_assert = re.compile(r"assert *",re.I)
re_check = re.compile(r".*[() ].*")

