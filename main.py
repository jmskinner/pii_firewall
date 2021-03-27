import json
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path
from IPython.display import clear_output
from pii_firewall import PIIFirewall
import os

def parse_args():
    try:
        with open(sys.argv[1]) as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')

def parse_args_test():

    try:
        with open("/Users/skinner/Desktop/mpcs/practicum/pii_firewall/config.json") as json_file:
            return json.load(json_file)
    except Exception:
        print(f'Error reading file from source: {sys.argv[1]}')

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)

def run_benchmark():
    results_path = '/Users/skinner/Desktop/mpcs/practicum/pii_firewall/testing/output'
    test_files_path = '/Users/skinner/Desktop/mpcs/practicum/pii_firewall/testing/benchmarking_tests'
    sets_to_bench = ['b2']
    num_cpus = [1]
    num_cpus.extend(list(range(2,16,2)))
    num_threads = [2]
    n_repeats = 2
    config = parse_args_test()
    iteration = "v3"
    all_results = []
    final_path = os.path.join(results_path,iteration)
    Path(final_path).mkdir(parents=True, exist_ok=True)

    for set in sets_to_bench:
        data_path = os.path.join(test_files_path,set)
        config['runtime_config']['endpoints'] = [str(data_path+" --> "+"/Users/skinner/Desktop/mpcs/practicum/output")]
        print(config['runtime_config']['endpoints'])
        for cpu_count in num_cpus:
            config['runtime_config']['max_cpus'] = cpu_count
            for thread_count in num_threads:
                config['runtime_config']['max_threads'] = thread_count
                config['task_config']['max_thread_per_task'] = thread_count
                for pete in range(n_repeats):
                    counter = f"  Running iteration {pete+1} on {set} for cpu={cpu_count}, threads={thread_count}  "
                    print('\n' * 1)
                    print(bordered(counter.upper()))
                    print('\n' * 1)
                    analyzer = PIIFirewall(config)
                    start = datetime.now()
                    analyzer.run()
                    end = datetime.now()
                    delta = end - start
                    results = {"run":[pete],
                               "benchmark":[set],
                               "cpus":[cpu_count],
                               "threads":[thread_count],
                                "time": [delta.total_seconds()]}


                    df = pd.DataFrame.from_dict(results)
                    df.to_csv(final_path+"/benchmark_results.csv",mode='a',header=False,index=False)

    df = pd.DataFrame(all_results)
    final_path = os.path.join(results_path,iteration)
    Path(final_path).mkdir(parents=True, exist_ok=True)
    df.to_csv(final_path+"/benchmark_results.csv",index=False)



if __name__ == '__main__':
    results_path = '/Users/skinner/Desktop/mpcs/practicum/pii_firewall/testing/output'
    print("Running the program now")
    config = parse_args_test()
    analyzer = PIIFirewall(config)
    analyzer.run()
    # run_benchmark()
