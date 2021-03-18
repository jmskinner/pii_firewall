import work_strategies.work_pdf_strategy as pdf
import work_strategies.work_csv_strategy as csv
import work_strategies.work_image_strategy as img
import work_strategies.work_text_strategy as txt

class WorkerStrategyFactory:

    @staticmethod
    def make_strategy(task):
        task_type = task.task_type
        domain = task.domain

        if domain == 'application':

            if task_type == 'json':
                print ("Can't parse JSON files just yet")
                raise ValueError(f" failed to process task with file path {task.in_endpoint}")
            elif task_type == 'pdf':
                print('Made a pdf task and added to queque')
                return pdf.WorkerPDFStrategy(domain, task_type)

        elif domain == "image":
            return img.WorkerImageStrategy(domain, task_type)

        elif domain == 'text':
            if task_type == 'csv':
                return csv.WorkerCSVStrategy(domain, task_type)
            elif task_type == 'plain':
                return txt.WorkerTextStrategy(domain, task_type)

        else:
            raise ValueError(f" failed to process task with file path {task.in_endpoint}")

    @staticmethod
    def check_strategy(strategy, task):
        if task.domain == 'image':
            return strategy.domain == task.domain
        else:
            return strategy.domain == task.domain and strategy.task_type == task.task_type



