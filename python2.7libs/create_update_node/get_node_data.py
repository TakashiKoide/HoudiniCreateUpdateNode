# -*- coding: utf-8 -*-
import hou
import os

def get_all_parm_templates(all_parms, node_type):
    parms = node_type.parmTemplates()
    for parm in parms:
        if parm.type() == hou.parmTemplateType.Folder:
            get_all_parm_templates(all_parms, parm)
        elif parm.type() != hou.parmTemplateType.FolderSet:
            all_parms.append(parm)
    return all_parms

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
            all_parms = get_all_parm_templates([], node_type)
            node_info['parms'] = [parm.name() for parm in all_parms]
            category_data.append(node_info)

        node_data[category_name] = category_data

    print(node_data)
    return node_data

if __name__ == "__main__":
    main()
