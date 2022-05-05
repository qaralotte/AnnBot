import collections


# <KEY, deque<ELEMENT>>
class HistoryMap:
    # 历史记录队列最大储存量
    MAX_SIZE = 5

    def __init__(self):
        # 历史记录队列 (双向队列)
        self.container = {}

    def __getitem__(self, key):
        return self.container[key]

    def put(self, key, element):

        # 如果字典没有 key 则创建一个
        if key not in self.container:
            self.container[key] = collections.deque()

        # 如果队列已满，则推出一个元素
        if len(self.container[key]) == self.MAX_SIZE:
            self.container[key].popleft()

        self.container[key].append(element)

    def top(self, key):
        element = self.container[key].pop()
        self.container[key].append(element)
        return element
