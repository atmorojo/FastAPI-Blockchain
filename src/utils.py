
def pipe(value, *functions):
    for func in functions:
        value = func(value)
    return value
