from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os, psutil
import time


def main() :
    text= "My name is Jake and my phone number is 817-584-0149, myy credit card is  123412085721768 and my ssn is  567-43-2345"
    # Set up the engine, loads the NLP module (spaCy model by default)]
    start_time = time.time()
    # and other PII recognizers
    analyzer = AnalyzerEngine()
    print("analyzer loaded ", time.time()-start_time)
    # Call analyzer to get results
    results = analyzer.analyze(text=text,
                               language='en')
    print("analyzer called ", time.time()-start_time)
    print(results)

    # Analyzer results are passed to the AnonymizerEngine for anonymization

    anonymizer = AnonymizerEngine()
    print("anon loaded ", time.time()-start_time)

    anonymized_text = anonymizer.anonymize(text=text,analyzer_results=results)
    print("anon called ", time.time()-start_time)
    print(anonymized_text)
    process = psutil.Process(os.getpid())
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

if __name__ == '__main__':
    test = "https://jakelikestodance.com"
    local = any(x in test for x in ['https','http'])

    print(local)
