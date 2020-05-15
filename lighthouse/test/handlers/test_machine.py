import uuid
from unittest.mock import patch

from aiohttp.test_utils import unittest_run_loop

from lighthouse.machine import set_machine, clear_machine_sys_info
from lighthouse.models.machine import Machine
from lighthouse.models.network_interface import NetworkInterface
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
        clear_machine_sys_info()


class TestReboot(AioHTTPTestCaseWithDB):
    url = "/machines/{}/reboot"
    target_id = uuid.uuid4()

    def setUp(self):
        super().setUp()
        self.persist_test_machines()

    def persist_test_machines(self):
        self.target_machine_data = {
            'id': self.target_id,
            'sid': 'pv6unfHUGAeslPlTYJJZTvQhkbJQNbcf',
            'name': 'target',
            'external_ip': '000.000.000.00',
            'mac_address': '00:00:00:00:00:00',
            'network_interfaces': [NetworkInterface(
                name='en0',
                ip_address='192.168.178.41',
                netmask='255.255.255.0'
            )]
        }
        self.wol_capable_machine_data = {
            'id': uuid.uuid4(),
            'sid': 'OvFOP2azfft0rc5RD639MEkRitJmjdJY',
            'name': 'wol',
            'external_ip': '000.000.000.00',
            'mac_address': '11:11:11:11:11:11',
            'network_interfaces': [NetworkInterface(
                name='en0',
                ip_address='192.168.178.23',
                netmask='255.255.255.0'
            )]
        }
        self.persist_all((
            Machine(**self.target_machine_data),
            Machine(**self.wol_capable_machine_data)
        ))
        self.target_machine_data.pop('network_interfaces')
        self.wol_capable_machine_data.pop('network_interfaces')

    @unittest_run_loop
    async def test_machine_not_found(self):
        await self.login()
        resp = await self.client.request('POST', self.url.format(uuid.uuid4()))
        self.assertEqual(resp.status, 404)

    @unittest_run_loop
    async def test_no_WOL_capable_machine_available(self):
        return
        await self.login()
        await set_machine(self.target_machine_data['sid'],
                          self.target_machine_data)

        resp = await self.client.request('POST',
                                         self.url.format(self.target_id))

        self.assertEqual(resp.status, 409)

    @unittest_run_loop
    async def test_machine_offline(self):
        await self.login()
        await set_machine(self.wol_capable_machine_data['sid'],
                          self.wol_capable_machine_data)

        with patch('lighthouse.handlers.machine._wake') as wake:
            resp = await self.client.request('POST',
                                             self.url.format(self.target_id))

            wake.assert_called()
            self.assertEqual(resp.status, 200)

    @unittest_run_loop
    async def test_reboot_after_disconnect(self):
        pass

    @unittest_run_loop
    async def test_reboot_after_max_polling_reached(self):
        pass

    def tearDown(self):
        super().tearDown()
        clear_machine_sys_info()
