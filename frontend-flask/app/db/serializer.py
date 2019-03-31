from sqlalchemy import inspect

# Миксин для сериализации разных классов в JSON. Идея взята отсюда https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]