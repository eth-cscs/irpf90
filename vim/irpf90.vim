" Vim syntax file
" Language:	IRPF90
" Version:	0.1
" URL:		
" Last Change:	2011 Nov. 9
" Maintainer:	
" Usage:	Do :help irpf90-syntax from Vim
" Credits:
"  Version 0.1 was based on the fortran 95 syntax file by Ajit J. Thakkar 

if version < 600
  let b:current_syntax = "fortran"
  finish
elseif exists("b:current_syntax")
  finish
endif
let b:current_syntax = "irpf90"

syn case ignore


syn match irpf90Identifier	"\<\a\w*\>" contains=irpf90SerialNumber
syn match irpf90ConstructName	"^\s*\zs\a\w*\ze\s*:"
syn match irpf90ConstructName "\(\<end\s*do\s\+\)\@<=\a\w*"
syn match irpf90ConstructName "\(\<end\s*if\s\+\)\@<=\a\w*"
syn match irpf90ConstructName "\(\<end\s*select\s\+\)\@<=\a\w*"

syn match   irpf90UnitHeader	"^\s*end\s*$"
syn match   irpf90UnitHeader	"^\s*end/>"

syn keyword irpf90Type		character complex integer
syn keyword irpf90Type		intrinsic
syn match irpf90Type		"\<implicit\>"
syn keyword irpf90Structure	dimension
syn keyword irpf90StorageClass	parameter save
syn match irpf90UnitHeader	"\<subroutine\>"
syn keyword irpf90Call		call
syn match irpf90UnitHeader	"\<function\>"
syn match irpf90UnitHeader	"\<program\>"
syn keyword irpf90Statement	return stop
syn keyword irpf90Conditional	else then
syn match irpf90Conditional	"\<if\>"
syn match irpf90Repeat		"\<do\>"

syn keyword irpf90Todo		contained todo fixme

"Catch errors caused by too many right parentheses
syn region irpf90Paren transparent start="(" end=")" contains=ALLBUT,irpf90ParenError,@irpf90CommentGroup,cIncluded
syn match  irpf90ParenError   ")"

syn match irpf90Operator	"\.\s*n\=eqv\s*\."
syn match irpf90Operator	"\.\s*\(and\|or\|not\)\s*\."
syn match irpf90Operator	"\(+\|-\|/\|\*\)"

syn match irpf90Boolean	"\.\s*\(true\|false\)\s*\."

syn keyword irpf90ReadWrite	backspace close inquire open rewind endfile
syn keyword irpf90ReadWrite	read write print

"If tabs are allowed then the left margin checks do not work
if exists("irpf90_have_tabs")
  syn match irpf90Tab		"\t"  transparent
else
  syn match irpf90Tab		"\t"
endif

syn keyword irpf90IO		unit file iostat access blank fmt form
syn keyword irpf90IO		recl status exist opened number named name
syn keyword irpf90IO		sequential direct rec
syn keyword irpf90IO		formatted unformatted nextrec

syn keyword irpf9066Intrinsic		cabs ccos cexp clog csin csqrt
syn keyword irpf9066Intrinsic		dacos dasin datan datan2 dcos dcosh
syn keyword irpf9066Intrinsic		ddim dexp dint dlog dlog10 dmod dabs
syn keyword irpf9066Intrinsic		dnint dsign dsin dsinh dsqrt dtan
syn keyword irpf9066Intrinsic		dtanh iabs idim idnint isign idint ifix
syn keyword irpf9066Intrinsic		amax0 amax1 dmax1 max0 max1
syn keyword irpf9066Intrinsic		amin0 amin1 dmin1 min0 min1
syn keyword irpf9066Intrinsic		amod float sngl alog alog10

" Intrinsics provided by some vendors
syn keyword irpf90ExtraIntrinsic	cdabs cdcos cdexp cdlog cdsin cdsqrt
syn keyword irpf90ExtraIntrinsic	cqabs cqcos cqexp cqlog cqsin cqsqrt
syn keyword irpf90ExtraIntrinsic	qacos qasin qatan qatan2 qcos qcosh
syn keyword irpf90ExtraIntrinsic	qdim qexp iqint qlog qlog10 qmod qabs
syn keyword irpf90ExtraIntrinsic	qnint qsign qsin qsinh qsqrt qtan
syn keyword irpf90ExtraIntrinsic	qtanh qmax1 qmin1
syn keyword irpf90ExtraIntrinsic	dimag qimag dcmplx qcmplx dconjg qconjg
syn keyword irpf90ExtraIntrinsic	gamma dgamma qgamma algama dlgama qlgama
syn keyword irpf90ExtraIntrinsic	erf derf qerf erfc derfc qerfc
syn keyword irpf90ExtraIntrinsic	dfloat

syn keyword irpf90Intrinsic	abs acos aimag aint anint asin atan atan2
syn keyword irpf90Intrinsic	cos sin tan sinh cosh tanh exp log log10
syn keyword irpf90Intrinsic	sign sqrt int cmplx nint min max conjg
syn keyword irpf90Intrinsic	char ichar index
syn match irpf90Intrinsic	"\<len\s*[(,]"me=s+3
syn match irpf90Intrinsic	"\<real\s*("me=s+4
syn match irpf90Type		"\<implicit\s\+real"
syn match irpf90Type		"^\s*real\>"
syn match irpf90Intrinsic	"\<logical\s*("me=s+7
syn match irpf90Type		"\<implicit\s\+logical"
syn match irpf90Type		"^\s*logical\>"

"Numbers of various sorts
" Integers
syn match irpf90Number	display "\<\d\+\(_\a\w*\)\=\>"
" floating point number, without a decimal point
syn match irpf90FloatNoDec	display	"\<\d\+[deq][-+]\=\d\+\(_\a\w*\)\=\>"
" floating point number, starting with a decimal point
syn match irpf90FloatIniDec	display	"\.\d\+\([deq][-+]\=\d\+\)\=\(_\a\w*\)\=\>"
" floating point number, no digits after decimal
syn match irpf90FloatEndDec	display	"\<\d\+\.\([deq][-+]\=\d\+\)\=\(_\a\w*\)\=\>"
" floating point number, D or Q exponents
syn match irpf90FloatDExp	display	"\<\d\+\.\d\+\([dq][-+]\=\d\+\)\=\(_\a\w*\)\=\>"
" floating point number
syn match irpf90Float	display	"\<\d\+\.\d\+\(e[-+]\=\d\+\)\=\(_\a\w*\)\=\>"
" Numbers in formats
syn match irpf90FormatSpec	display	"\d*f\d\+\.\d\+"
syn match irpf90FormatSpec	display	"\d*e[sn]\=\d\+\.\d\+\(e\d+\>\)\="
syn match irpf90FormatSpec	display	"\d*\(d\|q\|g\)\d\+\.\d\+\(e\d+\)\="
syn match irpf90FormatSpec	display	"\d\+x\>"
" The next match cannot be used because it would pick up identifiers as well
" syn match irpf90FormatSpec	display	"\<\(a\|i\)\d\+"

" Numbers as labels
syn match irpf90LabelNumber	display	"^\d\{1,5}\s"me=e-1
syn match irpf90LabelNumber	display	"^ \d\{1,4}\s"ms=s+1,me=e-1
syn match irpf90LabelNumber	display	"^  \d\{1,3}\s"ms=s+2,me=e-1
syn match irpf90LabelNumber	display	"^   \d\d\=\s"ms=s+3,me=e-1
syn match irpf90LabelNumber	display	"^    \d\s"ms=s+4,me=e-1

if version >= 600 && exists("irpf90_more_precise")
  " Numbers as targets
  syn match irpf90Target	display	"\(\<if\s*(.\+)\s*\)\@<=\(\d\+\s*,\s*\)\{2}\d\+\>"
  syn match irpf90Target	display	"\(\<do\s\+\)\@<=\d\+\>"
  syn match irpf90Target	display	"\(\<go\s*to\s*(\=\)\@<=\(\d\+\s*,\s*\)*\d\+\>"
endif

syn keyword irpf90TypeEx	external
syn keyword irpf90IOEx		format
syn keyword irpf90StatementEx	continue
syn match irpf90StatementEx	"\<go\s*to\>"
syn region irpf90StringEx	start=+'+ end=+'+ contains=irpf90ContinueMark,irpf90LeftMargin,irpf90SerialNumber
syn keyword irpf90IntrinsicEx	dim lge lgt lle llt mod
syn keyword irpf90StatementOb	assign pause to

syn keyword irpf90Type	type none

syn keyword irpf90Structure	private public intent optional
syn keyword irpf90Structure	pointer target allocatable
syn keyword irpf90StorageClass	in out
syn match irpf90StorageClass	"\<kind\s*="me=s+4
syn match irpf90StorageClass	"\<len\s*="me=s+3

syn match irpf90UnitHeader	"\<module\>"
syn keyword irpf90UnitHeader	use only contains
syn keyword irpf90UnitHeader	result operator assignment
syn match irpf90UnitHeader	"\<interface\>"
syn match irpf90UnitHeader	"\<recursive\>"
syn keyword irpf90Statement	allocate deallocate nullify cycle exit
syn match irpf90Conditional	"\<select\>"
syn keyword irpf90Conditional	case default where elsewhere

syn match irpf90Operator	"\(\(>\|<\)=\=\|==\|/=\|=\)"
syn match irpf90Operator	"=>"

syn region irpf90String	start=+"+ end=+"+	contains=irpf90LeftMargin,irpf90ContinueMark,irpf90SerialNumber
syn keyword irpf90IO		pad position action delim readwrite
syn keyword irpf90IO		eor advance nml

syn keyword irpf90Intrinsic	adjustl adjustr all allocated any
syn keyword irpf90Intrinsic	associated bit_size btest ceiling
syn keyword irpf90Intrinsic	count cshift date_and_time
syn keyword irpf90Intrinsic	digits dot_product eoshift epsilon exponent
syn keyword irpf90Intrinsic	floor fraction huge iand ibclr ibits ibset ieor
syn keyword irpf90Intrinsic	ior ishft ishftc lbound len_trim
syn keyword irpf90Intrinsic	matmul maxexponent maxloc maxval merge
syn keyword irpf90Intrinsic	minexponent minloc minval modulo mvbits nearest
syn keyword irpf90Intrinsic	pack present product radix random_number
syn match irpf90Intrinsic		"\<not\>\(\s*\.\)\@!"me=s+3
syn keyword irpf90Intrinsic	random_seed range repeat reshape rrspacing scale
syn keyword irpf90Intrinsic	selected_int_kind selected_real_kind scan
syn keyword irpf90Intrinsic	shape size spacing spread set_exponent
syn keyword irpf90Intrinsic	tiny transpose trim ubound unpack verify
syn keyword irpf90Intrinsic	precision sum system_clock
syn match irpf90Intrinsic	"\<kind\>\s*[(,]"me=s+4

syn match  irpf90UnitHeader	"\<end\s*function"
syn match  irpf90UnitHeader	"\<end\s*interface"
syn match  irpf90UnitHeader	"\<end\s*module"
syn match  irpf90UnitHeader	"\<end\s*program"
syn match  irpf90UnitHeader	"\<end\s*subroutine"
syn match  irpf90Repeat	"\<end\s*do"
syn match  irpf90Conditional	"\<end\s*where"
syn match  irpf90Conditional	"\<select\s*case"
syn match  irpf90Conditional	"\<end\s*select"
syn match  irpf90Type	"\<end\s*type"
syn match  irpf90Type	"\<in\s*out"

syn keyword irpf90UnitHeaderEx	procedure
syn keyword irpf90IOEx		namelist
syn keyword irpf90ConditionalEx	while
syn keyword irpf90IntrinsicEx	achar iachar transfer

syn keyword irpf90Include		include
syn keyword irpf90StorageClassR	sequence

syn match   irpf90Conditional	"\<end\s*if"
syn match   irpf90IO		contains=irpf90Operator "\<e\(nd\|rr\)\s*=\s*\d\+"
syn match   irpf90Conditional	"\<else\s*if"

syn keyword irpf90UnitHeaderR	entry
syn match irpf90TypeR		display "double\s\+precision"
syn match irpf90TypeR		display "double\s\+complex"
syn match irpf90UnitHeaderR	display "block\s\+data"
syn keyword irpf90StorageClassR	common equivalence data
syn keyword irpf90IntrinsicR	dble dprod
syn match   irpf90OperatorR	"\.\s*[gl][et]\s*\."
syn match   irpf90OperatorR	"\.\s*\(eq\|ne\)\s*\."

syn keyword irpf90Repeat		forall
syn match irpf90Repeat		"\<end\s*forall"
syn keyword irpf90Intrinsic	null cpu_time
syn match irpf90Type			"\<elemental\>"
syn match irpf90Type			"\<pure\>"
syn match irpf90ConstructName "\(\<end\s*forall\s\+\)\@<=\a\w*\>"

syn cluster irpf90CommentGroup contains=irpf90Todo

syn match irpf90ContinueMark		display "&"

syn match irpf90Comment	excludenl "!.*$" contains=@irpf90CommentGroup

"cpp is often used with irpf90
syn match	cPreProc		"^\s*#\s*\(define\|ifdef\)\>.*"
syn match	cPreProc		"^\s*#\s*\(elif\|if\)\>.*"
syn match	cPreProc		"^\s*#\s*\(ifndef\|undef\)\>.*"
syn match	cPreCondit		"^\s*#\s*\(else\|endif\)\>.*"
syn region	cIncluded	contained start=+"[^(]+ skip=+\\\\\|\\"+ end=+"+ contains=irpf90LeftMargin,irpf90ContinueMark,irpf90SerialNumber
syn match	cIncluded		contained "<[^>]*>"
syn match	cInclude		"^\s*#\s*include\>\s*["<]" contains=cIncluded

"Synchronising limits assume that comment and continuation lines are not mixed
syn sync linecont "&" maxlines=40

""""IRPF90 specific
syn match   irpf90UnitHeader	"^\s*begin_shell\s*"
syn match   irpf90UnitHeader	"^\s*end_shell\s*$"
syn match   irpf90UnitHeader	"^\s*begin_template\s*"
syn match   irpf90UnitHeader	"^\s*end_template\s*$"
syn match   irpf90UnitHeader	"^\s*subst\s*$"
syn match   irpf90Comment	"^\s*begin_doc\s*"
syn match   irpf90Comment	"^\s*end_doc\s*$"
syn match   irpf90UnitHeader	"^\s*&*\s*begin_provider\s*"
syn match   irpf90UnitHeader	"^\s*end_provider\s*$"
syn match   irpf90UnitHeader	"^\s*assert"
syn match   irpf90UnitHeader	"^\s*touch"
syn match   irpf90UnitHeader	"^\s*soft_touch"
syn match   irpf90UnitHeader	"^\s*provide"
syn match   irpf90UnitHeader	"^\s*free"
syn match   irpf90UnitHeader	"^\s*irp_if"
syn match   irpf90UnitHeader	"^\s*irp_else"
syn match   irpf90UnitHeader	"^\s*irp_endif"
syn match   irpf90UnitHeader	"^\s*irp_read"
syn match   irpf90UnitHeader	"^\s*irp_write"
"""
if exists("irpf90_fold")

  syn sync fromstart
    syn region irpf90Program transparent fold keepend start="^\s*program\s\+\z(\a\w*\)" skip="^\s*[!#].*$" excludenl end="\<end\s*\(program\(\s\+\z1\>\)\=\|$\)" contains=ALLBUT,irpf90Module
    syn region irpf90Module transparent fold keepend start="^\s*module\s\+\(procedure\)\@!\z(\a\w*\)" skip="^\s*[!#].*$" excludenl end="\<end\s*\(module\(\s\+\z1\>\)\=\|$\)" contains=ALLBUT,irpf90Program
    syn region irpf90Function transparent fold keepend extend start="^\s*\(elemental \|pure \|recursive \)\=\s*function\s\+\z(\a\w*\)" skip="^\s*[!#].*$" excludenl end="\<end\s*\($\|function\(\s\+\z1\>\)\=\)" contains=ALLBUT,irpf90Program,irpf90Module
    syn region irpf90Subroutine transparent fold keepend extend start="^\s*\(elemental \|pure \|recursive \)\=\s*subroutine\s\+\z(\a\w*\)" skip="^\s*[!#].*$" excludenl end="\<end\s*\($\|subroutine\(\s\+\z1\>\)\=\)" contains=ALLBUT,irpf90Program,irpf90Module
    syn region irpf90BlockData transparent fold keepend start="\<block\s*data\s\+\z(\a\w*\)" skip="^\s*[!#].*$" excludenl end="\<end\s*\($\|block\s*data\(\s\+\z1\>\)\=\)" contains=ALLBUT,irpf90Program,irpf90Module,irpf90Subroutine,irpf90Function,irpf90Loop,irpf90Case,irpf90Loop,irpf90IfBlock
    syn region irpf90Interface transparent fold keepend extend start="^\s*interface\>" skip="^\s*[!#].*$" excludenl end="\<end\s*interface\>" contains=ALLBUT,irpf90Program,irpf90Module,irpf90Loop,irpf90Case,irpf90Loop,irpf90IfBlock

  if exists("irpf90_fold_conditionals")
      syn region irpf90Loop transparent fold keepend start="\<do\s\+\z(\d\+\)" end="^\s*\z1\>" contains=ALLBUT,irpf90UnitHeader,irpf90Structure,irpf90StorageClass,irpf90Type,irpf90Program,irpf90Module,irpf90Subroutine,irpf90Function,irpf90BlockData
      syn region irpf90Loop transparent fold keepend extend start="\(\<end\s\+\)\@<!\<do\(\s\+\a\|\s*$\)" skip="^\s*[!#].*$" excludenl end="\<end\s*do\>" contains=ALLBUT,irpf90UnitHeader,irpf90Structure,irpf90StorageClass,irpf90Type,irpf90Program,irpf90Module,irpf90Subroutine,irpf90Function,irpf90BlockData
      syn region irpf90IfBlock transparent fold keepend extend start="\(\<e\(nd\|lse\)\s\+\)\@<!\<if\s*(.\+)\s*then\>" skip="^\s*[!#].*$" end="\<end\s*if\>" contains=ALLBUT,irpf90UnitHeader,irpf90Structure,irpf90StorageClass,irpf90Type,irpf90Program,irpf90Module,irpf90Subroutine,irpf90Function,irpf90BlockData
      syn region irpf90Case transparent fold keepend extend start="\<select\s*case\>" skip="^\s*[!#].*$" end="\<end\s*select\>" contains=ALLBUT,irpf90UnitHeader,irpf90Structure,irpf90StorageClass,irpf90Type,irpf90Program,irpf90Module,irpf90Subroutine,irpf90Function,irpf90BlockData
  endif

  if exists("irpf90_fold_multilinecomments")
    syn match irpf90MultiLineComments transparent fold "\(^\s*!.*\(\n\|\%$\)\)\{4,}" contains=ALLBUT,irpf90MultiCommentLines
  endif
endif

if !exists("did_irpf90_syn_inits")
  command -nargs=+ HiLink hi def link <args>

  " The default highlighting differs for each dialect.
  " Transparent groups:
  " irpf90Paren, irpf90LeftMargin
  " irpf90Program, irpf90Module, irpf90Subroutine, irpf90Function,
  " irpf90BlockData
  " irpf90Loop, irpf90Loop, irpf90IfBlock, irpf90Case
  " irpf90MultiCommentLines
  HiLink irpf90Statement		Statement
  HiLink irpf90ConstructName	Special
  HiLink irpf90Conditional		Conditional
  HiLink irpf90Repeat		Repeat
  HiLink irpf90Todo			Todo
  HiLink irpf90ContinueMark		Todo
  HiLink irpf90String		String
  HiLink irpf90Number		Number
  HiLink irpf90Operator		Operator
  HiLink irpf90Boolean		Boolean
  HiLink irpf90LabelError		Error
  HiLink irpf90Obsolete		Todo
  HiLink irpf90Type			Type
  HiLink irpf90Structure		Type
  HiLink irpf90StorageClass		StorageClass
  HiLink irpf90Call			irpf90UnitHeader
  HiLink irpf90UnitHeader		irpf90PreCondit
  HiLink irpf90ReadWrite		irpf90Intrinsic
  HiLink irpf90IO			irpf90Intrinsic
  HiLink irpf90Intrinsic		irpf90Intrinsic
  HiLink irpf90Intrinsic		irpf90Intrinsic
  HiLink irpf90Intrinsic		Special

  HiLink irpf90StatementOb	Statement
  HiLink irpf9066Intrinsic	irpf90Intrinsic
  HiLink irpf90IntrinsicR	irpf90Intrinsic
  HiLink irpf90UnitHeaderR	irpf90PreCondit
  HiLink irpf90TypeR		irpf90Type
  HiLink irpf90StorageClassR	irpf90StorageClass
  HiLink irpf90OperatorR	irpf90Operator
  HiLink irpf90Include		Include
  HiLink irpf90StorageClassR	irpf90StorageClass

  HiLink irpf90LabelNumber	Special
  HiLink irpf90Target		Special
  HiLink irpf90FormatSpec		Identifier
  HiLink irpf90FloatDExp		irpf90Float
  HiLink irpf90FloatNoDec		irpf90Float
  HiLink irpf90FloatIniDec	irpf90Float
  HiLink irpf90FloatEndDec	irpf90Float
  HiLink irpf90TypeEx		irpf90Type
  HiLink irpf90IOEx		irpf90IO
  HiLink irpf90StatementEx	irpf90Statement
  HiLink irpf90StringEx		irpf90String
  HiLink irpf90IntrinsicEx	irpf90Intrinsic
  HiLink irpf90UnitHeaderEx	irpf90UnitHeader
  HiLink irpf90ConditionalEx	irpf90Conditional
  HiLink irpf90IntrinsicEx	irpf90Intrinsic

  HiLink irpf90Float		Float
  "Uncomment the next line if you want all irpf90 variables to be highlighted
" HiLink irpf90Identifier		Identifier
  HiLink irpf90PreCondit		PreCondit
  HiLink irpf90Include		Include
  HiLink cIncluded			Error
  HiLink cInclude			Error
  HiLink cPreProc			Error
  HiLink cPreCondit			Error
  HiLink irpf90ParenError		Error
  HiLink irpf90Comment		Comment
  HiLink irpf90SerialNumber		Todo
  HiLink irpf90Tab			Error
  " Vendor extensions
  HiLink irpf90ExtraIntrinsic	Special

  delcommand HiLink
endif

fun! ReadMan()
  let s:man_word = expand('<cword>')
  :exe ":!irpman " . s:man_word 
endfun
map K :call ReadMan()<CR>

" vim: ts=8 tw=132
