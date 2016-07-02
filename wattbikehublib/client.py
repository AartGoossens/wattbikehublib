import datetime
import re

from dateutil import parser
import requests


BASE_HUB_URL = 'http://hub.wattbike.com/{username}/sessions/{start_date}/{end_date}'
BASE_SESSION_URL = 'http://hub.wattbike.com/ranking/getSessionRows?sessionId={session_id}'
BASE_ZONE_RECORDS_URL = 'http://hub.wattbike.com/{username}/zone-records'


class Client:
    def __init__(self, username):
        self.username = username

    def get_session_ids(self, start_date=None, end_date=None):
        if not end_date:
            end_date = datetime.datetime.now().date()
        if not start_date:
            start_date = end_date - datetime.timedelta(days=30)

        resp = requests.get(
            BASE_HUB_URL.format(
                username=self.username,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()))

        return re.findall(
            pattern='\/session\/(?P<session_id>[a-z0-9]+)"',
            string=resp.text)

    def get_session(self, session_id):
        response = requests.get(
            BASE_SESSION_URL.format(
                session_id=session_id))
        return response.json()

    def get_new_sessions(self, start_date=None, end_date=None):
        new_sessions = []
        for session_id in self.get_session_ids(start_date, end_date):
            session = self.get_session(session_id)
            new_sessions.append(session)
        return new_sessions

    def get_training_zones(self):
        training_zone_regex = (
            '<tr>[\s]*<th>(?P<zone_name>[a-zA-Z0-9-\s]+)<\/th>[\s]*'
            '<td>(?P<heartrate>[<>\-\s\dN\/A]+)<\/td>[\s]*'
            '<td>(?P<power>[<>\-\s\d]+)<\/td>[\s]*<\/tr>')

        matches = re.findall(
            pattern=training_zone_regex,
            string=self._get_zone_records_html())
        return matches

    def get_current_zone_record(self):
        current_record_regex = (
            'currentRecord">(?P<unit>[MMP|MHR]+)'
            '["<>:a-zA-z\s]*(?P<value>[\d]+)')

        matches = re.findall(
            pattern=current_record_regex,
            string=self._get_zone_records_html())
        return {i[0]: i[1] for i in matches if i[0] in ['MMP', 'MHR']}

    def get_historical_zone_records(self):
        current_record_regex = (
            '<tr>[\s]*<td>(?P<date>[a-zA-Z0-9\-\s]+)<\/td>[\s]*'
            '<td>(?P<power>[\d]+)<\/td>[\s]*'
            '<td>(?P<heartrate>[\d]+)<\/td>[\s]*'
            '<td>[\w]+<\/td>[\s]*<\/tr>')

        zone_records = re.findall(
            pattern=current_record_regex,
            string=self._get_zone_records_html())

        historical_zones = []
        for record in zone_records:
            historical_zones.append(dict(
                date=parser.parse(record[0]).date(),
                power=int(record[1]),
                heartrate=int(record[2])))
        return historical_zones

    def _get_zone_records_html(self):
        return requests.get(
            BASE_ZONE_RECORDS_URL.format(username=self.username)).text
