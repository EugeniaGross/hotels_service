# class Bank:
#     def __init__(self, name):
#         self.name = name
        
        
# class Organization:
#     def __init__(self, name):
#         self.name = name
        
        
# class Physical:
#     def __init__(self, last_name, first_name, middle_name):
#         self.last_name = last_name
#         self.first_name = first_name
#         self.middle_name = middle_name
        
        
# class FNS:
#     pass


# class CenterBank:
#     pass


def get_mean_median():
    data = []
    while True:
        elem = int(input())
        if elem == 0:
            break
        data.append(elem)
    data = sorted(data)
    data_lenght = len(data) 
    center = (data_lenght // 2 - 1, data_lenght // 2) if data_lenght % 2 == 0 else (data_lenght // 2, )
    q1 = len(data[0: center[0] + 1]) // 2 - 1
    if len(center) == 2:
        q3 = center[1] + len(data[center[1]:]) // 2 if len(data[center[1]:]) % 2 == 0 else center[1] + len(data[center[1]:]) // 2 + 1
    else:
        q3 = center[0] + len(data[center[0]:]) // 2 if len(data[center[0]:]) % 2 == 0 else center[0] + len(data[center[0]:]) // 2 + 1
    mean_median = sum(data[q1+1:q3-1])/len(data[q1+1:q3-1])
    return mean_median

print(get_mean_median())