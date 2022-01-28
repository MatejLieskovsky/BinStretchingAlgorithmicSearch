#!/usr/bin/env python3
from itertools import product
from history import History
from functools import cache
from mip import Model, BINARY, xsum, OptimizationStatus
import sys
from time import time

# Pass data as a (levels, history) pair

# Try to solve the game from a given state
# Return problematic item size or None

def place(levels, size, position):  # Helper function for increasing levels
    l = list()
    for i in range(len(levels)):
        if i == position:
            l.append(levels[i]+size)
        else:
            l.append(levels[i])
    l.sort(reverse=True)  # This effectively makes search use best fit.
    return tuple(l)

class Problem ():
    def __init__ (self, M, K, S):
        self.M = M
        self.K = K
        self.S = S
        self.V = M*K
        self.overflows = list(product((0,1), repeat=M))
        self.cache = dict()  # Dictionary of lower (lost) and upper (won) bounds
        self.cache_hits = 0
        self.cache_misses = 0

    def solve (self, levels, history):
        if sum(levels) >= self.V:
            return True  # Opponent cheated by using too much volume (remember the +epsilons)
            
        remaining = self.V - sum(levels) - 1
        if remaining + min(levels) < self.S:
            return True  # Throw the rest into emptiest bin

        if levels not in self.cache:
            self.cache[levels] = (set(), set())

        if any(history <= h for h in self.cache[levels][0]):
            self.cache_hits += 1
            return False  # Cached loss

        if any(history >= h for h in self.cache[levels][1]):
            self.cache_hits += 1
            return True  # Cached win

        self.cache_misses += 1
        
        size_limit = min((remaining, self.K))

        items = [(0,[1]*self.M)] + [(s,o) for s in range(1,size_limit) for o in self.overflows]
        for item in items:
            if not self.search(item, levels, history+item[0]):
                self.cache[levels][0].add(history)
                return False
        self.cache[levels][1].add(history)
        return True
            

    def search (self, item, levels, history):
        for target in range(self.M):
            size = item[0]+item[1][target]
            l = place(levels, size, target)
            if l[0] < self.S and self.solve(l, history):
                return True
        return self.check(history)  # Did the opponent cheat with item sizes?

            

    @cache(maxsize=None)
    def check(self, history):
        history = history.a_list()
        m = Model()
        m.verbose = 0
        m.emphasis = 1
        n = len(history)

        # x[i][j] is bool "is i-th item in j-th bin?"
        x = [[m.add_var(var_type=BINARY) for j in range(self.M)] for i in range(n)]

        # every item is in exactly one bin
        for i in range(len(history)):
            m += xsum(x[i][j] for j in range(self.M)) == 1

        # every bin is not overfull
        for j in range(self.M):
            m += xsum(x[i][j]*history[i] for i in range(n)) <= self.K-1

        status = m.optimize()

        if status == OptimizationStatus.INT_INFEASIBLE or status == OptimizationStatus.INFEASIBLE:
            return True
        return False

    def run(self):
        return self.solve((0,)*self.M, History((0,)*self.K))

    def sci(self):
        return "CacheInfo(hits={}, misses={})".format(self.cache_hits, self.cache_misses)

    def cci(self):
        return self.check.cache_info()

def main ():
    M = int(sys.argv[1])
    K = int(sys.argv[2])
    T = int(sys.argv[3])
    
    P = Problem(M, K, T)
    start = time()
    result = P.run()
    end = time()

    report = """
Result: {}
Solve: {}
Check: {}
Time taken: {}
""".format(result, P.sci(), P.cci(), end-start)
    print(report)


    #with open("OUTPUT_DIR/report{}_{}_{}".format(*sys.argv[1:4]),"w") as r:
    #    r.write(report)
    
if __name__ == "__main__":
    main()
