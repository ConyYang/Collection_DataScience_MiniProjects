a = 1
b = 2
dict = {'a': a, 'b':b}
import pickle

with open('test.pkl', 'wb') as handle:
    pickle.dump(dict, handle)

with open('test.pkl', 'rb') as handle:
    new_dict = pickle.load(handle)

print(new_dict)