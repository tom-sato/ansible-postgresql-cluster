def my_next_usable(items):
    return '.'.join([list(items)[0].rsplit('.', 1)[0], str(min(set(range(3, 255)) - set(map(lambda x: x.split('.')[3], list(items)))))])
class FilterModule(object):
    def filters(self):
        return {
            'my_next_usable': my_next_usable
        }
