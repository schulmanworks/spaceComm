# g1(x) = x^5 + x^2 + 1
# g2(x) = x^5 + x^4 +_ x^2 + x + 1
import binascii
import pdb
def shift(s, g):
    feedback = s[-1]
    s_new = [feedback & g[0]]
    i = 1
    for val in s[0:-1]:
        t = val ^ (feedback & g[i])
        s_new.append(t)
        i += 1
    print s_new
    return s_new
def LFSRseq(g,k,s):
    # g is list in format starting at low order and going high
    # so  1 + x^2 + x^5=> g = [1,0,1,0,0,1]
    # s is also a list
    pattern = [] # will be in binary list
    # constVal = int("".join(str(e) for e in g), 2)
    for x in range(k):
        # pdb.set_trace()
        curOut = s[-1]
        pattern.append(curOut)
        s = shift(s, g)
    return pattern
print LFSRseq([1,0,1,1], 8, [1,0,0])
