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


class Reservation(base.Resource):

    date_fields = ['start', 'end']

    def __repr__(self):
        return "<Reservation %s>" % self.id


class ReservationManager(base.BasicManager):

    base_url = 'v1/reservations'
    resource_class = Reservation

    def delete(self, reservation_id):
        return self._delete('/%s/%s/' % (self.base_url, reservation_id))

    def create(self, flavor_id, start, end):
        data = {'flavor_id': flavor_id,
                'start': start,
                'end': end}
        return self._create("/%s/" % self.base_url, data=data)