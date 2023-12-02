from threading import Thread, Condition
from typing import Callable, Dict, NoReturn, Iterable, Any
from copy import deepcopy
from time import time
from uuid import uuid4, UUID
from enum import Enum


class DataService:

    """
    DataService provides a thread safe service for thread shared variables generically \n
    Variables can be:
     - added to the service by calling the `add` method
     - modified by calling the `modify` method
     - retrieved as a deep copy by calling `deep_copy` method

    Prior to using the service, it must be started using the `start_service` method\n
    To propertly collapse the execution stack, `stop_service` method must be called\n
    ---
    There are no public instance fields for this class.  All fields should be treated\n
    as private and should not be accessed by implementers.
    """

    DataAccessor = Callable[[Any], NoReturn]

    class __WatchMapEntry:
        def __init__(self, func: Callable):
            self.__func = func
            self.__uuid = uuid4()

        def get_function(self) -> Callable:
            return self.__func

        def get_uuid(self) -> UUID:
            return self.__uuid

    class __DataServiceQueryQueryTypeEnum(Enum):
        UPSERT = (0,)
        MODIFY = (1,)
        READ = (2,)

    class __DataServiceQueueEntry:

        """
        __DataServiceQueueEntry is a (private) inner class representation of
        information needed for each Queue entry


        -----------
        FIELDS
        -----------

        key : str
            The data map key associated with the queue entry action
        func : Callable
            The function object to be executed against the data map object
        args : Iterable[Any]
            A list of arguments to be sent to the func function object when calling it
        condition : Condition
            A Condition object to notify upon completion of func execution
        callback : Callable
            A Callback object to exeucte upon completion of fun execution
        """

        def __init__(
            self,
            key: str,
            func: Callable,
            args: Iterable[Any],
            query_type: "DataService.__DataServiceQueryQueryTypeEnum",
            condition: Condition = None,
            callback: Callable = None,
        ):
            self.key = key
            self.func = func
            self.args = args
            self.query_type = query_type
            self.condition = condition
            self.callback = callback

    def __init__(self, timeout_duration: int = 5):
        """
        Constructor for DataService

        Args:
            timeout_duration (int, optional): The amount of time in seconds to allow passed functional arguments to execute before stopping them. Defaults to 5.
        """
        self.__data_map = {}
        self.__data_map_condition = Condition()
        self.__deep_copy_map = {}
        self.__queue = []
        self.__thread = Thread(target=self.__listen)
        self.__timeout_duration = timeout_duration
        self.__running = False
        self.__highest_queue_count = 0
        self.__watch_map = {}

    def _get_highest_queue_count(self) -> int:
        """
        Produces captured metric `!!!WILL BE REMOVED!!!`

        Returns:
            int: The most number of items seen in the queue up unto this point
        """
        return self.__highest_queue_count

    def _get_watch_map(self) -> Dict[str, __WatchMapEntry]:
        return self.__watch_map

    def modify(
        self,
        key: str,
        func: DataAccessor,
        condition: Condition = None,
        callback: Callable = None,
        asyync: bool = False,
    ) -> None:
        """
        Used to modify an object already tracked by this data_service.\n
        This method will take the requested action and add it to the internal queue.\n
        Can be handled in a synchronise or asynchronise fashion

        ---
        Args
        ---
            `key` (str): The name of the object to execute the `func` function provided against

            `func` (DataAccessor): What to do with the object with name `key`

            `condition` (Condition, optional): Condition to be notified when `func` function completes execution. `asyync cannot be False if provided` Defaults to None.

            `callback` (Callable, optional): Callback to be executed when `func` function completes execution. `asyync cannot be False if provided` Defaults to None.

            `asyync` (bool, optional): Whether calling this method should lock calling thread until completion. Defaults to False.

        ---
        Raises
        ---
            KeyError: If `key` provided doesn't exist in the data map
            AttributeError: If `condition` and `callback` are both defined
            AttributeError: If `asyync` is False and `condition` is defined
            AttributeError: If `asyync` is False and `callback` is defined
        """
        if key not in self.__data_map:
            raise KeyError(key + " not managed by this DataService...")
        if condition is not None and callback is not None:
            raise AttributeError("Condition and callback may not both be supplied...")
        if not asyync and condition is not None:
            raise AttributeError(
                "If accessing this in a synchronous fashion, a Condtion may not also be passed"
            )
        if not asyync and callback is not None:
            raise AttributeError(
                "If accessing this in a synchronous fashion, a Callback may not also be passed"
            )

        entry = DataService.__DataServiceQueueEntry(
            key,
            func,
            [self.__data_map.get(key, None)],
            DataService.__DataServiceQueryQueryTypeEnum.MODIFY,
            condition,
            callback,
        )

        self.__add_to_queue(entry, asyync)

    def watch(self, key: str, func: Callable) -> UUID:
        entry = DataService.__WatchMapEntry(func)
        if key not in self.__watch_map:
            self.__watch_map.update({key: []})
        self.__watch_map[key].append(entry)
        return entry.get_uuid()

    def remove_watch(self, key: str, uuid: UUID) -> None:
        self.__watch_map[key].remove(
            [watch for watch in self.__watch_map[key] if watch.get_uuid() == uuid][0]
        )

    def __add_to_queue(
        self, entry: __DataServiceQueueEntry, asyync: bool = False
    ) -> None:
        """
        `PRIVATE METHOD, DO NOT ACCESS OR CALL`
        """

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

    def start_service(self) -> None:
        """
        Starts the underlying thread for the data service
        """
        if not self.__running:
            self.__running = True
            self.__thread.start()

    def __listen(self) -> None:
        """
        `PRIVATE METHOD, DO NOT ACCESS OR CALL`
        """

        def exec_callable_with_timeout(
            func: Callable, args: Iterable, duration: int
        ) -> None:
            timeout_process = Thread(target=func, args=args)
            timeout_process.start()

            timeout_process.join(duration)

        while self.__running:
            self.__data_map_condition.acquire()
            self.__data_map_condition.wait_for(
                lambda: not self.__running or len(self.__queue) > 0
            )
            self.__data_map_condition.release()
            if len(self.__queue):
                self.__highest_queue_count = max(
                    len(self.__queue), self.__highest_queue_count
                )
                entry = self.__queue.pop(0)
                if entry.condition is not None:
                    entry.condition.acquire()

                exec_callable_with_timeout(
                    entry.func, entry.args, self.__timeout_duration
                )

                if entry.condition is not None:
                    entry.condition.notify()
                    entry.condition.release()

                if (
                    entry.query_type
                    == DataService.__DataServiceQueryQueryTypeEnum.MODIFY
                    and entry.key in self.__watch_map
                    and len(self.__watch_map[entry.key])
                ):
                    for watch in self.__watch_map[entry.key]:
                        Thread(target=watch.get_function()).start()

                if entry.callback is not None:
                    exec_callable_with_timeout(
                        entry.callback, [], self.__timeout_duration
                    )

    def stop_service(self) -> None:
        """
        Stops the underlying thread for the data service
        """
        if self.__running:
            self.__running = False
            self.__data_map_condition.acquire()
            self.__data_map_condition.notify()
            self.__data_map_condition.release()
            self.__thread.join(self.__timeout_duration + 1)

    def upsert(
        self, key: str, val: Any, condition: Condition = None, asyync: bool = False
    ) -> None:
        """
        Adds a new variable to be tracked by the data service\n
        Can be handled in a synchronise or asynchronise fashion

        Args:
            `key` (str): The name of the object

            `val` (Any): The value of the object

            `condition` (Condition, optional): Condition to be notified when object added to data map. Defaults to None.

            `callback` (Callable, optional): Callback to be executed when object added to data map. Defaults to None.

            `asyync` (bool, optional): Whether calling this method should lock calling thread until completion. Defaults to False.
        """
        entry = DataService.__DataServiceQueueEntry(
            key,
            self.__add_it,
            [key, val],
            DataService.__DataServiceQueryQueryTypeEnum.UPSERT,
            condition,
            lambda: self.__watch_map.update({key: []})
            if self.__watch_map.get(key) is None
            else None,
        )
        self.__add_to_queue(entry, asyync=asyync)

    def deep_copy(self, key: str) -> Any:
        """
        Retrieves a copy of an object from the data service\n

        Args:
            `key` (str): The name of the object
        """
        actual_key = key + str(time())
        entry = DataService.__DataServiceQueueEntry(
            key,
            lambda data_map, deep_copy_map, k, ak: deep_copy_map.update(
                {ak: deepcopy(data_map[k])}
            ),
            [self.__data_map, self.__deep_copy_map, key, actual_key],
            DataService.__DataServiceQueryQueryTypeEnum.READ,
            None,
            None,
        )
        self.__add_to_queue(entry)
        return self.__deep_copy_map.pop(actual_key)

    def __add_it(self, k, v) -> None:
        """
        `PRIVATE METHOD, DO NOT ACCESS OR CALL`
        """
        self.__data_map[k] = v
