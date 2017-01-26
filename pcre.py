#!usr/bin/env python

#       pypcre.py
#
#       Copyright 2009 ahmed youssef <xmonader@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from defs import *


class Regex(object):

    def __init__(self, pattern, flags=PCRE_ANCHORED):
        self.reg = self.compile(pattern, flags)
        self.flags = flags
        self.capcount = captured_count(self.reg)
        self.flags = 0

    def compile(self, pattern, flags):
        return compile(pattern, flags)

    def match(self, against, flags=None):
        if flags is None:
            flags = self.flags
        self._lastmatchagainst = against
        res = exec_match(self.reg, against, flags)
        if res:
            return Match(self.reg, against, flags, *res)
        return None



    def isearch(self, s, flags=None):
        x = 0
        while x < len(s):
            m = self.match(s[x:], flags)
            if m:
                # s=s[m.end():]
                yield m
                x += m.end()
            else:
                x += 1

    def ifindall(self, s, flags=None):
        x = 0
        while x < len(s):
            m = self.match(s[x:], flags)
            if m:
                yield m.group()
                x += m.end()
            else:
                x += 1

    def isplit(self, s, flags=None):
        x = 0
        lastafter = None
        while x < len(s):
            m = self.match(s[x:], flags)
            firsttime = True
            if m:
                before = s[:x + m.start()]
                after = s[x + m.end():]
                lastafter = after
                if firsttime:
                    yield before
                    firsttime = False
                else:
                    yield after
                s = s[x + m.end():]
            else:
                x += 1
        yield lastafter

    def sub(self, repl, s, flags=None):
        x = 0
        while x < len(s):
            m = self.match(s[x:], flags)
            if m:
                sbeforematch = s[:x]
                sinmatch = s[x + m.start():x + m.end()]
                safter = s[x + m.end():]
                s = sbeforematch + repl + safter
                x = m.end()
            else:
                x += 1
        return s

    replace = sub

    def subn(self, repl, s, flags=None, count=10):
        x = 0
        while x < len(s) and count != 0:
            m = self.match(s[x:], flags)
            if m:
                sbeforematch = s[:x]
                sinmatch = s[x + m.start():x + m.end()]
                safter = s[x + m.end():]
                s = sbeforematch + repl + safter
                count -= 1  # dec
                x = m.end()
            else:
                x += 1
        return s

    replacen = subn

    def expand(self):
        raise NotImplementedError


class Match(object):

    def __init__(self, reg, against, flags, rc, ovec):
        self.reg = reg
        self.against = bytes(against, encoding='utf8')
        self.flags = flags
        self._rc = rc
        self._ovec = ovec
        self.capcount = captured_count(self.reg)
        self._groupdict = {}

    def groups(self):
        for i in range(self.capcount+1):
            if self.group(i):
                yield self.group(i)
    
    #FIXME: build index here not just fetch the names 
    ## TOO SLOW.
    def get_name_table(self):
        p = c_char_p()
        namecount = captured_count(self.reg)
        entrysize = c_int()
        table = c_char_p()
        capcount = captured_count(self.reg)

        pcre_fullinfo(self.reg, None, PCRE_INFO_NAMEENTRYSIZE, byref(entrysize))
        pcre_fullinfo(self.reg, None, PCRE_INFO_NAMETABLE, byref(table)) 
        tbl = cast(table, POINTER(c_char))
        #WIP
        groups = []
        for i in range(namecount):
            # key starts from tbl[2] 
            gname = b""
            idx = 2
            while tbl[idx] != b"\x00":
                gname += (tbl[idx])
                idx += 1
            groups.append(gname.decode('utf8'))
            # import pdb; pdb.set_trace()
            void_p = cast(tbl, c_voidp).value+entrysize.value
            tbl = cast(void_p, POINTER(c_char))

        return groups

    def groupdict(self):
        for gname in self.get_name_table():
            gname = str(gname)
            self._groupdict[gname] = self.group(gname)
        return self._groupdict


    def group(self, n=0):
        # n: int or n:string
        if isinstance(n, int):
            # groupIndex
            if n > self.capcount:
                raise IndexError('groupIndex<%d> must be < %d' %
                                 (n, self.capcount))
            i = n * 2
            if self._ovec[i] < 0:
                return None
            return self.against[self._ovec[i]: self._ovec[i + 1]]

        elif isinstance(n, str):
            # groupByName
            gidx = self._group_index_by_name(n)
            return self.group(gidx)

    # EXPERIMENTAL
# int pcre_get_named_substring(const pcre *code,
            # const char *subject, int *ovector,
            # int stringcount, const char *stringname,
            # const char **stringptr);
    def group_by_name(self, n):
        n = bytes(n, encoding='utf8')
        p = c_char_p()
        r = pcre_get_named_substring(self.reg, c_char_p(
            self.against), self._ovec, self._rc, c_char_p(n),  byref(p))
        return p.value

    def _group_index_by_name(self, n):
        n = bytes(n, encoding='utf8')
        return pcre_get_stringnumber(self.reg, c_char_p(n))

    def span(self, n=0):
        return self.start(n), self.end(n)  # tuple

    def start(self, n=0):
        if isinstance(n, str):
            n = self._group_index_by_name(n)
            return self.start(n)
        elif isinstance(n, int):
            return self._ovec[n * 2]
        else:
            raise ValueError

    def end(self, n=0):
        if isinstance(n, str):
            n = self._group_index_by_name(n)
            return self.end(n)
        elif isinstance(n, int):
            return self._ovec[n * 2 + 1]
        else:
            raise ValueError

    def __str__(self):
        return "pcre.Match<{_id}> span: {span}".format(_id=id(self), span=self.span())
