import write_strategies.write_pdf_strategy as pdf
import write_strategies.write_csv_strategy as csv
import write_strategies.write_image_strategy as img
import write_strategies.write_text_strategy as txt

class WriterStrategyFactory:

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
                return pdf.WriterPDFStrategy(domain, task_type)

        elif domain == "image":
            return img.WriterImageStrategy(domain, task_type)

        elif domain == 'text':
            if task_type == 'csv':
                return csv.WriterCSVStrategy(domain, task_type)
            elif task_type == 'plain':
                return txt.WriterTextStrategy(domain, task_type)

        else:
            raise ValueError(f" failed to write task with file path {task.in_endpoint}")

    @staticmethod
    def check_strategy(strategy, task):
        if task.domain == 'image':
            return strategy.domain == task.domain
        else:
            return strategy.domain == task.domain and strategy.task_type == task.task_type



