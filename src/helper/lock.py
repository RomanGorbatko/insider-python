import hashlib
from pathlib import Path


class Lock:
    def __init__(self, namespace, clear=False):
        self.namespace = namespace

        if clear:
            self.clear()

    def get_hash(self, string):
        return hashlib.md5(string.encode()).hexdigest() + '.' + self.namespace

    @staticmethod
    def get_lock_dir() -> Path:
        current_dir = Path(__file__).parent.parent.parent.resolve()

        return Path(current_dir / 'data' / 'lock')

    def glob(self):
        return self.get_lock_dir().glob('*.' + self.namespace)

    def get_lock_file_path(self, name):
        return Path(self.get_lock_dir().__str__() + '/' + name)

    def exists(self, name=None) -> bool:
        if name:
            return self.get_lock_file_path(
                self.get_hash(name)
            ).is_file()
        else:
            return bool(list(self.glob()))

    def create(self, name):
        name = self.get_hash(name)

        open(self.get_lock_file_path(name), 'w').close()

    def clear(self):
        for file in self.glob():
            file.unlink()
