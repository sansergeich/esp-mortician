# ESP-mortician

It is a simple stand-alone CLI utility for decoding ESP32 backtrace.
Initially was made for fun and personal use.

Possible further improvements:
* objdump tool discovery. Maybe some auto-discovery instead of argumand or hard-coded default value
* some assertions checks and other validations.


## Help output:
```
user@host:~/py/esp-mortician$ ./esp-mortician.py -h
usage: esp-mortician [-h] [-t TOOL] -e ELF -b BACKTRACE

Utility for decoding ESP backtraces

optional arguments:
  -h, --help            show this help message and exit
  -t TOOL, --tool TOOL  Path to xtensa-esp32-elf-objdump tool used for
                        dissasembly.
  -e ELF, --elf ELF     Path to firmware elf file to decode with.
  -b BACKTRACE, --backtrace BACKTRACE
                        Backtrace string from esp monitor, like following:
                        "Backtrace: 0x400D5E8B:0x3FFB0FE0
                        0x400D6012:0x3FFB1000 ..."
```

## Usage example:
```
user@host:~/py/esp-mortician$ ./esp-mortician.py -e test-fe.elf -b "Backtrace: 0x4008212e:0x3ffb0b10 0x400865f1:0x3ffb0b30 0x4008b39a:0x3ffb0b50 0x40082fa3:0x3ffb0bc0 0x400830e1:0x3ffb0bf0 0x4008315a:0x3ffb0c10 0x400de5f9:0x3ffb0c40 0x400e173d:0x3ffb0f50 0x400e9565:0x3ffb0f80 0x4008b24d:0x3ffb0fb0 0x400d1381:0x3ffb1000 0x4008287d:0x3ffb1020 0x400d0f2c:0x3ffb4c50 0x400d0f7f:0x3ffb4c80 0x400e8eee:0x3ffb4ca0 0x40089025:0x3ffb4cd0"


Used objdump tool: "~/.platformio/packages/toolchain-xtensa-esp32/bin/xtensa-esp32-elf-objdump"
Elf file: "test-fe.elf"
Backtrace line:
"Backtrace: 0x4008212e:0x3ffb0b10 0x400865f1:0x3ffb0b30 0x4008b39a:0x3ffb0b50 0x40082fa3:0x3ffb0bc0 0x400830e1:0x3ffb0bf0 0x4008315a:0x3ffb0c10 0x400de5f9:0x3ffb0c40 0x400e173d:0x3ffb0f50 0x400e9565:0x3ffb0f80 0x4008b24d:0x3ffb0fb0 0x400d1381:0x3ffb1000 0x4008287d:0x3ffb1020 0x400d0f2c:0x3ffb4c50 0x400d0f7f:0x3ffb4c80 0x400e8eee:0x3ffb4ca0 0x40089025:0x3ffb4cd0"

--------calls rollback----------
0x4008212e called from <panic_abort> function at 0x4008211c
0x400865f1 called from <esp_system_abort> function at 0x400865ec
0x4008b39a called from <abort> function at 0x4008b310
0x40082fa3 called from <lock_acquire_generic> function at 0x40082f60
0x400830e1 called from <_lock_acquire_recursive> function at 0x400830d8
0x4008315a called from <__retarget_lock_acquire_recursive> function at 0x4008314c
0x400de5f9 called from <_vfprintf_r> function at 0x400de560
0x400e173d called from <vprintf> function at 0x400e1710
0x400e9565 called from <esp_log_writev> function at 0x400e9540
0x4008b24d called from <esp_log_write> function at 0x4008b230
0x400d1381 called from <udma_interupt_handler> function at 0x400d1360
0x4008287d called from <_xt_coproc_exc> function at 0x4008266c
0x400d0f2c called from <main> function at 0x400d0e68
0x400d0f7f called from <app_main> function at 0x400d0f7c
0x400e8eee called from <main_task> function at 0x400e8e84
0x40089025 called from <__getreent> function at 0x40088d34
--------calls rollback end------
```