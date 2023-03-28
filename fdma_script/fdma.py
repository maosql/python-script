import os
import sys
import time
import datetime
import pdb

from rich.progress import Progress
from optparse import OptionParser

from uart.uart import *
from sys_register.pmm_register import pmm_register_dict
from sys_register.wifi_register import wifi_register_dict
from sys_register.dtop_register import dtop_register_dict
from sys_register.bt_register import bt_register_dict

ROM_BAUDRATE = 115200

cwd = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(cwd, 'log')
log_time = datetime.datetime.now().strftime('%F_%H-%M-%S')
log_name = os.path.join(log_path, log_time + '.log')

def uart_log(data):
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file = open(log_name,'a+')
        data = data.decode('utf-8')
        log_file.writelines(data)
        log_file.close()
    except Exception as e:
        pass

PMM_SYS     = 0
WIFI_SYS    = 1
DTOP_SYS    = 2
BT_SYS      = 3

class fdma():
    def __init__(self, port, bps = None,args=[]):
        if bps:
            self.port = uart(port, bps)
        else:
            self.port = uart(port, ROM_BAUDRATE)
        # open uart
        self.port.open()
        self.args = args

        # write cmd
        self.port.write('use\r\n')
        time.sleep(0.2)
        uart_log(self.port.read_all())
        self.port.write('help\r\n')
        time.sleep(0.2)
        uart_log(self.port.read_all())

        with Progress() as progress:
            task1 = progress.add_task('[red]pmm...', total=160)
            task2 = progress.add_task('[green]wifi...', total=320)
            task3 = progress.add_task('[cyan]dtop...', total=320)
            task4 = progress.add_task('[blue]bt...', total=160)

            for sys in range(4):
                hex_sys = hex(sys)
                if sys == PMM_SYS:
                    uart_log(b"\r\n------------------------- pmm -------------------------\r")
                    uart_log(b"dbg_mod_sel | dbg_sig_sel |     val     | register\r")
                    for sig in range(16):
                        self.port.write('spi_debug_bus {S_sys} 0x0 {S_sig}\r\n'.format(S_sys=hex_sys, S_sig=hex(sig)))
                        progress.update(task1, advance=10)
                        time.sleep(0.2)
                        if pmm_register_dict[sig] != None:
                            pmm_read = self.port.readline().rstrip('\r'.encode()) + pmm_register_dict[sig].encode() + b'\r'
                            uart_log(pmm_read)
                        else:
                            uart_log(self.port.readline())
                elif sys == WIFI_SYS:
                    uart_log(b"\r\n------------------------ wifi -------------------------\r")
                    uart_log(b"dbg_mod_sel | dbg_sig_sel |     val     | register\r")
                    for sig in range(64):
                        self.port.write('spi_debug_bus {S_sys} 0x0 {S_sig}\r\n'.format(S_sys=hex_sys, S_sig=hex(sig)))
                        progress.update(task2, advance=10)
                        time.sleep(0.2)
                        if wifi_register_dict[sig] != None:
                            wifi_read = self.port.readline().rstrip('\r'.encode()) + wifi_register_dict[sig].encode() + b'\r'
                            uart_log(wifi_read)
                        else:
                            uart_log(self.port.readline())
                elif sys == DTOP_SYS:
                    uart_log(b"\r\n------------------------ dcore ------------------------\r")
                    uart_log(b"dbg_mod_sel | dbg_sig_sel |     val     | register\r")
                    for sig in range(32):
                        self.port.write('spi_debug_bus {S_sys} 0x0 {S_sig}\r\n'.format(S_sys=hex_sys, S_sig=hex(sig)))
                        progress.update(task3, advance=10)
                        time.sleep(0.2)
                        if dtop_register_dict[sig] != None:
                            dtop_read = self.port.readline().rstrip('\r'.encode()) + dtop_register_dict[sig].encode() + b'\r'
                            uart_log(dtop_read)
                        else:
                            uart_log(self.port.readline())
                elif sys == BT_SYS:
                    uart_log(b"\r\n------------------------- bt --------------------------\r")
                    uart_log(b"dbg_mod_sel | dbg_sig_sel |     val     | register\r")
                    for sig in range(16):
                        self.port.write('spi_debug_bus {S_sys} 0x0 {S_sig}\r\n'.format(S_sys=hex_sys, S_sig=hex(sig)))
                        progress.update(task4, advance=10)
                        time.sleep(0.2)
                        if bt_register_dict[sig] != None:
                            bt_read = self.port.readline().rstrip('\r'.encode()) + bt_register_dict[sig].encode() + b'\r'
                            uart_log(bt_read)
                        else:
                            uart_log(self.port.readline())
                        

        time.sleep(0.3)
        uart_log(b"\nUART Receive the success")
        # close uart
        self.port.close()


def main(argv):
    parser = OptionParser()

    parser.add_option("-p", "--port", dest="port", help="serial port to use.")
    parser.add_option("-b", "--baudrate", dest="baudrate", help="serial baudrate to use.")
    parser.add_option("-l", "--list", dest="list", help="serial com list.")

    (options, args) = parser.parse_args()

    if options.list:
        uart_list()
        sys.exit(0)
    fdma(options.port, options.baudrate, args)

if __name__ == "__main__":
    main(sys.argv[1:])