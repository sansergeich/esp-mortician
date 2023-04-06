#!/usr/bin/python3
import os
import csv
import argparse
import subprocess
import re


def get_tool_path():
    return "~/.platformio/packages/toolchain-xtensa-esp32/bin/xtensa-esp32-elf-objdump"

def prepare_arguments():
    parser = argparse.ArgumentParser(
        prog="esp-mortician",
        description="Utility for decoding ESP backtraces",
    )
    parser.add_argument('-t', '--tool', default=get_tool_path(),
                        help="Path to xtensa-esp32-elf-objdump tool used for dissasembly.", required=False)
    parser.add_argument('-e', '--elf', help="Path to firmware elf file to decode with.",
                        required=True)
    parser.add_argument('-b', '--backtrace',
                        help="Backtrace string from esp monitor, like following: \"Backtrace: 0x400D5E8B:0x3FFB0FE0 0x400D6012:0x3FFB1000 ...\"",
                        required=True)
    return parser.parse_args()

class Decoder:
    def __init__(self, tool=None, elf=None, trace=None) -> None:
        self.tool = os.path.abspath(os.path.expanduser(tool))
        self.elf = os.path.abspath(os.path.expanduser(elf))
        self.trace = trace

    def prepare_trace(self):
        tok = self.trace.split()

        if tok[0] == "Backtrace:":
            tok = tok[1:]

        call_points = [token.split(":")[0].lower() for token in tok]
        call_points = [token.split("x")[1] for token in call_points]
        self.call_points = call_points

    def get_dissasm(self):
        result = subprocess.check_output([self.tool, "-d", self.elf]).decode()
        self.diss_lines = result.split('\n')

    def get_address_table(self):
        self.addr_table = {}
        for line in self.diss_lines:
            line = line.split(":")
            if len(line) == 2:
                self.addr_table[line[0]] = line[1]

    def get_functions_table(self):
        self.functions_table = []
        funcs = list(filter(lambda line : re.match("[0-9a-f]{8} <[a-z_]+>:", line), self.diss_lines))

        for func in funcs:
            func = func.split(" ")
            self.functions_table.append((func[0],func[1].split(":")))

        self.functions_table.sort(key=lambda x : x[0])

    def get_callers(self):
        self.callers = []
        for call in self.call_points:
            for func in self.functions_table:
                if func[0] < call: continue
                idx = self.functions_table.index(func)
                func = self.functions_table[idx - 1]
                self.callers.append((call, func))
                break

    def print_callers(self):
        print("--------calls rollback----------")
        for call in self.callers:
            print("0x{} called from {} function at 0x{}".format(call[0], call[1][1][0], call[1][0]))
        print("--------calls rollback end------")
        print("\n")


    def search_calls(self):
        for call_point in self.call_points:
            print(call_point)
            print(self.addr_table.get(call_point, "Nothing"))


if __name__ == "__main__":

    args = prepare_arguments()
    print("\n")
    print("Used objdump tool: \"{}\"".format(args.tool))
    print("Elf file: \"{}\"".format(args.elf))
    print("Backtrace line:\n\"{}\"\n".format(args.backtrace))

    decoder = Decoder(tool=args.tool,
                      elf=args.elf,
                      trace=args.backtrace)
    decoder.prepare_trace()
    decoder.get_dissasm()
    decoder.get_functions_table()
    decoder.get_callers()
    decoder.print_callers()