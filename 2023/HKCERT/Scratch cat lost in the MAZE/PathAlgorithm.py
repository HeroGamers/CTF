import asyncio
import heapq
import math
import os
from typing import Any, Optional, List, Tuple, Set, Dict, Union
import numpy as np

# Taken from an old project of mine

def calculate_distance(position1: Tuple[int, int], position2: Tuple[int, int]) -> float:
    """
    Calculates the distance between two points.

    Args:
        position1 (Tuple[int, int]): The first position.
        position2 (Tuple[int, int]): The second position.

    Returns:
        float: The distance between the two points.
    """
    return abs(math.sqrt(pow(position1[0] - position2[0], 2) + pow(position1[1] - position2[1], 2)))

class Node:
    def __init__(self, coordinates: tuple) -> None:
        """
        Initializes a new instance of the Node class.

        Args:
            coordinates (tuple): The coordinates of the node as a tuple of (x, y).

        Returns:
            None
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.neighbours: List[Dict[str, Union['Node', float]]] = []

    def __lt__(self, other: Any) -> bool:
        """
        Less than comparison operator.

        Args:
            other (Any): The other object to compare.

        Returns:
            bool: Always returns True.
        """
        return True

    def __le__(self, other: Any) -> bool:
        """
        Less than or equal to comparison operator.

        Args:
            other (Any): The other object to compare.

        Returns:
            bool: Always returns True.
        """
        return True

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the position of the node as a tuple of (x, y) coordinates.

        Returns:
            Tuple[int, int]: The position of the node.
        """
        return self.x, self.y

    def add_neighbour(self, node: 'Node', weight: float = None) -> None:
        """
        Adds a neighbour node with an optional weight to the current node.

        Args:
            node (Node): The neighbour node to add.
            weight (float, optional): The weight of the edge connecting the nodes. If not provided,
                the weight is calculated based on the Euclidean distance between the nodes.

        Returns:
            None
        """
        if not weight:
            if self.x == node.x or self.y == node.y:
                weight = max(abs(self.x - node.x), abs(self.y - node.y))
            else:
                weight = calculate_distance(self.get_position(), node.get_position())
        self.neighbours.append({"node": node, "weight": weight})

    def remove_neighbour(self, node: 'Node') -> None:
        """
        Removes a neighbour node from the current node.

        Args:
            node (Node): The neighbour node to remove.

        Returns:
            None
        """
        for i in range(len(self.neighbours)):
            if self.neighbours[i]["node"] == node:
                self.neighbours.pop(i)
                return

    def get_neighbour_nodes(self) -> List['Node']:
        """
        Returns a list of neighbour nodes.

        Returns:
            List[Node]: A list of neighbour nodes.
        """
        return [neighbour["node"] for neighbour in self.neighbours]

class NodeData:
    def __init__(self, node: Node, g: float = math.inf, h: float = math.inf, parent: Optional[Node] = None) -> None:
        """
        Initializes a new instance of the NodeData class.

        Args:
            node (Node): The node associated with the data.
            g (float): The cost from the start node to the current node.
            h (float): The estimated cost from the current node to the goal node.
            parent (Optional[Node]): The parent node. Defaults to None.

        Returns:
            None
        """
        self.node = node
        self.g = g
        self.h = h
        self.parent = parent

        self.f = self.g + self.h

    def __lt__(self, other: Any) -> bool:
        """
        Less than comparison operator.

        Args:
            other (Any): The other object to compare.

        Returns:
            bool: Always returns True.
        """
        return True

    def __le__(self, other: Any) -> bool:
        """
        Less than or equal to comparison operator.

        Args:
            other (Any): The other object to compare.

        Returns:
            bool: Always returns True.
        """
        return True


class Graph:
    def __init__(self, size_x: int = 51, size_y: int = 51) -> None:
        """
        Initializes a new instance of the Graph class.
        :param size_x: The width of the graph.
        :param size_y: The height of the graph.
        """
        if size_x and size_y:
            range_x = range(size_x)
            range_y = range(size_y)
            self.nodes: np.ndarray[Node] = np.empty((size_y, size_x), dtype=Node)

            # Create nodes
            for y in range_y:
                for x in range_x:
                    pos = (x, y)
                    node = Node(pos)
                    self.nodes[y, x] = node

            # Connect neighbors
            rows, cols = self.nodes.shape

            for y in range(rows):
                for x in range(cols):
                    pass

    def get_node(self, pos: tuple) -> Optional[Node]:
        """
        Gets the node at the specified position.
        :param pos: The position of the node.
        :return: The node at the specified position.
        """
        if 0 <= pos[0] < len(self.nodes[0]) and 0 <= pos[1] < len(self.nodes):
            return self.nodes[pos[1]][pos[0]]
        else:
            print(f"Node with position {pos} not found, not within x and y bounds = ({len(self.nodes[0])}, {len(self.nodes)})")
            return None

    def add_edge(self, node_1: Node, node_2: Node) -> None:
        """
        Adds an edge between two nodes.
        :param node_1: The first node.
        :param node_2: The second node.
        :return: None
        """
        if node_1 is not node_2 and node_1 and node_2:
            if node_2 not in node_1.get_neighbour_nodes():
                node_1.add_neighbour(node_2)
            if node_1 not in node_2.get_neighbour_nodes():
                node_2.add_neighbour(node_1)

    def remove_edge(self, node_1: Node, node_2: Node) -> None:
        """
        Removes an edge between two nodes.
        :param node_1: The first node.
        :param node_2: The second node.
        :return: None
        """
        if node_1 is not node_2 and node_1 and node_2:
            if node_2 in node_1.get_neighbour_nodes():
                node_1.remove_neighbour(node_2)
            if node_1 in node_2.get_neighbour_nodes():
                node_2.remove_neighbour(node_1)

    # Manhattan Distance heuristic for A*
    def h(self, start_node: Node, dst_node: Node) -> float:
        """
        The heuristic function for A*. This is the Manhattan Distance.
        :param start_node: The start node.
        :param dst_node: The destination node.
        :return: The heuristic value.
        """
        dx = abs(start_node.x - dst_node.x)
        dy = abs(start_node.y - dst_node.y)
        return dx + dy

    # Get path and cost using A*
    def get_path(self, start_node: Node, dst_node: Node) -> List[NodeData]:
        """
        Gets the path between two nodes using A*.
        :param start_node: The start node.
        :param dst_node: The destination node.
        :return: A list of nodes in the path.
        """
        # print(f"Getting path between {start_node.x}, {start_node.y} and {dst_node.x}, {dst_node.y}")

        # Initialize the start node data
        start_node_data = NodeData(start_node, 0, self.h(start_node, dst_node), None)

        # Create open and closed sets
        open_set: Set[Node] = {start_node}
        closed_set: Dict[Node, NodeData] = {}

        # A dictionary to store the best known cost from start to each node
        g_scores: Dict[Node, float] = {start_node: 0}

        # A dictionary to store the estimated total cost from start to each node
        f_scores: Dict[Node, float] = {start_node: start_node_data.f}

        # A priority queue to efficiently extract the node with the lowest f-score
        open_queue: List[Tuple[float, Node]] = [(f_scores[start_node], start_node)]

        # A counter to track the number of iterations
        iteration = 0

        # The current node
        current_node: Node
        while open_queue:
            iteration += 1

            _, current_node = heapq.heappop(open_queue)

            closed_set[current_node] = NodeData(
                node=current_node,
                g=g_scores[current_node],
                h=self.h(current_node, dst_node),
                parent=closed_set.get(current_node, None).parent if closed_set.get(current_node, None) else None
            )

            if current_node is dst_node:
                # Destination reached, construct and return the final path
                final_path: List[NodeData] = []
                while current_node:
                    final_path.insert(0, closed_set[current_node])
                    current_node = closed_set[current_node].parent
                return final_path

            for neighbour in current_node.neighbours:
                neighbour_node: Node = neighbour["node"]
                neighbour_weight: float = neighbour["weight"]

                if neighbour_node in closed_set:
                    continue

                neighbour_g_score = g_scores[current_node] + neighbour_weight

                if neighbour_node not in open_set:
                    # Add the neighbour to the open set
                    neighbour_data = NodeData(
                        node=neighbour_node,
                        g=neighbour_g_score,
                        h=self.h(neighbour_node, dst_node),
                        parent=current_node
                    )
                    open_set.add(neighbour_node)
                    closed_set[neighbour_node] = neighbour_data
                    g_scores[neighbour_node] = neighbour_g_score
                    f_scores[neighbour_node] = neighbour_data.f
                    heapq.heappush(open_queue, (f_scores[neighbour_node], neighbour_node))
                elif neighbour_g_score < g_scores[neighbour_node]:
                    # Update the neighbour's scores and parent if a better path is found
                    neighbour_data = closed_set[neighbour_node]
                    neighbour_data.g = neighbour_g_score
                    neighbour_data.parent = current_node
                    g_scores[neighbour_node] = neighbour_g_score
                    f_scores[neighbour_node] = neighbour_data.f
                    heapq.heapify(open_queue)

        # No path found
        return []
