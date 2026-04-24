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

import logging

from nectarclient_lib import exceptions
from osc_lib.command import command
from osc_lib import utils as osc_utils


class ListMaintenanceWindows(command.Lister):
    """List maintenance windows."""

    log = logging.getLogger(__name__ + '.ListMaintenanceWindows')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        windows = client.maintenancewindows.list()
        columns = ['id', 'start', 'end', 'note', 'flavors']
        for w in windows:
            w.flavors = ', '.join(
                f.get('name', f.get('id', '')) for f in (w.flavors or [])
            )
        return (
            columns,
            (osc_utils.get_item_properties(w, columns) for w in windows),
        )


class MaintenanceWindowCommand(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id', metavar='<id>', help='ID of maintenance window'
        )
        return parser


class ShowMaintenanceWindow(MaintenanceWindowCommand):
    """Show maintenance window details."""

    log = logging.getLogger(__name__ + '.ShowMaintenanceWindow')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        try:
            window = client.maintenancewindows.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return self.dict2columns(window.to_dict())


class CreateMaintenanceWindow(command.ShowOne):
    """Create a maintenance window."""

    log = logging.getLogger(__name__ + '.CreateMaintenanceWindow')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--start',
            metavar='<start>',
            required=True,
            help='Start time (YYYY-MM-DDTHH:MM:SS+00:00)',
        )
        parser.add_argument(
            '--end',
            metavar='<end>',
            required=True,
            help='End time (YYYY-MM-DDTHH:MM:SS+00:00)',
        )
        parser.add_argument(
            '--note',
            metavar='<note>',
            help='Note describing the maintenance window',
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            action='append',
            dest='flavors',
            default=[],
            help='Flavor (name or ID) affected by this window (repeatable)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre

        flavor_ids = []
        for f in parsed_args.flavors:
            flavor = osc_utils.find_resource(
                client.flavors, f, all_projects=True
            )
            flavor_ids.append(flavor.id)

        window = client.maintenancewindows.create(
            start=parsed_args.start,
            end=parsed_args.end,
            note=parsed_args.note,
            flavor_ids=flavor_ids or None,
        )
        return self.dict2columns(window.to_dict())


class UpdateMaintenanceWindow(MaintenanceWindowCommand):
    """Update a maintenance window."""

    log = logging.getLogger(__name__ + '.UpdateMaintenanceWindow')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--start',
            metavar='<start>',
            help='Start time (YYYY-MM-DDTHH:MM:SS+00:00)',
        )
        parser.add_argument(
            '--end',
            metavar='<end>',
            help='End time (YYYY-MM-DDTHH:MM:SS+00:00)',
        )
        parser.add_argument(
            '--note',
            metavar='<note>',
            help='Note describing the maintenance window',
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            action='append',
            dest='flavors',
            help='Flavor (name or ID) affected by this window (repeatable). '
            'Replaces the existing list of flavors.',
        )
        parser.add_argument(
            '--no-flavors',
            action='store_true',
            default=False,
            help='Clear the list of flavors affected by this window',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre

        if parsed_args.flavors and parsed_args.no_flavors:
            raise exceptions.CommandError(
                "Can't specify --flavor and --no-flavors"
            )

        data = {}
        if parsed_args.start:
            data['start'] = parsed_args.start
        if parsed_args.end:
            data['end'] = parsed_args.end
        if parsed_args.note is not None:
            data['note'] = parsed_args.note
        if parsed_args.no_flavors:
            data['flavor_ids'] = []
        elif parsed_args.flavors:
            flavor_ids = []
            for f in parsed_args.flavors:
                flavor = osc_utils.find_resource(
                    client.flavors, f, all_projects=True
                )
                flavor_ids.append(flavor.id)
            data['flavor_ids'] = flavor_ids

        try:
            window = client.maintenancewindows.update(parsed_args.id, **data)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return self.dict2columns(window.to_dict())


class DeleteMaintenanceWindow(MaintenanceWindowCommand):
    """Delete a maintenance window."""

    log = logging.getLogger(__name__ + '.DeleteMaintenanceWindow')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.warre
        try:
            client.maintenancewindows.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return [], []
