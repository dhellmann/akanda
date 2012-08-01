import json
import os

from twisted.internet import utils
from twisted.python import log
from twisted.web import resource, server
from twisted.internet import threads

from txroutes import Dispatcher

from akanda import meta
from akanda.routerapi import base
from akanda.drivers import ifconfig

from akanda.drivers import pf
from akanda import utils


# For info on how to use deferreds with routes, see examples here:
#   https://github.com/dreamhost/txroutes
#
# Thoughts that should guide REST implementations:
#
#   For collections (e.g., /json/v1/firewall/groups):
#       GET - list the details of the groups
#       PUT - replace the current groups data entirely with new groups data
#       POST - create a new group in the groups collection
#       DELETE - delete the entire collection
#
#   For elements (e.g., /json/v1/firewall/{name}/rule/{rule-number}):
#       GET - retreive rule data for the given firewall rule
#       PUT - replace the given firewall rule with a new one
#       DELETE - delete the given firewall rule
#
#   For elements (e.g., /json/v1/firewall/{name}/rule/):
#       POST - create a new firewall rule
#
# Also, be sure to look at akanda.api.routes (both code and comments), as
# this provides useful information on how the API methods below will be used.


class Demo(base.RESTAPIBase):
    """
    """
    def longRunningProcess(self, request):

        # XXX generalized forms of these can be created and then moved out to
        # the top-level class (at which point the request object will no longer
        # be in-scope, so you'll need to pass it when calling the
        # callbacks or errbacks).
        def yay(result):
            stdout, stderr, exitCode = result
            if exitCode == 0:
                log.msg(result)
                request.write(json.dumps({"date": stdout.strip()}))
            else:
                log.err(result)
                request.write("Error! See the log for more details.")
            request.finish()

        def uhoh(failure):
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        #cmd = "/bin/ls"
        cmd = "/bin/date"
        args = []
        deferred = utils.getProcessOutputAndValue(
            cmd, args, env=os.environ)
        deferred.addCallback(yay)
        deferred.addErrback(uhoh)
        return server.NOT_DONE_YET


class Configuration(base.RESTAPIBase):
    """
    """


class NetPortManagement(base.RESTAPIBase):
    """
    """


class PortForward(base.RESTAPIBase):
    """
    """


class AliasManagement(base.RESTAPIBase):
    """
    """


class FirewallRules(base.RESTAPIBase):
    """
    Version 1.0 will be just a plain text dump (ugly and repeating code).
    Implement parsers for each get_xyz under pf.py for version 1.1.
    """
    pf_mgr = pf.PfManager()

    def get_rules(self, request):

        def parse_pf_rules_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_rules)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_rules_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_states(self, request):

        def parse_pf_states_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_states)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_states_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_anchors(self, request):

        def parse_pf_anchors_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_anchors)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_anchors_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_sources(self, request):

        def parse_pf_sources_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_sources)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_sources_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_info(self, request):

        def parse_pf_info_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_info)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_info_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_tables(self, request):

        def parse_pf_tables_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_tables)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_tables_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_labels(self, request):

        def parse_pf_labels_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_labels)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_labels_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_timeouts(self, request):

        def parse_pf_timeouts_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_timeouts)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_timeouts_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_memory(self, request):

        def parse_pf_memory_results(results):
            log.msg(results)
            request.write(results)
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.pf_mgr.get_memory)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_pf_memory_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET


class NAT(base.RESTAPIBase):
    """
    """


class VPN(base.RESTAPIBase):
    """
    """


class System(base.RESTAPIBase):
    """
    """
    if_mgr = ifconfig.InterfaceManager()

    def get_interface(self, request, ifname):

        def parse_if_config_result(result):
            log.msg(result)
            request.write(json.dumps({"interface": result.to_dict()}, cls=utils.ModelSerializer))
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.if_mgr.get_interface, ifname)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_if_config_result)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET

    def get_interfaces(self, request):

        def parse_ifconfig_results(results):
            log.msg(results)
            interfaces = [x.to_dict() for x in results]
            request.write(json.dumps({"interfaces": interfaces}, cls=utils.ModelSerializer))
            request.finish()

        def handle_error(failure):
            # XXX HTTP status/code
            log.err(failure)
            request.write("Error! See the log for more details.")
            request.finish()

        deferred = threads.deferToThread(self.if_mgr.get_interfaces)
        deferred.addErrback(handle_error)
        deferred.addCallback(parse_ifconfig_results)
        deferred.addErrback(handle_error)
        return server.NOT_DONE_YET


class Metadata(base.RESTAPIBase):
    """
    """
    # XXX create a json.dumps decorator for json-returning methods
    def version(self, request):
        major, minor, point = meta.version.split(".")
        return json.dumps({"version": {
            "major": 0,
            "minor": 1,
            "point": 0}})


class API(base.RESTAPIBase):
    """
    """
    demo = Demo()
    system = System()
    meta = Metadata()
    config = Configuration()
    firewall = FirewallRules()
    portForward = PortForward()
    aliasManagement = AliasManagement()
    netPortManagement = NetPortManagement()
    nat = NAT()
    vpn = VPN()

    # XXX create a json.dumps decorator for json-returning methods
    def index(self, request):
        """
        This is really nothing more than a demo of what can be done and to
        provide some initial data with which we can test a running instance of
        the REST service.
        """
        return json.dumps({
            "class name": self.__class__.__name__,
            "class methods": dir(self),
            "class data": vars(self),
            })

    def set_interfaces(self, list_of_iface_data):
        """
        HTTP POST
        """

    def set_interface(self, dict_of_iface_data):
        """
        HTTP POST
        """

    def get_rules(self):
        """
        HTTP GET
        """

    def set_rules(self, list_of_rules):
        """
        HTTP POST
        """

    def set_rule(self, rule_data):
        """
        Append the provided rule data as a new rule at the end of the PF rule
        set table.

        HTTP POST
        """

    def set_table(self, data):
        """
        HTTP POST
        """
