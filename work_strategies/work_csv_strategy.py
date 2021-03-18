import pandas as pd
from work_strategies.work_base_strategy import WorkerBaseStrategy
import re

class WorkerCSVStrategy(WorkerBaseStrategy):

    # shoutout to http://www.regular-expressions.info/creditcard.html for these regex expressions!
    regex_patterns = {'email':"^[\w\.=-]+@[\w\.-]+\.[\w]{2,3}$",
                      "ssn":"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d))([-]?|\s{1})(?!00)\d\d\2(?!0000)\d{4}\b",
                      "ssn2": "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$" ,
                      "ipv4": "^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$",
                      "ipv6": "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                      "cc_mastercard":"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}",
                      "cc_visa":" ^4[0-9]{12}(?:[0-9]{3})?",
                      "cc_amer_exp":"^3[47][0-9]{13}$",
                      "cc_other": "((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])",
                      "US_zip":"^((\d{5}-\d{4})|(\d{5})|([A-Z]\d[A-Z]\s\d[A-Z]\d))$",
                      "local_file_path": "\\[^\\]+$",
                      "us_phone" :"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$",
                      "intl_phone" : "^(\+0?1\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$",
                      "street_address_full": "/\s+(\d{2,5}\s+)(?![a|p]m\b)(([a-zA-Z|\s+]{1,5}){1,2})?([\s|\,|.]+)?(([a-zA-Z|\s+]{1,30}){1,4})(court|ct|street|st|drive|dr|lane|ln|road|rd|blvd)([\s|\,|.|\;]+)?(([a-zA-Z|\s+]{1,30}){1,2})([\s|\,|.]+)?\b(AK|AL|AR|AZ|CA|CO|CT|DC|DE|FL|GA|GU|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VI|VT|WA|WI|WV|WY)([\s|\,|.]+)?(\s+\d{5})?([\s|\,|.]+)/i",
                      "street_address_partial": "/\b(\d{2,5}\s+)(?![a|p]m\b)(NW|NE|SW|SE|north|south|west|east|n|e|s|w)?([\s|\,|.]+)?(([a-zA-Z|\s+]{1,30}){1,4})(court|ct|street|st|drive|dr|lane|ln|road|rd|blvd)/i",
                      "street_addr2": "\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)",

                      }

    # def __init__(self,domain, task_type):
    #     super().__init__(domain, task_type)
    #     self.patterns = {key:re.compile(pattern) for (key,pattern) in self.regex_patterns}


    def _fetch(self, task):
        try:
            task.data = pd.read_csv(task.in_endpoint)
        except Exception:
            print(f'Error reading file from source: {task.in_endpoint}')
        return task

    def _process(self, task):
        new_col_names = {}
        try:
            for col in task.data.columns.tolist():
                new_col_names[col] = col
                for key,pattern in self.regex_patterns.items():
                    if any(task.data[col].astype(str).str.contains(pattern)):
                        task.data[col] = task.data[col].astype(str).str.replace(pattern,"PII_"+key.upper(),regex=True,case=False)
                        new_col_names[col] = "PII_DETECTED_REDACTED_"+col
                        break
            task.data.rename(columns=new_col_names)
            return task
        except Exception as e :
            print(f"There was an error reading and writing the CSV at {task.in_endpoint}")
            print(e)



    def _push(self, worker, task):
        print(f"Worker {worker.id} pushed task at {task.in_endpoint}")
        worker.write_queue.put(task)