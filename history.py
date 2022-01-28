class History (tuple) :
    def __le__ (self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return FFD(self.d_list(), other.a_list())
        return NotImplemented

    def __lt__ (self, other):
        return self <= other and self != other

    def __ge__ (self, other):
        return other <= self

    def __gt__ (self, other):
        return other <= self and self != other

    def a_list (self):
        l = list()
        for x in ([i]*self[i] for i in range(len(self))):
            l.extend(x)
        return l

    def d_list (self):
        return list(reversed(self.a_list()))

    def __add__ (self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return History([self[i]+other[i] for i in range(len(self))])
        
        if isinstance(other, int):
            o = [0]*len(self)
            o[other] = 1
            return self+tuple(o)

        return NotImplemented


def FFD (items, bins):
    for item in items:
        t = None
        for i in range(len(bins)):
            if bins[i] >= item:
                t = i
                break
        if t is None:
            return False
        bins[t] -= item
    return True
