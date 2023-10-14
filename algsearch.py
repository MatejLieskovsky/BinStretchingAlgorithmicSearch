#!/usr/bin/env python3

import sys

from domcache import DomCache
from levels import Levels
from itemsets import ItemSet
from time import time
from collections import defaultdict
from pickle import dump

class Problem ():
    def __init__ (self, bins, granularity, stretch):
        self.M = bins
        self.K = granularity
        self.S = stretch

        self.T = self.K+self.S
        self.V = (self.K+1)*self.M-1

        self.cache = defaultdict(DomCache)

        # Set up levels
        Levels.limit = self.T

        # Set up item sets
        self.empty = ItemSet((0,)*self.K)
        self.optimum = self.empty
        for _ in range(self.M): self.optimum+=(self.K-1)

    def solve (self, levels, history):

        remaining = self.V - sum(levels)

        if remaining + min(levels) <= self.T: return True

        C = self.cache[levels]
        p = C.probe(history)

        if p is True: return True
        if p is False: return False

        size_limit = min((remaining, self.K))

        res = True
        for i in range(size_limit):
            H = history+i
            I = i+1
            res = any(all(self.solve(L,H) for L in option)
                      for option in levels.options(I)
                      )
            if not res: res = not (H <= self.optimum)
            if not res: break

        C.add(history, res)
        return res

    def run (self):
        return self.solve(Levels((0,)*self.M), self.empty)
        
def run(bins, granularity, stretch):
    P = Problem(bins, granularity, stretch)
    start = time()
    result = P.run()
    end = time()

    report = """
Input: {} {} {}
{}/{} = {}
Result: {}
Time taken: {}
Pack: {}
Dom: {}
""".format(bins, granularity, stretch,
           granularity+stretch, granularity, (granularity+stretch)/granularity,
           result, end-start,
           ItemSet.cache_info(), DomCache.cache_info())
    DomCache.reset_counters()


    print(report)
    with open("reports/{}_{}_{}".format(bins,granularity,stretch),"w") as r:
        r.write(report)

    with open("/aux/ml/153/data_{}_{}_{}".format(bins,granularity,stretch),"wb") as f:
        dump(P.cache, f)
    print("=============")
    print()

    return result

if __name__=="__main__":
    run(*map(int,sys.argv[1:]))
