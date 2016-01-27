import re

from server.models import get_flatten,get_munis
from tree import Tree
from bson.objectid import ObjectId

# from server.utils import profile


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
        return [node]

    nodes = []
    for x in node.children:
        nodes.extend(_get_layer(x, layer-1))

    return nodes

def get_budget(muni=None, year=None, layer=4):
    if not (0 <= layer <= 4):
        layer = 4

    munis = get_munis()

    if muni is None:
        munis = list(munis.find({}))
    else:
        munis = list(munis.find({'name':muni}))

    quries = []
    if year is None:
        for muni in munis:
            quries.extend([(muni['name'], year) for year in muni['years']])
    else:
        years = [year]
        quries.extend([(muni['name'], year) for muni in munis if int(year) in muni['years']])

    budgets = []
    for query in quries:
        budgets.extend(_get_layer(get_root(*query,layer=layer), layer))

    budgets = [budget.to_dict(0) for budget in budgets]
    return budgets
        
def get_node_subtree(_id, layer=4):
    budgets = _get_layer(get_subtree(_id,layer=layer), layer)
    # Repeats get_budget. Consider refactoring
    budgets = [budget.to_dict(0) for budget in budgets]
    return budgets

def get_root(muni, year, layer=4):
    munis = get_munis()
    flatten = get_flatten()
    entry = munis.find_one({'name':muni})
    root_id = entry['roots'][str(year)]

    root_tree = get_subtree(root_id,layer)
    munis.close()
    flatten.close()
    return root_tree

def get_subtree(_id,layer):
    if not isinstance(_id,ObjectId):
        _id = ObjectId(_id)
    flatten = get_flatten()
    print type(_id)
    print type(_id)=='unicode'
    root = flatten.find_one(_id)
    root_tree = Tree.from_db(flatten, root, layer)

    flatten.close()
    return root_tree