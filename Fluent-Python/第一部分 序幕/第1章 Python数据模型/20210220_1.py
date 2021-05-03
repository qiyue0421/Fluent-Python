# 如何实现 __getitem__ 和 __len__ 两个特殊方法
from random import choice
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])  # 命名元组用于构建只有少数属性但没有方法的对象


# 定义纸牌类，包含不同牌号和花色
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = ['spades', 'diamonds', 'clubs', 'hearts']

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    # __getitem__方法把 [] 操作交给了self._cards列表，所以自动支持切片操作
    def __getitem__(self, position):
        return self._cards[position]


# 获取一个纸牌对象，其中包含52张牌
beer_card = Card('7', 'diamonds')
print(beer_card)

# 初始化类得到一个实例
deck = FrenchDeck()

# len()函数查看多少张
print(len(deck))

# 取出特定位置的纸牌
print(deck[0])
print(deck[-1])

# 随机抽取纸牌
print(choice(deck))

# 切片操作
print(deck[:3])
print(deck[12::13])

# __getitem__方法同样实现了迭代操作
# for card in deck:
#     print(card)
#
# for card in reversed(deck):  # 反向迭代
#     print(card)


# 进行升序排序
# suit_values = dict(spades=3, hearts=2, diamonds=第5章 一等函数, clubs=0)  # 赋予花色相应的值
#
#
# def spades_high(card):
#     rank_value = FrenchDeck.ranks.index(card.rank)
#     return rank_value * len(suit_values) + suit_values[card.suit]  # 牌号值加上花色值
#
#
# for card in sorted(deck, key=spades_high):
#     print(card)