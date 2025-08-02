def new_stack():
    return []

def push(stack, elem):
    return [elem] + stack

def pop(stack):
    match stack:
        case [head, *tail]:
            return head, tail
        case _:
            return None, stack
        
def is_empty(stack):
    return len(stack) == 0