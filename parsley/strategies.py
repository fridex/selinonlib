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
"""
Functions for scheduling dispatcher - Dispatcher strategy configuration functions. All of them are receiving:

  * previous_retry - value of previous retry, None if scheduling for the first time
  * active_nodes - active nodes within the system
  * failed_nodes - failed nodes within the system
  * started_nodes - newly started nodes the system
  * fallback_nodes - newly started fallback nodes

Other parameters are specific for strategy function and are configurable from YAML configuration file.
"""

from random import randint as gen_random


def linear_increase(start_retry, max_retry, step,
                    previous_retry, active_nodes, failed_nodes, started_nodes, fallback_nodes):
    """
    Increase linearly if no node started, decrease drastically to start_retry if a node scheduled

    :param start_retry: starting retry to use
    :param max_retry: upper limit of scheduling
    :param step: step to use in linear increase
    """
    if len(started_nodes) > 0 or len(fallback_nodes) > 0:
        retry = previous_retry + step
        if retry > max_retry:
            return max_retry
        else:
            return retry
    else:
        return start_retry


def linear_adopt(start_retry, max_retry, step,
                 previous_retry, active_nodes, failed_nodes, started_nodes, fallback_nodes):
    """
    Increase linearly if no node started, decrease linearly if a node scheduled

    :param start_retry: starting retry to use
    :param max_retry: upper limit of scheduling
    :param step: step to use in linear increase
    """
    if len(started_nodes) > 0 or len(fallback_nodes) > 0:
        retry = previous_retry + step
        if retry > max_retry:
            return max_retry
        else:
            return retry
    else:
        retry = previous_retry - step
        if retry < start_retry:
            return start_retry
        else:
            return retry


def biexponential_increase(start_retry, max_retry,
                           previous_retry, active_nodes, failed_nodes, started_nodes, fallback_nodes):
    """
    Increase exponentially if no node started, decrease drastically to start_retry if a node scheduled

    :param start_retry: starting retry to use
    :param max_retry: upper limit of scheduling
    """
    if previous_retry is None:
        return start_retry

    if len(started_nodes) > 0 or len(fallback_nodes) > 0:
        retry = previous_retry * 2
        if retry > max_retry:
            return max_retry
        else:
            return retry
    else:
        return start_retry


def biexponential_adopt(start_retry, max_retry,
                        previous_retry, active_nodes, failed_nodes, started_nodes, fallback_nodes):
    """
    Increase exponentially if no node started, decrease exponentially if a node scheduled

    :param start_retry: starting retry to use
    :param max_retry: upper limit of scheduling
    """
    if previous_retry is None:
        return start_retry

    if len(started_nodes) > 0 or len(fallback_nodes) > 0:
        retry = previous_retry * 2
        if retry > max_retry:
            return max_retry
        else:
            return retry
    else:
        retry = previous_retry / 2
        if retry < start_retry:
            return start_retry
        else:
            return retry


def random(start_retry, max_retry, previous_retry, active_nodes, failed_nodes, started_nodes, fallback_nodes):
    """
    Schedule randomly
    :param start_retry: lower limit of scheduling
    :param max_retry: upper limit of scheduling
    """
    return gen_random(start_retry, max_retry)


