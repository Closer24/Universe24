from event_universe.rows import CARRIER, PLANE


def fed_horizon(node, at):
    """test_the_node.fed_horizon copied by hand: the carrier's x axis line fed to 2 Gamma at the Node, its light to four times."""
    axis = node.row(CARRIER).lines[1]
    axis.now[at] = 2 * node.gamma
    axis.before[at] = 2 * node.gamma
    light = node.row(PLANE, gap=0).lines[0]
    light.now[at] = 4 * int(light.now[at])
    node.ride_walls()
    return node
