def print_box(Data: list[tuple], maxlen: tuple[int], tuple_size: int):
    '''
    To print a box around data to give some semblence to structure
    It is assumed all tuples in data are in equal length
    It is also assumed that all the values in maxlen correspond to max length of each data in each tuple 
    of the list
    '''
    
    head = Data[0]
    for j in range(tuple_size):
        print('+' + '-' * (maxlen[j] + 2), end = '')
    print('+')
    for i in range(tuple_size):
        space: int = maxlen[i] + 2
        print('|' + f'{head[i]:^{space}}', end = '')
    print('|')
    for j in range(tuple_size):
        print('+' + '-' * (maxlen[j] + 2), end = '')
    print('+')

    Data = Data[1:]
    for i in Data:
        for j in range(tuple_size):
            space = maxlen[j] + 2
            print('|' + f'{i[j]:^{space}}', end = '')
        print('|')

    for j in range(tuple_size):
        space = maxlen[j] + 2
        print('+' + '-' * space, end = '')
    print('+')

