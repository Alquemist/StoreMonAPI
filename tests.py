
# def filterData(obj, keysForDel):
#     return {key: obj[key] for key in obj.keys() if (key not in keysForDel)}


# d = {'prodId': 1, 'naziv': 'inv', 'kolicina': 0, 'jedMjere': 'kom', 'ukupno': '1.0000', 'zapKolicina': '1', 'vrijednost': '1', 'trosak': '1', 'rabat': '1'}

# d2 = filterData(d, ['kolicina', 'naziv', 'jedMjere', 'prodId' ])
# print(d2)

# sl = [{'a': '1,0000', 'b': 'B', 'c': [1,2,3], 'd': '0.100', 'e':'1.00.1'}]

# def strToFloat(s):
#     try:
#         return float(s)
#     except:
#         return(s)

# data = [{key:strToFloat(val) for (key, val) in lst.items()} for lst in sl]
# print(data)

# d = {'a':1, 'b':2}
# #d.update({'c':3})
# print(**{**d, 'c':3})
#q1 = {"a":[1,2]}
q2 = {"b": 1, "c": 2, "a":0}

# def fn1(x):
#     print(1, x)

# def fn2(x):
#     print(2, x)

# switch = {"a":fn1, "b": fn2}

# # switch.get(list(q1.keys())[0])("nesto")
# q2 = {"b": 1, "c": 2, "a":0}
# b, c, a
# b, c, a = **q2
# print(b)

# foo = {"foo": 1, "bar": 2}
# foo, bar = **{"foo": 1, "bar": 2}
a = ['a', 'b']
print(a[-1])