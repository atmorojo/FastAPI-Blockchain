from htpy import details, summary

def accordion(label, children, det_att="", sum_att=""):
    return details(det_att)[summary(sum_att)[label], children]
