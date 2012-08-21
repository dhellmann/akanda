from quantum.api.v2 import attributes
from quantum.db import models_v2
from quantum.extensions import extensions

from akanda.userapi import _authzbase
from akanda.userapi.db import models


# XXX: I used Network as an existing model for testing.  Need to change to
# use an actual PortForward model.
#
# Duncan: cool, we'll get a PortForward model in place ASAP, so that this code
# can be updated to use it.


class FirewallResource(_authzbase.ResourceDelegate):
    """
    """
    model = models.Firewall
    resource_name = 'firewall'
    collection_name = 'firewalls'

    ATTRIBUTE_MAP = {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:regex': attributes.UUID_PATTERN},
               'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'default': '', 'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'is_visible': True},
    }

    def make_dict(self, firewall):
        """
        Convert a firewall model object to a dictionary.
        """
        res = {'id': firewall['id'],
               'action': firewall['action'],
               'protocol': firewall['protocol'],
               'source_alias': firewall['source_alias'],
               'source_port': firewall['source_port'],
               'destination_alias': firewall['destination_alias'],
               'destination_port': firewall['destination_port'],
               'created_at': firewall['created_at']}
        return res


_authzbase.register_quota('portforward', 'quota_portforward')


class Portforward(object):
    """
    """
    def get_name(self):
        return "port forward"

    def get_alias(self):
        return "dhportforward"

    def get_description(self):
        return "A port forwarding extension"

    def get_namespace(self):
        return 'http://docs.dreamcompute.com/api/ext/v1.0'

    def get_updated(self):
        return "2012-08-02T16:00:00-05:00"

    def get_resources(self):
        return [extensions.ResourceExtension(
            'dhportforward',
            _authzbase.create_extension(PortforwardResource()))]
            #_authzbase.ResourceController(PortforwardResource()))]

    def get_actions(self):
        return []

    def get_request_extensions(self):
        return []
