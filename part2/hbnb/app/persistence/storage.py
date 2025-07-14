class InMemoryStorage:
    def __init__(self):
        self._data = {}

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self._data[key] = obj

    def save(self):
        pass  # No action needed for in-memory

    def get(self, cls, obj_id):
        key = f"{cls.__name__}.{obj_id}"
        return self._data.get(key)

    def all(self, cls=None):
        if cls:
            return {k: v for k, v in self._data.items() if k.startswith(cls.__name__)}
        return self._data


# Global instance
storage = InMemoryStorage()
