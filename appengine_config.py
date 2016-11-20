"""`appengine_config` gets loaded when starting a new application instance."""
import os
import sys
import vendor
# insert `lib` as a site directory so our `main` module can load
# third-party libraries, and override built-ins with newer
# versions.
vendor.add('lib')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gaenv'))
