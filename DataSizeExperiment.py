from FIM.Experiment import *
from time import time
import matplotlib.pyplot as plt

def load_dataset(path, row=0):
    '''
    读取数据集，通过row参数控制读取的数据H行数，默认全部读取
    :param path: 文件路径
    :param row: 要读取的数据的行数
    :return: data_set,数据结构[f_set]
    '''
    with open(path, 'rb') as data_file:
        data_set = []
        count = 0
        for line in data_file:
            if row and count == row:
                break
            line = line.split()
            int_line = frozenset(map(int, line))
            data_set.append(int_line)
            count += 1

    return data_set

def cal_time(algorithm, data_set, min_support):
    t0 = time()
    print(len(data_set))
    sup_dict = algorithm(data_set, min_support)
    print(len(sup_dict))
    t1 = time()
    return t1-t0

def get_y_value(path, size_list, min_support, replication=1):

    algorithm_list = [Apriori.apriori, Eclat.eclat, FP_Growth.fp_growth]
    time_matrix = []
    for size in size_list:
        data_set = load_dataset(path, size)
        time_list = []
        for algorithm in algorithm_list:
            time_span = 0
            for i in range(replication):
                time_span += cal_time(algorithm, data_set, min_support)
            time_list.append(time_span/replication)
        time_matrix.append(time_list)

    y_value = []
    for i in range(len(time_matrix[0])):
        temp = []
        for j in range(len(time_matrix)):
            temp.append(time_matrix[j][i])
        y_value.append(temp)

    return y_value

def visualize(x_value, y_value, title, xlabel, ylabel='Time/s'):
    plt.plot(x_value, y_value[0], marker='o', linestyle='-', label='Apriori')
    plt.plot(x_value, y_value[1], marker='s', linestyle='--', label='Ecalt')
    plt.plot(x_value, y_value[2], marker='*', linestyle=':', label='FP-Growth')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.show()

def do_data_size_experiment(data_file, size_list, min_support, replication=1):

    xlabel = 'Data Size' + ' | min support={}'.format(min_support)
    title = data_file.title()

    path = './DataSet/' + data_file + '.dat'
    y_value = get_y_value(path, size_list, min_support, replication)
    print(y_value)
    x_value = size_list
    visualize(x_value, y_value, title, xlabel)

if __name__ == '__main__':
    t0 = time()
    data_file = 'T10I4D100K'
    min_support = 0.5
    size_list = range(10000, 110000, 10000)
    do_data_size_experiment(data_file, size_list, min_support)
    t1 = time()
    print(t1-t0)