# AVL Tree Project

A full implementation of an AVL Tree in Python, developed as part of the "Data Structures" course at Tel Aviv University.

## Features

- Insertion and Deletion operations with automatic balancing
- Rotations (LL, RR, LR, RL)
- Height maintenance and balance factor calculations
- Efficient search and traversal
- Runtime complexity analysis (amortized)
- Written in clean OOP structure with separate node and tree classes
- Includes test cases for major operations

## Getting Started

To run the code, simply clone the repository and execute the main Python file:

```bash
git clone https://github.com/oferdadia/AVL-Tree-Project.git
cd AVL-Tree-Project
python AVLTree.py
```

## File Structure

- `AVLTree.py` – Core AVL Tree implementation
- `AVLFullTester.py` – Test cases for insert, delete, and search

## Example

```python
tree = AVLTree()
tree.insert(10)
tree.insert(20)
tree.insert(30)  # Balancing will occur here
tree.delete(10)
```

## Author

Ofer Dadia
Email: oferdadya10@gmail.com
GitHub: [oferdadia](https://github.com/oferdadia)

---

This project was created as part of university coursework in data structures.
