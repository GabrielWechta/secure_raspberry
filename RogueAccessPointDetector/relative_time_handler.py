import multiprocessing


class RelativeTimeHandler:
    def __init__(self):
        self.queue_of_dict_relative_time = multiprocessing.Queue()

    def get_list_of_dict_relative_time(self):
        list_of_dict_relative_time = []
        while not self.queue_of_dict_relative_time.empty():
            list_of_dict_relative_time.append(self.queue_of_dict_relative_time.get())
        return list_of_dict_relative_time
