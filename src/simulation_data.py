import copy

from src.arena import SampleTemplate

sample_stock = {1: [
        SampleTemplate([0, 3, 0, 0, 0], 1, 0),
        SampleTemplate([0, 0, 0, 2, 1], 1, 0),
        SampleTemplate([0, 1, 1, 1, 1], 1, 0),
        SampleTemplate([0, 2, 0, 0, 2], 1, 0),
        SampleTemplate([0, 0, 4, 0, 0], 10, 0),
        SampleTemplate([0, 1, 2, 1, 1], 1, 0),
        SampleTemplate([0, 2, 2, 0, 1], 1, 0),
        SampleTemplate([3, 1, 0, 0, 1], 1, 0),
        SampleTemplate([1, 0, 0, 0, 2], 1, 1),
        SampleTemplate([0, 0, 0, 0, 3], 1, 1),
        SampleTemplate([1, 0, 1, 1, 1], 1, 1),
        SampleTemplate([0, 0, 2, 0, 2], 1, 1),
        SampleTemplate([0, 0, 0, 4, 0], 10, 1),
        SampleTemplate([1, 0, 1, 2, 1], 1, 1),
        SampleTemplate([1, 0, 2, 2, 0], 1, 1),
        SampleTemplate([0, 1, 3, 1, 0], 1, 1),
        SampleTemplate([2, 1, 0, 0, 0], 1, 2),
        SampleTemplate([0, 0, 0, 3, 0], 1, 2),
        SampleTemplate([1, 1, 0, 1, 1], 1, 2),
        SampleTemplate([0, 2, 0, 2, 0], 1, 2),
        SampleTemplate([0, 0, 0, 0, 4], 10, 2),
        SampleTemplate([1, 1, 0, 1, 2], 1, 2),
        SampleTemplate([0, 1, 0, 2, 2], 1, 2),
        SampleTemplate([1, 3, 1, 0, 0], 1, 2),
        SampleTemplate([0, 2, 1, 0, 0], 1, 3),
        SampleTemplate([3, 0, 0, 0, 0], 1, 3),
        SampleTemplate([1, 1, 1, 0, 1], 1, 3),
        SampleTemplate([2, 0, 0, 2, 0], 1, 3),
        SampleTemplate([4, 0, 0, 0, 0], 10, 3),
        SampleTemplate([2, 1, 1, 0, 1], 1, 3),
        SampleTemplate([2, 0, 1, 0, 2], 1, 3),
        SampleTemplate([1, 0, 0, 1, 3], 1, 3),
        SampleTemplate([0, 0, 2, 1, 0], 1, 4),
        SampleTemplate([0, 0, 3, 0, 0], 1, 4),
        SampleTemplate([1, 1, 1, 1, 0], 1, 4),
        SampleTemplate([2, 0, 2, 0, 0], 1, 4),
        SampleTemplate([0, 4, 0, 0, 0], 10, 4),
        SampleTemplate([1, 2, 1, 1, 0], 1, 4),
        SampleTemplate([2, 2, 0, 1, 0], 1, 4),
        SampleTemplate([0, 0, 1, 3, 1], 1, 4)
    ],
    2: [
        SampleTemplate([0, 0, 0, 5, 0], 20, 0),
        SampleTemplate([6, 0, 0, 0, 0], 30, 0),
        SampleTemplate([0, 0, 3, 2, 2], 10, 0),
        SampleTemplate([0, 0, 1, 4, 2], 20, 0),
        SampleTemplate([2, 3, 0, 3, 0], 10, 0),
        SampleTemplate([0, 0, 0, 5, 3], 20, 0),
        SampleTemplate([0, 5, 0, 0, 0], 20, 1),
        SampleTemplate([0, 6, 0, 0, 0], 30, 1),
        SampleTemplate([0, 2, 2, 3, 0], 10, 1),
        SampleTemplate([2, 0, 0, 1, 4], 20, 1),
        SampleTemplate([0, 2, 3, 0, 3], 20, 1),
        SampleTemplate([5, 3, 0, 0, 0], 20, 1),
        SampleTemplate([0, 0, 5, 0, 0], 20, 2),
        SampleTemplate([0, 0, 6, 0, 0], 30, 2),
        SampleTemplate([2, 3, 0, 0, 2], 10, 2),
        SampleTemplate([3, 0, 2, 3, 0], 10, 2),
        SampleTemplate([4, 2, 0, 0, 1], 20, 2),
        SampleTemplate([0, 5, 3, 0, 0], 20, 2),
        SampleTemplate([5, 0, 0, 0, 0], 20, 3),
        SampleTemplate([0, 0, 0, 6, 0], 30, 3),
        SampleTemplate([2, 0, 0, 2, 3], 10, 3),
        SampleTemplate([1, 4, 2, 0, 0], 20, 3),
        SampleTemplate([0, 3, 0, 2, 3], 10, 3),
        SampleTemplate([3, 0, 0, 0, 5], 20, 3),
        SampleTemplate([0, 0, 0, 0, 5], 20, 4),
        SampleTemplate([0, 0, 0, 0, 6], 30, 4),
        SampleTemplate([3, 2, 2, 0, 0], 10, 4),
        SampleTemplate([0, 1, 4, 2, 0], 20, 4),
        SampleTemplate([3, 0, 3, 0, 2], 10, 4),
        SampleTemplate([0, 0, 5, 3, 0], 20, 4)
    ],
    3: [
        SampleTemplate([0, 0, 0, 0, 7], 40, 0),
        SampleTemplate([3, 0, 0, 0, 7], 50, 0),
        SampleTemplate([3, 0, 0, 3, 6], 40, 0),
        SampleTemplate([0, 3, 3, 5, 3], 30, 0),
        SampleTemplate([7, 0, 0, 0, 0], 40, 1),
        SampleTemplate([7, 3, 0, 0, 0], 50, 1),
        SampleTemplate([6, 3, 0, 0, 3], 40, 1),
        SampleTemplate([3, 0, 3, 3, 5], 30, 1),
        SampleTemplate([0, 7, 0, 0, 0], 40, 2),
        SampleTemplate([0, 7, 3, 0, 0], 50, 2),
        SampleTemplate([3, 6, 3, 0, 0], 40, 2),
        SampleTemplate([5, 3, 0, 3, 3], 30, 2),
        SampleTemplate([0, 0, 7, 0, 0], 40, 3),
        SampleTemplate([0, 0, 7, 3, 0], 50, 3),
        SampleTemplate([0, 3, 6, 3, 0], 40, 3),
        SampleTemplate([3, 5, 3, 0, 3], 30, 3),
        SampleTemplate([0, 0, 0, 7, 0], 40, 4),
        SampleTemplate([0, 0, 0, 7, 3], 50, 4),
        SampleTemplate([0, 0, 3, 6, 3], 40, 4),
        SampleTemplate([3, 3, 5, 3, 0], 30, 4)
    ]
}

def rotate(l, n):
    return l[n:] + l[:n]

sample_id = 1

def get_sample(rank: int) -> SampleTemplate:
    sample = copy.deepcopy(sample_stock[rank][0])
    sample_stock[rank] = rotate(sample_stock[rank], 1)

    global sample_id 
    sample.id = sample_id
    sample_id += 1
    sample.rank = rank

    return sample