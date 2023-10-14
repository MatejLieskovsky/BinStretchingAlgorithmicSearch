from functools import cache

class ItemSet (tuple):
    def __le__ (self, other): return pack(self, other)
    def __lt__ (self, other): return pack(self, other) and self != other
    def __ge__ (self, other): return pack(other, self)
    def __gt__ (self, other): return pack(other, self) and self != other

    def __add__ (self, other):
        if other == 0: return self

        l = list(self)
        l[other]+=1
        l[0]+=other
        return ItemSet(l)

    def cache_info (): return _pack.cache_info()

def pack (items, bins) :
    data = [bins[i]-items[i] for i in range(len(bins))]
    return _pack(tuple(largescan(data)))

@cache
def _pack(instance):
    if instance[0] < 0: return False
    
    l = len(instance)

    # exhaustive search prioritizing BFD
    for i in reversed(range(1,l)):
        if instance[i] < 0:  # found largest item
            for b in range(i+1,l):
                if instance[b] > 0:  # found a useable bin
                    data = list(instance)
                    data[i]+=1
                    data[b]-=1
                    data[b-i]+=1
                    if _pack(tuple(largescan(data))): return True
            return False  # no good placement for that item
    return True  # no item found

def largescan(data):  # Pack largest items while non-ambiguous

    l = len(data)
    b = l-1 # maximal possible index of the largest bin
    
    while True:
        while b > 0:
            if data[b] > 0: break  # largest bin
            if data[b] < 0: return (-1,)*l  # unpackable item
            b-=1
        else : return (0,)*l  # empty instance

        i = b-1

        while i > 0:
            if data[i] > 0: return smallscan(data)  # non-trivial instance
            if data[i] < 0: # pack an item and repeat
                data[i]+=1
                data[b]-=1
                data[b-i]+=1
                break
            i-=1
        else: return (0,)*l  # no item found

def smallscan (data):  # Pack smallest items while non-ambiguous

    l = len(data)
    i = 1

    while True:
        while i < l:
            if data[i] < 0: break  # smallest item
            if data[i] > 0: # discard unuseably small bins
                data[0] -= i*data[i]
                data[i] = 0
            i += 1
            
        if data[0] < 0: return (-1,)*l  # too much volume
        if i == l: return (0,)*l  # no items found
        
        b = i+1

        while b < l:
            if data[b] < 0: return data  # non-trivial instance
            if data[b] > 0: # pack an item and repeat
                data[b]-=1
                data[i]+=1
                r = b-i
                if r >= i: data[r]+=1
                else: data[0]-=r
                break
            b+=1
        else: print("FAIL", data)
