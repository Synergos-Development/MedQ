"""
avl_tree.py
Implementasi AVL Tree untuk menyimpan data pasien berdasarkan Nomor RM.

Kompleksitas:
- Insert : O(log n)
- Search : O(log n)
- Delete : O(log n)
"""


class AVLNode:
    """Node dalam AVL Tree"""

    def __init__(self, nomor_rm: str, data: dict):
        self.nomor_rm = nomor_rm
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL Tree untuk manajemen data pasien"""

    def __init__(self):
        self.root = None

    # =========================
    # UTILITAS
    # =========================

    def _height(self, node) -> int:
        return node.height if node else 0

    def _balance_factor(self, node) -> int:
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(
            self._height(node.left),
            self._height(node.right)
        )

    # =========================
    # ROTASI AVL
    # =========================

    def _rotate_right(self, z):
        y = z.left
        t3 = y.right

        y.right = z
        z.left = t3

        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_left(self, z):
        y = z.right
        t2 = y.left

        y.left = z
        z.right = t2

        self._update_height(z)
        self._update_height(y)

        return y

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # =========================
    # INSERT
    # =========================

    def insert(self, nomor_rm: str, data: dict):
        self.root = self._insert(self.root, nomor_rm, data)

    def _insert(self, node, nomor_rm: str, data: dict):
        if node is None:
            return AVLNode(nomor_rm, data)

        if nomor_rm < node.nomor_rm:
            node.left = self._insert(node.left, nomor_rm, data)

        elif nomor_rm > node.nomor_rm:
            node.right = self._insert(node.right, nomor_rm, data)

        else:
            # Update data jika nomor RM sudah ada
            node.data = data
            return node

        return self._rebalance(node)

    # =========================
    # SEARCH
    # =========================

    def search(self, nomor_rm: str):
        node = self._search(self.root, nomor_rm)
        return node.data if node else None

    def _search(self, node, nomor_rm: str):
        if node is None:
            return None

        if nomor_rm == node.nomor_rm:
            return node

        if nomor_rm < node.nomor_rm:
            return self._search(node.left, nomor_rm)

        return self._search(node.right, nomor_rm)

    # =========================
    # DELETE
    # =========================

    def delete(self, nomor_rm: str):
        self.root = self._delete(self.root, nomor_rm)

    def _delete(self, node, nomor_rm: str):
        if node is None:
            return None

        if nomor_rm < node.nomor_rm:
            node.left = self._delete(node.left, nomor_rm)

        elif nomor_rm > node.nomor_rm:
            node.right = self._delete(node.right, nomor_rm)

        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            successor = self._min_node(node.right)

            node.nomor_rm = successor.nomor_rm
            node.data = successor.data

            node.right = self._delete(
                node.right,
                successor.nomor_rm
            )

        return self._rebalance(node)

    def _min_node(self, node):
        current = node

        while current.left:
            current = current.left

        return current

    # =========================
    # TRAVERSAL
    # =========================

    def inorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.data)
            self._inorder(node.right, hasil)

    # =========================
    # UTILITAS PUBLIK
    # =========================

    def get_height(self):
        return self._height(self.root)

    def is_empty(self):
        return self.root is None

    def __len__(self):
        return len(self.inorder())


# Instance global
pasien_tree = AVLTree()