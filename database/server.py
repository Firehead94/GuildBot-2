import discord


class Server:

    def __init__(self, id, name, roles, categories, channels, data):
        self.id = id
        self.name = name
        self.roles = roles
        self.categories = categories
        self.channels = channels
        self.data = data

    @property
    def admin_roles(self):
        roles = []
        for role in self.roles:
            if role.permissions.administrator:
                roles.append(role)
        return roles

    @property
    def everyone_role(self):
        for role in self.roles:
            if role.is_default():
                return role
        return None

    def __repr__(self):
        return "Server({}, '{}', {}, {}, {}, {})".format(self.id, self.name, self.roles, self.categories, self.channels, self.data)