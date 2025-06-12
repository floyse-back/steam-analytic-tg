from typing import Dict,Callable


class DispatcherCommands:
    def __init__(self,command_map:Dict[str,Callable]):
        self.command_map:Dict[str,Callable] = command_map

    async def dispatch(self, command_name: str, *args, **kwargs):
        try:
            command = self.command_map.get(command_name)
            if not command:
                raise ValueError(f"Unknown command: {command_name}")
            return await command(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Dispatcher error: {e}")