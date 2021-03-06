
from ctypes import *
libpcre = None
try:
    libpcre = CDLL("libpcre.so")
except ImportError:
    print("libpcre is not installed.")
    exit(-1)

# CONSTANTS
# The current PCRE version information.
PCRE_MAJOR = 7
PCRE_MINOR = 8
PCRE_DATE = "2008-09-05"

# OPTIONS
CASELESS = IGNORECASE = I = PCRE_CASELESS = 0x00000001
MULTILINE = M = PCRE_MULTILINE = 0x00000002
DOTALL = S = PCRE_DOTALL = 0x00000004
PCRE_EXTENDED = 0x00000008
ANCHORED = PCRE_ANCHORED = 0x00000010
DOLLARENDONLY = PCRE_DOLLAR_ENDONLY = 0x00000020
PCRE_EXTRA = 0x00000040
PCRE_NOTBOL = 0x00000080
PCRE_NOTEOL = 0x00000100
PCRE_UNGREEDY = 0x00000200
PCRE_NOTEMPTY = 0x00000400
UNICODE = U = PCRE_UTF8 = 0x00000800
PCRE_NO_AUTO_CAPTURE = 0x00001000
PCRE_NO_UTF8_CHECK = 0x00002000
PCRE_AUTO_CALLOUT = 0x00004000
PCRE_PARTIAL = 0x00008000
PCRE_DFA_SHORTEST = 0x00010000
PCRE_DFA_RESTART = 0x00020000
PCRE_FIRSTLINE = 0x00040000
PCRE_DUPNAMES = 0x00080000
PCRE_NEWLINE_CR = 0x00100000
PCRE_NEWLINE_LF = 0x00200000
PCRE_NEWLINE_CRLF = 0x00300000
PCRE_NEWLINE_ANY = 0x00400000
PCRE_NEWLINE_ANYCRLF = 0x00500000
PCRE_BSR_ANYCRLF = 0x00800000
PCRE_BSR_UNICODE = 0x01000000
PCRE_JAVASCRIPT_COMPAT = 0x02000000


# Exec-time and get/set-time error codes
PCRE_ERROR_NOMATCH = -1
PCRE_ERROR_NULL = -2
PCRE_ERROR_BADOPTION = -3
PCRE_ERROR_BADMAGIC = -4
PCRE_ERROR_UNKNOWN_OPCODE = -5
PCRE_ERROR_UNKNOWN_NODE = -5
PCRE_ERROR_NOMEMORY = -6
PCRE_ERROR_NOSUBSTRING = -7
PCRE_ERROR_MATCHLIMIT = -8
PCRE_ERROR_CALLOUT = -9
PCRE_ERROR_BADUTF8 = -10
PCRE_ERROR_BADUTF8_OFFSET = -11
PCRE_ERROR_PARTIAL = -12
PCRE_ERROR_BADPARTIAL = -13
PCRE_ERROR_INTERNAL = -14
PCRE_ERROR_BADCOUNT = -15
PCRE_ERROR_DFA_UITEM = -16
PCRE_ERROR_DFA_UCOND = -17
PCRE_ERROR_DFA_UMLIMIT = -18
PCRE_ERROR_DFA_WSSIZE = -19
PCRE_ERROR_DFA_RECURSE = -20
PCRE_ERROR_RECURSIONLIMIT = -21
PCRE_ERROR_NULLWSLIMIT = -22
PCRE_ERROR_BADNEWLINE = -23

# Request types for pcre_fullinfo()
PCRE_INFO_OPTIONS = 0
PCRE_INFO_SIZE = 1
PCRE_INFO_CAPTURECOUNT = 2
PCRE_INFO_BACKREFMAX = 3
PCRE_INFO_FIRSTBYTE = 4
PCRE_INFO_FIRSTCHAR = 4
PCRE_INFO_FIRSTTABLE = 5
PCRE_INFO_LASTLITERAL = 6
PCRE_INFO_NAMEENTRYSIZE = 7
PCRE_INFO_NAMECOUNT = 8
PCRE_INFO_NAMETABLE = 9
PCRE_INFO_STUDYSIZE = 10
PCRE_INFO_DEFAULT_TABLES = 11
PCRE_INFO_OKPARTIAL = 12
PCRE_INFO_JCHANGED = 13
PCRE_INFO_HASCRORLF = 14


#/* Request types for pcre_config(). Do not re-arrange, in order to remain compatible.
PCRE_CONFIG_UTF8 = 0
PCRE_CONFIG_NEWLINE = 1
PCRE_CONFIG_LINK_SIZE = 2
PCRE_CONFIG_POSIX_MALLOC_THRESHOLD = 3
PCRE_CONFIG_MATCH_LIMIT = 4
PCRE_CONFIG_STACKRECURSE = 5
PCRE_CONFIG_UNICODE_PROPERTIES = 6
PCRE_CONFIG_MATCH_LIMIT_RECURSION = 7
PCRE_CONFIG_BSR = 8

#/* Bit flags for the pcre_extra structure. Do not re-arrange or redefine these bits,
# just add new ones on the end, in order to remain compatible.
PCRE_EXTRA_STUDY_DATA = 0x0001
PCRE_EXTRA_MATCH_LIMIT = 0x0002
PCRE_EXTRA_CALLOUT_DATA = 0x0004
PCRE_EXTRA_TABLES = 0x0008
PCRE_EXTRA_MATCH_LIMIT_RECURSION = 0x0010


# TYPES
realpcre = c_void_p
PCRE_SPTR = c_char_p


#/* The structure for passing additional data to pcre_exec(). This is defined in
# such as way as to be extensible. Always add new fields at the end, in order to
# remain compatible. */

# typedef struct pcre_extra {
# unsigned long int flags;        /* Bits for which fields are set */
# void *study_data;               /* Opaque data from pcre_study() */
# unsigned long int match_limit;  /* Maximum number of calls to match() */
# void *callout_data;             /* Data passed back in callouts */
# const unsigned char *tables;    /* Pointer to character tables */
# unsigned long int match_limit_recursion; /* Max recursive calls to match() */
#} pcre_extra;


class pcre_extra(Structure):
    _fields_ = [
        ("flags", c_long),
        ("data", c_void_p),
        ("callout", c_void_p),
        ("tables", c_char_p),
        ("match_limit_recursion", c_ulong)
    ]

pcre_extra_p = POINTER(pcre_extra)
pcre_p = c_void_p

# typedef struct pcre_callout_block {
# int          version;           /* Identifies version of block */
#/* ------------------------ Version 0 ------------------------------- */
# int          callout_number;    /* Number compiled into pattern */
# int         *offset_vector;     /* The offset vector */
# PCRE_SPTR    subject;           /* The subject being matched */
# int          subject_length;    /* The length of the subject */
# int          start_match;       /* Offset to start of this match attempt */
# int          current_position;  /* Where we currently are in the subject */
# int          capture_top;       /* Max current capture */
# int          capture_last;      /* Most recently closed capture */
# void        *callout_data;      /* Data passed in with the call */
#/* ------------------- Added for Version 1 -------------------------- */
# int          pattern_position;  /* Offset to next item in the pattern */
# int          next_item_length;  /* Length of next item in the pattern */
#/* ------------------------------------------------------------------ */
#} pcre_callout_block;

# FUNCTIONS


class pcre_callout_block(Structure):
    _fields_ = [
        ("callout_number", c_int),
        ("offset_vector", POINTER(c_int)),
        ("subject", PCRE_SPTR),
        ("subject_length", c_int),
        ("start_match", c_int),
        ("current_position", c_int),
        ("capture_top", c_int),
        ("capture_last", c_int),
        ("callout_data", c_char_p),
        ("pattern_position", c_int),
        ("next_item_length", c_int)
    ]

#/* Exported PCRE functions */

# PCRE_EXP_DECL pcre *pcre_compile(const char *, int, const char **, int *,
    # const unsigned char *);

# pcre *pcre_compile(const char *pattern, int options,
    # const char **errptr, int *erroffset,
    # const unsigned char *tableptr);


pcre_compile = libpcre.pcre_compile
pcre_compile.restype = c_void_p
pcre_compile.argstype = [c_char_p, c_int, POINTER(
    c_char_p), POINTER(c_int), POINTER(c_ubyte)]


def compile(pattern, flags=PCRE_ANCHORED):
    pattern = bytes(pattern, encoding="utf8")
    s = c_char_p(pattern)
    options = c_int(flags)
    errptr = c_char_p()
    erroffset = c_int(0)
    tableptr = c_char_p()
    reg = pcre_compile(s, options, byref(errptr), byref(erroffset), None)
    return reg


# PCRE_EXP_DECL pcre *pcre_compile2(const char *, int, int *, const char **,
    # int *, const unsigned char *);

# pcre *pcre_compile2(const char *pattern, int options,
    #int *errorcodeptr,
    # const char **errptr, int *erroffset,
    # const unsigned char *tableptr);


pcre_compile2 = libpcre.pcre_compile2
pcre_compile2.restype = c_char_p
pcre_compile2.argstype = [c_char_p, c_int, POINTER(c_char_p), POINTER(
    c_int), POINTER(c_char_p), POINTER(c_int), c_ubyte]


# PCRE_EXP_DECL int  pcre_config(int, void *);
pcre_config = libpcre.pcre_config
pcre_config.restype = c_int
pcre_config.argstype = [c_int, c_void_p]


# PCRE_EXP_DECL int  pcre_copy_named_substring(const pcre *, const char *,
# int *, int, const char *, char *, int);
pcre_copy_named_substring = libpcre.pcre_copy_named_substring
pcre_copy_named_substring.restype = c_int
pcre_copy_named_substring.argstype = [c_void_p, c_char_p]

# PCRE_EXP_DECL int  pcre_copy_substring(const char *, int *, int, int, char *,
# int);
pcre_copy_substring = libpcre.pcre_copy_substring
pcre_copy_substring.restype = c_int
pcre_copy_substring.argstype = [
    c_char_p, POINTER(c_int), c_int, c_int, c_char_p, c_int]

# PCRE_EXP_DECL int  pcre_dfa_exec(const pcre *, const pcre_extra *,
# const char *, int, int, int, int *, int , int *, int);
pcre_dfa_exec = libpcre.pcre_dfa_exec
pcre_dfa_exec.restype = c_int
pcre_dfa_exec.argstype = [pcre_p, pcre_extra_p, c_char_p, c_int,
                          c_int, c_int, POINTER(c_int), c_int, POINTER(c_int), c_int]

# int pcre_exec(const pcre *code, const pcre_extra *extra,
# const char *subject, int length, int startoffset,
# int options, int *ovector, int ovecsize);


# PCRE_EXP_DECL int  pcre_exec(const pcre *, const pcre_extra *, PCRE_SPTR,
# int, int, int, int *, int);
pcre_exec = libpcre.pcre_exec
pcre_exec.restype = c_int
pcre_exec.argstype = [pcre_p, pcre_extra_p, PCRE_SPTR,
                      c_int, c_int, c_int, POINTER(c_int), c_int]

# PCRE_EXP_DECL void pcre_free_substring(const char *);
pcre_free_substring = libpcre.pcre_free_substring
pcre_free_substring.restype = None
pcre_free_substring.argstype = [c_char_p]

# PCRE_EXP_DECL void pcre_free_substring_list(const char **);
pcre_free_substring_list = libpcre.pcre_free_substring_list
pcre_free_substring_list.restype = None
pcre_free_substring_list.argstype = [POINTER(c_char_p)]


# int pcre_fullinfo(const pcre *code, const pcre_extra *extra,
# int what, void *where);

# PCRE_EXP_DECL int  pcre_fullinfo(const pcre *, const pcre_extra *, int,
# void *);
pcre_fullinfo = libpcre.pcre_fullinfo
pcre_fullinfo.restype = c_int
pcre_fullinfo.argstype = [pcre_p, pcre_extra_p, c_int, c_void_p]


# PCRE_EXP_DECL int  pcre_get_named_substring(const pcre *, const char *,
# int *, int, const char *, const char **);

# int pcre_get_named_substring(const pcre *code,
# const char *subject, int *ovector,
# int stringcount, const char *stringname,
# const char **stringptr);

pcre_get_named_substring = libpcre.pcre_get_named_substring
pcre_get_named_substring.restype = c_int
pcre_get_named_substring.argstype = [
    pcre_p, c_char_p, POINTER(c_int), c_int, c_char_p, POINTER(c_char_p)]


# PCRE_EXP_DECL int  pcre_get_stringnumber(const pcre *, const char *);
pcre_get_stringnumber = libpcre.pcre_get_stringnumber
pcre_get_stringnumber.restype = c_int
pcre_get_stringnumber.argstype = [pcre_p, c_char_p]

# PCRE_EXP_DECL int  pcre_get_stringtable_entries(const pcre *, const char *,
# char **, char **);
pcre_get_stringtable_entries = libpcre.pcre_get_stringtable_entries
pcre_get_stringtable_entries.restype = c_int
pcre_get_stringtable_entries.argstype = [
    pcre_p, c_char_p, POINTER(c_char_p), POINTER(c_char_p)]

# PCRE_EXP_DECL int  pcre_get_substring(const char *, int *, int, int,
# const char **);
pcre_get_substring = libpcre.pcre_get_substring
pcre_get_substring.restype = c_int
pcre_get_substring.argstype = [c_char_p, POINTER(
    c_int), c_int, c_int, POINTER(c_char_p)]

# PCRE_EXP_DECL int  pcre_get_substring_list(const char *, int *, int,
# const char ***);
pcre_get_substring_list = libpcre.pcre_get_substring_list
pcre_get_substring_list.restype = c_int
pcre_get_substring_list.argstype = [
    c_char_p, POINTER(c_int), c_int, POINTER(POINTER(c_char_p))]

# PCRE_EXP_DECL int  pcre_info(const pcre *, int *, int *);
pcre_info = libpcre.pcre_info
pcre_info.restype = c_int
pcre_info.argstype = [pcre_p, POINTER(c_int), POINTER(c_int)]

# PCRE_EXP_DECL const unsigned char *pcre_maketables(void);
pcre_maketables = libpcre.pcre_maketables
pcre_maketables.restype = POINTER(POINTER(c_ubyte))

# PCRE_EXP_DECL int  pcre_refcount(pcre *, int);
pcre_refcount = libpcre.pcre_refcount
pcre_refcount.restype = c_int
pcre_refcount.argstype = [pcre_p, c_int]

# PCRE_EXP_DECL pcre_extra *pcre_study(const pcre *, int, const char **);
pcre_study = libpcre.pcre_study
pcre_study.restype = pcre_extra_p
pcre_study.argstype = [pcre_p, c_int, POINTER(c_char_p)]

# PCRE_EXP_DECL const char *pcre_version(void);
pcre_version = libpcre.pcre_version
pcre_version.restype = c_char_p


def captured_count(code):
    capcount = c_long()
    pcre_fullinfo(code, None, PCRE_INFO_CAPTURECOUNT, byref(capcount))
    return capcount.value

def exec_match(reg, against, flags=0):
    against = bytes(against, encoding="utf8")
    sagainst = c_char_p(against)
    slen = len(against)
    ncapcount = captured_count(reg)
    ovecsize = (ncapcount + 1) * 3
    ovectype = (c_int * ovecsize)
    ovec = ovectype()

    p_pcre_extra = pcre_extra_p()
    rc = pcre_exec(reg, p_pcre_extra, sagainst, slen, 0, flags, ovec, ovecsize)
    if rc < 0:
        return None
    else:
        return rc, ovec