# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This test module contains AEA cli tests for P2PLibp2p connection."""

import functools
import os
import random
import shutil
import string
import tempfile
import time

import pytest

from aea.mail.base import Envelope
from aea.multiplexer import Multiplexer
from aea.protocols.default.message import DefaultMessage
from aea.test_tools.test_cases import BaseAEATestCase

from ....conftest import (
    _make_libp2p_connection,
    libp2p_log_on_failure,
    skip_test_windows,
)

DEFAULT_PORT = 10234
DEFAULT_DELEGATE_PORT = 11234
DEFAULT_NET_SIZE = 4

DEFAULT_LAUNCH_TIMEOUT = 25

def with_new_agent(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._create_agent()
        fn(self, *args, **kwargs)
        self.delete_agents(self.agent_name)
    return wrapper

@skip_test_windows
class TestP2PLibp2pConnectionAEARunning(BaseAEATestCase):
    """Test AEA with p2p_libp2p connection is correctly run"""

    @classmethod
    def setup_class(cls):
        """Set up the test class."""
        BaseAEATestCase.setup_class()

    @with_new_agent
    def test_default_config_node(self):
        self.add_item("connection", "fetchai/p2p_libp2p:0.2.0")
        self.set_config(
            "agent.default_connection", "fetchai/p2p_libp2p:0.2.0"
        )  # TOFIX(LR) not sure is needed

        process = self.run_agent()
        self._assert_node_running(process)

    @with_new_agent
    def test_full_node(self):
        self.add_item("connection", "fetchai/p2p_libp2p:0.2.0")

        # setup a full node: with public uri, relay service, and delegate service
        config_path = "vendor.fetchai.connections.p2p_libp2p.config"
        self.set_config(
            "{}.local_uri".format(config_path), "127.0.0.1:{}".format(DEFAULT_PORT)
        )
        self.set_config(
            "{}.public_uri".format(config_path), "127.0.0.1:{}".format(DEFAULT_PORT)
        )
        self.set_config(
            "{}.delegate_uri".format(config_path),
            "127.0.0.1:{}".format(DEFAULT_DELEGATE_PORT),
        )

        process = self.run_agent()
        self._assert_full_node_running(process)

    def _create_agent(self):
        self.agent_name = "agent-" + "".join(random.choices(string.ascii_lowercase, k=5))
        self.set_agent_context(self.agent_name)
        self.create_agents(self.agent_name)

    def _assert_node_running(self, process, check_strings = "My libp2p addresses: ["):
        is_running = self.is_running(process, timeout=DEFAULT_LAUNCH_TIMEOUT)
        assert is_running, "AEA not running within timeout!"

        missing_strings = self.missing_from_output(process, check_strings)
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in agent output.".format(missing_strings)

        self.terminate_agents(process)
        assert self.is_successfully_terminated(
            process
        ), "AEA wasn't successfully terminated."

    def _assert_full_node_running(self, process):
        check_strings = "My libp2p addresses: ['/dns4/"
        self._assert_node_running(process, check_strings)

    def _relay_node_running(self, process):
        check_strings = "My libp2p addresses: []"
        self._assert_node_running(process, check_strings)
