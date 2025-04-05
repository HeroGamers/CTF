from __future__ import annotations

PAIRINGS = {
    "M": ["A"],
    "A": ["S"],
    "S": []
}

class Node:
    def __init__(self, letter: str, position: tuple[int, int]):
        self.letter = letter
        self.position = position
        #print(f"Created: {str(self)}")
        self.neighbours: list[tuple[int, Node]] = []
    
    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.letter == other.letter and self.position == other.position

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return True
    
    def add_neighbour(self, neighbour: Node):
        if not neighbour:
            return
        #print(f"- Adding {str(neighbour)} as neighbour to {str(self)}")
        weight = -1
        if self.letter in PAIRINGS and neighbour.letter in PAIRINGS[self.letter]:
            #print(f"Letter neighbour found, setting weight to 1")
            weight = 1
        
        if not neighbour in [n[1] for n in self.neighbours]:
            self.neighbours.append((weight, neighbour))
        # if not self in [n[1] for n in neighbour.neighbours]:
        #     neighbour.neighbours.append((weight, self))

        # Sort
        self.neighbours.sort()
        # neighbour.neighbours.sort()
    
    def get_neighbours(self, graph: WordGraph):
        #print(f"Getting neighbours for {str(self)}")
        x, y = self.position
        for dx in [x-1, x+1]:
            for dy in [y-1, y+1]:
                #print(f"Getting neighbour at {dx}, {dy}")
                neighbour = graph.get_node(dx, dy)
                if neighbour:
                    if neighbour.position != (dx, dy):
                        #print(f"{str(neighbour)} does not have position ({dx}, {dy})")
                        raise Exception
                    self.add_neighbour(neighbour)
                # else:
                #     print(f"No neighbour found")
    
    def get_valid_neighbours(self) -> list[Node]:
        return [neighbour[1] for neighbour in self.neighbours if neighbour[0] == 1]
    
    def get_xmases(self, parent: Node = None) -> list[list[Node]]:
        #print(f"Getting xmas for {str(self)}")
        valid_neighbours = self.get_valid_neighbours()
        #print(f"Valid neighbours: {[str(neighbour) for neighbour in valid_neighbours]}")
        if not parent:
            xmases = [node.get_xmases(self) for node in valid_neighbours]
            #print(f"xmases: {xmases}")
            valid_xmases = [xmas for xmas in xmases if len(xmas) == 3]
            #print(f"valid xmases: {valid_xmases}")
            return valid_xmases
        
        if self.letter == "S":
            return [parent, self]
        
        # Get current direction from parent
        x, y = self.position
        px, py = parent.position
        dx, dy = (x-px, y-py)

        # Calculate neighbour x
        neighbour_pos = (x+dx, y+dy)

        # Get our neighbour from that pos
        for weight, neighbour in self.neighbours:
            if not weight == 1:
                continue
            if not neighbour.position == neighbour_pos:
                continue
            #print(f"Found valid neighbour, {str(neighbour)}")
            # shush, this is not the correct return type, but idc
            result = [parent] + neighbour.get_xmases(self)
            #print(f"Result {[str(node) for node in result]}")
            return result
        return []
    
    def __str__(self):
        return f"{self.letter} {self.position}"
            

class WordGraph:
    def __init__(self, lines: list[str]):
        self.nodes: list[list[Node]] = []
        self.m_nodes: list[Node] = []

        # Add lines as nodes
        for y, line in enumerate(lines):
            node_list = []
            for x, letter in enumerate(line.replace("\n", "")):
                #print(f"Adding node: {x}, {y}")
                node = Node(letter, (x, y))
                node_list.append(node)
                if letter == "M":
                    self.m_nodes.append(node)
            #print(f"Created row: {[str(node) for node in node_list]}")
            self.nodes.append(node_list)
        
        # Add neighbours to all nodes
        for row in self.nodes:
            for node in row:
                node.get_neighbours(self)
        
        #print(f"X's: {[str(node) for node in self.x_nodes]}")
                
        
    def get_node(self, x, y):
        if x < 0 or y < 0:
            return None
        # this is so dirty lmfao
        try:
            return self.nodes[y][x]
        except Exception:
            return None
    
    def get_xmases(self):
        xmases = [node.get_xmases() for node in self.m_nodes]
        return [xmas for xmaseses in xmases for xmas in xmaseses if xmas]
    
    def draw_xmases(self, xmases: list[list[Node]]):
        nodes = [node for nodelist in xmases for node in nodelist]
        #print(nodes)


        for nodelist in self.nodes:
            for node in nodelist:
                if node in nodes:
                    print(f"{node.letter}", end="")
                else:
                    print(".", end="")
            print()



def main():
    with open("04-Ceres-Search.txt") as f:
        lines = f.readlines()
    
    print(part_2(lines))


def part_2(lines):
    graph = WordGraph(lines)
    xmases = graph.get_xmases()

    x_mases = []
    for mas in xmases:
        for mas2 in xmases:
            if mas == mas2:
                continue
            # If the same A is in the middle
            if mas[1] == mas2[1]:
                # If this xmas isn't already in x_mases
                already_added = False
                for xmas in x_mases:
                    for node in xmas:
                        if node == mas[1]:
                            already_added = True
                            break
                    if already_added: break
                if not already_added:
                    xmas = mas.copy()
                    for node in mas2:
                        if node not in xmas:
                            xmas.append(node)
                    x_mases.append(xmas)
    
    x_mases_dedup = []
    for xmas in x_mases:
        if len(xmas) != 5:
            print(f"Something went wrong for {[str(node) for node in xmas]}")
            raise Exception

        a_node = [node for node in xmas if node.letter == "A"]
        if len(a_node) != 1:
            print(f"Something went wrong for {[str(node) for node in xmas]}")
            raise Exception
        a_node = a_node[0]
        not_duplicate = True
        for xmas2 in x_mases_dedup:
            if xmas == xmas2:
                not_duplicate = False
                break
            if not not_duplicate:
                break
            a_nodes = [node for node in xmas2 if node.letter == "A"]
            for a in a_nodes:
                if a == a_node:
                    not_duplicate = False
                    break

        if not_duplicate:
            x_mases_dedup.append(xmas)
    x_mases = x_mases_dedup

    print([[str(node) for node in nodes] for nodes in x_mases])
    #graph.draw_xmases(x_mases)
    return len(x_mases)


if __name__ == "__main__":
    main()
