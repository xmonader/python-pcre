from pcre import *


def test_simple_matching():
    patterns = ('abc', 'def', 'ghi')
    for pat in patterns:
        reg = Regex(pat)
        assert reg.match(pat) is not None

def test_matching_sentence():
    reg = Regex("my name is ahmed")
    assert reg.match("my name is ahmed") is not None


def test_not_matching_partial():
    reg = Regex("my name is ahmed")
    assert reg.match("my name") is None


def test_matching_caseless():
    reg = Regex("my name is ahmed", flags=PCRE_ANCHORED|CASELESS)
    assert reg.match("MY NAME IS AHMED") is not None


def test_complex_matching():
    reg = Regex("my name is \w+? and my age is \d+")
    assert reg.match("my name is ahmed and my age is 90") is not None


def test_complex_matching2():
    reg = Regex("\w+\d+")
    assert reg.match("ahmed90") is not None


def test_complex_matching_grouping():
    reg = Regex("(\w+)(\d+)")
    assert reg.match("ahmed90") is not None


def test_complex_matching_groups_len():
    reg = Regex("([a-z]+)(\d+)")
    m = reg.match("ahmed90")
    assert m is not None # 1
    assert len(list(m.groups())) == 3 # 2 + full match group

def test_complex_matching_groups_get():
    reg = Regex("([a-z]+)\s(\d+)")
    m = reg.match("ahmed 90")
    assert m is not None # 1
    groups = list(m.groups())
    assert groups[0] == b'ahmed 90' # FULL MATCH is group 0
    assert groups[1] == b'ahmed' 
    assert groups[2] == b'90'


def test_match_by_groupname():
    reg = Regex("(?P<name>[a-z]+)\s(?P<age>\d+)")
    m = reg.match("ahmed 90")
    assert m is not None


def test_get_by_index_namelessgroup():
    reg = Regex("(\w+)\s(\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    assert m.group(0) == b"Ahmed 90"
    assert m.group(1) == b'Ahmed'
    assert m.group(2)  == b'90'


def test_get_by_index_namedgroup():
    reg = Regex("(?P<name>\w+)\s(?P<age>\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    assert m.group_by_name("name") == b'Ahmed'
    assert m.group_by_name("age")  == b'90'

    reg = Regex("(?P<name>\w+)\s(?P<age>\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    assert m.group(0) == b"Ahmed 90"
    assert m.group(1) == b'Ahmed'
    assert m.group(2)  == b'90'


def test_isearch():
    reg = Regex("(\d+)")
    assert len([m.group() for m in reg.isearch("that 12 and more 32 as 311")])==3


def test_get_name_table():
    reg = Regex("(?P<name>\w+)\s(?P<age>\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    groupnames = m.get_name_table()
    assert len(groupnames) == 2
    assert set(groupnames) == {"name", "age"}

def test_groupdict():
    reg = Regex("(?P<name>\w+)\s(?P<age>\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    assert m.groupdict() == {'name':b'Ahmed', 'age':b'90'}


def test_split():
    reg = Regex("( SEP )")
    s = "hello SEP world SEP earth"
    assert len((list(reg.isplit(s)))) == 3
    assert list(reg.isplit(s)) == ['hello', 'world', 'earth']

    reg = Regex(",")
    s = "1,2,3"
    assert len((list(reg.isplit(s)))) == 3
    assert list(reg.isplit(s)) == ['1', '2', '3']


def test_sub():
    reg = Regex(",")
    s = "1,2,3"
    assert reg.sub(":::", s) == "1:::2:::3"


def test_subn():
    reg = Regex(",")
    s = "1,2,3"
    assert reg.subn(":::", s, count=1) == "1:::2,3"


def test_findall_returns():
    reg = Regex("name")
    assert list(reg.ifindall("my name is ahmed and this is another name")) != []


def test_findall_returns_values():
    reg = Regex("name")
    assert len(list(reg.ifindall("my name is ahmed and this is another name"))) == 2


def test_findall_group_returns_values():
    reg = Regex("\d+")
    assert len(list(reg.ifindall("he is 25 and she's 30"))) == 2
