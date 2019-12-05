# -*- coding: utf-8 -*-
import hou
import os

def main():
    node_data = {}
    categories = hou.nodeTypeCategories()
    for category_name, category in categories.items():
        category_data = []
        nodes = category.nodeTypes()

        for node_name, node_type in nodes.items():
            node_info = {}
            node_info['node_name'] = node_name
            node_info['node_label'] = node_type.description()
            parms = node_type.parmTemplates()
            node_info['parms'] = [parm.name() for parm in parms]
            category_data.append(node_info)

        node_data[category_name] = category_data

    print(node_data)
    return node_data

if __name__ == "__main__":
    main()