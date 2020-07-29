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
