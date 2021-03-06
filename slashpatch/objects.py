class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


class SlashPatchObject:
    type: int
    name: int


class String(SlashPatchObject):
    """A slash commands string option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.STRING


class Integer(SlashPatchObject):
    """A slash commands integer option."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.type = OptionType.INTEGER


class Boolean(SlashPatchObject):
    """A slash commands boolean option."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        self.type = OptionType.BOOLEAN


class User(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.USER


class Channel(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.CHANNEL


class Role(SlashPatchObject):
    """A slash commands user option."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.type = OptionType.ROLE


class SubCommand(SlashPatchObject):
    """A slash commands subcommand option."""

    def __init__(self, name: str, options: list):
        self.name = name
        self.type = OptionType.SUB_COMMAND

        self.options = []

        for option in options:
            type = option["type"]

            if type == OptionType.STRING:
                c = String
            elif type == OptionType.INTEGER:
                c = Integer
            elif type == OptionType.BOOLEAN:
                c = Boolean
            elif type == OptionType.USER:
                c = User
            elif type == OptionType.CHANNEL:
                c = Channel
            elif type == OptionType.ROLE:
                c = Role
            else:
                raise TypeError(f"Invalid option received! <Type={type}>")

            self.options.append(c(option["name"], option["value"]))


class SubCommandGroup(SlashPatchObject):
    """A slash commands subcommand group option."""

    def __init__(self, name: str, options: list):
        self.name = name
        self.type = OptionType.SUB_COMMAND

        self.options = []

        for option in options:
            type = option["type"]

            if type == OptionType.STRING:
                c = String
            elif type == OptionType.INTEGER:
                c = Integer
            elif type == OptionType.BOOLEAN:
                c = Boolean
            elif type == OptionType.USER:
                c = User
            elif type == OptionType.CHANNEL:
                c = Channel
            elif type == OptionType.ROLE:
                c = Role
            elif type == OptionType.SUB_COMMAND:
                self.options.append(SubCommand(option["name"], option.get("options", [])))
                continue
            else:
                raise TypeError(f"Invalid option received! <Type={type}>")

            self.options.append(c(option["name"], option["value"]))
