from distutils.version import LooseVersion
def my_version_sort(items):
    return sorted(items, key=LooseVersion)
class FilterModule(object):
    def filters(self):
        return {
            'my_version_sort': my_version_sort
        }
