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

import json

from nectarclient_lib.tests.unit import utils

from warreclient.tests.unit.v1 import fakes
from warreclient.v1 import maintenancewindows


WINDOW_ID = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'


class MaintenanceWindowsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_list(self):
        windows = self.cs.maintenancewindows.list()
        self.cs.assert_called('GET', '/v1/maintenancewindows/')
        for w in windows:
            self.assertIsInstance(w, maintenancewindows.MaintenanceWindow)
        self.assertEqual(1, len(windows))

    def test_get(self):
        window = self.cs.maintenancewindows.get(WINDOW_ID)
        self.cs.assert_called('GET', f'/v1/maintenancewindows/{WINDOW_ID}/')
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)
        self.assertEqual(WINDOW_ID, window.id)

    def test_create(self):
        start = '2026-05-01T00:00:00+00:00'
        end = '2026-05-02T00:00:00+00:00'
        window = self.cs.maintenancewindows.create(start=start, end=end)
        expected = json.dumps({'start': start, 'end': end})
        self.cs.assert_called('POST', '/v1/maintenancewindows/', data=expected)
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)

    def test_create_with_note(self):
        start = '2026-05-01T00:00:00+00:00'
        end = '2026-05-02T00:00:00+00:00'
        note = 'Test maintenance'
        window = self.cs.maintenancewindows.create(
            start=start, end=end, note=note
        )
        expected = json.dumps({'start': start, 'end': end, 'note': note})
        self.cs.assert_called('POST', '/v1/maintenancewindows/', data=expected)
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)

    def test_create_with_flavor_ids(self):
        start = '2026-05-01T00:00:00+00:00'
        end = '2026-05-02T00:00:00+00:00'
        flavor_ids = ['d6506b62-13c2-4dec-a556-b306bb5e959f']
        window = self.cs.maintenancewindows.create(
            start=start, end=end, flavor_ids=flavor_ids
        )
        expected = json.dumps(
            {'start': start, 'end': end, 'flavor_ids': flavor_ids}
        )
        self.cs.assert_called('POST', '/v1/maintenancewindows/', data=expected)
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)

    def test_update(self):
        note = 'Updated note'
        window = self.cs.maintenancewindows.update(WINDOW_ID, note=note)
        self.cs.assert_called(
            'PATCH',
            f'/v1/maintenancewindows/{WINDOW_ID}/',
            json.dumps({'note': note}),
        )
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)

    def test_update_multiple_fields(self):
        start = '2026-06-01T00:00:00+00:00'
        end = '2026-06-02T00:00:00+00:00'
        flavor_ids = ['d6506b62-13c2-4dec-a556-b306bb5e959f']
        window = self.cs.maintenancewindows.update(
            WINDOW_ID, start=start, end=end, flavor_ids=flavor_ids
        )
        self.cs.assert_called(
            'PATCH',
            f'/v1/maintenancewindows/{WINDOW_ID}/',
            json.dumps({'start': start, 'end': end, 'flavor_ids': flavor_ids}),
        )
        self.assertIsInstance(window, maintenancewindows.MaintenanceWindow)

    def test_delete(self):
        self.cs.maintenancewindows.delete(WINDOW_ID)
        self.cs.assert_called('DELETE', f'/v1/maintenancewindows/{WINDOW_ID}/')

    def test_repr(self):
        window = self.cs.maintenancewindows.get(WINDOW_ID)
        self.assertEqual(f'<MaintenanceWindow {WINDOW_ID}>', repr(window))

    def test_to_dict(self):
        window = self.cs.maintenancewindows.get(WINDOW_ID)
        result = window.to_dict()
        self.assertEqual('s2.small', result.get('flavors'))

    def test_to_dict_flavor_id_fallback(self):
        window = maintenancewindows.MaintenanceWindow(
            None,
            {
                'id': 'test',
                'start': '2026-05-01T00:00:00+00:00',
                'end': '2026-05-02T00:00:00+00:00',
                'flavors': [{'id': 'some-flavor-id'}],
            },
        )
        result = window.to_dict()
        self.assertEqual('some-flavor-id', result.get('flavors'))

    def test_to_dict_no_flavors(self):
        window = maintenancewindows.MaintenanceWindow(
            None,
            {
                'id': 'test',
                'start': '2026-05-01T00:00:00+00:00',
                'end': '2026-05-02T00:00:00+00:00',
                'flavors': [],
            },
        )
        result = window.to_dict()
        self.assertEqual('', result.get('flavors'))

    def test_to_dict_multiple_flavors(self):
        window = maintenancewindows.MaintenanceWindow(
            None,
            {
                'id': 'test',
                'start': '2026-05-01T00:00:00+00:00',
                'end': '2026-05-02T00:00:00+00:00',
                'flavors': [
                    {'id': 'id-1', 'name': 'flavor-a'},
                    {'id': 'id-2', 'name': 'flavor-b'},
                ],
            },
        )
        result = window.to_dict()
        self.assertEqual('flavor-a, flavor-b', result.get('flavors'))
