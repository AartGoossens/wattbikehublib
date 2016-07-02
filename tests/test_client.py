import datetime
from unittest import TestCase, skip

from freezegun import freeze_time

from .vcr import vcr
from wattbikehublib.client import Client


class TestClient(TestCase):
    def setUp(self):
        self.client = Client(username='aart.goossens')

    def test_client_init(self):
        client = Client(username='aart.goossens')
        self.assertTrue(client)

    def test_get_session_ids(self):
        with vcr.use_cassette('test_get_session_ids.yaml') as cass:
            start_date = datetime.date(2016, 3, 1)
            end_date = datetime.date(2016, 5, 1)
            session_ids = self.client.get_session_ids(
                start_date=start_date,
                end_date=end_date)
            self.assertTrue(isinstance(session_ids, list))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/sessions/2016-03-01/2016-05-01',
                cass.requests[0].uri)

    def test_get_session_ids_no_start_date(self):
        with vcr.use_cassette('test_get_session_ids_no_start_date.yaml') as cass:
            end_date = datetime.date(2016, 4, 1)
            session_ids = self.client.get_session_ids(
                end_date=end_date)
            self.assertTrue(isinstance(session_ids, list))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/sessions/2016-03-02/2016-04-01',
                cass.requests[0].uri)

    @freeze_time('2016-07-03')
    def test_get_session_ids_no_end_date(self):
        with vcr.use_cassette('test_get_session_ids_no_end_date.yaml') as cass:
            start_date = datetime.date(2016, 4, 1)
            session_ids = self.client.get_session_ids(
                start_date=start_date)
            self.assertTrue(isinstance(session_ids, list))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/sessions/2016-04-01/2016-07-03',
                cass.requests[0].uri)

    def test_get_session(self):
        with vcr.use_cassette('test_get_session.yaml') as cass:
            session = self.client.get_session('df9ed1e2d2f3d147d357071e3004c1b0')
            self.assertTrue(isinstance(session, dict))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                ('http://hub.wattbike.com/ranking/getSessionRows?'
                 'sessionId=df9ed1e2d2f3d147d357071e3004c1b0'),
                cass.requests[0].uri)

    def test_get_session_non_existent_session_id(self):
        # @TODO: Fixing catching non-existent session_id
        with vcr.use_cassette('test_get_session_non_existent_session_id.yaml') as cass:
            session = self.client.get_session('nonexistentsessionid')

    def test_get_new_sessions(self):
        with vcr.use_cassette('test_get_new_sessions.yaml') as cass:
            start_date = datetime.date(2016, 5, 1)
            end_date = datetime.date(2016, 6, 1)
            new_sessions = self.client.get_new_sessions(
                start_date=start_date,
                end_date=end_date)
            self.assertEqual(5, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/sessions/2016-05-01/2016-06-01',
                cass.requests[0].uri)
            self.assertTrue(cass.requests[1].uri.startswith(
                'http://hub.wattbike.com/ranking/getSessionRows?'))
            self.assertTrue(isinstance(new_sessions, list))
            self.assertTrue(isinstance(new_sessions[0], dict))

    def test_get_new_sessions_none_available(self):
        with vcr.use_cassette('test_get_new_sessions_none_available.yaml') as cass:
            start_date = datetime.date(2016, 6, 1)
            end_date = datetime.date(2016, 6, 1)
            new_sessions = self.client.get_new_sessions(
                start_date=start_date,
                end_date=end_date)
            self.assertTrue(isinstance(new_sessions, list))
            self.assertEqual(0, len(new_sessions))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/sessions/2016-06-01/2016-06-01',
                cass.requests[0].uri)

    def test_get_training_zones(self):
        with vcr.use_cassette('test_get_training_zones.yaml') as cass:
            training_zones = self.client.get_training_zones()
            self.assertEqual(8, len(training_zones))
            self.assertEqual(3, len(training_zones[0]))
            self.assertEqual('Recovery', training_zones[0][0])
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/zone-records',
                cass.requests[0].uri)

    def test_get_current_zone_record(self):
        with vcr.use_cassette('test_get_current_zone_record.yaml') as cass:
            current_zone_record = self.client.get_current_zone_record()
            self.assertTrue(isinstance(current_zone_record, dict))
            self.assertTrue('MMP' in current_zone_record)
            self.assertTrue('MHR' in current_zone_record)
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/zone-records',
                cass.requests[0].uri)

    def test_get_historical_zone_records(self):
        with vcr.use_cassette('test_get_historical_zone_records.yaml') as cass:
            historical_zone_records = self.client.get_historical_zone_records()
            self.assertTrue(isinstance(historical_zone_records, list))
            self.assertEqual(1, len(historical_zone_records))
            zone_record = historical_zone_records[0]
            self.assertTrue(isinstance(zone_record, dict))
            self.assertTrue('date' in zone_record)
            self.assertTrue('power' in zone_record)
            self.assertTrue(isinstance(zone_record['power'], int))
            self.assertTrue('heartrate' in zone_record)
            self.assertTrue(isinstance(zone_record['heartrate'], int))
            self.assertEqual(1, len(cass))
            self.assertEqual(
                'http://hub.wattbike.com/aart.goossens/zone-records',
                cass.requests[0].uri)
