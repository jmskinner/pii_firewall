from tasking import task as t

class TaskFactory:
    @staticmethod
    def make_task(domain, file_type,in_endpoint,out_endpoint):

        if domain == 'application':

            if file_type == 'json':
                print ("Can't parse JSON files just yet")
                raise ValueError(in_endpoint,out_endpoint)
            elif file_type == 'pdf':
                print('Made a pdf task and added to queque')
                return t.PDFTask(domain,file_type,in_endpoint,out_endpoint)

        elif domain == "image":
            return t.ImageTask(domain, file_type, in_endpoint,out_endpoint)

        elif domain == 'text':

            if file_type == 'csv':
                return t.CSVTask(domain,file_type, in_endpoint,out_endpoint)
            elif file_type == 'plain':
                return t.TextTask(domain,file_type,in_endpoint,out_endpoint)
            else:
                raise ValueError(in_endpoint,out_endpoint)

        else:
            raise ValueError(in_endpoint,out_endpoint)
