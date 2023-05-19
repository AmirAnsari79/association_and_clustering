from collections import defaultdict
from itertools import combinations, chain


def retrieve_item_set(
    item_set_list,
):
    new_item_set = set()
    for item_set in item_set_list:
        for item in item_set:
            new_item_set.add(frozenset([item]))
    return new_item_set


def filter_freq_item_set(
    item_set,
    item_set_list,
    min_sup,
    global_item_set_with_sup,
):
    freq_item_set = set()
    local_item_set_with_sup = defaultdict(int)
    for item in item_set:
        for item_set in item_set_list:
            if item.issubset(item_set):
                global_item_set_with_sup[item] += 1
                local_item_set_with_sup[item] += 1
    for item, sup_count in local_item_set_with_sup.items():
        support = float(sup_count / len(item_set_list))
        if support >= min_sup:
            freq_item_set.add(item)
    return freq_item_set


def get_union(
    item_set,
    length,
):
    return set(
        [a.union(b) for a in item_set for b in item_set if len(a.union(b)) == length]
    )


def pruning(
    candidate_set,
    previous_freq_set,
    length,
):
    temp_candidate_set = candidate_set.copy()
    for item in candidate_set:
        subsets = combinations(item, length)
        for subset in subsets:
            if frozenset(subset) not in previous_freq_set:
                temp_candidate_set.remove(item)
                break
    return temp_candidate_set


def get_powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def association_rule(
    freq_item_set,
    item_set_with_sup,
    min_conf,
):
    rules = []
    for k, item_set in freq_item_set.items():
        for item in item_set:
            subsets = get_powerset(item)
            for s in subsets:
                confidence = float(
                    item_set_with_sup[item] / item_set_with_sup[frozenset(s)]
                )
                if confidence > min_conf:
                    rules.append([set(s), set(item.difference(s)), confidence])
    return rules


def apriori(
    item_set_list,
    min_sup,
    min_conf,
):
    candidate_item_set = retrieve_item_set(item_set_list)
    global_freq_item_set = dict()
    global_item_set_with_sup = defaultdict(int)
    filtered_item_set = filter_freq_item_set(
        candidate_item_set,
        item_set_list,
        min_sup,
        global_item_set_with_sup,
    )
    current_l_set = filtered_item_set
    k = 2

    while current_l_set:
        global_freq_item_set[k - 1] = current_l_set
        candidate_item_set = get_union(current_l_set, k)
        candidate_item_set = pruning(
            candidate_item_set,
            current_l_set,
            k - 1,
        )
        current_l_set = filter_freq_item_set(
            candidate_item_set,
            item_set_list,
            min_sup,
            global_item_set_with_sup,
        )
        k += 1

    rules = association_rule(
        global_freq_item_set,
        global_item_set_with_sup,
        min_conf,
    )
    rules.sort(key=lambda x: x[2])

    return global_freq_item_set, rules


dataset = [
    ["Milk", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
    ["Dill", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
    ["Milk", "Apple", "Kidney Beans", "Eggs"],
    ["Milk", "Unicorn", "Corn", "Kidney Beans", "Yogurt"],
    ["Corn", "Onion", "Onion", "Kidney Beans", "Ice cream", "Eggs"],
]
freq_item_set, rules = apriori(dataset, min_sup=0.6, min_conf=0.7)

print(freq_item_set)
print(rules)
