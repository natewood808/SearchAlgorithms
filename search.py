import math
import sys

from utils import *
from grid import *
from problem import Problem
from node import Node

fail = Node(Point(-1, -1))
expanded_count = 0


def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons


def expand(problem, node):
    """Generate all child nodes by considering the available
       actions for the state of the given 'node'"""
    global expanded_count
    expanded_count += 1
    s = node.state
    for action in problem.actions(s):
        result = problem.result(s, action)
        #TODO: Action-cost method
        cost = node.path_cost + problem.action_cost(result)
        yield Node(state=result, parent=node, action=action, path_cost=cost)


def calculate_heuristic(node, destination):
    """Calculates the straight line distance heuristic
       for the given 'node' relative to the 'destination'"""
    point1 = node.state.to_tuple()
    point2 = destination.to_tuple()

    return math.dist(point1, point2)


def depth_first_search(problem):
    frontier = Stack()
    reached = [problem.initial]
    frontier.push(Node(problem.initial))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node):
            return node
        for child in expand(problem, node):
            if child.state not in reached:
                reached.append(child.state)
                frontier.push(child)
    return fail


def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.isGoal(node):
        return node
    frontier = Queue()
    frontier.push(node)
    reached = [node.state]
    while not frontier.isEmpty():
        node = frontier.pop()
        for child in expand(problem, node):
            if problem.isGoal(child):
                return child
            if child.state not in reached:
                reached.append(child.state)
                frontier.push(child)
    return fail


def greedy_best_first_search(problem):
    node = Node(problem.initial)
    frontier = PriorityQueue()
    sld = calculate_heuristic(node, problem.goal)
    frontier.push(node, sld)
    reached = {node.state.to_tuple(): node}
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node):
            return node
        for child in expand(problem, node):
            if child.state.to_tuple() not in reached or child.path_cost < reached[child.state.to_tuple()].path_cost:
                reached[child.state.to_tuple()] = child
                sld = calculate_heuristic(child, problem.goal)
                frontier.update(child, sld)
    return fail


def a_star_search(problem):
    node = Node(problem.initial)
    frontier = PriorityQueue()
    sld = calculate_heuristic(node, problem.goal)
    heuristic = node.path_cost + sld
    frontier.push(node, heuristic)
    reached = {node.state.to_tuple(): node}
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node):
            return node
        for child in expand(problem, node):
            if child.state.to_tuple() not in reached or child.path_cost < reached[child.state.to_tuple()].path_cost:
                reached[child.state.to_tuple()] = child
                sld = calculate_heuristic(child, problem.goal)
                heuristic = child.path_cost + sld
                frontier.update(child, heuristic)
    return fail


if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world2_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world2_turfs.txt')

    source = Point(8, 10)
    dest = Point(43, 45)
    problem = Problem(source, dest, epolygons, tpolygons)


    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point

    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1) % len(polygon)].x], [polygon[i].y, polygon[(i+1) % len(polygon)].y])

    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1) % len(polygon)].x], [polygon[i].y, polygon[(i+1) % len(polygon)].y])

    #### Here call your search to compute and collect res_path

    print("1) Depth First Search\n2) Breadth First Search\n3) Greedy Best First Search\n4) A*")

    while True:
        choice = input("Select an algorithm 1-4: ")

        match choice:
            case "1":
                result_node = depth_first_search(problem)
                break
            case "2":
                result_node = breadth_first_search(problem)
                break
            case "3":
                result_node = greedy_best_first_search(problem)
                break
            case "4":
                result_node = a_star_search(problem)
                break
            case _:
                print("Invalid choice")

    if result_node.state != fail.state:
        res_path = result_node.construct_path()
        res_path.reverse()
        print(f"Path cost: {result_node.path_cost}")
        print(f"Number of Expanded Nodes: {expanded_count}")
    else:
        print("No path possible!")
        sys.exit()

    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        plt.pause(0.01)

    plt.show()
