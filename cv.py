from typing import List


def get_edges(mask: List[List[bool]], bbox: List[int] = None) -> List[List[int]]:
    """
    Extracts the edge locations from an image mask.
    
    :param mask: A mask of an image with True and False values
    :param bbox: The bounding box for the ROI in the mask, providing this makes for faster retrieval.
                 The bbox values provided should take form: [x_min, y_min, x_max, y_max]
    :return: edges
    """

    # The bounding box reduces the number of iterations to be made
    if bbox:
        x_min = bbox[0]
        y_min = bbox[1]
        x_max = bbox[2] + 1
        y_max = bbox[3] + 1
    else:
        x_min = 0
        y_min = 0
        x_max = len(mask[0])
        y_max = len(mask)

    # A point is considered an edge if it is Truthy and at least
    # one of the surrounding points is Falsy.
    edges = []
    for i in range(y_min, y_max):
        for j in range(x_min, x_max):
            if mask[i][j] is not True:
                continue
            try:
                boundaries = [
                    mask[i - 1][j - 1], mask[i][j - 1],
                    mask[i + 1][j - 1], mask[i - 1][j],
                    mask[i + 1][j], mask[i - 1][j + 1],
                    mask[i][j + 1], mask[i + 1][j + 1],
                ]
                if all(boundaries):
                    continue
                else:
                    edges.append([j, i])
            except IndexError:
                continue
    return edges


def remove_redundant(edges: List[List[float]], y: bool = True) -> List[List[float]]:
    """
    Removes redundant points from a list of edges.

    For example: [[574, 16], [..., 16], [750, 16],...]

    Becomes: [[574, 16], [750, 16], ...]

    Eliminating the points in between as they are not needed to maintain a straight line.

    :param edges:
    :param y: Determines if redundancy is removed on the `y` axis, otherwise it uses the `x` axis.
    :return:
    """
    if y:
        axis = 1
    else:
        axis = 0
    edges = sorted(edges, key=lambda x: x[axis])
    # Tracking the first and last index of the coordinate in focus
    coord = None
    first = None
    last = None
    new_edges = []
    for index, point in enumerate(edges):
        if coord is None:
            coord = point[axis]
            first = index
            last = index
            continue

        if point[axis] != coord:
            points = [edges[first]]
            if last - first > 0:
                points.append(edges[last])
            new_edges.extend(points)
            coord = point[axis]
            first = index
            last = index

        else:
            last = index
    return new_edges
