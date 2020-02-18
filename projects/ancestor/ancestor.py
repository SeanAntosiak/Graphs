
def earliest_ancestor(ancestors, starting_node):
    next = []
    for x in ancestors:
        if x[1] == starting_node:
            next.append(x)
    if next == []:
        return(-1)
    else:
        ances = []
        while len(next) > 0:
            new_next = []
            for x in next:
                for y in ancestors:
                    if x[0] == y[1]:
                        new_next.append(y)
            if new_next:
                next = new_next
            else:
                for x in next:
                    ances.append(x[0])
                return(min(ances))
