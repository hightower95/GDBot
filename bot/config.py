import configparser

'''
Configuration file reader
'''


class Config:

    def __init__(self, config_file):

        self.config_file = config_file

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        config_sections = {"Credentials", "Chat", "Arma"}.difference(config.sections())

        # Credentials
        self.login_token = config.get('Credentials', 'Token',
                                      fallback=ConfigDefaults.token)

        # General
        self.owner_id = config.get('General', 'OwnerID',
                                   fallback=ConfigDefaults.owner_id)
        self.admin_role = config.get('General', 'AdminRole',
                                     fallback=ConfigDefaults.admin_role)

        # Chat
        self.command_prefix = config.get('Chat', 'CommandPrefix',
                                         fallback=ConfigDefaults.command_prefix)
        self.announcement_channel_id = config.get('Chat', 'AnnouncementChannelID',
                                                  fallback=ConfigDefaults.announcement_channel_id)

        # Arma
        self.mission_upload_channel_id = config.get('Arma', 'MissionUploadChannelID',
                                                    fallback=ConfigDefaults.mission_upload_channel_id)
        self.holding_area_path = config.get('Arma', 'HoldingAreaPath',
                                            fallback=ConfigDefaults.holding_area_path)
        self.server_missions_path = config.get('Arma', 'ServerMissionsPath',
                                               fallback=ConfigDefaults.server_missions_path)
        self.mission_upload_role = config.get('Arma', 'MissionUploadRole',
                                              fallback=ConfigDefaults.server_missions_path)
        self.mission_manage_role = config.get('Arma', 'MissionManageRole',
                                              fallback=ConfigDefaults.mission_manage_role)


class ConfigDefaults:

    # Credentials
    token = None

    # General
    owner_id = None
    admin_role = 'Admin'

    # Chat
    command_prefix = '!'
    announcement_channel_id = None

    # Arma
    mission_upload_channel_id = None
    holding_area_path = '..\\mission_holding_area\\'
    server_missions_path = '..\\server_missions\\'
    mission_upload_role = 'admin'
    mission_manage_role = 'admin'