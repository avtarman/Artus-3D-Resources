from ArtusAPI.artus_api import ArtusAPI

artusapi = ArtusAPI(communication_method='WiFi',hand_type='right',communication_channel_identifier='ArtusLite000')

artusapi.connect()

artusapi.firmware_update()