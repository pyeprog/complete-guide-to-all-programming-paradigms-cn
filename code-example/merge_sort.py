def merge_sort(lst: list) -> list:
    def split(lst: list) -> tuple[list, list]:
        return lst[:(len(lst)//2)], lst[len(lst)//2:]

    def merge(lst1: list, lst2: list) -> list:
        match (lst1, lst2):
            case ([], l):
                return l

            case (l, []):
                return l

            case ([h1, *t1], [h2, *t2]) if h1 < h2:
                return [h1, *merge(t1, lst2)]

            case ([h1, *t1], [h2, *t2]) if h1 >= h2:
                return [h2, *merge(lst1, t2)]

            case _:
                return []


    match lst:
        case []:
            return []
        case [x]:
            return lst
        case _:
            part1, part2 = split(lst)
            return merge(merge_sort(part1), merge_sort(part2))

