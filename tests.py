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
    assert m.gbyname("name") == b'Ahmed'
    assert m.gbyname("age")  == b'90'

    reg = Regex("(?P<name>\w+)\s(?P<age>\d+)")
    m = reg.match("Ahmed 90")
    assert m is not None
    assert m.group(0) == b"Ahmed 90"
    assert m.group(1) == b'Ahmed'
    assert m.group(2)  == b'90'


def test_findall_returns():
    reg = Regex("name")
    assert list(reg.ifindall("my name is ahmed and this is another name")) != []

def test_findall_returns_values():
    reg = Regex("name")
    assert len(list(reg.ifindall("my name is ahmed and this is another name"))) == 2