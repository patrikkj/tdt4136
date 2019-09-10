class PriorityQueue():
    def __init__(self, data=None, compare_keys=lambda k1, k2: k1 < k2, key_attr=None):
        self.data = data[:] if data else []
        self.size = len(self.data)

        # Function for accessing key for given node
        self.key_attr = key_attr
        if key_attr is None:
            self.node_to_key = lambda node: node
        else:
            self.node_to_key = lambda node: getattr(node, key_attr)

        # Comparison functions
        self.compare_nodes = lambda u, v: compare_keys(
            self.node_to_key(u), self.node_to_key(v))
        self.compare_keys = compare_keys

        # Build heap
        self._build_heap()

    # Public functions
    def top(self):
        if self.is_empty():
            raise IndexError('The queue is empty.')

        return self.data[0]

    def extract(self):
        top_node = self.top()
        self.data[0] = self.data[self.size - 1]
        self.size -= 1
        del self.data[-1]
        self._heapify(0)
        return top_node

    def delete(self):
        self.extract()

    def insert(self, node):
        self.size += 1
        self.data.append(node)
        self.modify_key(self.size - 1, self.node_to_key(node))

    def modify_key(self, i, key):
        _key = self.node_to_key(self.data[i])
        if self.compare_keys(_key, key):
            raise ValueError(
                'Key cannot be replaced with a key of lower priority.')

        # Update key
        if self.key_attr is None:
            self.data[i] = key
        else:
            setattr(self.data[i], self.key_attr, key)

        # Update node priority
        while i > 0 and self.compare_nodes(self.data[i], self.data[PriorityQueue._parent(i)]):
            self.data[i], self.data[PriorityQueue._parent(
                i)] = self.data[PriorityQueue._parent(i)], self.data[i]
            i = PriorityQueue._parent(i)

    def modify_key_noderef(self, node, key):
        self.modify_key(self.data.index(node), key)

    def is_empty(self):
        return self.size == 0

    # Private functions
    def _build_heap(self):
        # Heapify every internal node
        for i in range((self.size - 1) // 2, -1, -1):
            self._heapify(i)

    def _heapify(self, i):
        l = PriorityQueue._left(i)
        r = PriorityQueue._right(i)

        # Identify node with the highest priority
        if l < self.size and self.compare_nodes(self.data[l], self.data[i]):
            prioritized = l
        else:
            prioritized = i
        if r < self.size and self.compare_nodes(self.data[r], self.data[prioritized]):
            prioritized = r
        if prioritized != i:
            self.data[i], self.data[prioritized] = self.data[prioritized], self.data[i]
            self._heapify(prioritized)

    # Special methods
    def __len__(self):
        return self.size

    def __str__(self):
        return str([str(elem) for elem in self.data])

    def __contains__(self, elem):
        return elem in self.data

    # Static methods
    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    @staticmethod
    def _left(i):
        return 2 * i + 1

    @staticmethod
    def _right(i):
        return 2 * i + 2


class MinHeap(PriorityQueue):
    def __init__(self, data=None, key_attr=None):
        super().__init__(data=data, compare_keys=lambda k1, k2: k1 < k2, key_attr=key_attr)

    def insert(self, node):
        return super().insert(node)

    def minimum(self):
        return super().top()

    def extract_min(self):
        return super().extract()

    def decrease_key(self, i, key):
        return super().modify_key(i, key)

    def decrease_key_noderef(self, node, key):
        return super().modify_key_noderef(node, key)

