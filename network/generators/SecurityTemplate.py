import json
from utils.Misc import unhexlify_array


class SecurityTemplate:
    _path = "../config/Templates.json"
    last_template = -1

    def __init__(self):
        with open(self._path) as config:
            raw_template = json.load(config)
            self.size = raw_template['size']
            self.masks = raw_template['masks']
            self.masks_bin = unhexlify_array(self.masks)

    def check(self, msg):
        for template in self.masks_bin:
            if template == msg & template:
                return True
        return False

    def check_with_mask(self, msg):
        for template in self.masks_bin:
            if template == msg & template:
                self.last_template = template
                return True, template
        return False, -1
