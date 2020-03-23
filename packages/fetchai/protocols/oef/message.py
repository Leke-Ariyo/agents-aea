# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020 fetchai
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

"""This module contains oef's message definition."""

from enum import Enum
from typing import Set, Tuple, cast

from aea.configurations.base import ProtocolId
from aea.protocols.base import Message

from packages.fetchai.protocols.oef.custom_types import Description as CustomDescription
from packages.fetchai.protocols.oef.custom_types import (
    OefErrorOperation as CustomOefErrorOperation,
)
from packages.fetchai.protocols.oef.custom_types import Query as CustomQuery

DEFAULT_BODY_SIZE = 4


class OefMessage(Message):
    """A protocol for interacting with an OEF service."""

    protocol_id = ProtocolId("fetchai", "oef", "0.1.0")

    Description = CustomDescription

    OefErrorOperation = CustomOefErrorOperation

    Query = CustomQuery

    class Performative(Enum):
        """Performatives for the oef protocol."""

        OEF_ERROR = "oef_error"
        REGISTER_SERVICE = "register_service"
        SEARCH_RESULT = "search_result"
        SEARCH_SERVICES = "search_services"
        UNREGISTER_SERVICE = "unregister_service"

        def __str__(self):
            """Get the string representation."""
            return self.value

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs,
    ):
        """
        Initialise an instance of OefMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=OefMessage.Performative(performative),
            **kwargs,
        )
        self._performatives = {
            "oef_error",
            "register_service",
            "search_result",
            "search_services",
            "unregister_service",
        }
        assert (
            self._is_consistent()
        ), "This message is invalid according to the 'oef' protocol."

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        assert self.is_set("dialogue_reference"), "dialogue_reference is not set."
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        assert self.is_set("message_id"), "message_id is not set."
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # noqa: F821
        """Get the performative of the message."""
        assert self.is_set("performative"), "performative is not set."
        return cast(OefMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        assert self.is_set("target"), "target is not set."
        return cast(int, self.get("target"))

    @property
    def agents(self) -> Tuple[str, ...]:
        """Get the 'agents' content from the message."""
        assert self.is_set("agents"), "'agents' content is not set."
        return cast(Tuple[str, ...], self.get("agents"))

    @property
    def operation(self) -> CustomOefErrorOperation:
        """Get the 'operation' content from the message."""
        assert self.is_set("operation"), "'operation' content is not set."
        return cast(CustomOefErrorOperation, self.get("operation"))

    @property
    def query(self) -> CustomQuery:
        """Get the 'query' content from the message."""
        assert self.is_set("query"), "'query' content is not set."
        return cast(CustomQuery, self.get("query"))

    @property
    def service_description(self) -> CustomDescription:
        """Get the 'service_description' content from the message."""
        assert self.is_set(
            "service_description"
        ), "'service_description' content is not set."
        return cast(CustomDescription, self.get("service_description"))

    @property
    def service_id(self) -> str:
        """Get the 'service_id' content from the message."""
        assert self.is_set("service_id"), "'service_id' content is not set."
        return cast(str, self.get("service_id"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the oef protocol."""
        try:
            assert (
                type(self.dialogue_reference) == tuple
            ), "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                type(self.dialogue_reference)
            )
            assert (
                type(self.dialogue_reference[0]) == str
            ), "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                type(self.dialogue_reference[0])
            )
            assert (
                type(self.dialogue_reference[1]) == str
            ), "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                type(self.dialogue_reference[1])
            )
            assert (
                type(self.message_id) == int
            ), "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                type(self.message_id)
            )
            assert (
                type(self.target) == int
            ), "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                type(self.target)
            )

            # Light Protocol Rule 2
            # Check correct performative
            assert (
                type(self.performative) == OefMessage.Performative
            ), "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                self.valid_performatives, self.performative
            )

            # Check correct contents
            actual_nb_of_contents = len(self.body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == OefMessage.Performative.REGISTER_SERVICE:
                expected_nb_of_contents = 2
                assert (
                    type(self.service_description) == CustomDescription
                ), "Invalid type for content 'service_description'. Expected 'Description'. Found '{}'.".format(
                    type(self.service_description)
                )
                assert (
                    type(self.service_id) == str
                ), "Invalid type for content 'service_id'. Expected 'str'. Found '{}'.".format(
                    type(self.service_id)
                )
            elif self.performative == OefMessage.Performative.UNREGISTER_SERVICE:
                expected_nb_of_contents = 1
                assert (
                    type(self.service_description) == CustomDescription
                ), "Invalid type for content 'service_description'. Expected 'Description'. Found '{}'.".format(
                    type(self.service_description)
                )
            elif self.performative == OefMessage.Performative.SEARCH_SERVICES:
                expected_nb_of_contents = 1
                assert (
                    type(self.query) == CustomQuery
                ), "Invalid type for content 'query'. Expected 'Query'. Found '{}'.".format(
                    type(self.query)
                )
            elif self.performative == OefMessage.Performative.SEARCH_RESULT:
                expected_nb_of_contents = 1
                assert (
                    type(self.agents) == tuple
                ), "Invalid type for content 'agents'. Expected 'tuple'. Found '{}'.".format(
                    type(self.agents)
                )
                assert all(
                    type(element) == str for element in self.agents
                ), "Invalid type for tuple elements in content 'agents'. Expected 'str'."
            elif self.performative == OefMessage.Performative.OEF_ERROR:
                expected_nb_of_contents = 1
                assert (
                    type(self.operation) == CustomOefErrorOperation
                ), "Invalid type for content 'operation'. Expected 'OefErrorOperation'. Found '{}'.".format(
                    type(self.operation)
                )

            # Check correct content count
            assert (
                expected_nb_of_contents == actual_nb_of_contents
            ), "Incorrect number of contents. Expected {}. Found {}".format(
                expected_nb_of_contents, actual_nb_of_contents
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                assert (
                    self.target == 0
                ), "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                    self.target
                )
            else:
                assert (
                    0 < self.target < self.message_id
                ), "Invalid 'target'. Expected an integer between 1 and {} inclusive. Found {}.".format(
                    self.message_id - 1, self.target,
                )
        except (AssertionError, ValueError, KeyError) as e:
            print(str(e))
            return False

        return True
