from timeit import Timer

join_setup_list = """
def test(s1, s2, s3):
    return ''.join([s1, "foo", s2, "foo", s3])
a = 'foo' * 1000
b = 'baz' * 1000
c = 'bang' * 1000
"""

join_setup_tuple = """
def test(s1, s2, s3):
    return ''.join((s1, "foo", s2, "foo", s3))
a = 'foo' * 1000
b = 'baz' * 1000
c = 'bang' * 1000
"""

format_setup = """
def test(s1, s2, s3):
    return '{}foo{}foo{}'.format(s1, s2, s3)
a = 'foo' * 1000
b = 'baz' * 1000
c = 'bang' * 1000
"""


jointimer = Timer("test(a, b, c)", join_setup_list)
print(jointimer.timeit(number=20000000))
jointimer = Timer("test(a, b, c)", join_setup_tuple)
print(jointimer.timeit(number=20000000))
formattimer = Timer("test(a, b, c)", format_setup)
print(formattimer.timeit(number=20000000))