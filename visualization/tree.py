def code_len_cmp(a, b):
    return cmp(len(a.code), len(b.code))

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
                       muni = None,
                       year = None,
                       expense = None,
                       children=None,
                       _id = None,
                       *args,
                       **kws):
        self.name = name
        if amount is not None:
            self.amount = int(amount)
        else:
            self.amount = UndefinedAmount()

        if expense == "EXPENDITURE":
            self.expense = True
        elif expense == "REVENUE":
            self.expense = False
        else:
            self.expense = None

        self.code = code
        self.muni = muni
        self.year = year
        self._id = _id
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

    def update_field(self,field_name,field_value):
        setattr(self, field_name, field_value)
        for child in self.children:
            child.update_field(field_name,field_value)

    @classmethod
    def from_dict(cls,dictionary):
        dictionary['children'] = [cls.from_dict(child)
                                  for child in dictionary['children']]

        # FIXME: might be problematic but it's pretty :)
        root = cls(**dictionary)

        return root


    def to_dict(self, level=999):
        if isinstance(self.amount, UndefinedAmount):
            amount = None
        else:
            amount = str(self.amount)

        tree_dict = {'code': self.code,
                'amount': amount,
                # TODO: Fix this hack. (Nitzan happy now?)
                'size': amount,
                'name': self.name,
                'muni': self.muni,
                'expense': self.expense,
                'year': self.year,
                '_id':self._id,
                }

        if level > 0:
            tree_dict['children'] = [i.to_dict(level -1) for i in self.children]

        return tree_dict
        
            


    def node_to_db(self,dataset,children):
        if isinstance(self.amount, UndefinedAmount):
            amount = None
        else:
            amount = str(self.amount)
        return dataset.insert({'code': self.code,
                               'amount': amount,
                               'expense': self.expense,
                               'name': self.name,
                               'muni': self.muni,
                               'year': self.year,
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
    def from_db(cls, dataset, root_dict, layer=999):

        children = []

        if layer > 0:
            for _id in root_dict['children']:
                child = dataset.find_one({'_id': _id})
                children.append(cls.from_db(dataset, child,layer-1))

        root_dict['children'] = children
        root = cls(**root_dict)
        return root

    # TODO: figure out what to do with the fist_digit
    def insert_node(self, node):
        if node.code == '':
            return 
            
        first_digit, code = node.code[0], node.code[1:]
        self._insert_node(node, code)


    def _insert_node(self, node, code):
        if code == '' or not self.children:
            self.add_child(node)
        else:
            self.children.sort(cmp=code_len_cmp, reverse=True)
            for child in self.children:
                if code.startswith(child.code):
                    code = code[len(child.code):]
                    return child._insert_node(node, code)


    def update_amount(self):
        self.amount = self.amount + sum(child.update_amount() for child in self.children)
        return self.amount

