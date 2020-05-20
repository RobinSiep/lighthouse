import uuid
from unittest.mock import patch

from aiohttp.test_utils import unittest_run_loop

from lighthouse.machine import set_machine
from lighthouse.models.machine import Machine, get_machine_by_id
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

    @unittest_run_loop
    async def test_machine_not_found(self):
        await self.login()
        resp = await self.client.request('GET', self.url.format(uuid.uuid4()))
        self.assertEqual(resp.status, 404)

    @unittest_run_loop
    async def test_machine_offline(self):
        await self.login()
        resp = await self.client.request('GET',
                                         self.url.format(self.machine_id))
        self.assertEqual(resp.status, 409)

    @unittest_run_loop
    async def test_success(self):
        await self.login()
        await set_machine(self.test_machine_data['sid'],
                          self.test_machine_data)

        async def emit_mock(event, to, callback):
            callback([80, 443])

        with patch('lighthouse.handlers.machine.port.sio.emit',
                   new=emit_mock):
            resp = await self.client.request('GET',
                                             self.url.format(self.machine_id))

        machine = get_machine_by_id(self.machine_id)
        port_numbers = [port.number for port in machine.ports]
        self.assertEqual(resp.status, 200)
        self.assertIn(80, port_numbers)
        self.assertIn(443, port_numbers)
