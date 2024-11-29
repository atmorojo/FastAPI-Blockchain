from templates import accordion

def nested_menu(label, children):
    return accordion(label, children, sum_att={"role": "link"})

