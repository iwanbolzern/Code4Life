import copy

from data_holder import Sample

sample_stock = {1: [
        Sample([0, 3, 0, 0, 0], 1, 'A'),
        Sample([0, 0, 0, 2, 1], 1, 'A'),
        Sample([0, 1, 1, 1, 1], 1, 'A'),
        Sample([0, 2, 0, 0, 2], 1, 'A'),
        Sample([0, 0, 4, 0, 0], 10, 'A'),
        Sample([0, 1, 2, 1, 1], 1, 'A'),
        Sample([0, 2, 2, 0, 1], 1, 'A'),
        Sample([3, 1, 0, 0, 1], 1, 'A'),
        Sample([1, 0, 0, 0, 2], 1, 'B'),
        Sample([0, 0, 0, 0, 3], 1, 'B'),
        Sample([1, 0, 1, 1, 1], 1, 'B'),
        Sample([0, 0, 2, 0, 2], 1, 'B'),
        Sample([0, 0, 0, 4, 0], 10, 'B'),
        Sample([1, 0, 1, 2, 1], 1, 'B'),
        Sample([1, 0, 2, 2, 0], 1, 'B'),
        Sample([0, 1, 3, 1, 0], 1, 'B'),
        Sample([2, 1, 0, 0, 0], 1, 'C'),
        Sample([0, 0, 0, 3, 0], 1, 'C'),
        Sample([1, 1, 0, 1, 1], 1, 'C'),
        Sample([0, 2, 0, 2, 0], 1, 'C'),
        Sample([0, 0, 0, 0, 4], 10, 'C'),
        Sample([1, 1, 0, 1, 2], 1, 'C'),
        Sample([0, 1, 0, 2, 2], 1, 'C'),
        Sample([1, 3, 1, 0, 0], 1, 'C'),
        Sample([0, 2, 1, 0, 0], 1, 'D'),
        Sample([3, 0, 0, 0, 0], 1, 'D'),
        Sample([1, 1, 1, 0, 1], 1, 'D'),
        Sample([2, 0, 0, 2, 0], 1, 'D'),
        Sample([4, 0, 0, 0, 0], 10, 'D'),
        Sample([2, 1, 1, 0, 1], 1, 'D'),
        Sample([2, 0, 1, 0, 2], 1, 'D'),
        Sample([1, 0, 0, 1, 3], 1, 'D'),
        Sample([0, 0, 2, 1, 0], 1, 'E'),
        Sample([0, 0, 3, 0, 0], 1, 'E'),
        Sample([1, 1, 1, 1, 0], 1, 'E'),
        Sample([2, 0, 2, 0, 0], 1, 'E'),
        Sample([0, 4, 0, 0, 0], 10, 'E'),
        Sample([1, 2, 1, 1, 0], 1, 'E'),
        Sample([2, 2, 0, 1, 0], 1, 'E'),
        Sample([0, 0, 1, 3, 1], 1, 'E')
    ],
    2: [
        Sample([0, 0, 0, 5, 0], 20, 'A'),
        Sample([6, 0, 0, 0, 0], 30, 'A'),
        Sample([0, 0, 3, 2, 2], 10, 'A'),
        Sample([0, 0, 1, 4, 2], 20, 'A'),
        Sample([2, 3, 0, 3, 0], 10, 'A'),
        Sample([0, 0, 0, 5, 3], 20, 'A'),
        Sample([0, 5, 0, 0, 0], 20, 'B'),
        Sample([0, 6, 0, 0, 0], 30, 'B'),
        Sample([0, 2, 2, 3, 0], 10, 'B'),
        Sample([2, 0, 0, 1, 4], 20, 'B'),
        Sample([0, 2, 3, 0, 3], 20, 'B'),
        Sample([5, 3, 0, 0, 0], 20, 'B'),
        Sample([0, 0, 5, 0, 0], 20, 'C'),
        Sample([0, 0, 6, 0, 0], 30, 'C'),
        Sample([2, 3, 0, 0, 2], 10, 'C'),
        Sample([3, 0, 2, 3, 0], 10, 'C'),
        Sample([4, 2, 0, 0, 1], 20, 'C'),
        Sample([0, 5, 3, 0, 0], 20, 'C'),
        Sample([5, 0, 0, 0, 0], 20, 'D'),
        Sample([0, 0, 0, 6, 0], 30, 'D'),
        Sample([2, 0, 0, 2, 3], 10, 'D'),
        Sample([1, 4, 2, 0, 0], 20, 'D'),
        Sample([0, 3, 0, 2, 3], 10, 'D'),
        Sample([3, 0, 0, 0, 5], 20, 'D'),
        Sample([0, 0, 0, 0, 5], 20, 'E'),
        Sample([0, 0, 0, 0, 6], 30, 'E'),
        Sample([3, 2, 2, 0, 0], 10, 'E'),
        Sample([0, 1, 4, 2, 0], 20, 'E'),
        Sample([3, 0, 3, 0, 2], 10, 'E'),
        Sample([0, 0, 5, 3, 0], 20, 'E')
    ],
    3: [
        Sample([0, 0, 0, 0, 7], 40, 'A'),
        Sample([3, 0, 0, 0, 7], 50, 'A'),
        Sample([3, 0, 0, 3, 6], 40, 'A'),
        Sample([0, 3, 3, 5, 3], 30, 'A'),
        Sample([7, 0, 0, 0, 0], 40, 'B'),
        Sample([7, 3, 0, 0, 0], 50, 'B'),
        Sample([6, 3, 0, 0, 3], 40, 'B'),
        Sample([3, 0, 3, 3, 5], 30, 'B'),
        Sample([0, 7, 0, 0, 0], 40, 'C'),
        Sample([0, 7, 3, 0, 0], 50, 'C'),
        Sample([3, 6, 3, 0, 0], 40, 'C'),
        Sample([5, 3, 0, 3, 3], 30, 'C'),
        Sample([0, 0, 7, 0, 0], 40, 'D'),
        Sample([0, 0, 7, 3, 0], 50, 'D'),
        Sample([0, 3, 6, 3, 0], 40, 'D'),
        Sample([3, 5, 3, 0, 3], 30, 'D'),
        Sample([0, 0, 0, 7, 0], 40, 'E'),
        Sample([0, 0, 0, 7, 3], 50, 'E'),
        Sample([0, 0, 3, 6, 3], 40, 'E'),
        Sample([3, 3, 5, 3, 0], 30, 'E')
    ]
}

def rotate(l, n):
    return l[n:] + l[:n]

sample_id = 0

def get_sample(rank: int) -> Sample:
    sample = copy.deepcopy(sample_stock[rank][0])
    sample_stock[rank] = rotate(sample_stock[rank], 1)

    global sample_id
    sample.id = sample_id
    sample_id += 1
    sample.rank = rank

    return sample
