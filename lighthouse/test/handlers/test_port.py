import uuid

from lighthouse.models.machine import Machine
from lighthouse.test import AioHTTPTestCaseWithDB


class TestListPorts(AioHTTPTestCaseWithDB):
    url = "/machines/{}/ports"
    machine_id = uuid.uuid4()

    def setUp(self):
        super().setUp()
        self.persist_test_machine()

    def persist_test_machine(self):
        self.test_machine_data = {
            'id': self.machine_id,
            'sid': 'pv6unfHUGAeslPlTYJJZTvQhkbJQNbcf',
            'name': 'target',
            'external_ip': '000.000.000.00',
            'mac_address': '00:00:00:00:00:00'
        }
        self.persist_all((
            Machine(**self.test_machine_data),
        ))

    async def test_machine_not_found(self):
        await self.login()
        resp = await self.client.request('POST', self.url.format(uuid.uuid4()))
        self.assertEqual(resp.status, 404)

    def test_machine_offline(self):
        pass

    def test_success(self):
        pass
