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
import itertools
import logging

from openstackclient.identity import common
from osc_lib.command import command
from osc_lib import utils


class ListLimits(command.Lister):
    """List limits."""

    log = logging.getLogger(__name__ + '.ListLimits')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        kwargs = {}
        if parsed_args.project:
            identity_client = self.app.client_manager.identity
            project = common.find_project(
                identity_client,
                common._get_token_resource(
                    identity_client, 'project', parsed_args.project
                ),
                parsed_args.project_domain,
            )
            kwargs['project_id'] = project.id
        limits = client.limits.get(**kwargs)
        columns = ["Name", "Value"]
        return (
            columns,
            (
                utils.get_item_properties(s, columns)
                for s in itertools.chain(limits.absolute)
            ),
        )

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--project',
            '--project-id',
            dest='project',
            metavar='<project>',
            help="List limits for project (name or ID) (admin only)",
        )
        parser.add_argument(
            '--project-domain',
            default='default',
            metavar='<project_domain>',
            help='Project domain (name or ID)',
        )
        return parser
