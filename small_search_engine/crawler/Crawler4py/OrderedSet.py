﻿'''
@Author: Raymond Hettiger, and released under the MIT license
@Source: http://code.activestate.com/recipes/576694/ 
'''

import collections

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:        
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


class OrderedSetForFrontier(OrderedSet):
    def __init__(self, iterable = None):
        self._keyParts = set()
        return super(OrderedSetForFrontier, self).__init__(iterable)

    def add(self, key):
        super(OrderedSetForFrontier, self).add(key)
        try: 
            self._keyParts.add(key[0])
        except:
            "No keypart tuple"

    def pop(self, last = True):
        popped = super(OrderedSetForFrontier, self).pop(last)
        try: 
            self._keyParts.remove(popped[0])
        except:
            "No keypart tuple to worry about"
        return popped

    def discard(self, key):
        super(OrderedSetForFrontier, self).discard(key)
        try: 
            self._keyParts.remove(key[0])
        except:
            "No keypart tuple to worry about"

    def contains_url(self, url):
        return url in self._keyParts


