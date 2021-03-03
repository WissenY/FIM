from collections import Counter
from time import time

def fp_growth(data_set, min_support):
    data_dict = dict(Counter(data_set))
    min_support_count = len(data_dict) * min_support
    # 初始化生成头指针表和FP-Tree
    fp_header, fp_order = init_header(data_dict, min_support_count)
    fp_header = build_tree(data_dict, fp_header, fp_order)
    # 递归生成CP-Tree并返回支持度字典
    sup_dict = cp_tree(fp_header, fp_order, min_support_count)

    return sup_dict

class node:
    '''FP-Tree和CP-Tree上的节点，包括纵向的链接和横向的链接'''
    def __init__(self, item, father_node, support_count=1):
        self.name = item
        self.count = support_count
        self.link = None            #链接到树中同名节点
        self.father = father_node
        self.children = {}
    '''仅做测试用，检查构造的树是否正确
    def disp(self, ind=1):
        print('    ' * ind, self.name, '  ', self.count)
        ind += 1
        for child in self.children.values():
            child.disp(ind)
    '''

def init_header(data_dict, min_support_count):
    '''
    第一次扫描数据集，构建频繁一项集与其支持度计数的字典作为头指针表的初值（缺指针），生成按支持度计数降序的频繁一项集列表
    :param data_dict:计算重复transaction的次数来压缩数据集，数据机构 {f_set:count}
    :param min_support_count:
    :return:header_table = {item:[support_count, None]}; order_itme = [item]
    '''
    header_table = {}
    item_set = frozenset([item for transaction in data_dict for item in transaction])
    for item in item_set:
        support_count = 0
        for transaction in data_dict:
            if item in transaction:
                support_count += data_dict[transaction]
        if support_count >= min_support_count:
            header_table[item] = support_count
    '''字典存入后是乱序，因此还需要一个列表存入排序后的头指针表字典的键，排序按值的降序进行，当值相同时则按键的字典序'''
    order_item = [item_sup[0] for item_sup in sorted(header_table.items(), key=lambda x: (x[1], x[0]), reverse=True)] #TODO 识别最小元素项为单个字母还是数字

    for item in header_table:
        header_table[item] = [header_table[item], None]

    return header_table, order_item

def build_tree(data_dict, header_table, order_item):
    '''
    第二次扫描数据集，构建fp_tree
    :param data_dict:
    :param header_table:
    :param order_item:
    :return:
    '''
    root = node('root',None)
    for transaction in data_dict:
        father_node = root              #对于数据集中的每项交易，fp_tree都从其根节点开始构建
        for item in order_item:
            if item in transaction:
                count = data_dict[transaction]
                father_node = update(item, father_node, header_table, count)
    '''仅作测试用'''
    #tree = root
    return header_table

def update(item, father_node, header_table, count):
    '''
    更新fp_tree与链表
    :param item:
    :param father_node:
    :param header_table:
    :return:
    '''
    if item not in father_node.children:
        new_node = node(item, father_node, count)
        father_node.children[item] = new_node
        '''更新同名项链表'''
        link_node = header_table[item][1]
        if link_node == None:
            header_table[item][1] = new_node
        else:                           #头指针非空，但出现新节点new_node，故应该通过链表的尾指针添加新节点来更新链表
            while link_node.link != None:
                link_node = link_node.link
            link_node.link = new_node
    else:
        father_node.children[item].count += count
    return father_node.children[item]

def trace(item, header_table):
    '''
    根据头指针表和fp-tree回溯，返回各项的条件模式基
    :param header_table:
    :param order_item:
    :return:
    '''
    cp_base = {}                                    #条件模式基
    head_node = header_table[item][1]
    '''由头指针表横向搜索所有同名项'''
    while head_node != None:
        prefix = []
        #leaf_node = deepcopy(head_node)
        leaf_node = head_node
        while leaf_node.father != None:
            prefix.append(leaf_node.name)
            leaf_node = leaf_node.father

        if len(prefix) > 1:
            cp_base[frozenset(prefix[1:])] = head_node.count
        head_node = head_node.link
    return cp_base

def cp_tree(header_table, order_item, min_support_count, suffix=set(), item_dict={}):
    '''
    通过回溯FP——Tree来递归地生成CP-Tree,从而不断延长频繁的后缀
    :param header_table: 头指针表
    :param order_item: 降序
    :param min_support_count:
    :param suffix: 后缀
    :param item_dict: 后缀对应支持度的字典
    :return:
    '''
    for item in reversed(order_item):
        new_item = suffix.copy()
        new_item.add(item)
        item_dict[frozenset(new_item)] = item_dict.get(frozenset(new_item),0) + header_table[item][0]
        cp_base = trace(item, header_table)
        cp_header, cp_order = init_header(cp_base, min_support_count)
        cp_header = build_tree(cp_base, cp_header, cp_order)
        if cp_header != None:
            cp_tree(cp_header, cp_order, min_support_count, new_item, item_dict)
    return item_dict

