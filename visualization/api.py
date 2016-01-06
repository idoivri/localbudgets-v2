from server.models import get_flatten,get_munis
from tree import Tree
import re

def search_code(muni,year,code):
    # TODO : rewrite this code
    dataset = get_flatten()
    results = []
    code_rex = re.compile("^%s*" %(code,))
    for item in dataset.find({'muni':muni,'year':year,'code': code_rex}):
        results.append({key: value for key, value in item.items() if (key != "_id") and (key != 'children')})

    for result in results:
        result['amount'] = int(result['amount'])
    dataset.close()
    return results


def get_budget_tree(muni, year, layer=2):
    if not (0 <= layer <= 4):
        layer = 4
    root = get_root(muni, year)

    return root.to_dict(layer)


def _get_layer(node ,layer):
    if not layer:
        return node

    nodes = []
    nodes.extend(_get_layer(x, layer-1) for x in node.children)

    return nodes

def get_budget(muni, year, layer=4):
    if not (0 <= layer <= 4):
        layer = 4

    root = get_root(muni, year)

    return _get_layer(root, layer)


def get_root(muni, year):
    munis = get_munis()
    flatten = get_flatten()
    entry = munis.find_one({'name':muni})
    root_id =  entry['roots'][str(year)]
    root = flatten.find_one(root_id)
    root_tree = Tree.from_db(flatten, root)

    munis.close()
    flatten.close()
    return root_tree
