import itertools


def groupList(items, size=2):
    """Group a list of items in batches of a given size.

    :param items: itertable of items to process
    :param int size: number of items in each batch
    """
    for (idx, items) in itertools.groupby(enumerate(items), lambda f: f[0]/size):
        yield [x[1] for x in items]
