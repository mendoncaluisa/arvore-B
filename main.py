import random


class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Grau mínimo (metade da ordem)
        self.leaf = leaf  # True se o nó é folha
        self.keys = []  # Lista de chaves
        self.children = []  # Lista de filhos

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def search(self, k, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])

    def insert(self, k):
        root = self.root
        if len(root.keys) == 2*self.t - 1:
            temp = BTreeNode(self.t)
            self.root = temp
            temp.children.append(root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == 2*self.t - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(t, y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2*t - 1)]
        y.keys = y.keys[0:t-1]
        if not y.leaf:
            z.children = y.children[t:(2*t)]
            y.children = y.children[0:t]



def simulate_operations(btree, num_blocks):
    for _ in range(num_blocks):
        operation = random.choice(['insert', 'delete'])
        key = random.randint(1, num_blocks * 10)
        if operation == 'insert':
            btree.insert(key)
        # Implementar remoção (delete)
        # elif operation == 'delete':
        #    btree.delete(key)

    return btree

def calculate_metrics(btree):
    def calculate_height(node):
        if node.leaf:
            return 1
        return 1 + calculate_height(node.children[0])

    def calculate_utilization(node):
        return len(node.keys) / (2 * node.t - 1)

    def count_disk_accesses(node):
        if node.leaf:
            return 1
        return 1 + sum(count_disk_accesses(child) for child in node.children)

    height = calculate_height(btree.root)
    utilization = calculate_utilization(btree.root)
    disk_accesses = count_disk_accesses(btree.root)

    return height, utilization, disk_accesses

def run_simulation(order, num_blocks):
    btree = BTree(order)
    btree = simulate_operations(btree, num_blocks)
    height, utilization, disk_accesses = calculate_metrics(btree)

    print(f"Ordem da árvore B: {order}")
    print(f"Quantidade de blocos: {num_blocks}")
    print(f"Altura média da árvore: {height}")
    print(f"Utilização média da árvore: {utilization:.2f}")
    print(f"Quantidade média de acessos ao disco: {disk_accesses}")

# Simulações
orders = [200, 500, 1000]
num_blocks_options = [20000, 50000, 100000]

for order in orders:
    for num_blocks in num_blocks_options:
        run_simulation(order, num_blocks)
