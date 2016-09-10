#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ####################################################################
# Copyright (C) 2016  Fridolin Pokorny, fpokorny@redhat.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################


class GlobalConfig(object):
    predicates_module = 'parsley.predicates'
    trace = None
    dispatcher_strategy = None

    # TODO: Possible candidates for "global" configuration;
    #  * make dispatcher strategy configurable - e.g. strategy: linear/exponential_backoff/...
    #  * trace configuration - possibly remove Config.trace_by_logging() and generate this directly to config.py
    #                        - reuse databases for tracepoints

    @classmethod
    def from_dict(cls, d):
        if 'predicates_module' in d:
            cls.predicates_module = d['predicates_module']