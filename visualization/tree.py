
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

    @classmethod
    def from_dict(cls,dictionary):
        dictionary['children'] = [cls.from_dict(child)
                                  for child in dictionary['children']]

        # FIXME: might be problomatic but it's prety :)
        root = cls(**dictionary)

        return root

    def __repr__(self):
        # return str(self.code)
        return (str(self.code) +
                "(" +
                ", ".join(map(repr,self.children)) +
                ")")

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def to_dict(self):
        if isinstance(self.amount, UndefinedAmount):
            amount = None
        else:
            amount = str(self.amount)

        return {'code': self.code,
                'amount': amount,
                'name': self.name,
                'children': [i.to_dict() for i in self.children]}

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
                # import pdb
                # pdb.set_trace()
                if child.code == subcode:
                    # print 'Got in: %s'%subcode
                    # pdb.set_trace()
                    went_down = True
                    location = child
                    break
        location.add_child(node)

    def update_amount(self):
        self.amount = self.amount + sum(child.update_amount() for child in self.children)
        return self.amount

