from weatherapp.core.commands import Configurate, Providers

from weatherapp.core import abstract


class CommandManager(abstract.Manager):
    """ Manager for app commands.
    """

    def __init__(self):
        self._commands = {}
        self._load_commands()

    def add(self, name, command):
        """
        :param name: command name
        :type name: str
        :param command: command class
        :type command: abstract.Command
        """

        self._commands[name] = command

    def _load_commands(self):
        """Load all external (from an entrypoints) commands."""

        for command in [Configurate, Providers]:
            self.add(command.name, command)

    def get(self, name):
        """
        :param name: command name from argv
        :type name: str
        """

        return self._commands.get(name, None)

    def __getitem__(self, name):
        return self._commands[name]

    def __contains__(self, name):
        return name in self._commands

    def __iter__(self):
        for key, value in self._commands.items():
            yield (key, value)
