#username - oferdadia
#id1      - 213033913
#name1    - Ofer Dadia


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None      # Left child
        self.right = None     # Right child
        self.parent = None    # Parent node
        self.height = -1      # Height of node (-1 for virtual nodes)
        self.bf = 0          # Balance factor = left.height - right.height
                            # Positive: left heavy, Negative: right heavy

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.  

    """
    def __init__(self):
        self.root = None
        self.max = None
        self.virtual = AVLNode(None, None)
        self.countNodes = 0
        self.zeroBfCounter = 0


    def create_node(self, key, val, new_parent=None, direction=None):
        new_node = AVLNode(key, val)
        new_node.left = self.virtual
        new_node.right = self.virtual
        new_node.height = 0
        if new_parent is not None:
            if direction == "right":
                new_parent.right = new_node
            else:
                new_parent.left = new_node
            new_node.parent = new_parent

        self.zeroBfCounter += 1
        return new_node

    def update_node_info(self, node):
        if not node or not node.is_real_node():
            return False
            
        prev_height = node.height
        prev_bf = node.bf
            
        left_height = node.left.height if node.left and node.left.is_real_node() else -1
        right_height = node.right.height if node.right and node.right.is_real_node() else -1
        
        node.height = 1 + max(left_height, right_height)
        
        actual_bf = left_height - right_height
        node.bf = actual_bf
        
        if prev_bf == 0 and actual_bf != 0:
            self.zeroBfCounter -= 1

        if actual_bf == 0 and prev_bf != 0:
            self.zeroBfCounter += 1

        return prev_height != node.height

    def update_max(self, deleted_node):
        if deleted_node is not self.max:
            return

        if not self.root:
            self.max = None
            return

        current = deleted_node

        if current.left.is_real_node():
            current = current.left
            while current.right.is_real_node():
                current = current.right
        else:
            current = current.parent
        self.max = current

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """
    def search(self, key):
        current = self.root
        while current and current.is_real_node():
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @param start: can be either "root" or "max"
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def insert(self, key, val, start="root"):
        self.countNodes += 1
        if start == "root":
            return self.insert_by_root(key, val)
        return self.insert_by_max(key, val)

    def insert_by_root(self, key, val, startNode=None):
        if self.root is None:
            self.root = self.create_node(key, val)
            self.max = self.root
            return 0

        current = startNode or self.root
        while True:
            if key < current.key:
                if not current.left.is_real_node():
                    insertedNode = self.create_node(key, val, current, "left")
                    break
                current = current.left
            else:
                if not current.right.is_real_node():
                    insertedNode = self.create_node(key, val, current, "right")
                    break
                current = current.right

        if key > self.max.key:
            self.max = insertedNode
        return self.rebalance(insertedNode.parent)

    def insert_by_max(self, key, val):
        if self.root is None:
            self.root = self.create_node(key, val)
            self.max = self.root
            return 0
        if key > self.max.key:
            return self.insert_by_root(key, val, self.max)
        current = self.max
        while current.parent and key <= current.parent.key:
            current = current.parent
        return self.insert_by_root(key, val, current)

    def rebalance(self, delNodeParent, operation = "insert"):
        if not delNodeParent:
            return 0

        numOfCorrections = 0
        current = delNodeParent
        while current:
            heightChanged = self.update_node_info(current)

            if abs(current.bf) < 2:
                if not heightChanged:
                    break
                current = current.parent
                numOfCorrections += 1
                continue

            if current.bf == 2:
                leftChild = current.left
                if leftChild.bf >= 0:
                    self.rightRotation(current, operation)
                    numOfCorrections += 1
                    if operation == "insert":
                        return numOfCorrections
                else:
                    self.leftRotation(leftChild, operation)
                    self.rightRotation(current, operation)
                    numOfCorrections += 2
                    if operation == "insert":
                        return numOfCorrections

            elif current.bf == -2:
                rightChild = current.right
                if rightChild.bf <= 0:
                    self.leftRotation(current, operation)
                    numOfCorrections += 1
                    if operation == "insert":
                        return numOfCorrections
                else:
                    self.rightRotation(rightChild, operation)
                    self.leftRotation(current, operation)
                    numOfCorrections += 2
                    if operation == "insert":
                        return numOfCorrections

            if operation == "delete" and current.parent:
                    self.update_node_info(current.parent)
                    current = current.parent.parent
            else:
                current = current.parent

        return numOfCorrections

    def rightRotation(self, node, operation = "insert"):
        """Performs a right rotation around the given node
        
        @type node: AVLNode
        @param node: node to rotate around
        @rtype: AVLNode
        @returns: new root of the subtree after rotation
        """
        prevParent = node.parent
        leftSon = node.left

        node.left = leftSon.right
        if leftSon.right.is_real_node():
            leftSon.right.parent = node

        leftSon.right = node
        leftSon.parent = prevParent
        node.parent = leftSon

        if prevParent is None:
            self.root = leftSon
        else:
            if prevParent.left is node:
                prevParent.left = leftSon
            else:
                prevParent.right = leftSon

        self.update_node_info(node)

        if operation == "insert":
            self.update_node_info(leftSon)
        return leftSon

    def leftRotation(self, node, operation):
        prevParent = node.parent
        rightSon = node.right

        node.right = rightSon.left
        if rightSon.left.is_real_node():
            rightSon.left.parent = node

        rightSon.left = node
        rightSon.parent = prevParent
        node.parent = rightSon

        if prevParent is None:
            self.root = rightSon
        else:
            if prevParent.left is node:
                prevParent.left = rightSon
            else:
                prevParent.right = rightSon

        self.update_node_info(node)
        if operation == "insert":
            self.update_node_info(rightSon)      
        return rightSon

    def successor(self, node):
        if not node or not node.is_real_node():
            return self.virtual
        if node.right.is_real_node():
            current = node.right
            while current.left.is_real_node():
                current = current.left
            return current
        current = node
        while current.parent and current == current.parent.right:
            current = current.parent
        return current.parent if current.parent else self.virtual

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def delete(self, node):
        self.update_max(node)

        leftChild, rightChild = node.left, node.right

        if not (leftChild.is_real_node() or rightChild.is_real_node()):
            if not node.parent:
                self.root = None
                self.countNodes -= 1
                self.zeroBfCounter -= 1
                return 0

            delNodeParent = node.parent
            if delNodeParent.right is node:
                delNodeParent.right = self.virtual
            else:
                delNodeParent.left = self.virtual
            node.parent = node.left = node.right = None
            self.countNodes -= 1
            self.zeroBfCounter -= 1

            return self.rebalance(delNodeParent, "delete")

        elif leftChild.is_real_node() != rightChild.is_real_node():
            child = leftChild if leftChild.is_real_node() else rightChild

            if not node.parent:
                self.root = child
                child.parent = None
                self.countNodes -= 1
                self.update_node_info(self.root)
                return self.rebalance(self.root, "delete")

            else:
                delNodeParent = node.parent
                if delNodeParent.right == node:
                    delNodeParent.right = child
                else:
                    delNodeParent.left = child
                child.parent = delNodeParent
                node.parent = node.left = node.right = None
                self.countNodes -= 1

                return self.rebalance(delNodeParent, "delete")

        else:
            nodeSuccessor = self.successor(node)
            if nodeSuccessor is self.virtual:
                return 0

            if nodeSuccessor.bf == 0:
                self.zeroBfCounter -= 1

            originalSuccessorRight = nodeSuccessor.right
            wasRightChild = nodeSuccessor.parent.right is nodeSuccessor

            successorParent = nodeSuccessor.parent
            if successorParent is node:
                successorParent = nodeSuccessor

            startBalanceNode = successorParent

            if wasRightChild:
                nodeSuccessor.parent.right = originalSuccessorRight
            else:
                nodeSuccessor.parent.left = originalSuccessorRight
            if originalSuccessorRight.is_real_node():
                originalSuccessorRight.parent = nodeSuccessor.parent

            nodeSuccessor.left = node.left
            nodeSuccessor.right = node.right
            nodeSuccessor.parent = node.parent
            nodeSuccessor.height = node.height
            nodeSuccessor.bf = node.bf

            if node.left.is_real_node():
                node.left.parent = nodeSuccessor
            if node.right.is_real_node():
                node.right.parent = nodeSuccessor

            if node.parent is None:
                self.root = nodeSuccessor
            else:
                if node.parent.left is node:
                    node.parent.left = nodeSuccessor
                else:
                    node.parent.right = nodeSuccessor

            node.parent = node.left = node.right = None
            self.countNodes -= 1

            return self.rebalance(startBalanceNode, "delete")


    def _inorder(self, node, result):
        if not node or not node.is_real_node():
            return
        self._inorder(node.left, result)
        result.append((node.key, node.value))
        self._inorder(node.right, result)


    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        result = []
        self._inorder(self.root, result)
        return result



    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self.countNodes

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

    """gets amir's suggestion of balance factor

    @returns: the number of nodes which have balance factor equals to 0 divided by the total number of nodes
    """
    def get_amir_balance_factor(self):
        if self.countNodes == 0:
            return 0
        return self.zeroBfCounter / self.countNodes


    