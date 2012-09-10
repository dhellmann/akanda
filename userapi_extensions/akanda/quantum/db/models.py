# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
# @author: Murali Raju, New Dream Network, LLC (DreamHost)
# @author: Mark Mcclain, New Dream Network, LLC (DreamHost)

from datetime import datetime
import logging
import netaddr
import re

import sqlalchemy as sa
from sqlalchemy import Column, String
from sqlalchemy import orm
from sqlalchemy.orm import validates


from quantum.api import api_common as common
from quantum.db import model_base
from quantum.db import models_v2 as models
from quantum.openstack.common import timeutils


BASE = model_base.BASE
LOG = logging.getLogger(__name__)


#DreamHost PortFoward, Firewall(FilterRule), AddressBook models as
#Quantum extensions

#VALIDATORS
#Validate private and public port ranges
def _validate_port_range(port, valid_values=None):
    min_value = valid_values[0]
    max_value = valid_values[65536]
    if port >= min_value and port <= max_value:
        return
    else:
        msg_dict = dict(port=port, min_value=min_value, 
            max_value=max_value)
        msg = _("%(port) is not in the range between %(min_value)"
            "and %(max_value)") % msg_dict
        LOG.debug("validate_port_range: %s", msg)
        return msg

#Used by type() regex to check if IDs are UUID
HEX_ELEM = '[0-9A-Fa-f]'
UUID_PATTERN = '-'.join([HEX_ELEM + '{8}', HEX_ELEM + '{4}',
                         HEX_ELEM + '{4}', HEX_ELEM + '{4}',
                         HEX_ELEM + '{12}'])


class PortForward(model_base.BASEV2, models.HasId, models.HasTenant):

    __tablename__ = 'portfowards'

    name = sa.Column(sa.String(255))
    public_port = sa.Column(sa.Integer, nullable=False)
    instance_id = sa.Column(sa.String(36), nullable=False)
    private_port = sa.Column(sa.Integer, nullable=True)
    # Quantum port address are stored in ipallocation which are internally
    # referred to as fixed_id, thus the name below.
    # XXX can we add a docsting to this model that explains how fixed_id is
    # used?
    fixed_id = sa.Column(
        sa.String(36), sa.ForeignKey('ipallocations.id', ondelete="CASCADE"),
        nullable=True)
    op_status = Column(String(16))

    #PortForward Model Validators using sqlalchamey simple validators

    @validates('name')
    def validate_name(self, key, name):
        assert isinstance(name, basestring) is str
        assert len(name) <= 255
        return name

    @validates('public_port')
    def validate_public_port(self, key, public_port):
        public_port = int(public_port)
        assert _validate_port_range(public_port)
        return public_port

    @validates('instance_id')
    def validate_instance_id(self, key, instance_id):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(instance_id), retype)
        assert len(instance_id) <= 36
        return instance_id

    @validates('private_port')
    def validate_private_port(self, key, private_port):
        private_port = int(private_port)
        assert _validate_port_range(private_port)
        return private_port

    @validates('fixed_id')
    def validate_fixed_id(self, key, fixed_id):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(fixed_id), retype)
        assert len(fixed_id) <= 36
        return fixed_id

    @validates('op_status')
    def validate_op_status(self, key, op_status):
        assert isinstance(op_status, basestring) is str
        assert len(op_status) <= 16
        return op_status


class AddressBookEntry(model_base.BASEV2, models.HasId, models.HasTenant):

    __tablename__ = 'addressbookentries'

    group_id = sa.Column(sa.String(36), sa.ForeignKey('addressbookgroups.id'),
        nullable=False)
    cidr = sa.Column(sa.String(64), nullable=False)

    #AddressBookEntry Model Validators using sqlalchamey simple validators
    @validates('group_id')
    def validate_name(self, key, group_id):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(group_id), retype)
        assert len(group_id) <= 36
        return group_id

    @validates('cidr')
    def validate_public_port(self, key, cidr):
        assert netaddr.IPNetwork(cidr)
        assert len(cidr) <= 64
        return cidr


class AddressBookGroup(model_base.BASEV2, models.HasId, models.HasTenant):

    __tablename__ = 'addressbookgroups'

    name = sa.Column(sa.String(255), nullable=False, primary_key=True)
    table_id = sa.Column(sa.String(36), sa.ForeignKey('addressbooks.id'),
        nullable=False)
    entries = orm.relationship(AddressBookEntry, backref='groups')

    #AddressBookGroup Model Validators using sqlalchamey simple validators
    @validates('name')
    def validate_name(self, key, name):
        assert isinstance(name, basestring) is str
        assert len(name) <= 255
        return name

    @validates('table_id')
    def validate_table_id(self, key, table_id):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(table_id), retype)
        assert len(table_id) <= 36
        return table_id


class AddressBook(model_base.BASEV2, models.HasId, models.HasTenant):

    __tablename__ = 'addressbooks'

    name = sa.Column(sa.String(255), nullable=False, primary_key=True)
    groups = orm.relationship(AddressBookGroup, backref='book')

    #AddressBook Model Validators using sqlalchamey simple validators
    @validates('name')
    def validate_name(self, key, name):
        assert isinstance(name, basestring) is str
        assert len(name) <= 255
        return name


class FilterRule(model_base.BASEV2, models.HasId, models.HasTenant):

    __tablename__ = 'filterrules'

    action = sa.Column(sa.String(6), nullable=False, primary_key=True)
    ip_version = sa.Column(sa.Integer, nullable=True)
    protocol = sa.Column(sa.String(4), nullable=False)
    source_alias = sa.Column(sa.String(36),
        sa.ForeignKey('addressbookentries.id'),
        nullable=False)
    source_port = sa.Column(sa.Integer, nullable=True)
    destination_alias = sa.Column(sa.String(36),
        sa.ForeignKey('addressbookentries.id'),
        nullable=False)
    destination_port = sa.Column(sa.Integer, nullable=True)
    created_at = sa.Column(sa.DateTime, default=timeutils.utcnow,
         nullable=False)

    #FilterRule Model Validators using sqlalchamey simple validators
    @validates('action')
    def validate_name(self, key, action):
        assert isinstance(action, basestring) is str
        assert len(action) <= 6
        return action

    @validates('ip_version')
    def validate_ip_version(self, key, ip_version):
        assert isinstance(ip_version) is int
        assert isinstance(ip_version, None)
        return ip_version

    @validates('protocol')
    def validate_protocol(self, key, protocol):
        assert isinstance(protocol, basestring) is str
        assert protocol.lower() in ('tcp', 'udp', 'icmp')
        assert len(protocol) <= 4
        return protocol

    @validates('source_alias')
    def validate_source_alias(self, key, source_alias):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(source_alias), retype)
        assert len(source_alias) <= 36
        return source_alias

    @validates('source_port')
    def validate_source_port(self, key, source_port):
        source_port = int(source_port)
        assert _validate_port_range(source_port)
        assert len(source_port) <= 36
        return source_port

    @validates('destination_alias')
    def validate_destination_alias(self, key, destination_alias):
        retype = type(re.compile(UUID_PATTERN))
        assert isinstance(re.compile(destination_alias), retype)
        assert len(destination_alias) <= 36
        return destination_alias

    @validates('destination_port')
    def validate_destination_port(self, key, destination_port):
        destination_port = int(destination_port)
        assert _validate_port_range(destination_port)
        assert len(destination_port) <= 36
        return destination_port

    @validates('created_at')
    def validate_created_at(self, key, created_at):
        assert isinstance(created_at) is datetime
        return created_at
