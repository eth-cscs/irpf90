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

re_test  = re.compile(r"\( *(.*)(\.[a-zA-Z]*\.|[<>]=?|[=/]=)([^=]*)\)")

re_string = re.compile(r"'.*'")

