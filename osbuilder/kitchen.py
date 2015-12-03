import os
import errno
import json
import nutils


class Kitchen(object):
    @nutils.convert_exceptions
    def __init__(self, path):
        self.abs_path = os.path.abspath(path)
        self.desc_path = os.path.join(self.abs_path, 'kitchen.json')
        self.data = {}

        try:
            os.makedirs(self.abs_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                with open(self.desc_path, encoding='utf-8') as fp:
                    self.data = json.loads(fp.read())
            else:
                raise

        self.data['abs_path'] = self.abs_path
        self.save()

    @nutils.convert_exceptions
    def save(self):
        with open(self.desc_path, 'w') as fp:
            json.dump(self.data, fp, ensure_ascii=False, indent=4, sort_keys=True)

    def get(self, key, default):
        if key not in self.data:
            self.set(key, default)

        return self.data[key]

    def set(self, key, value):
        self.data[key] = value
