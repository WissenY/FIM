from os import listdir
from scipy.stats import mode
from time import time

def load_dataset(path, row=0):
    '''
    读取数据集，通过row参数控制读取的数据H行数，默认全部读取
    :param path: 文件路径
    :param row: 要读取的数据的行数
    :return: data_set,数据结构[f_set]
    '''
    with open(path,'rb') as data_file:
        data_set = []
        count = 0
        for line in data_file:
            if row and count == row:
                break
            line = line.split()
            int_line = frozenset(map(int, line))
            data_set.append(int_line)
            count += 1

    len_list = [len(record) for record in data_set]
    max_item = max(len_list)
    min_item = min(len_list)
    mode_item = mode(len_list)[0][0]
    item_set = frozenset([item for record in data_set for item in record])
    print('''
    DataSet: {FileName}
    Number of transactions: {LenOfDataset}
    Number of item: {LenOfItemSet}
    Max length of transactions: {MaxLenOfTransactions}
    Min length of transactions: {MinLenOfTransactions}
    Mode length of transactions: {ModeLenOfTransactions}
    -----------------------------------------------------'''.format(
        FileName=path[10:],
        LenOfDataset=len(data_set),
        LenOfItemSet=len(item_set),
        MaxLenOfTransactions=max_item,
        MinLenOfTransactions=min_item,
        ModeLenOfTransactions=mode_item))

    return data_set, item_set

if __name__ == '__main__':
    t0 = time()
    file_list = listdir('DataSet')
    for file in file_list:
        path = './DataSet/' + file
        load_dataset(path)
    t1 = time()
    print(t1-t0)