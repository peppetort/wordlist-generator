import argparse
import threading
from support.configuration import Operations, Configuration
from support.queue import Queue
from support.output_file import OutputFile
from support.generator_tools import Tools

_sentinel = object()


def dequeue_and_write(queue: Queue, configuration: Configuration):
    output_file = OutputFile(configuration.output_file_path)

    while True:
        for i in range(0, len(queue.queue)):
            element = queue.dequeue()
            if element is _sentinel:
                output_file.close()
                return
            output_file.write(element)


def compute(queue: Queue, conf: Configuration, keyword_chunk: []):
    generator = Tools(conf)

    keywords = [] + keyword_chunk
    keywords_upperized = []
    keywords_leetified = []

    keywords.extend(generator.mix(keyword_chunk))
    queue.enqueue(keywords)

    for kw in keywords:
        if conf.operations.upperize:
            keywords_upperized.extend(generator.upperize(kw))

        if conf.operations.leetify:
            keywords_leetified.extend(generator.leetify(kw))

        if conf.operations.years:
            queue.enqueue((generator.add_year(kw)))

        if conf.operations.special:
            queue.enqueue((generator.add_special(kw)))

    queue.enqueue(keywords_upperized)
    queue.enqueue(keywords_leetified)

    for up_kw in keywords_upperized:
        if conf.operations.years:
            queue.enqueue((generator.add_year(up_kw)))

        if conf.operations.special:
            queue.enqueue((generator.add_special(up_kw)))

    for leet_kw in keywords_leetified:
        if conf.operations.years:
            queue.enqueue((generator.add_year(leet_kw)))

        if conf.operations.special:
            queue.enqueue((generator.add_special(leet_kw)))

    if conf.operations.upperize:
        for kw in keywords:
            keywords_upperized.extend(generator.upperize(kw))
        queue.enqueue(keywords_upperized)

    if conf.operations.leetify:
        for kw in keywords:
            keywords_leetified.extend(generator.leetify(kw))


def run(configuration: Configuration):
    queue = Queue()

    write_thread = threading.Thread(target=dequeue_and_write, args=(queue, configuration))
    write_thread.start()

    chunk_list = Tools(configuration).create_chunks()

    chunk_to_process = []
    for chunk in chunk_list:
        chunk_to_process.append(chunk)

        if len(chunk_to_process) == configuration.thread_number:
            thread_list = []
            for i in range(0, configuration.thread_number):
                t = threading.Thread(target=compute, args=(queue, configuration, chunk_to_process.pop()))
                t.start()
                thread_list.append(t)
            for t in thread_list:
                t.join()

    if len(chunk_to_process) != 0:
        thread_list = []
        for i in range(0, min(configuration.thread_number, len(chunk_to_process))):
            t = threading.Thread(target=compute, args=(queue, configuration, chunk_to_process.pop(i)))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

    queue.enqueue([_sentinel])
    write_thread.join()


'''def x():
    configuration = Config()
    queue = Queue()
    write_thread = threading.Thread(target=dequeue_and_write, args=(queue, configuration.name + '.txt'))
    write_thread.start()

    chunk_list = configuration.create_chunks()

    c_list = []
    for c in chunk_list:
        c_list.append(c)

        if len(c_list) == THREADS_NUMBER:
            thread_list = []
            for i in range(0, THREADS_NUMBER):
                t = threading.Thread(target=compute, args=(queue, c_list[i], configuration))
                t.start()
                thread_list.append(t)
            for t in thread_list:
                t.join()
            c_list.clear()

    queue.enqueue([_sentinel])
    write_thread.join()
    print('ok')'''

'''def run():
    generated_words_counter = 0

    c = Configuration()
    c.clear_output_file()
    keyword_chunk_list = c.create_chunks()

    for keywords_chunk in keyword_chunk_list:
        keywords_mix = []
        keywords_upperized = []
        keywords_mix_upperized = []
        keywords_leetified = []
        keywords_mix_leetified = []

        print(f'{Bcolors.HEADER} WORKING ON CHUNK: {keywords_chunk} {Bcolors.ENDC}')
        print(f'\t{Bcolors.BOLD}1){Bcolors.ENDC}', end=' ')
        print(f'{Bcolors.UNDERLINE}Generate all possible keywords mix{Bcolors.ENDC}', end='...')
        keywords_mix = keywords_mix + mix(keywords_chunk)
        c.write(keywords_chunk)
        c.write(keywords_mix)
        generated_words_counter = generated_words_counter + len(keywords_chunk) + len(keywords_mix)
        print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

        if operations['U']:
            print(f'\t{Bcolors.BOLD}2){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.OKBLUE}UpPeRIZe {Bcolors.ENDC}')
            print(f'\t\t{Bcolors.BOLD}2.1){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Upperizing plain keywords{Bcolors.ENDC}', end='...')
            for kw in keywords_chunk:
                keywords_upperized = keywords_upperized + upperize(kw)
            c.write(keywords_upperized)
            generated_words_counter = generated_words_counter + len(keywords_upperized)
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')
            print(f'\t\t{Bcolors.BOLD}2.2){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Upperizing keywords mix{Bcolors.ENDC}', end='...')
            for kw in keywords_mix:
                keywords_mix_upperized = keywords_mix_upperized + upperize(kw)
            c.write(keywords_mix_upperized)
            generated_words_counter = generated_words_counter + len(keywords_mix_upperized)
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

        if operations['L']:
            print(f'\t{Bcolors.BOLD}3){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.OKBLUE}L33t1fy {Bcolors.ENDC}')
            print(f'\t\t{Bcolors.BOLD}3.1){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Leetify plain keywords{Bcolors.ENDC}', end='...')
            for kw in keywords_chunk:
                keywords_leetified = keywords_leetified + leetify(kw, c.leet)
            c.write(keywords_leetified)
            generated_words_counter = generated_words_counter + len(keywords_leetified)
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')
            print(f'\t\t{Bcolors.BOLD}3.2){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Leetify keywords mix{Bcolors.ENDC}', end='...')
            for kw in keywords_mix:
                keywords_mix_leetified = keywords_mix_leetified + leetify(kw, c.leet)
            c.write(keywords_mix_leetified)
            generated_words_counter = generated_words_counter + len(keywords_mix_leetified)
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

        if operations['Y']:
            print(f'\t{Bcolors.BOLD}4){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.OKBLUE}Years {Bcolors.ENDC}')

            to_write = []

            print(f'\t\t{Bcolors.BOLD}4.1){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Adding years to keywords{Bcolors.ENDC}', end='...')
            for kw in keywords_chunk:
                to_write = to_write + add_year(kw, c.years)
            c.write(to_write)
            generated_words_counter = generated_words_counter + len(to_write)
            to_write.clear()
            for kw in keywords_mix:
                to_write = to_write + add_year(kw, c.years)
            c.write(to_write)
            generated_words_counter = generated_words_counter + len(to_write)
            to_write.clear()
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

            if len(keywords_upperized) != 0:
                print(f'\t\t{Bcolors.BOLD}4.2){Bcolors.ENDC}', end=' ')
                print(f'{Bcolors.UNDERLINE}Adding years to upperized keywords{Bcolors.ENDC}', end='...')
                for kw in keywords_upperized:
                    to_write = to_write + add_year(kw, c.years)
                for kw in keywords_mix_upperized:
                    to_write = to_write + add_year(kw, c.years)
                c.write(to_write)
                generated_words_counter = generated_words_counter + len(to_write)
                to_write.clear()
                print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

            if len(keywords_leetified) != 0:
                print(f'\t\t{Bcolors.BOLD}4.3){Bcolors.ENDC}', end=' ')
                print(f'{Bcolors.UNDERLINE}Adding years to leetified keywords{Bcolors.ENDC}', end='...')
                for kw in keywords_leetified:
                    to_write = to_write + add_year(kw, c.years)
                for kw in keywords_mix_leetified:
                    to_write = to_write + add_year(kw, c.years)
                c.write(to_write)
                generated_words_counter = generated_words_counter + len(to_write)
                to_write.clear()
                print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

        if operations['SC']:
            print(f'\t{Bcolors.BOLD}4){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.OKBLUE}Special chars !@% {Bcolors.ENDC}')
            to_write = []

            print(f'\t\t{Bcolors.BOLD}5.1){Bcolors.ENDC}', end=' ')
            print(f'{Bcolors.UNDERLINE}Adding special chars to keywords{Bcolors.ENDC}', end='...')
            for kw in keywords_chunk:
                to_write = to_write + add_special(kw, c.special)
            for kw in keywords_mix:
                to_write = to_write + add_special(kw, c.special)
            c.write(to_write)
            generated_words_counter = generated_words_counter + len(to_write)
            to_write.clear()
            print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

            if len(keywords_upperized) != 0:
                print(f'\t\t{Bcolors.BOLD}5.2){Bcolors.ENDC}', end=' ')
                print(f'{Bcolors.UNDERLINE}Adding special chars to upperized keywords{Bcolors.ENDC}', end='...')
                for kw in keywords_upperized:
                    to_write = to_write + add_special(kw, c.special)
                for kw in keywords_mix_upperized:
                    to_write = to_write + add_special(kw, c.special)
                c.write(to_write)
                generated_words_counter = generated_words_counter + len(to_write)
                to_write.clear()
                print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

            if len(keywords_leetified) != 0:
                print(f'\t\t{Bcolors.BOLD}5.3){Bcolors.ENDC}', end=' ')
                print(f'{Bcolors.UNDERLINE}Adding special chars to leetified keywords{Bcolors.ENDC}', end='...')
                for kw in keywords_leetified:
                    to_write = to_write + add_special(kw, c.special)
                for kw in keywords_mix_leetified:
                    to_write = to_write + add_special(kw, c.special)
                c.write(to_write)
                generated_words_counter = generated_words_counter + len(to_write)
                to_write.clear()
                print(f'{Bcolors.OKGREEN}Done{Bcolors.ENDC}', end='\n')

        print(f'{Bcolors.WARNING}Generated words: {generated_words_counter}{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}Output file size: {c.get_output_file_size() / 100000} M{Bcolors.ENDC}')
        print('\n')

    print(f'{Bcolors.FAIL}TOTAL: {generated_words_counter} words{Bcolors.ENDC}')
    print(f'{Bcolors.FAIL}Output file size: {c.get_output_file_size() / 100000} M{Bcolors.ENDC}')'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--upperize", help="upperize keywords", action='store_true')
    parser.add_argument("-l", "--leetify", help="leet keywords substitution", action='store_true')
    parser.add_argument("-y", "--years", help="add years at the end of each generated word", action='store_true')
    parser.add_argument("-s", "--special", help="add special characters at the end of each generated word",
                        action='store_true')
    args = parser.parse_args()

    o = Operations()
    o.upperize = args.upperize
    o.leetify = args.leetify
    o.years = args.years
    o.special = args.special

    c = Configuration('conf.cfg', o)
    c.print()
    run(c)
