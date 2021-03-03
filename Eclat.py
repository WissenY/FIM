def eclat(data_set, min_support):
    n_trans = len(data_set)
    min_sup_count = n_trans * min_support
    '''生成初始频繁1项集的垂直表示'''
    f1_tid = {}
    f1_sup = {}
    c1_set = frozenset([item for transaction in data_set for item in transaction])
    for item in c1_set:
        c1_tid = set()
        support_count = 0
        for tid in range(n_trans):
            if item in data_set[tid]:
                c1_tid.add(tid)
                support_count += 1
        if support_count >= min_sup_count:
            itemset = frozenset([item])
            f1_tid[itemset] = frozenset(c1_tid)
            f1_sup[itemset] = support_count

    sup_dict = gen_fk(f1_tid, f1_sup, min_sup_count)
    return sup_dict

def gen_fk(f_tid, sup_dict, min_support_count):
    '''
    递归生成频繁项集
    :param f_tid: 频繁项集与tidset的字典，数据结构{f_set:f_set}
    :param sup_dict: 存储所有频繁项集的字典，键为频繁项集，值为支持度，数据结构{f_set:int}
    :param min_support_count: 最小支持度计数
    :return:
    '''
    f_set = list(f_tid.keys())
    tid_set = list(f_tid.values())
    n_item = len(f_set)

    for i in range(n_item-1):
        fp_tid = {}
        for j in range(i+1, n_item):
            cp_set = f_set[i] | f_set[j]
            cp_tid = tid_set[i] & tid_set[j]
            support_count = len(cp_tid)
            if support_count >= min_support_count:
                fp_tid[cp_set] = cp_tid
                sup_dict[cp_set] = support_count
        if len(fp_tid) > 1:
            gen_fk(fp_tid, sup_dict, min_support_count)
    return sup_dict
