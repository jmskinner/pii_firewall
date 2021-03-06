from datetime import datetime

class Task():

    def __init__(self,domain,task_type,in_endpoint,out_endpoint,profile_endpoint,task_config):
        self.task_type = task_type
        self.data = None
        self.config = task_config
        self.profile = {}
        self.in_endpoint = in_endpoint
        self.out_endpoint = out_endpoint
        self.profile_endpoint = profile_endpoint
        self.domain = domain
        self.in_is_local =  not any(x in in_endpoint for x in ['https','http'])
        self.out_is_local = not any(x in out_endpoint for x in ['https','http'])
        self.start_time = datetime.now()
        self._make_baseline_profile()




    def has_data(self):
        return self.data != None

    def _make_baseline_profile(self):
        self.profile['in_endpoint'] = self.in_endpoint
        self.profile['out_endpoint'] = self.out_endpoint
        self.profile['profile_endpoint'] = self.profile_endpoint
        self.profile['domain'] = self.domain
        self.profile['task_type'] = self.task_type



#
#
# class CSVTask(Task):
#
#     def fetch(self):
#         try:
#             if "https://" in self.in_endpoint or "http://" in self.in_endpoint:
#                 self.is_local = False
#             self.data = [pd.read_csv(self.in_endpoint, index_col=0)]
#         except Exception:
#             print(f'Error reading file from source: {self.in_endpoint}')
#
#
# class TextTask(Task):
#
#     def fetch(self):
#         text_lines = []
#         try:
#             if "https://" in self.in_endpoint or "http://" in self.in_endpoint:
#                 self.is_local = False
#                 for line in urlopen(self.in_endpoint):
#                     text_lines.append(line.decode('utf-8'))
#             else:
#                 with open(self.in_endpoint) as local_file:
#                     for line in locals():
#                         text_lines.append(line)
#             self.data = text_lines
#         except Exception:
#             print(f'Error reading file from source: {self.in_endpoint}')
#
#
# class PDFTask(Task):
#     # must be local
#    def fetch(self):
#        try:
#            images = convert_from_path(self.in_endpoint)
#        except Exception:
#            print(f'Error reading file from source: {self.in_endpoint}')
#
#


# class TextTask(Task):
#
#     def read_in_chunks(file_object, chunk_size=1024):
#         """Lazy function (generator) to read a file piece by piece.
#         Default chunk size: 1k."""
#         while True:
#             data = file_object.read(chunk_size)
#             if not data:
#                 break
#             yield data
#
#     def fetch(self):
#         text_lines = []
#         try:
#             if "https://" in self.endpoint or "http://" in self.endpoint:
#                 self.is_local = False
#                 data = urlopen(self.endpoint)
#                 self.data =
#             else:
#                 with open("log.txt") as infile:
#                     for line in infile:
#
#             self.data = image[:, :, ::-1]
#         except Exception:
#             print(f'Error reading file from source: {self.endpoint}')

