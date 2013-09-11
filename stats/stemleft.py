import numpy as np
from math import *
import scipy.stats as stat


def stemleafpairs(data, Round=True, stempos= 0, leafwidth=1):
    """
    X - data array
    stempos - position of last digit of stem,
    from decimal point.
    leafwidth - number of digits in leaves.

    Return value:
        a list of stem-leaf pairs
    """

    stem10 = pow(10, stempos)
    leaf10 = 10**leafwidth

    output = []

    for x in data:
        if stempos > 0:
            leaf, stem = modf (x / stem10)
        else:
            leaf, stem = modf(x * stem10)

        leaf = abs(leaf * leaf10)

        if Round:
            leaf = round(leaf)

        #print x, int(stem), round(leaf) # decomment after testing!

        output.append((int(stem), int(leaf) ))

    return output


def prettyprint(Pairs, blanks=False, stemwidth=4):
    """
    Given a list of Pairs (stem, leaf), prints out a stem and left plot

    blanks - whether to include the stem of numbers that aren't there
    stemwidth - the max amount of numbers in the stem, including spaces

    Return value:
        stem and left plot

    """
    Pairs.sort()
    minstem = Pairs[0][0]

    laststem = minstem
    outstr = "%*d" % (stemwidth, minstem) + "|"
    for (stem, leaf) in Pairs:
        if stem!= laststem:
            print outstr
            outstr = ""

            if blanks:
                for i in range(laststem+1, stem):
                    outstr = "%*d" % (stemwidth, i) + "|"
                    print outstr

            outstr = "%*d" % (stemwidth, stem) + "|"
            laststem = stem

        outstr += str(leaf)
    print outstr + '\n'


if __name__ == '__main__':

    file1 = '1950life.txt'
    file2 = '2012life.txt'
    data1 =  np.loadtxt(file1)
    data2 =  np.loadtxt(file2)

    Pairs1 = stemleafpairs(data1)
    Pairs2 = stemleafpairs(data2)

    print '\n'+file1 + '\n'
    #without blanks
    prettyprint(Pairs1)
    #with blanks
    prettyprint(Pairs1, blanks=True)

    print file2 + '\n'
    prettyprint(Pairs2)

