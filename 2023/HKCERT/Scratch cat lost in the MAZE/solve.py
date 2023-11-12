import json
import cv2
from PathAlgorithm import *
import asyncio

LEVEL_SIZE = {
    "width": 720,
    "height": 720
}
SQUARE_SIZE = 14

def get_levels():
    with open("maze/maze_levels.json", "r") as f:
        return [{"file": "maze/"+level["md5ext"]} for level in json.load(f)]


async def get_maze_graph(level_id, level):
    # Get maze graph
    im = cv2.imread(level["file"])[:, :723]
    # print(im.shape)
    # print(im)

    # Remove every 14th row and column
    # im = im[::14, ::14]
    # do it with opencv instead
    im = cv2.resize(im, (720, 720), interpolation=cv2.INTER_NEAREST_EXACT)
    # im = cv2.resize(im, (352, 352), interpolation=cv2.INTER_NEAREST_EXACT)
    # and first row and column

    im = im[4:, 4:]
    im = im[::8, ::8]
    im = im[::2, ::2]

    # im = im[1:, 1:]
    # print(im.shape)

    # show image
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # cv2.imshow("window", im)
    # cv2.waitKey(0)
    #
    # return
    #
    # # Time to manually make a new image by moving a character inside yay
    # # im2 = np.ones_like(im) * 255
    # positions = np.ones((44, 44, 3))
    # for x in range(44):
    #     im_x = x*8+4
    #     for y in range(44):
    #         im_y = y*8+4
    #
    #         x_walkable_count = [
    #             # (im[im_y][im_x-3] == [0, 0, 0]).all(),
    #             # (im[im_y][im_x-2] == [0, 0, 0]).all(),
    #             (im[im_y][im_x-1] == [0, 0, 0]).all(),
    #             (im[im_y][im_x] == [0, 0, 0]).all(),
    #             # (im[im_y][im_x+1] == [0, 0, 0]).all(),
    #             # (im[im_y][im_x+2] == [0, 0, 0]).all(),
    #             # (im[im_y][im_x+3] == [0, 0, 0]).all()
    #         ].count(True)
    #         y_walkable_count = [
    #             # (im[im_y-3][im_x] == [0, 0, 0]).all(),
    #             # (im[im_y-2][im_x] == [0, 0, 0]).all(),
    #             (im[im_y-1][im_x] == [0, 0, 0]).all(),
    #             (im[im_y][im_x] == [0, 0, 0]).all(),
    #             # (im[im_y+1][im_x] == [0, 0, 0]).all(),
    #             # (im[im_y+2][im_x] == [0, 0, 0]).all(),
    #             # (im[im_y+3][im_x] == [0, 0, 0]).all()
    #         ].count(True)
    #         if x_walkable_count >= 1 or y_walkable_count >= 1:
    #             print(f"({x}, {y}) is walkable")
    #             positions[y][x] = [0, 0, 0]
    #         else:
    #             positions[y][x] = im[im_y][im_x]
    #
    # print(positions.shape)
    # im = positions
    # # show image
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # cv2.imshow("window", im)
    # cv2.waitKey(0)
    #
    # # print(im)
    # # print(im[5])
    # # print(im[-9])
    # return

    def get_walkable_neighbours(x, y):
        neighbours = []
        if x > 0 and (im[y][x-1] == [0, 0, 0]).all():
            neighbours.append((x-1, y))
        if y > 0 and (im[y-1][x] == [0, 0, 0]).all():
            neighbours.append((x, y-1))
        if x < im.shape[1]-1 and (im[y][x+1] == [0, 0, 0]).all():
            neighbours.append((x+1, y))
        if y < im.shape[0]-1 and (im[y+1][x] == [0, 0, 0]).all():
            neighbours.append((x, y+1))
        return neighbours

    # Create graph
    graph = Graph(im.shape[1], im.shape[0])
    start_node = None
    end_node = None
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            im_node = im[y][x]
            is_end_node = False
            is_start_node = False
            # End node (red - 0,0,255 - BGR)
            if (im_node == [0, 0, 255]).all():
                # print(f"Found end node? ({x}, {y})")
                is_end_node = True
            # Start node (green - 0,255,0 - BGR)
            elif (im_node == [0, 255, 0]).all():
                # print(f"Found start node? ({x}, {y})")
                is_start_node = True
            # Walkable node (transparent/black - 0,0,0 - BGR)
            elif (im_node != [0, 0, 0]).all():
                # not walkable
                continue

            # Add edges to walkable neighbours
            node = graph.get_node((x, y))
            neighbours = get_walkable_neighbours(x, y)
            if neighbours and (is_end_node or is_start_node):
                if is_end_node:
                    end_node = node
                if is_start_node:
                    start_node = node
            for neighbour in neighbours:
                graph.add_edge(graph.get_node(neighbour), node)

    if not start_node or not end_node:
        raise Exception("Start or end node not found")

    # Find path
    path: List[NodeData] = graph.get_path(start_node, end_node)

    # Make path into a sequence of moves
    seq = []
    for i in range(len(path)-1):
        node = path[i].node
        next_node = path[i+1].node
        if node.x > next_node.x:
            seq.append('l')
        elif node.x < next_node.x:
            seq.append('r')
        elif node.y > next_node.y:
            seq.append('u')
        elif node.y < next_node.y:
            seq.append('d')

    # print(seq)
    res = calculate_result(seq)
    print(f"Level {level_id}: {res}")
    return level_id, res


def calculate_result(seq):
    _i = 0
    _cl = 0
    _cu = 0
    _cr = 0
    _cd = 0
    for move in seq:
        _i += 1
        if move == 'l':
            _cl += _i
        elif move == 'u':
            _cu += _i
        elif move == 'r':
            _cr += _i
        elif move == 'd':
            _cd += _i
    result = (_cl % 4) * 64 + (_cu % 4) * 16 + (_cr % 4) * 4 + (_cd % 4) * 1
    return result


def calculate_flag(results):
    assert len(results) % 20 == 0
    _i = 0
    flag = ""
    # result_subsets = [results[i:i+20] for i in range(0, len(results), 20)]
    for i in range(len(results)//20):
        _j = 0
        for _ in range(20):
            _j += results[_i]
            _i += 1
        _j = _j % 256
        flag += chr(_j)
    return flag


async def main():
    levels = get_levels()
    assert len(levels) % 20 == 0
    tasks = [get_maze_graph(i, levels[i]) for i in range(len(levels))]
    results = await asyncio.gather(*tasks)
    results.sort(key=lambda x: x[0])
    results_out = [x[1] for x in results]
    flag = calculate_flag(results_out)
    print(flag)

if __name__ == "__main__":
    asyncio.run(main())
