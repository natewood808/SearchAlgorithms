import copy
import matplotlib.path
import numpy

from grid import Point


class Problem:
    def __init__(self, initial, goal, epolygons, tpolygons):
        self.initial = initial
        self.goal = goal
        self.epaths = self.gen_epaths(epolygons)
        self.tpaths = self.gen_tpaths(tpolygons)

    def isGoal(self, node):
        return node.state.__eq__(self.goal)

    def actions(self, state):
        """Returns a set of actions that is possible from
           the given 'state'. This is where I will filter out
           points available to go to if they fall off the grid
           or land inside a polygon"""
        actions = []
        if state.y + 1 <= 49:
            actions.append("up")
            # Check each polygon to see if the new point is contained within that polygon
            for path in self.epaths:
                if path.contains_point((state.x, state.y + 1), radius=-0.1):
                    actions.remove("up")
        if state.x + 1 <= 49:
            actions.append("right")
            for path in self.epaths:
                if path.contains_point((state.x + 1, state.y), radius=-0.1):
                    actions.remove("right")
        if state.y - 1 >= 0:
            actions.append("down")
            for path in self.epaths:
                if path.contains_point((state.x, state.y - 1), radius=-0.1):
                    actions.remove("down")
        if state.x - 1 >= 0:
            actions.append("left")
            for path in self.epaths:
                if path.contains_point((state.x - 1, state.y), radius=-0.1):
                    actions.remove("left")

        return actions

    def action_cost(self, result):
        """Returns 1.5 if the 'result' state is inside a turf
           polygon, otherwise return 1"""
        for path in self.tpaths:
            if path.contains_point((result.x, result.y), radius=-0.1):
                return 1.5
        return 1

    def result(self, initial, action):
        """Returns the state that results in doing 'action'
           on the 'initial' state"""
        result = copy.copy(initial)
        match action:
            case "up":
                result.y += 1
                return result
            case "right":
                result.x += 1
                return result
            case "down":
                result.y -= 1
                return result
            case "left":
                result.x -= 1
                return result

    def gen_epaths(self, epolygons):
        """Generates a list of matplotlib.path.Path objects
           with each Path object representing an enclosure polygon"""
        epath_list = []
        for polygon in epolygons:
            point_list = []
            for point in polygon:
                point_list.append([point.x, point.y])
            path = matplotlib.path.Path(numpy.asarray(point_list))
            epath_list.append(path)
        return epath_list

    def gen_tpaths(self, tpolygons):
        """Generates a list of matplotlib.path.Path objects
           with each Path object representing a turf polygon"""
        tpath_list = []
        for polygon in tpolygons:
            point_list = []
            for point in polygon:
                point_list.append([point.x, point.y])
            path = matplotlib.path.Path(numpy.asarray(point_list))
            tpath_list.append(path)
        return tpath_list
