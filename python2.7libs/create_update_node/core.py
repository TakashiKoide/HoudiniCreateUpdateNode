# -*- coding: utf-8 -*-
import hou
import os
import sys
import subprocess
from subprocess import PIPE

from .get_node_data import get_all_parm_templates

def get_compare_version(hfs):
    version_root = os.path.dirname(hfs)
    versions = os.listdir(version_root)
    version_num = hou.applicationVersionString()
    current_version = 'Houdini ' + version_num
    if current_version in versions:
        versions.remove(current_version)
    #UIのオプション用辞書
    kwargs = {
        'exclusive': True,
        'title': 'Select Compare Version',
        'column_header': 'Versions'
    }
    #Houdini17.0以降はUIのwidth、heightオプションを使う
    if float('.'.join(version_num.split('.')[:-1])) > 17.0:
        kwargs['width'] = 240
        kwargs['height'] = 240
    #バージョンを選択用のリストビューを表示
    sel_version = hou.ui.selectFromList(
        versions, **kwargs)
    if not sel_version:
        return
    version = versions[sel_version[0]]
    return version

def get_env_from_version(version, hfs, pref_dir):
    old_hfs = '{}/{}'.format(os.path.dirname(hfs), version)
    old_pref_dir = '{}/{}'.format(
        os.path.dirname(pref_dir),
        '.'.join(version.replace('Houdini ', 'houdini').split('.')[:2])
    )
    return old_hfs, old_pref_dir

def set_base_env(path, hfs, pref_dir):
    #環境変数とPythonパスを設定する
    os.putenv('PATH', path)
    os.putenv('HFS', hfs)
    os.putenv('HOUDINI_USER_PREF_DIR', pref_dir)

def get_old_node_data(old_hfs, old_pref_dir):
    script_root = os.path.dirname(__file__)
    script = os.path.normpath(script_root + "/get_node_data.py")
    hython = os.path.normpath(old_hfs + '/bin/hython.exe')
    #hythonに投げる前に必要な環境変数とPythonのパスを通す
    path = '{}/bin;{}'.format(old_hfs, os.getenv('PATH'))
    set_base_env(path, old_hfs, old_pref_dir)
    #hythonでスクリプトを実行する
    p = subprocess.Popen([hython, script], shell=True, stdout=PIPE, stderr=PIPE)
    #スクリプトからの戻り値を取得
    stdout, stderr = p.communicate()
    if stderr:
        hou.ui.displayMessage('Script Error', severity=hou.severityType.Error)
        return
    #戻ってくる値は文字列なので、evalで辞書に変換
    old_node_data = eval(stdout)
    return old_node_data

def get_node_info(node_name, node_label):
    node_info = {}
    node_info['Node Name'] = node_name
    node_info['Node Label'] = node_label
    return node_info

def compare(old_node_data):
    new_node_data = {}
    new_parm_node_data = {}
    categories = hou.nodeTypeCategories()
    for category, type_category in categories.items():
        new_nodes = []
        new_parm_nodes = []
        nodes = type_category.nodeTypes()
        old_nodes = old_node_data.get(category)
        #カテゴリ自体が存在しない場合の処理
        if not old_nodes:
            for node_name, node_type in sorted(nodes.items()):
                node_label = node_type.description()
                node_info = get_node_info(node_name, node_label)
                new_nodes.append(node_info)
            if new_nodes:
                new_node_data[category] = new_nodes
            continue
        #カテゴリは存在する場合
        old_node_names = [node_info['node_name'] for node_info in old_nodes]
        for node_name, node_type in sorted(nodes.items()):
            node_label = node_type.description()
            node_info = get_node_info(node_name, node_label)
            if node_name in old_node_names:
                all_parms = get_all_parm_templates([], node_type)
                index = old_node_names.index(node_name)
                parm_sets = set(old_nodes[index]['parms'])
                new_parms = [parm.name() for parm in all_parms if not parm.name() in parm_sets]
                if new_parms:
                    node_info['parms'] = new_parms
                    new_parm_nodes.append(node_info)
            else:
                new_nodes.append(node_info)
        if new_nodes:
            new_node_data[category] = new_nodes
        if new_parm_nodes:
            new_parm_node_data[category] = new_parm_nodes
    return new_node_data, new_parm_node_data

def create_nodes(node_data, root_node):
    for category, nodes in node_data.items():
        #ノードを作成するためのカテゴリに合わせた親ノードを作る
        if category == 'Object':
            parent_node = root_node.createNode('subnet', category)
        elif category == 'Driver':
            parent_node = root_node.createNode('ropnet', category)
        elif category == 'Sop':
            parent_node = root_node.createNode('geo', category)
        elif category == 'Vop':
            parent_node = root_node.createNode('matnet', category)
        elif not 'Net' in category:
            try:
                parent_node = root_node.createNode(
                    category.lower() + 'net', category, run_init_scripts=False)
            except:
                continue
        else:
            parent_node = root_node.createNode(category.lower(), category)
        #ノードの作成
        for node_info in nodes:
            #ノードの名前を取得して作成
            node_name = node_info['Node Name']
            try:
                new_node = parent_node.createNode(node_name)
            except:
                continue
            #パラメータの取得
            parms = node_info.get('parms')
            if not parms:
                continue
            #パラメータにエクスプレッションを設定
            for parm_name in parms:
                try:
                    if parm_name[-1] == '#':
                        parm_name = parm_name[:-1] + '1'
                    parm_tuple = new_node.parmTuple(parm_name)
                    if not parm_tuple:
                        continue
                    for parm in parm_tuple:
                        parm.setExpression('constant()')
                except:
                    pass
        #ノード整理
        parent_node.layoutChildren()
    root_node.layoutChildren()

def create_new_nodes(new_node_data):
    root_node = hou.node('/obj').createNode('subnet', 'NewNodes')
    create_nodes(new_node_data, root_node)

def create_new_parm_nodes(new_parm_node_data):
    root_node = hou.node('/obj').createNode('subnet', 'NewParmNodes')
    create_nodes(new_parm_node_data, root_node)

def main():
    hfs = os.getenv('HFS')
    #比較するバージョンを取得
    version = get_compare_version(hfs)
    if not version:
        return
    pref_dir = os.getenv('HOUDINI_USER_PREF_DIR')
    path = os.getenv('PATH')
    #比較するバージョンの環境変数を取得
    old_hfs, old_pref_dir = get_env_from_version(
        version, hfs, pref_dir)
    #比較するバージョンのノード情報を取得
    old_node_data = get_old_node_data(old_hfs, old_pref_dir)
    if not old_node_data:
        return
    #hython用にセットした環境変数を元に戻す
    set_base_env(path, hfs, pref_dir)
    #現在のバージョンにあるノードと比較してノードの情報を取得
    new_node_data, new_parm_node_data = compare(old_node_data)
    #現在のバージョンのみに存在するノードを作成
    create_new_nodes(new_node_data)
    #現在のバージョンでパラメータが追加されたノードを作成
    create_new_parm_nodes(new_parm_node_data)
    #ノードの整理
    hou.node('/obj').layoutChildren()
