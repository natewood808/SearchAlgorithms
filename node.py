from grid import Point


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, sld=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.sld = sld

    def construct_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(Point(current_node.state.x, current_node.state.y))
            current_node = current_node.parent
        path.append(Point(current_node.state.x, current_node.state.y))

        return path
