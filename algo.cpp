#include <iostream>
#include <string>
#include <unordered_map>
#include <map>
#include <algorithm>
#include <utility>
#include <math.h>
#include <chrono>
#include <sstream>
#include <fstream>
#include <set>
#include <unordered_set>
#define ll long long
#define ull unsigned ll
#define uint unsigned int
using namespace std;

template <class T>
inline void hash_combine(std::size_t &seed, const T &v)
{
    std::hash<T> hasher;
    seed ^= hasher(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

namespace std
{
    template <typename S, typename T>
    struct hash<pair<S, T>>
    {
        inline size_t operator()(const pair<S, T> &v) const
        {
            size_t seed = 0;
            ::hash_combine(seed, v.first);
            ::hash_combine(seed, v.second);
            return seed;
        }
    };
}

#include <stack>

struct Node
{
    int data;
    Node *right, *left, *prec;

    Node(int x) : data(x), right(nullptr), left(nullptr), prec(nullptr) {}
};

void out_tree_preorder(Node *root)
{
    if (!root)
        return;
    cout << root->data << ' ';
    out_tree_preorder(root->left);
    out_tree_preorder(root->right);
}

void out_tree_postorder(Node *root)
{
    if (!root)
        return;
    out_tree_postorder(root->left);
    out_tree_postorder(root->right);
    cout << root->data << ' ';
}

void out_tree_inorder(Node *root)
{
    if (!root)
        return;
    out_tree_inorder(root->left);
    cout << root->data << ' ';
    out_tree_inorder(root->right);
}

void build_subtree(Node *&root, pair<int, int> &root_xy, unordered_set<pair<int, int>> &vertices, unordered_map<pair<int, int>, int> &vertices_data, unordered_map<pair<int, int>, pair<pair<int, int>, pair<int, int>>> &edges)
{

    if (edges.contains({root_xy.first, root_xy.second}))
    {
        pair<int, int> left_xy = edges[{root_xy.first, root_xy.second}].first;
        if (vertices.count(left_xy))
        {
            Node *left = new Node(vertices_data[left_xy]);
            build_subtree(left, left_xy, vertices, vertices_data, edges);
            root->left = left;
        }
        pair<int, int> right_xy = edges[{root_xy.first, root_xy.second}].second;
        if (vertices.count(right_xy))
        {
            Node *right = new Node(vertices_data[right_xy]);
            build_subtree(right, right_xy, vertices, vertices_data, edges);
            root->right = right;
        }
    }
}

void find_paths(Node *root, vector<int> &path, vector<vector<int>> &pathes, int sum)
{
    if (!root)
        return;
    path.push_back(root->data);
    sum += root->data;

    if (!root->left && !root->right)
    {
        pathes.push_back(path);
        pathes[pathes.size() - 1].push_back(sum);
    }

    find_paths(root->left, path, pathes, sum);
    find_paths(root->right, path, pathes, sum);

    path.pop_back();
}

int main()
{
    pair<int, int> root_xy = {462, 241};
    unordered_set<pair<int, int>> vertices;                                    /*{{290, 189}, {218, 139}, {257, 267}, {295, 43},{309, 103}};*/
    unordered_map<pair<int, int>, int> vertices_data;                          /*{
                                  {{309, 103}, 1},
                                  {{462, 241}, 4},
                                  {{290, 189}, 2},
                                  {{218, 139}, 5},
                                  {{257, 267}, 0},
                                  {{295, 43}, 5}
                              };*/
    unordered_map<pair<int, int>, pair<pair<int, int>, pair<int, int>>> edges; /* = {
           {{462, 241}, {{309, 103}, {290, 189}}},
           {{290, 189}, {{218, 139}, {257, 267}}},
           {{309, 103}, {{295, 43}, {-1, -1}}}
       }; */

    ifstream temp("temp.log");
    int nv;
    temp >> nv;
    if (nv == 0)
        return 0;
    int x, y, w;
    temp >> x >> y >> w;
    root_xy = {x, y};
    vertices.insert(root_xy);
    vertices_data[root_xy] = w;
    for (int i = 1; i < nv; i++)
    {
        temp >> x >> y >> w;
        vertices.insert({x, y});
        vertices_data[{x, y}] = w;
    }

    int ne;
    temp >> ne;
    int count, fromx, fromy, to1x, to1y, to2x, to2y;
    for (int i = 0; i < ne; i++)
    {
        temp >> count >> fromx >> fromy;
        temp >> to1x >> to1y;
        temp >> to2x >> to2y;

        edges[{fromx, fromy}] = {{to1x, to1y}, {to2x, to2y}};
    }

    int sum = 0;
    Node *root = new Node(vertices_data[root_xy]);
    build_subtree(root, root_xy, vertices, vertices_data, edges);

    out_tree_preorder(root);
    cout << endl;

    vector<int> path;
    vector<vector<int>> paths;

    find_paths(root, path, paths, sum);

    ofstream out("out.log");
    int summary = 0;
    for (const auto &path : paths)
    {
        for (int i = 0; i < path.size() - 1; i++)
        {
            cout << path[i] << " -> ";
            out << path[i] << " -> ";
        }
        cout << "sum: " << path.back() << endl;
        out << "sum: " << path.back() << endl;
        summary += path.back();
    }
    cout << "summary: " << summary << endl;
    out << "summary: " << summary << endl;
    return 0;
}
