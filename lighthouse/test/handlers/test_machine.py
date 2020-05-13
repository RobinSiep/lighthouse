import uuid

from aiohttp.test_utils import unittest_run_loop

from lighthouse.machine import set_machine, set_machine_offline
from lighthouse.models.machine import Machine
from lighthouse.test import AioHTTPTestCaseWithDB


class TestShutdown(AioHTTPTestCaseWithDB):
    url = "/machines/{}/shutdown"
    test_machine_sid = 'pv6unfHUGAeslPlTYJJZTvQhkbJQNbcf'

    @unittest_run_loop
    async def test_shutdown_404(self):
        await self.login()
        resp = await self.client.request('POST', self.url.format(uuid.uuid4()))
        self.assertEqual(resp.status, 404)

    @unittest_run_loop
    async def test_success(self):
        await self.login()
        machine_data = {
            'sid': self.test_machine_sid,
            'external_ip': "000.000.000.00",
            'name': 'test',
            'mac_address': "00:00:00:00:00:00"
        }

        machine_id = self.persist_machine(machine_data)
        await set_machine(self.test_machine_sid, machine_data)

        resp = await self.client.request('POST', self.url.format(
            str(machine_id)))

        self.assertEqual(resp.status, 200)

    @unittest_run_loop
    async def test_offline(self):
        await self.login()
        machine_data = {
            'sid': self.test_machine_sid,
            'external_ip': "000.000.000.00",
            'name': 'test',
            'mac_address': "00:00:00:00:00:00"
        }
        machine_id = self.persist_machine(machine_data)

        resp = await self.client.request('POST', self.url.format(
            str(machine_id)))

        self.assertEqual(resp.status, 409)

    def persist_machine(self, machine_data):
        machine_id = uuid.uuid4()
        self.persist_all([
            Machine(
                id=machine_id,
                **machine_data
            )
        ])
        return machine_id

    def tearDown(self):
        super().tearDown()
        set_machine_offline(self.test_machine_sid)
