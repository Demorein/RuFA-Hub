import CLI_commans
from system_commands import SystemCommands
import CLI_list

class CLI:
    def __init__(self, queue):
        pass


#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######FIXME#######

    def main(self):
        while True:
            user_command = input()
            if user_command.split()[0] in CLI_list.commands:
                pass


    def logger(self, name = "None"):
        if name == "None":
            SystemCommands._logger(__name__, "CLI.log")
        else:
            SystemCommands._logger()
        


# RuFA-Hub
# Copyright (C) 2025 Gromov Evgeniy Vyacheslavovich

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 2 for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.