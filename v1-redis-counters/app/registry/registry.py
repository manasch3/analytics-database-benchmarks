class FeatureRegistry:
    def __init__(self):
        self.features = {}

    def add(self, tenant_id, feature):
        self.features[(tenant_id, feature["name"])] = feature

    def get(self, tenant_id, name):
        return self.features.get((tenant_id, name))

    def list(self, tenant_id):
        return [
            f for (t, _), f in self.features.items() if t == tenant_id
        ]
