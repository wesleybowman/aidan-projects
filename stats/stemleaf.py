import numpy as np
from math import *

def stemleafpairs(data, Round=False, byFive=False, stempos= 0, leafwidth=1):
    """
    data - data array

    Round - whether you want to round (WARNING: may round up to 10)

    byFive- if you want the bins to be by five

    stempos - position of last digit of stem,
    from decimal point

    leafwidth - number of digits in leaves

    Return value:
        output - a list of stem-leaf pairs

        stems - only one copy of the stem with all of it's leaves
    """

    stem10 = pow(10, stempos)
    leaf10 = pow(10,leafwidth)

    output = []

    for x in data:
        if stempos > 0:
            leaf, stem = modf (x / stem10)
        else:
            leaf, stem = modf(x * stem10)

        leaf = abs(leaf * leaf10)

        if Round:
            leaf = round(leaf)

        output.append((int(stem), int(leaf) ))

    dtype=[('stem',int),('leaf',int)]
    output = np.array(output,dtype=dtype)
    output = np.sort(output,order='stem')

    laststem = False
    stems = []

    for s,l in output:
        if s!=laststem:
            leafs = []
            leafs.append(l)
            stems.append((s,leafs))

        if s==laststem:
            leafs.append(l)

        laststem = s

    for s,l in stems:

        if byFive:
            less = []
            greater = []

            for v in l:

                if v<5:
                    less.append(v)
                if v>=5:
                    greater.append(v)

            if less:
                print s, '|', less
            if greater:
                print s, '|', greater

        else:
            print s, '|', l

    return output, stems

if __name__ == '__main__':

    data = np.random.random_integers(12,50,100)

    '''
    Examples:
    #Pairs = stemleafpairs(data)
    #Pairs = stemleafpairs(data, stempos=1)
    #Pairs = stemleafpairs(data, byFive=True)
    '''

    Pairs = stemleafpairs(data, byFive=True, stempos=1)
