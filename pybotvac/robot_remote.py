import itertools


class CapabilityProxy(object):
    def __init__(self, obj, capabilities, handler):
        self.obj = obj
        self.capabilities = capabilities
        self.handler = handler

    @property
    def is_supported(self):
        return bool(self.handler)

    def __call__(self, *args, **kwargs):
        return self.handler(self.obj, *args, **kwargs)


class CapabilityMap(object):
    valid_capabilities = {
        "findMe": ["basic-1"],
        "generalInfo": ["basic-1", "advanced-1"],
        "houseCleaning": ["basic-1", "minimal-2", "basic-2"],
        "localStats": ["advanced-1"],
        "manualCleaning": ["basic-1", "advanced-1"],
        "maps": ["basic-1"],
        "preferences": ["basic-1", "advanced-1"],
        "schedule": ["basic-1", "basic-2", "minimal-1"],
        "spotCleaning": ["basic-1", "micro-2", "minimal-2", "basic-2"],
    }

    def __init__(self):
        self._map = {}

    def __get__(self, obj, type=None):
        enabled_capabilities = set(obj.capabilities.items())
        available_capabilities = set(self._map.keys())
        joint_capabilities = enabled_capabilities & available_capabilities

        return CapabilityProxy(
            obj,
            joint_capabilities,
            self._map.get(next(iter(joint_capabilities), None)))

    def add(self, capability, level, func):
        key = (capability, level)
        if key in self._map:
            raise ValueError("Already bound")
        self._map[key] = func


class CapabilityDispatcher(object):
    def __init__(self):
        self._maps = {}

    def __call__(self, availability):
        def decorator(func):
            attr = func.__name__
            capability_map = self._maps.get(attr)
            if capability_map is None:
                capability_map = CapabilityMap()
                self._maps[attr] = capability_map

            for capability, level in availability:
                capability_map.add(capability, level, func)
            return capability_map
        return decorator

    def simple(self, capability, level):
        return self([(capability, level)])


# Capabilities for general cleaning control functions 
_general_cleaning = list(itertools.product(
    ["houseCleaning", "spotCleaning"],
    ["basic-1", "basic-2", "minimal-2"]
))


class RobotRemote(object):
    capability_dispatcher = CapabilityDispatcher()

    def __init__(self, capabilities=None):
        self.counter = itertools.count()

        if capabilities is None:
            capabilities = {}
        self.capabilities = capabilities

    @capability_dispatcher.simple("findMe", "basic-1")
    def find_me(self):
        return {"cmd": "findMe"}

    @capability_dispatcher(
        itertools.product(["generalInfo"], ["basic-1", "advanced-1"]))
    def get_info(self):
        return {"cmd": "getGeneralInfo"}

    def get_debug_info(self):
        return {"cmd": "getRobotInfo"}

    def get_state(self):
        return {"cmd": "getRobotState"}

    def dismiss_alert(self):
        return {"cmd": "dismissCurrentAlert"}

    @capability_dispatcher.simple("houseCleaning", "basic-1")
    def start_cleaning(self, eco_mode=False):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 2,
                "mode": 1 if eco_mode else 2,
                "modifier": 1,
            },
        }

    @capability_dispatcher.simple("houseCleaning", "minimal-2")
    def start_cleaning(self, extra_care=False):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 2,
                "navigationMode": 2 if extra_care else 1,
            },
        }

    @capability_dispatcher.simple("houseCleaning", "basic-2")
    def start_cleaning(self, eco_mode=False):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 2,
                "mode": 1 if eco_mode else 2,
                "modifier": 1,
                "navigationMode": 1 if extra_care else 2,
            },
        }

    @capability_dispatcher.simple("spotCleaning", "basic-1")
    def start_spot_cleaning(
            self, eco_mode=False, double_frequency=False, width=100,
            height=100):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 3,
                "mode": mode,
                "modifier": modifier,
                "spotWidth": width,
                "spotHeight": height,
            },
        }

    @capability_dispatcher.simple("spotCleaning", "micro-1")
    def start_spot_cleaning(self, extra_care=False):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 3,
                "navigationMode": 2 if extra_care else 1,
            }
        }


    @capability_dispatcher.simple("spotCleaning", "minimal-2")
    def start_spot_cleaning(self, double_frequency=False, extra_care=False):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 3,
                "modifier": 2 if double_frequency else 1,
                "navigationMode": 2 if extra_care else 1,
            }
        }

    @capability_dispatcher.simple("spotCleaning", "basic-2")
    def start_spot_cleaning(
            self, eco_mode=False, double_frequency=False, extra_care=False,
            width=100, height=100):
        return {
            "cmd": "startCleaning",
            "params": {
                "category": 3,
                "mode": 1 if eco_mode else 2,
                "modifier": 2 if double_frequency else 1,
                "navigationMode": 2 if extra_care else 1,
                "spotWidth": width,
                "spotHeight": height,
            }
        }

    @capability_dispatcher(_general_cleaning)
    def stop_cleaning(self):
        return {"cmd": "stopCleaning"}

    @capability_dispatcher(_general_cleaning)
    def pause_cleaning(self):
        return {"cmd": "pauseCleaning"}

    @capability_dispatcher(_general_cleaning)
    def resume_cleaning(self):
        return {"cmd": "resumeCleaning"}

    @capability_dispatcher(_general_cleaning)
    def return_to_base(self):
        return {"cmd": "sendToBase"}

    @capability_dispatcher.simple("localStats", "advanced-1")
    def get_local_stats(self):
        return {"cmd": "getLocalStats"}

    @capability_dispatcher.simple("manualControl", "basic-1")
    def manual_control_websocket():
        return {"cmd": "getRobotManualCleaningInfo"}

    @capability_dispatcher(
        itertools.product(["preferences"], ["basic-1", "advanced-1"]))
    def get_preferences():
        return {"cmd": "getPreferences"}
