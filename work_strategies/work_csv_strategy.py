import pandas as pd
from work_strategies.work_base_strategy import WorkerBaseStrategy
import re


class WorkerCSVStrategy(WorkerBaseStrategy):

    # shoutout to http://www.regular-expressions.info/creditcard.html for these regex expressions!
    regex_patterns = {'EMAIL_ADDRESS': "^[\w\.=-]+@[\w\.-]+\.[\w]{2,3}$",
                      "US_PASSPORT": "^(?!^0+$)[a-zA-Z0-9]{3,20}$",
                      "US_SSN": "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$",
                      "US_ITIN": "^(9\d{2})([ \-]?)([7]\d|8[0-8])([ \-]?)(\d{4})$",
                      "IP_ADDRESS_v4": "^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$",
                      "IP_ADDRESS_v6": "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                      "CC_MC": "^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}",
                      "CC_VISA": " ^4[0-9]{12}(?:[0-9]{3})?",
                      "CC_AMER": "^3[47][0-9]{13}$",
                      "CC_OTHER": "((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])",
                      "USS_ZIP": "^((\d{5}-\d{4})|(\d{5})|([A-Z]\d[A-Z]\s\d[A-Z]\d))$",
                      "local_file_path": "\\[^\\]+$",
                      "US_PHONE_NUMBER": "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$",
                      "INTL_PHONE": "^(\+0?1\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$",
                      "ADDRESS": "\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)",
                      }

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
                for key, pattern in self.regex_patterns.items():
                    if any(task.data[col].astype(str).str.contains(pattern)):
                        task.profile[key] = int(task.data[col].astype(str).str.count(pattern).sum())
                        task.data[col] = task.data[col].astype(str).str.replace(pattern, "PII_" + key.upper(),
                                                                                regex=True, case=False)
                        new_col_names[col] = "PII_DETECTED_REDACTED_" + col
                        break
            task.data.rename(columns=new_col_names)
            return task
        except Exception as e:
            print(f"There was an error reading and writing the CSV at {task.in_endpoint}")
            print(e)

    def _push(self, worker, task):
        print(f"Worker {worker.id} pushed task at {task.in_endpoint}")
        worker.write_queue.put(task)
