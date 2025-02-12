import os
from settings import PROJECT_FOLDER


def import_gmpes_weights(group_name):
    gmpes = []
    weights = []

    if group_name is None:
        return gmpes, weights

    if group_name is not None:
        group_path = os.path.join(PROJECT_FOLDER, group_name + '.txt')
        if os.path.exists(group_path):
            with open(group_path, 'r') as f:
                lines = [line.strip() for line in f.readlines()]
                for line in lines:
                    gmpe, weight = line.split()
                    gmpes.append(gmpe)
                    weights.append(int(weight))

    return gmpes, weights

