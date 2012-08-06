from django.utils.translation import ugettext as _

from horizon import tabs

from .firewall.tabs import FirewallTab
from .alias.tabs import AliasTab
from .portforwarding.tabs import PortForwardingTab


class ConfigurationTab(tabs.Tab):
    name = _("Configuration")
    slug = "configuration"
    template_name = "akanda/simple.html"

    def get_context_data(self, request):
        return {}


class NatTab(tabs.Tab):
    name = _("Nat")
    slug = "nat"
    template_name = "akanda/simple.html"

    def get_context_data(self, request):
        return {}


class VPNTab(tabs.Tab):
    name = _("VPN")
    slug = "vpn"
    template_name = "akanda/simple.html"

    def get_context_data(self, request):
        return {}


class NetworkingTabs(tabs.TabGroup):
    slug = "networkingtabs"
    tabs = (AliasTab, ConfigurationTab, FirewallTab,
            NatTab, PortForwardingTab, VPNTab)