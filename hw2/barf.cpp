#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

int longestRun(std::vector<bool> list) {
    int current = 0;
    int max = 0;

    for (int i = 0, l = list.size(); i < l; i++) {
        if (list[i]) {
            current++;
            max = std::max(max, current);
        } else {
            current = 0;
        }
    }

    return max;
}

using namespace std;

class Tree {
  public:
    unsigned value;
    vector<Tree *> children;

    Tree(unsigned value, vector<Tree *> children) {
        this->value = value;
        this->children = children;
    }
};

unsigned maxTreeValue(Tree *root) {
    if (!root)
        return 0;

    unsigned maximum = 0;
    queue<Tree *> q;
    q.push(root);

    while (!q.empty()) {
        Tree *current = q.front();
        q.pop();

        if (!current)
            continue;

        maximum = max(maximum, current->value);
        for (int i = 0, l = current->children.size(); i < l; i++) {
            q.push(current->children[i]);
        }
    }

    return maximum;
}

int main() {
    std::cout << longestRun(std::vector<bool>(
                     {true, true, false, true, true, true, false}))
              << std::endl;
    std::cout << longestRun(std::vector<bool>({true, false, true, true}))
              << std::endl;

    Tree *root = new Tree(5, vector<Tree *>());
    root->children.push_back(new Tree(2, vector<Tree *>()));
    root->children.push_back(new Tree(9, vector<Tree *>()));
    root->children.push_back(new Tree(0, vector<Tree *>()));
    root->children.push_back(new Tree(3, vector<Tree *>()));
    root->children[1]->children.push_back(new Tree(99, vector<Tree *>()));
    root->children[1]->children.push_back(new Tree(12, vector<Tree *>()));

    std::cout << maxTreeValue(root) << std::endl;

    return 0;
}
