class Levels (tuple):
    
    limit = None # Must be set by the algorithm

    def place (self, size, target):
        l = list(self)
        l[target] += size
        l.sort(reverse=True)
        return Levels(l)

    def options (self, size):
        if size == 1: # class 1 items must not underflow
            return [(self.place(1,i),)
                    for i in range(len(self))
                    if self[i]+1 <= Levels.limit
                    and (i == 0 or self[i] != self[i-1])
                    ]
        
        return [(self.place(size-1,i),self.place(size,i))
                for i in range(len(self))
                if self[i]+size <= Levels.limit
                and (i == 0 or self[i] != self[i-1])
                ]
