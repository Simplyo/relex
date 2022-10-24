import dataclasses
import typing


@dataclasses.dataclass()
class Report:
    server_name: str
    duration: int


class Durations:

    def __init__(self):
        self._durations = {}

    def add(self, server_name, duration):
        if server_name not in self._durations:
            self._durations[server_name] = []
        self._durations[server_name].append(duration)

    def durations(self, server_name: str = None) -> typing.List[int]:
        if server_name is not None:
            return self._durations[server_name]

        all_servers_durations = []
        for server_durations in self._durations.values():
            all_servers_durations.extend(server_durations)
        return all_servers_durations

    def server_durations(self):
        return self._durations.values()

    def server_names(self):
        return self._durations.keys()

    def items(self):
        return self._durations.items()
