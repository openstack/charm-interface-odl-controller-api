from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class ControllerAPIRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors = ['private-address', 'host', 'port',
                      'username', 'password']

    @hook('{requires:odl-controller-api}-relation-{joined,changed,departed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection():
            self.set_state('{relation_name}.access.available')
        else:
            self.remove_state('{relation_name}.access.available')

    @hook('{requires:odl-controller-api}-relation-broken')
    def broken(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.access.available')

    def connection(self):
        """OpenDayLight Controller Access Details

        Returns a dict of key value pairs for accessing the ODL controller API.
        """
        data = {
            'host': self.host() or self.private_address(),
            'port': self.port() or '8181',
            'username': self.username(),
            'password': self.password(),
        }
        if all(data.values()):
            return data
        else:
            return None
