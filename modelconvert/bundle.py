# abstracts output bundle functionality
# - configuration handling
# - actual rendering of templates and copying of files
# - custom task registration

# the bundles are actually python packages.
# bundles are registered globally in the config (no dynamics yet)
# INSTALLED_BUNDELS=('modelconvert.bundles.basic', etc.)
# this is kind of analog to django apps

class Bundle(object):
    def __init__(self):
        self.config = configparser.SafeConfigParser()
        self.config.read(['file', 'file'])


class Loader(object):
    pass