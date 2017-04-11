'''
#!/usr/bin/env python
import random


#fileout = open('million_3D_points.txt', 'w')
#text = []

for _ in xrange(10**6):
    #text.append(' '.join(str(random.randrange(100)) for _ in range(3)))
    print ' '.join(str(random.randrange(100)) for _ in range(3))
    
#fileout.writelines(text)

'''




from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))



'''

#!/usr/bin/env python
import numpy

NDIM = 3 # number of dimensions

# read points into array
a = numpy.fromfile('million_3D_points.txt', sep=' ')
#a = numpy.array([54.,  71.,  40.,71.,   7.,  94.])


print a
a.shape = a.size / NDIM, NDIM
print a.shape


point = numpy.random.uniform(0, 100, NDIM) # choose random point


print 'point:', point

d = ((a-point)**2).sum(axis=1)  # compute distances
print d


ndx = d.argsort() # indirect sort 
print ndx
# print 10 nearest points to the chosen one
import pprint
pprint.pprint(zip(a[ndx[:10]], d[ndx[:10]]))
'''
