import logging
import ConfigParser
import requests
import json
import click
import websocket


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class SlackBot(object):

    def __init__(
        self,
        api_token,
        base_url,
        events_map,
        debug=False,
        debug_ws=True,
    ):
        self.api_token = api_token
        self.base_url = base_url
        self.events_map = dict(events_map)
        self.debug = debug
        self.debug_ws = debug_ws

    def __call__(self):
        url = self._get_ws_url()
        websocket.enableTrace(self.debug_ws)
        ws = websocket.WebSocketApp(
            url,
            on_data=self.on_data
        )
        ws.run_forever()

    def _get_ws_url(self):
        resp = requests.post(
            'https://slack.com/api/rtm.start',
            data={'token': self.api_token}
        )

        return resp.json()['url']

    def _request(self, event, json_data):
        endpoint = self.events_map[event]
        url = (
            self.base_url.format(endpoint) +
            '?token={}'.format(self.api_token)
        )
        response = requests.post(
            url,
            json=json_data,
        )

        response.raise_for_status()

        return response

    def on_data(self, ws, data, data_type, flag):
        json_data = json.loads(data)
        if 'subtype' in json_data:
            event = json_data['subtype']
            if event in self.events_map:
                log.debug('%s event has specified action: %s', event, self.events_map[event] or event)
                return self._request(event, json_data)

        event = json_data['type']
        if event in self.events_map:
            log.debug('%s event has specified action: %s', event, self.events_map[event] or event)
            return self._request(event, json_data)

        log.debug('Event handler not found. Data received: %s', json_data)

@click.command()
@click.option('-c', '--ini', required=True)
def main(ini):
    config = ConfigParser.ConfigParser()
    config.read(ini)

    bot = SlackBot(
        config.get('main', 'api_token'),
        config.get('main', 'base_url'),
        config.items('events'),
        config.getboolean('main', 'debug'),
        config.getboolean('main', 'debug_ws')
    )
    bot()
