import discord
import configparser


class Config:

    def __init__(self, config_file):

        self.config_file = config_file

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        config_sections = {"Credentials", "Chat"}.difference(config.sections())

        # Credentials
        self.login_token = config.get('Credentials', 'Token',
                                      fallback=ConfigDefaults.token)

        # Chat
        self.command_prefix = config.get('Chat', 'CommandPrefix',
                                         fallback=ConfigDefaults.command_prefix)
        self.announcement_channel_id = config.get('Chat', 'AnnouncementChannelID',
                                                  fallback=ConfigDefaults.announcement_channel_id)


class ConfigDefaults:

    # Credentials
    token = None

    # Chat
    command_prefix = '!'
    announcement_channel_id = None

