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

    @property
    def discord_data(self):
        if "discord_data" in self.data:
            return self.data['discord_data']
        return False

    @property
    def twitch_data(self):
        if "twitch_data" in self.data:
            return self.data['twitch_data']
        return False

    @property
    def voice_data(self):
        if "voice_data" in self.data:
            return self.data['voice_data']
        return False

    @property
    def blacklist_data(self):
        if "blacklist_data" in self.data:
            return self.data['blacklist_data']
        return False

    @property
    def worldboss_data(self):
        if "worldboss_data" in self.data:
            return self.data['worldboss_data']
        return False