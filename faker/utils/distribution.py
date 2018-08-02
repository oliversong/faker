# coding=utf-8

import bisect
from faker.generator import random as mod_random


def random_sample(random=None):
    if random is None:
        random = mod_random
    return random.uniform(0.0, 1.0)


def cumsum(it):
    total = 0
    for x in it:
        total += x
        yield total


def choices_distribution_unique(a, p, random=None, length=1):
    # As of Python 3.7, there isn't a way to sample unique elements that takes
    # weight into account.
    if random is None:
        random = mod_random

    assert len(a) == len(p)

    choices = []

    for i in range(length):
        cdf = list(cumsum(p))
        normal = cdf[-1]
        cdf2 = [float(i) / float(normal) for i in cdf]
        uniform_sample = random_sample(random=random)
        idx = bisect.bisect_right(cdf2, uniform_sample)
        item = a[idx]
        choices.append(item)
        p.pop(item)
        del a[idx]
    return choices


def choices_distribution(a, p, random=None, length=1):
    if random is None:
        random = mod_random

    assert len(a) == len(p)

    if hasattr(random, 'choices'):
        choices = random.choices(a, weights=p, k=length)
        return choices
    else:
        choices = []

        cdf = list(cumsum(p))
        normal = cdf[-1]
        cdf2 = [float(i) / float(normal) for i in cdf]
        for i in range(length):
            uniform_sample = random_sample(random=random)
            idx = bisect.bisect_right(cdf2, uniform_sample)
            item = a[idx]
            choices.append(item)
        return choices
