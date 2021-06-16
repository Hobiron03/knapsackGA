import random
import math
import statistics


def main():
    # 持ち物（弁当）の定義。[重さ, 価値]
    bentos = [
        [9, 20],
        [7, 28],
        [8, 2],
        [2, 28],
        [10, 15],
        [7, 28],
        [7, 21],
        [8, 7],
        [5, 28],
        [4, 12],
        [7, 21],
        [5, 4],
        [7, 31],
        [5, 28],
        [2, 24],
        [8, 36],
        [3, 33],
        [2, 2],
        [9, 25],
        [6, 21],
    ]
    bento_num = len(bentos)  # 20
    gene_num = 10
    knapsack_max_weight = 70
    crossover_rate = 0.8
    mutation_rate = 0.05
    # エリート
    elete_num = 1
    # 交叉の時に選ぶ組みの数
    pair_num = 5

    genes = generate_first_genes(gene_num, bento_num)
    for i in range(50):
        print("------------第{}世代------------".format(i+1))
        # 手順2: 各交代の適応度の計算
        fitness_list = calculate_fitness(genes, knapsack_max_weight, bentos)
        print("平均適応度：{}".format(statistics.mean(fitness_list)))
        print("最大適応度：{}".format(max(fitness_list)))

        # 手順3: 交叉に利用する遺伝子の選択
        selected_genes = select_crossover_gene(genes, fitness_list)
        # selected_genes = select_crossover_gene_elete(
        #     genes, fitness_list, elete_num
        # )

        # 手順4 遺伝子型の交叉の実行
        new_generation_genes = crossover_genes(
            selected_genes, crossover_rate, pair_num
        )

        # 手順5 突然変異
        new_generation_genes = mutation(new_generation_genes, mutation_rate)

        genes = new_generation_genes


def generate_first_genes(gene_num: int, bento_num: int):
    # 入れるかどうかを0,1で表現。入れる場合は1
    # [0, 0, 1 ....] x 10
    genes = []
    for i in range(gene_num):
        genes.append([])
        for j in range(bento_num):
            genes[i].append(random.randrange(2))
    return genes


def calculate_fitness(genes: list, knapsack_max_weight: int, bentos: list) -> list:
    values = []
    weights = []
    for gene in genes:
        value_sum = 0
        weight_sum = 0
        for i, is_put_in in enumerate(gene):
            if is_put_in:
                weight, value = bentos[i]
                weight_sum += weight
                # 重量を超えるのが早いほどペナルティを重くしていく
                if weight_sum < knapsack_max_weight:
                    value_sum += value
                else:
                    value_sum -= value / i
                    weight_sum -= weight

        values.append(value_sum)
        weights.append(weight_sum)

    return values


def select_crossover_gene(genes: list, fitness_list: list):
    # len(genes)個の遺伝子から適応度比例選択でlen(genes）個選択する
    fitness_sum = sum(fitness_list)
    # ルーレット選択において各遺伝子が選択される比率を格納したもの(%)
    fitness_ratios = []
    for fitness in fitness_list:
        fitness_ratios.append(fitness/fitness_sum * 100)

    # roulet selrct
    selected_index_list = []
    for i in range(len(genes)):
        roulet_sum = 0
        roulet_num = random.randrange(100)
        for i, fitness_ratio in enumerate(fitness_ratios):
            if roulet_sum <= roulet_num <= roulet_sum + fitness_ratio:
                selected_index_list.append(i)
                roulet_sum = 0
                break
            roulet_sum += fitness_ratio

    selected_genes = []
    for si in selected_index_list:
        selected_genes.append(genes[si])

    return selected_genes


def select_crossover_gene_elete(genes: list, fitness_list: list, elete_num: int):
    # len(genes)個の遺伝子から適応度比例選択でlen(genes）個選択する
    fitness_sum = sum(fitness_list)
    # ルーレット選択において各遺伝子が選択される比率を格納したもの(%)
    fitness_ratios = []
    for fitness in fitness_list:
        fitness_ratios.append(fitness/fitness_sum * 100)

    # roulet selrct
    selected_index_list = []

    # 世代のエリートを1人追加数
    fitness_max = 0
    fitness_max_index = 0
    for i, fitness in enumerate(fitness_list):
        if fitness > fitness_max:
            fitness_max = fitness
            fitness_max_index = i
    selected_index_list.append(fitness_max_index)

    # 残りを追加
    for i in range(len(genes) - elete_num):
        roulet_sum = 0
        roulet_num = random.randrange(100)
        for i, fitness_ratio in enumerate(fitness_ratios):
            if roulet_sum <= roulet_num <= roulet_sum + fitness_ratio:
                selected_index_list.append(i)
                roulet_sum = 0
                break
            roulet_sum += fitness_ratio

    selected_genes = []
    for si in selected_index_list:
        selected_genes.append(genes[si])

    return selected_genes


def crossover_genes(selected_genes: list, crossover_rate: float, pair_num: int) -> list:
    # 二つの個体のペアをpair_num個（pair_num回）ランダムに選択し交叉する。
    new_generetions = []
    for i in range(pair_num):
        gene_a = selected_genes[random.randrange(10)]
        gene_b = selected_genes[random.randrange(10)]

        roulet = random.randrange(100)
        if roulet < crossover_rate * 100:
            # 単純交叉
            center = math.floor(len(gene_a)/2)
            gene_a_front = gene_a[0:center]
            gene_a_back = gene_a[center:]

            gene_b_front = gene_b[0:center]
            gene_b_back = gene_b[center:]

            new_generetions.append(gene_a_front + gene_b_back)
            new_generetions.append(gene_b_front + gene_a_back)

        else:
            # 交叉は行わずそのまま次の世代へ
            new_generetions.append(gene_a)
            new_generetions.append(gene_b)

    return new_generetions


def mutation(new_generetions_genes: list, mutation_rate: float) -> list:
    # ランダムな場所を反転させる
    for n_gene in new_generetions_genes:
        mutation_roulet = random.randrange(100)
        if mutation_roulet < mutation_rate * 100:
            mutate_place = random.randrange(len(n_gene))
            if n_gene[mutate_place] == 0:
                n_gene[mutate_place] = 1
            else:
                n_gene[mutate_place] = 0

    return new_generetions_genes


if __name__ == '__main__':
    main()
