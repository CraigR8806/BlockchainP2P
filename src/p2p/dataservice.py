from threading import Thread, Condition
from typing import Callable, Dict, NoReturn, Iterable, Any
from copy import deepcopy
from time import time


DataAccessor = Callable[[Any], NoReturn]


class DataService:

    class __DataServiceQueueEntry:

        def __init__(self, key:str, func:Callable, args:Iterable[Any], condition:Condition = None, callback:Callable = None):
            self.key = key
            self.func = func
            self.args = args
            self.condition = condition
            self.callback = callback

    def __init__(self, timeout_duration:int=5):
        self.__data_map = {}
        self.__data_map_condition = Condition()
        self.__deep_copy_map = {}
        self.__queue = []
        self.__thread = Thread(target=self.__listen)
        self.__timeout_duration = timeout_duration
        self.__running = False
        self.__highest_queue_count = 0

    def get_highest_queue_count(self):
        return self.__highest_queue_count

    def modify(self, key:str, func:DataAccessor, condition:Condition = None, callback:Callable = None, asyync:bool = False):
        if key not in self.__data_map:
            raise KeyError(key + " not managed by this DataService...")
        if condition is not None and callback is not None:
            raise AttributeError("Condition and callback may not both be supplied...")
        if not asyync and condition is not None:
            raise AttributeError("If accessing this in a synchronous fashion, a Condtion may not also be passed")
        if not asyync and callback is not None:
            raise AttributeError("If accessing this in a synchronous fashion, a Callback may not also be passed")
        
        entry = DataService.__DataServiceQueueEntry(key, func, [self.__data_map.get(key, None)], condition, callback)

        self.__add_to_queue(entry, asyync)


    def __add_to_queue(self, entry:__DataServiceQueueEntry, asyync:bool = False):
    
        entry.condition = entry.condition if asyync else Condition()
        self.__data_map_condition.acquire()
        if entry.condition is not None:
            entry.condition.acquire()
        self.__queue.append(entry)
        self.__data_map_condition.notify()
        self.__data_map_condition.release()
        if not asyync:
            entry.condition.wait()
            entry.condition.release()

    def start_service(self):
        if not self.__running:
            self.__running = True
            self.__thread.start()

    def __listen(self):

        def exec_callable_with_timeout(func:Callable, args:Iterable, duration:int):
            timeout_process = Thread(target=func, args=args)
            timeout_process.start()

            timeout_process.join(duration)

        while self.__running:
            self.__data_map_condition.acquire()
            self.__data_map_condition.wait_for(lambda:not self.__running or len(self.__queue) > 0)
            self.__data_map_condition.release()
            if len(self.__queue):
                self.__highest_queue_count = max(len(self.__queue), self.__highest_queue_count)
                entry = self.__queue.pop(0)
                if entry.condition is not None:
                    entry.condition.acquire()

                exec_callable_with_timeout(entry.func, entry.args, self.__timeout_duration)

                if entry.condition is not None:
                    entry.condition.notify()
                    entry.condition.release()

                if entry.callback is not None:
                    exec_callable_with_timeout(entry.callback, None, self.__timeout_duration)


            
    def stop_service(self):
        if self.__running:
            self.__running = False
            self.__data_map_condition.acquire()
            self.__data_map_condition.notify()
            self.__data_map_condition.release()
            self.__thread.join(self.__timeout_duration + 1)

    def add(self, key:str, val:Any, condition:Condition = None, callback:Callable = None, asyync:bool = False):
        entry = DataService.__DataServiceQueueEntry(key, self.__add_it, [key, val], condition, callback)
        self.__add_to_queue(entry, asyync=asyync)

    def deep_copy(self, key:str):
        actual_key=key + str(int(time()))
        entry = DataService.__DataServiceQueueEntry(key, 
                                        lambda data_map,deep_copy_map,k,ak:deep_copy_map.update({ak:deepcopy(data_map[k])}),
                                        [self.__data_map, self.__deep_copy_map, key, actual_key],
                                        None, None)
        self.__add_to_queue(entry)
        return self.__deep_copy_map.pop(actual_key)
    
    def __add_it(self, k, v):
        self.__data_map[k] = v