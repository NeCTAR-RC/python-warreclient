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

from warreclient.v1 import flavors

from warreclient.tests.unit import utils
from warreclient.tests.unit.v1 import fakes


class FlavorsTest(utils.TestCase):

    def setUp(self):
        super(FlavorsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_flavor_list(self):
        ul = self.cs.flavors.list()
        self.cs.assert_called('GET', '/v1/flavors/')
        for u in ul:
            self.assertIsInstance(u, flavors.Flavor)
        self.assertEqual(2, len(ul))

    def test_flavor_get(self):
        u = self.cs.flavors.get(123)
        self.cs.assert_called('GET', '/v1/flavors/123/')
        self.assertIsInstance(u, flavors.Flavor)
        self.assertEqual('d6506b62-13c2-4dec-a556-b306bb5e959f', u.id)

    def test_update(self):
        flavor = self.cs.flavors.update(123, slots=2)
        self.cs.assert_called('PATCH', '/v1/flavors/123/',
                              json.dumps({'slots': 2}))
        self.assertIsInstance(flavor, flavors.Flavor)
        self.assertEqual(2, flavor.slots)
