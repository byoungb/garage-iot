from connect import connect_to_ap
from tinyweb import webserver
from garage import Garage

connect_to_ap()

app = webserver()
app.add_resource(Garage, '/')

# # @app.route('/toggle/')
# # async def toggle_view(request, response):
# #     LOGGER.debug('Update relay. {}'.format(RELAY.value()))
# #     RELAY.value(not RELAY.value())
# #     # Send actual HTML page
# #     await response.redirect('/')
# #
# #
# # @app.route('/open/')
# # async def open_view(request, response):
# #     if SENSOR.value():
# #         LOGGER.debug('Already open.')
# #     # Send actual HTML page
# #     await response.redirect('/')
# #
# #
# # @app.route('/close/')
# # async def close_view(request, response):
# #     LOGGER.debug('Update relay. {}'.format(RELAY.value()))
# #     RELAY.value(not RELAY.value())
# #     # Send actual HTML page
# #     await response.redirect('/')
