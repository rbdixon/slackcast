import pyparsing as pp

__all__ = ['command_parser']

def expand(t):
    if len(t) == 3:
        if t[0] < t[2]:
            return list(range(t[0], t[2]+1))

    return t[0]

# Channel or user indicator
channel = pp.Word('@' + pp.alphanums)
person = pp.Word('#' + pp.alphanums)
join_target = channel | person

# off
off = 'off'

# History list
integer = pp.Word(pp.nums)
int_range = integer + pp.Optional('-' + integer)
integer.setParseAction(lambda t:int(t[0]))
int_range.setParseAction(expand)

join_or_history = join_target + pp.Optional(int_range)

command_parser = (off | join_or_history) + pp.LineEnd()
