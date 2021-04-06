#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from warreclient import base


class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor %s>" % self.attributes.get('id')


class FlavorManager(base.BasicManager):

    base_url = 'v1/flavors'
    resource_class = Flavor

    def update(self, flavor_id, **kwargs):
        return self._update('/%s/%s/' % (self.base_url, flavor_id),
                            data=kwargs)

    def create(self, name, vcpu, memory_mb, disk_gb, description=None,
               active=True, properties=None, max_length_hours=504, slots=1,
               is_public=True):
        data = {'name': name,
                'description': description,
                'vcpu': int(vcpu),
                'memory_mb': int(memory_mb),
                'disk_gb': int(disk_gb),
                'properties': properties,
                'active': active,
                'max_length_hours': int(max_length_hours),
                'slots': int(slots),
                'is_public': is_public}

        return self._create("/%s/" % self.base_url, data=data)
