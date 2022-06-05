from enum import Enum
import os
from support.printer import Bcolors


class Operations:
    def __init__(self):
        self.upperize = False
        self.leetify = False
        self.years = False
        self.special = False


class ConfigParameter(Enum):
    NAME = 'NAME'
    OUTPUT_DIR_PATH = 'OUTPUT_DIR_PATH'
    KEYWORDS = 'KEYWORDS'
    YEARS = 'YEARS'
    LEET = 'LEET'
    SPECIAL_CHARS = 'SPECIAL_CHARS'
    CHUNK_LEN = 'CHUNK_LEN'
    THREAD_NUMBER = 'THREAD_NUMBER'


class Configuration:
    def __init__(self, file_path: str, operations: Operations):
        self.operations = operations

        self.name = None
        self.output_dir_path = None
        self.keywords = None
        self.years = None
        self.leet = None
        self.special_chars = None
        self.chunk_len = 3
        self.thread_number = 2

        f = open(file_path, 'r')
        config_text = f.readlines()
        self.parse_configuration(config_text)

        if self.name is None:
            raise Exception('No name specified in configuration file')

        if self.keywords is None:
            raise Exception('No keyword specified in configuration file')

        if self.output_dir_path is None:
            self.output_file_path = os.getcwd() + '/' + self.name + '.txt'
        else:
            self.output_file_path = self.output_dir_path + '/' + self.name + '.txt'

    def parse_configuration(self, text_list: []):
        for line in text_list:
            stripped = ''.join(line).replace(' ', '')

            if stripped[0] == '#':
                continue

            start_index = stripped.find('{') + 1
            end_index = stripped.find('}')

            if ConfigParameter.NAME.name in stripped:
                self.name = stripped[start_index:end_index]
                continue

            if ConfigParameter.OUTPUT_DIR_PATH.name in stripped:
                self.output_dir_path = stripped[start_index:end_index]
                continue

            if ConfigParameter.KEYWORDS.name in stripped:
                self.keywords = stripped[start_index:end_index].split(',')
                continue

            if ConfigParameter.YEARS.name in stripped:
                self.years = stripped[start_index:end_index].split(',')
                continue

            if ConfigParameter.SPECIAL_CHARS.name in stripped:
                self.special_chars = stripped[start_index:end_index].split(',')
                continue

            if ConfigParameter.CHUNK_LEN.name in stripped:
                self.chunk_len = int(stripped[start_index:end_index])
                continue

            if ConfigParameter.THREAD_NUMBER.name in stripped:
                self.thread_number = int(stripped[start_index:end_index])
                continue

            if ConfigParameter.LEET.name in stripped:
                self.leet = eval(stripped[start_index - 1:end_index + 1])
                continue

    def print(self):
        print(f'{Bcolors.CYAN}CONFIGURATION{Bcolors.ENDC}')
        print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Name{Bcolors.ENDC}: {self.name}')
        print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Output file path{Bcolors.ENDC}: {self.output_file_path}')
        print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Keywords{Bcolors.ENDC}: {self.keywords}')
        if self.operations.upperize and self.years is not None:
            print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Years{Bcolors.ENDC}: {self.years}')
        if self.operations.leetify and self.leet is not None:
            print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Leet map{Bcolors.ENDC}: {self.leet}')
        print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Chunk size{Bcolors.ENDC}: {str(self.chunk_len)}')
        print(f'{Bcolors.UNDERLINE}{Bcolors.BOLD}Thread number{Bcolors.ENDC}: {str(self.thread_number)}')
