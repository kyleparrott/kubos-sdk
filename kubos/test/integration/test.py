#!/bin/python

import argparse
import tempfile
import os
import shutil
import serial
import serial.tools.list_ports as list_ports
import sys
import unittest

from kubos import init, target, build, flash, clean
from kubos.test.utils import get_arg_list, KubosTestCase

class SDKIntegrationTest(KubosTestCase):
    uart_read_size = 8
    expected_output = 'echo, x='
    project_name = 'project-test'
    init_args = argparse.Namespace(proj_name=[project_name],
                                   subcommand_name='init')
    build_args = argparse.Namespace(subcommand_name='build')
    flash_args = argparse.Namespace(subcommand_name='flash')
    clean_args = argparse.Namespace(subcommand_name='clean')

    def setUp(self):
        self.base_dir = os.getcwd()
        self.test_dir = os.path.join(self.base_dir, self.project_name)
        os.chdir(self.base_dir)


    def test_integration(self):
        for target in self.target_list:
            '''
            This is where the specific usb ports would be powered on and any
            other hardware set up for our specific CI config would happen.
            '''
            self.run_build(target)


    def run_build(self, hw_target):
        target_args = argparse.Namespace(subcommand_name='target',
                                         target=hw_target)

        init.execCommand(self.init_args, [])
        os.chdir(self.test_dir)
        target.execCommand(target_args, [])
        build.execCommand(self.build_args, [])
        flash.execCommand(self.flash_args, [])
        if not self.ignore_uart:
            output = self.get_uart_output()
            self.assertEqual(self.expected_output, output)
        clean.execCommand(self.clean_args, [])


    def get_uart_output(self):
        port = self.get_port()
        uart = serial.Serial(port=port, baudrate=115200)
        return uart.read(self.uart_read_size)


    def get_port(self):
        devs = list_ports.comports()
        for dev in devs:
            if 'usb' in dev.device:
                return dev.device
        print 'No Serial device found. Are you sure its connected?'
        sys.exit(1)


    def tearDown(self):
        os.chdir(self.base_dir)
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', help='Skip checking UART output from the target board after flashing')
    parser.add_argument('--targets', default='stm32f407-disco-gcc', nargs='*', help='enter a list of targets to run the test against')
    args = parser.parse_args()
    arg_dict = vars(args)
    target_list = arg_dict['targets']

    if type(target_list) is str:
        target_list = [target_list]
    SDKIntegrationTest.target_list = target_list
    if arg_dict['i']:
        SDKIntegrationTest.ignore_uart = True
    else:
        SDKIntegrationTest.ignore_uart = False
    sys.argv[1:] = list() #unittest is fussy about having extra command line arguments
    unittest.main()
