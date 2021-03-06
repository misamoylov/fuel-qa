#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import unicode_literals

import requests

from core.helpers.log_helpers import logwrap


class CollectorClient(object):
    """CollectorClient."""  # TODO documentation

    def __init__(self, collector_ip, endpoint):
        url = "http://{0}/{1}".format(collector_ip, endpoint)
        self.__url = url
        super(CollectorClient, self).__init__()

    @property
    def url(self):
        return self.__url

    def _get(self, endpoint):
        return requests.get(url=self.url + endpoint)

    @logwrap
    def get_oswls(self, master_node_uid):
        return self._get("/oswls/{0}".format(master_node_uid)).json()

    @logwrap
    def get_installation_info(self, master_node_uid):
        return self._get("/installation_info/{0}".format(
            master_node_uid)).json()

    @logwrap
    def get_action_logs(self, master_node_uid):
        return self._get("/action_logs/{0}".format(
            master_node_uid)).json()

    @logwrap
    def get_oswls_by_resource(self, master_node_uid, resource):
        return self._get("/oswls/{0}/{1}".format(master_node_uid,
                                                 resource)).json()

    @logwrap
    def get_oswls_by_resource_data(self, master_node_uid, resource):
        return self.get_oswls_by_resource(master_node_uid,
                                          resource)['objs'][0]['resource_data']

    @logwrap
    def get_action_logs_ids(self, master_node_uid):
        return [actions['id']
                for actions in self.get_action_logs(master_node_uid)]

    @logwrap
    def get_action_logs_count(self, master_node_uid):
        return len(self.get_action_logs_ids(master_node_uid))

    @logwrap
    def get_action_logs_additional_info_by_id(
            self, master_node_uid, action_id):
        return [actions['body']['additional_info']
                for actions in self.get_action_logs(master_node_uid)
                if actions['id'] == action_id]

    @logwrap
    def get_installation_info_data(self, master_node_uid):
        return self.get_installation_info(master_node_uid)['structure']
