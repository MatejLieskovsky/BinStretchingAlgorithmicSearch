class DomCache ():
    hits = 0
    elims = 0
    misses = 0
    def __init__ (self):
        self.upper = set()
        self.lower = set()

    def probe (self, x):
        if any(x >= y for y in self.upper):
            DomCache.hits+=1
            return True
        if any(x <= y for y in self.lower):
            DomCache.hits+=1
            return False
        DomCache.misses+=1
        return None

    def add (self, x, result):
        if result is True:
            for y in list(self.upper):
                if x < y:
                    self.upper.remove(y)
                    DomCache.elims+=1
            self.upper.add(x)
            return
            
        if result is False:
            for y in list(self.lower):
                if x > y:
                    self.lower.remove(y)
                    DomCache.elims+=1
            self.lower.add(x)
            return
        raise NotImplementedError

    def cache_info():
        return "CacheInfo(hits={},misses={},elims={},currsize={})".format(
            DomCache.hits,
            DomCache.misses,
            DomCache.elims,
            DomCache.misses-DomCache.elims)

    def reset_counters():
        DomCache.hits = 0
        DomCache.elims = 0
        DomCache.misses = 0
