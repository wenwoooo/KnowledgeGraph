from fractions import Fraction


# 定义一个函数用于计算概率
def calculate_probabilities(n, m, friend_pairs):
    # 创建邻接矩阵
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in friend_pairs:
        adj_matrix[u - 1][v - 1] = 1
        adj_matrix[v - 1][u - 1] = 1

    # 定义一个函数来检查两个学生是否为好友
    def are_friends(student1, student2):
        return adj_matrix[student1 - 1][student2 - 1] == 1

    # 定义一个函数来检查一个学生的好友列表
    def get_friends(student):
        return [i + 1 for i in range(n) if adj_matrix[student - 1][i] == 1]

    # 初始化结果列表
    results = []

    # 遍历每个学生
    for student in range(1, n + 1):
        # 计算每种情况下满足条件的小组数量
        no_friends_count = (n - len(get_friends(student))) * (n - len(get_friends(student)) - 1) // 2
        two_friends_with_self_count = len(get_friends(student)) * (n - len(get_friends(student)) - 1)
        two_friends_without_self_count = len(get_friends(student)) * (len(get_friends(student)) - 1) // 2
        two_pairs_with_self_count = sum(len(get_friends(friend)) - 1 for friend in get_friends(student))
        two_pairs_without_self_count = sum(
            (len(get_friends(friend)) - 1) * (n - len(get_friends(friend)) - 1) for friend in get_friends(student))
        all_friends_count = sum(len(get_friends(friend)) - 1 for friend in get_friends(student)) * (
                len(get_friends(student)) - 2) // 2

        # 计算总的可能小组数
        total_groups = n * (n - 1) * (n - 2) // 6

        # 计算概率并添加到结果列表
        results.append([
            Fraction(no_friends_count, total_groups),
            Fraction(two_friends_with_self_count, total_groups),
            Fraction(two_friends_without_self_count, total_groups),
            Fraction(two_pairs_with_self_count, total_groups),
            Fraction(two_pairs_without_self_count, total_groups),
            Fraction(all_friends_count, total_groups)
        ])

    return results


# 读取输入
n, m = map(int, input().split())
friend_pairs = [tuple(map(int, input().split())) for _ in range(m)]

# 计算概率
probabilities = calculate_probabilities(n, m, friend_pairs)

# 输出结果
for result in probabilities:
    print(' '.join(f"{frac.numerator}/{frac.denominator}" if frac != 0 else "0/1" for frac in result))
