
class UndefinedAmount(object):
    def __add__(self, other):
        return int(other)
    def __str__(self):
        return None

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root',
                       code=None,
                       amount=None,
                       children=None,
                       *args,
                       **kws):
        self.name = name
        if amount is not None:
            self.amount = int(amount)
        else:
            self.amount = UndefinedAmount()

        self.code = code
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)


    def __repr__(self):
        # return str(self.code)
        return (str(self.code) +
                "(" +
                ", ".join(map(repr,self.children)) +
                ")")

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


    @classmethod
    def from_dict(cls,dictionary):
        dictionary['children'] = [cls.from_dict(child)
                                  for child in dictionary['children']]

        # FIXME: might be problematic but it's pretty :)
        root = cls(**dictionary)

        return root


    def to_dict(self):
        if isinstance(self.amount, UndefinedAmount):
            amount = None
        else:
            amount = str(self.amount)

        return {'code': self.code,
                'amount': amount,
                'name': self.name,
                'children': [i.to_dict() for i in self.children]}


    def node_to_db(self,dataset,children):
        if isinstance(self.amount, UndefinedAmount):
            amount = None
        else:
            amount = str(self.amount)
        return dataset.insert({'code': self.code,
                                'amount': amount,
                                'name': self.name,
                                'children': children})


    def to_db(self,dataset):

        if not self.children:
            return self.node_to_db(dataset,[])

        else:
            children_codes = []
            for child in self.children:
                children_codes.append(child.to_db(dataset))
            return self.node_to_db(dataset,children_codes)


    @classmethod
    def from_db(cls, dataset, root_dict):
        # import pdb; pdb.set_trace()
        children = []
        for _id in root_dict['children']:
            child = dataset.find_one({'_id': _id})
            children.append(cls.from_db(dataset, child))

        root_dict['children'] = children
        root = cls(**root_dict)
        return root

    # TODO: Refactor - ugly...
    def insert_node(self,node):
        location = self
        subcode = ''
        went_down = True
        for c in node.code[1:]:
            subcode += c
            if not went_down:
                    break
            for child in location.children:
                went_down = False
                if child.code == subcode:
                    went_down = True
                    location = child
                    break
        location.add_child(node)

    def update_amount(self):
        self.amount = self.amount + sum(child.update_amount() for child in self.children)
        return self.amount

