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

from nectarclient_lib import base


class MaintenanceWindow(base.Resource):
    date_fields = ['start', 'end']

    def __repr__(self):
        return f"<MaintenanceWindow {self.id}>"

    def to_dict(self):
        res = super().to_dict()
        res['flavors'] = ', '.join(
            f.get('name', f.get('id', '')) for f in res.get('flavors', [])
        )
        return res


class MaintenanceWindowManager(base.BasicManager):
    base_url = 'v1/maintenancewindows'
    resource_class = MaintenanceWindow

    def create(self, start, end, note=None, flavor_ids=None):
        data = {'start': start, 'end': end}
        if note is not None:
            data['note'] = note
        if flavor_ids:
            data['flavor_ids'] = flavor_ids
        return self._create(f'/{self.base_url}/', data=data)

    def update(self, window_id, **kwargs):
        return self._update(f'/{self.base_url}/{window_id}/', data=kwargs)

    def delete(self, window_id):
        return self._delete(f'/{self.base_url}/{window_id}/')
