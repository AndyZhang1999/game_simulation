#! python3.9.6 64-bit
# Arknights_寻访模拟 - 模拟明日方舟干员寻访

import random as rd  # 随机器

# import pygame  # GUI界面

import data  # 从data.py导入数据


class simulation:
    '''创建模拟器对象'''

    def __init__(self, chars, star6_p_up, star5_p_up):

        self.chars = chars
        self.star6_p_up = star6_p_up
        self.star5_p_up = star5_p_up
        self._type = None

        def parsing(star: int):
            '''解析(分离)出<star>星级的干员, 工具函数'''

            return ''.join(self.chars.split('\n\n')[6 - star].split('\n')).split('／')

        # 定义干员列表,以及概率
        # p => probability
        # chars => characters
        self.star6_p = 2  # 2%
        self.star6_chars = parsing(6)

        self.star5_p = 8  # 8%
        self.star5_chars = parsing(5)

        self.star4_p = 50  # 50%
        self.star4_chars = parsing(4)

        self.star3_p = 40  # 40%
        self.star3_chars = parsing(3)

        # print(star6_char, star5_char, star4_char, star3_char, sep='\n\n')
        # 初始化计数器
        self.times = 0
        self.times_without_star6 = 0
        self.levelup = 0
        self.times_of_star6 = 0
        self.times_of_star5 = 0
        self.times_of_star4 = 0
        self.times_of_star3 = 0

    def chanp(self):  # change probability
        self.levelup = max((self.times_without_star6 - 50) * 2, 0)  # 增加概率
        k = (98 - self.levelup) / 98
        # 修改概率
        if self.levelup:
            self.star6_p = 2 + self.levelup
            self.star5_p = 8 * k
            self.star4_p = 50 * k
            self.star3_p = 40 * k

    def simulate(self):
        '''模拟抽奖一次'''

        selected = rd.randint(0, 100)  # 产生一个随机数
        result = ''  # 记录角色名称
        self._type = None  # 用于记录星级

        # 定义概率范围, 3/4星都简单, 六星与五星有概率up
        if selected <= self.star6_p:  # 抽中6星
            self.times += 1  # 计数器加一
            self.times_without_star6 = 0  # 抽中六星,计数归零
            self.levelup = 0
            self.star6_p = 2
            self.star5_p = 8
            self.star4_p = 50
            self.star3_p = 40
            self.times_of_star6 += 1
            self._type = 6
            up = data.star6_p_up  # 读取up数值

            if up:  # 如果data.star6_p_up存在
                occupation = up[-1]  # 读取占据的概率
                selected = rd.randint(0, 100)  # 再次做选择
                if selected <= occupation:  # 如果小于占用比例,则获得限定干员
                    # 处理多个限定干员的情况
                    if len(up) > 2:
                        # 再次做选择, 排除后面的占用len(up) - 2)
                        result = up[rd.randint(0, len(up) - 2)]

                    else:
                        result = up[0]

                else:  # 如果大于占用比例,则获得常驻干员
                    result = self.star6_chars[rd.randint(
                        0, len(self.star6_chars) - 1)]

            else:  # 如果没有up,则普通选择
                result = self.star6_chars[rd.randint(
                    0, len(self.star6_chars) - 1)]

        elif selected <= self.star5_p + self.star6_p:  # 抽中5星
            self.times += 1
            self.times_without_star6 += 1
            self.chanp()
            self.times_of_star5 += 1
            self._type = 5
            up = data.star5_p_up  # 读取up数值

            if up:  # 如果data.star5_p_up存在
                occupation = up[-1]  # 读取占据的概率
                selected = rd.randint(0, 100)  # 再次做选择
                if selected <= occupation:  # 如果小于占用比例,则获得限定干员
                    # 处理多个限定干员的情况
                    if len(up) > 2:
                        # 再次做选择, 排除后面的占用len(up) - 2)
                        result = up[rd.randint(0, len(up) - 2)]

                    else:
                        result = up[0]

                else:  # 如果大于占用比例,则获得常驻干员
                    result = self.star5_chars[rd.randint(
                        0, len(self.star5_chars) - 1)]

            else:  # 如果没有up,则普通选择
                result = self.star5_chars[rd.randint(
                    0, len(self.star5_chars) - 1)]

        elif selected <= self.star4_p + self.star5_p + self.star6_p:  # 抽中4星
            self.times += 1
            self.times_without_star6 += 1
            self.chanp()
            self.times_of_star4 += 1
            self._type = 4

            result = self.star4_chars[rd.randint(0, len(self.star4_chars) - 1)]

        elif selected <= self.star3_p + self.star4_p + self.star5_p + self.star6_p:  # 抽中3星
            self.times += 1
            self.times_without_star6 += 1
            self.chanp()
            self.times_of_star3 += 1
            self._type = 3

            result = self.star3_chars[rd.randint(0, len(self.star3_chars) - 1)]

        else:
            result = self.simulate()  # 防止溢出

        return result, self._type

    def consecutive(self):
        '''十连抽'''

        results = []
        _types = []
        for i in range(10):
            selected = self.simulate()
            results.append(selected[0])
            _types.append(selected[1])

        return results, _types


def main():
    import pprint as pp  # 漂亮打印
    # - TEST -
    obj = simulation(data.chars, data.star6_p_up, data.star5_p_up)  # 创建寻访模拟对象
    results = []
    for i in range(10):
        results.append(obj.consecutive()[0])  # 十连抽模拟
    pp.pprint(results)

    print('\n')
    print(f'总数:    {obj.times}')
    print(f'六星个数:{obj.times_of_star6}')
    print(f'五星个数:{obj.times_of_star5}')

    # - THE END -


if __name__ == '__main__':
    main()
