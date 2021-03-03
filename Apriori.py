from itertools import combinations
def apriori(data_set, min_support):
    '''
    生成频繁项集和其对应的支持度字典
    :param data_set: 导入的数据列表，数据结构为[f_set]
    :param min_support:
    :return: 支持度字典sup_dict,{f_set:support}
    '''
    #数据初始化
    min_support_count = len(data_set) * min_support
    #项集初始化，生成频繁一项集
    c1_set = []
    for transaction in data_set:
        for item in transaction:
            if [item] not in c1_set:
                c1_set.append([item])       #这里不应直接用frozenset函数直接转化，会拖慢算法计算效率
    c1_set.sort()  # 字典序
    c1_set = list(map(frozenset,c1_set))
    sup_dict = gen_fk(data_set,c1_set,min_support_count)
    #迭代初始化

    fk_dict = sup_dict
    k = 1       #频繁项集的项数
    while len(list(fk_dict.keys())) > 1:
        ckp_set = gen_ckp(fk_dict, k)
        ckp_set = cut(ckp_set, fk_dict, k)
        fk_dict = gen_fk(data_set, ckp_set, min_support_count)
        sup_dict.update(fk_dict)
        k += 1
    return sup_dict

def gen_fk(data_set, ck_set, min_support_count):
    '''
    扫描数据库，对候选k项集的集合进行剪枝，生成频繁k项集的集合
    :param data_set: Mashroom数据集，数据结构[f_set]
    :param ck_set: 候选k项集的集合，数据结构[f_set]
    :param min_support: 支持度阈值
    :return:其支持度字典fk_dict，数据结构{f_set:support}
    '''
    fk_dict = {}
    for candidate in ck_set:                               #candidate为候选项，数据结构为集合，便于使用issubset函数
        support_count = 0                              #每一个候选项的支持度计数赋初值为0
        for transaction in data_set:  #列表元素转换为frozenset
            if candidate.issubset(transaction):
                support_count += 1
        if support_count >= min_support_count:
            fk_dict[candidate] = support_count
    return fk_dict

def gen_ckp(fk_dict, k):
    '''
    生成候选(k+1)项集的集合
    :param fk_dict:频繁k项集的集合，数据结构{f_set:support}
    :param k:频繁项集的项数k
    :return:候选(k+1)项集的集合，数据结构[f_set]
    '''
    fk_set = list(fk_dict.keys())
    ckp_set = []
    n_f = len(fk_set)
    for  i in range(n_f-1):
        for j in range(i+1,n_f):
            temp1 = list(fk_set[i])[:(k - 1)]
            temp2 = list(fk_set[j])[:(k - 1)]
            temp1.sort()
            temp2.sort()
            if temp1 == temp2:
                ckp_set.append(fk_set[i] | fk_set[j])
    return ckp_set

def cut(ckp_set, fk_dict, k):
    '''利用Apriori原理剪枝'''
    for candidate in ckp_set:
        sub_set_list = list(combinations(candidate, k))
        for sub_set in sub_set_list:
            if frozenset(sub_set) not in fk_dict:
                ckp_set.remove(candidate)
                break
    return ckp_set