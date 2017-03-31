import re

from server.models import get_flatten, get_munis
from tree import Tree
from bson.objectid import ObjectId
from settings import MAX_LEVEL


def get_budget_tree(muni, year, layer=MAX_LEVEL, expense=None):

    if not (0 <= layer <= MAX_LEVEL):
        layer = MAX_LEVEL

    root = get_root_tree(muni, year, layer=layer, expense=expense)

    return root.to_dict(layer)


def _get_layer(node, layer):
    if not layer:
        return [node]

    nodes = []
    for x in node.children:
        nodes.extend(_get_layer(x, layer-1))

    return nodes


def get_node_subtree(_id, layer=4):
    budgets = _get_layer(get_subtree(_id,layer=layer), layer)
    # Repeats get_budget. Consider refactoring
    budgets = [budget.to_dict(0) for budget in budgets]
    return budgets


def get_root_tree(muni, year, layer=1000, expense=None):
    munis = get_munis()
    flatten = get_flatten()
    entry = munis.find_one({'name':muni})
    root_id = entry['roots'][str(year)]
    root_tree = get_subtree(root_id, layer, expense=expense)
    munis.close()
    flatten.close()
    return root_tree


def get_subtree(_id, layer, expense=None):
    if not isinstance(_id, ObjectId):
        _id = ObjectId(_id)
    flatten = get_flatten()
    root = flatten.find_one(_id)
    if expense is None:
        root_tree = Tree.from_db(flatten, root, layer, expense=expense)
    else:
        second_level_roots = [flatten.find_one(_id) for _id in root['children']]
        if second_level_roots[0]['expense'] is True:
            expenditure_root = second_level_roots[0]
            revenue_root = second_level_roots[1]
        else:
            expenditure_root = second_level_roots[1]
            revenue_root = second_level_roots[0]
        if expense:
            root_tree = Tree.from_db(flatten, expenditure_root, layer, expense=expense)
        else:
            root_tree = Tree.from_db(flatten, revenue_root, layer, expense=expense)

    flatten.close()
    return root_tree