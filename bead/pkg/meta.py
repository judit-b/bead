'''
Keys for accessing fields in .pkgmeta structures

.pkgmeta files are persistent python dictionaries,
with the following minimum structure:

{
    inputs: {
        'nick1' : {
            package uuid: ...,
            version hash: ...,
            version time: ...,
        },
        'nick2' : {
            package uuid: ...,
            version hash: ...,
            version time: ...,
        },
        ...
    },
    package uuid: ...,
    timestamp: ...,     # only archives - naive ordering
    default name: ...,  # only archives, package name for bootstrapping
}
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function


from collections import namedtuple


PACKAGE = 'package uuid'

INPUTS = 'inputs'

INPUT_PACKAGE = 'package uuid'
# FIXME: rename `version` to `content-hash`
INPUT_VERSION = 'version hash'
INPUT_TIME = 'version time'

InputSpec = namedtuple('InputSpec', 'name package version timestamp')


def parse_inputs(meta):
    '''
    Parse and yield input specification from meta as records.
    '''
    inputs = meta[INPUTS]
    for name in inputs:
        spec = inputs[name]
        yield InputSpec(name, spec[INPUT_PACKAGE], spec[INPUT_VERSION], spec[INPUT_TIME])


# Archive meta:
PACKAGE_TIMESTAMP = 'timestamp'
DEFAULT_NAME = 'default name'