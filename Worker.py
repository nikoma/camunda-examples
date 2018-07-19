# Simple Camunda's External Task Worker
# Copyright (C) 2018  Stefan Malewski C
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests as req
import asyncio

LOCAL_BASEURL = "http://localhost:8080/engine-rest/external-task"


class Worker:
    """ Camunda's External Task Worker.
        Only implements FetchAndLock and Complete.
    """
    idn = 0

    defaultOptions = {
        "maxTasks": 2,
        "lockDuration": 10000,
        "pollingInterval": 1500,
    }

    def __init__(self, baseUrl=LOCAL_BASEURL, options={}):
        """
        Creates a new Worker. Each worker has an unique ID.

        Parameters
        ----------
        baseUrl : url (Optional)
            Server's External Tasks' endpoint's url. (So many apostrophes :O)
            By default uses http://localhost:8080/engine-rest/external-task
        options : dict (Optional)
            Custom options for the worker. They can be:
            - maxTasks: Maximum number of tasks to be fetched
                        and locked with a single poll.
            - lockDuration: The duration to lock the external
                            tasks for in milliseconds.
            - pollingInterval: interval in milliseconds between polls.
        """

        self.workerId = str(type(self).idn)
        type(self).idn += 1

        self.baseUrl = baseUrl

        self.options = type(self).defaultOptions
        self.options.update(options)

        print(f"New Worker {self.workerId}")

    def subscribe(self, topicName, variableNames, action):
        """
        Subscribe to work at a specific topic.

        Parameters
        ----------
        topicName : string
            Name of the topic of the External Task.
        variableNames : [ string ]
            Variables to be fetched from the task execution.
        action : dict -> dict
            Work to be done. Receives the execution context and returns
            variables to be added (or updated) to the execution.
            Must return a dictionary of variable names to values.
        """

        # This is only the boilerplate necessary to work
        # asynchronously. All the real work is done by _subscribe

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._subscribe(topicName, variableNames, action)
            )
        loop.close()

    async def _subscribe(self, topicName, variableNames, action):
        """
        PRIVATE
        Subscribe to work at a specific topic.
        Shouldn't be called.

        Parameters
        ----------
        topicName : string
            Name of the topic of the External Task.
        variableNames : [ string ]
            Variables to be fetched from the task execution.
        action : dict -> dict
            Work to be done. Receives the execution context and returns
            variables to be added (or updated) to the execution.
            Must return a dictionary of variable names to values.
        """
        while True:
            r = await self._fetchAndLock(topicName)

            if r.json():
                print(f"Fetch: Worker {self.workerId}")
            else:
                print(f"Fetch: No work {self.workerId}")

            for context in r.json():
                taskId = context["id"]
                variables = await action(context)
                variables = self._format(variables)

                if await self._complete(taskId, variables):
                    print(f"Complete: Worker {self.workerId}")

            # Polling interval
            await asyncio.sleep(self.options["pollingInterval"] / 1000.0)
        print("Stopped")

    async def _fetchAndLock(self, topicName):
        """
        PRIVATE
        Fetches and Locks work.
        Doesn't handle errors.

        Parameters
        ----------
        topicName : string
            Name of the topic of the External Task.

        Returns
        -------
        requests
            Response of the fetch request.
        """
        url = self.baseUrl + "/fetchAndLock"

        topic = [
            {
                "topicName": topicName,
                "lockDuration": self.options["lockDuration"],
            }
        ]

        header = {
            "Content-Type": "application/json"
        }

        body = {
            "workerId": self.workerId,
            "maxTasks": self.options["maxTasks"],
            "topics": topic,
            }

        r = req.post(url, headers=header, json=body)

        return r

    async def _complete(self, id, variables):
        """
        PRIVATE
        Completes a Task. Modifies the environment of execution
        by adding or updating variables.
        Doesn't handle errors.

        Parameters
        ----------
        id : string
            Id of the Task execution to complete.
        variables : json
            Variables to be added (updated) to the exectuion.

        Returns
        -------
        bool
            Was successful?
        """
        url = f"{self.baseUrl}/{id}/complete"

        header = {
            "Content-Type": "application/json"
        }

        body = {
            "workerId": self.workerId,
            "variables": variables,
            "localVariables": {},
            }

        r = req.post(url, headers=header, json=body)

        return r.status_code == 204

    def _format(self, variables):
        """
        Gives the correct format to variables.

        Parameters
        ----------
        variables : dict
            Dictionary of variable names to values.

        Returns
        -------
            Dictionary of well formed variables

        Example
        -------
            {"var1": 1, "var2": True}
            ->
            {"var1": {"value": 1}, "var2": {"value": True}}
        """
        return {k: {"value": v} for k, v in variables.items()}


# Example
# Worker for "Camunda for Non-Java Developers"

import random


async def action(context):
    if random.random() < 0.9:
        print("[Germanic Tribe Fighter] The Roman Legions has won the battle!")
        message = "victorious"
    else:
        print("[Germanic Tribe Fighter] The battle has lost!")
        message = "defeated"

    return {"legionStatus": {"value": message}}

customOptions = {"maxTasks": 1}
w = Worker(options=customOptions)
w.subscribe("FightTribe", ["name"], action)
