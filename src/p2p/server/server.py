from p2p.peer.peer import Peer
from p2p.client.client import Client
from shared.pki.pki import PKI
from p2p.dataservice import DataService
from p2p.server.endpoint import Endpoint
from p2p.authentication.authentication_service import AuthenticationService
from p2p.authentication.role import Role
from http import HTTPStatus
from flask import Flask, request, Response
from uuid import uuid4
import threading
import shared.util as util
import time
import math
import typing as t


class Capability:
    BASE_DIRECTORY = "./resources/react_dynamic/"

    def __init__(self, name: str, js_file: str):
        self.__name = name
        self.__js_file = js_file
        self.__uuid = uuid4().hex

    def get_name(self) -> str:
        return self.__name

    def get_js_file(self) -> str:
        return self.__js_file

    def get_uuid(self) -> str:
        return self.__uuid


class Server:

    """
    Class representing the Server side of the P2P Node\n
    Spawns a thread using `start_server` method to run the server on\n
    To propertly collapse the execution stack, run `stop_server` method\n

    ---

    This class allows clients to this class to define more endpoints on the server\n
    allowing this class still be generic to P2P structure, but be 'extensable'\n
    allowing for more specific usages.

    ---

    ---
    FIELDS
    ---

    This class has no accessible fields
    """

    def __init__(
        self,
        parent_peer: Peer,
        client: Client,
        data_service: DataService,
        pki: PKI,
        authentication_service: AuthenticationService = None,
    ):
        """
        Constructor for Server

        Args:
            parent_peer (Peer): The `Peer` representation of the `ThisPeer` that runs this `Server`
            client (Client): The `Client` provided by the parent `ThisPeer`
            data_service (DataService): The `DataService` provided by the parent `ThisPeer`
            pki (PKI): The `PKI` object
            authentication_service (AuthenticationService)
        """
        self.__parent_peer = parent_peer
        self.__data_service = data_service
        self.__client = client
        self.__pki = pki
        self.__endpoints = []
        self.__authentication_service = authentication_service

        self.__app = Flask(__name__)
        self.add_endpoint(
            Endpoint(
                "/node/join",
                "Node Join Request",
                Endpoint.MethodEnum.POST,
                {"peers": "A py/set of Peers"},
                {"peer": "A Peer object"},
            ),
            self.__node_join,
        )
        self.add_endpoint(
            Endpoint("/api/shutdown", "shutdown", Endpoint.MethodEnum.GET, {}, {}),
            self.__shutdown_server,
        )
        self.add_endpoint(
            Endpoint(
                "/node/capabilities",
                "Get Node Capabilities",
                Endpoint.MethodEnum.GET,
                {"capabilties", "List of capabilities"},
                {},
            ),
            self.__get_capabilities,
        )
        self.add_endpoint(
            Endpoint(
                "/node/capability",
                "getCapability",
                Endpoint.MethodEnum.GET,
                {"text": "The JS file associated with the supplied UUID"},
                {"uuid": "The requested capability by UUID"},
            ),
            self.__get_capability,
        )

        self.__running = False

        self.__capabilities = [
            Capability(
                "General Information", "GeneralInformation/GeneralInformation.js"
            )
        ]

    def start_server(self) -> None:
        """
        Starts the server `Thread`
        """
        self.__start_time = time.time()
        self.__server_thread = threading.Thread(
            target=self.__app.run,
            kwargs={
                "host": self.__parent_peer.get_connection().get_host(),
                "port": self.__parent_peer.get_connection().get_port(),
                "ssl_context": self.__pki.get_ssl_context(),
            },
        )
        self.__server_thread.start()
        self.__running = True

    def stop_server(self) -> None:
        """
        Stops the server `Thread`
        """
        self.__server_thread.join()
        self.__running = False

    def add_endpoint(self, endpoint: Endpoint, func: t.Callable) -> None:
        """
        Adds an endpoint to the server

        Args:
            endpoint (Endpoint): The endpoint definition
            func (t.Callable): What to do when the endpoint is requested
        """

        def endpoint_wrapper():
            if request.method == Endpoint.MethodEnum.OPTIONS.value:
                return self.build_response(HTTPStatus.OK, {})

            if (
                self.__authentication_service is not None
                and endpoint.accessible_to() != Role.OPEN
            ):
                api_key = request.args.get("api_key", None)
                if api_key is None:
                    return self.build_response(
                        HTTPStatus.UNAUTHORIZED,
                        {
                            "message": "API Key must be supplied with each request as api_key"
                        },
                    )
                response = self.__authentication_service.load_user(api_key)
                if response.status != 0:
                    return self.build_response(
                        HTTPStatus.UNAUTHORIZED, {"message": response.message}
                    )
                user = response.returned_obj
                if not user.has_role(endpoint.accessible_to):
                    return self.build_response(
                        HTTPStatus.UNAUTHORIZED,
                        {"message": "You do not have access to this endpoint"},
                    )

            return func()

        self.__endpoints.append(endpoint)
        self.__app.add_url_rule(
            endpoint.get_uri(),
            endpoint.get_name(),
            endpoint_wrapper,
            methods=[*endpoint.get_method()],
        )
        if endpoint.get_method() == Endpoint.MethodEnum.POST.value:
            print("Here " + endpoint.get_uri() + " " + endpoint.get_name())
            self.__app.add_url_rule(
                endpoint.get_uri(),
                endpoint.get_name(),
                lambda: self.build_response(HTTPStatus.OK, {}),
                methods=["OPTIONS"],
            )

    def __node_join(self) -> Response:
        """
        Definition for /node/join `POST` endpoint\n
        Consumes the POST parameters which should consist of a `Peer` object\n
        Adds that `Peer` object to the active `Peer`s `set` and notifies all active `Peer`s\n

        Returns:
            Response: All active `Peer`s
        """
        peer = util.extract_data(request.get_data(as_text=True))["peer"]
        current_active_peers = self.__data_service.deep_copy("active_peers")

        if peer not in current_active_peers:
            self.__data_service.modify("active_peers", lambda v: v.add(peer))
            current_active_peers = self.__data_service.deep_copy("active_peers")
            responses = self.__client.join_network(
                [p for p in current_active_peers if p != self.__parent_peer],
                peer,
                logger=self.__app.logger,
            )
            for p in responses:
                self.__data_service.modify(
                    "active_peers",
                    lambda v: v.update(util.extract_data(responses[p].text)),
                )
            current_active_peers = self.__data_service.deep_copy("active_peers")

        return self.build_response(200, current_active_peers)

    def __shutdown_server() -> None:
        """
        Definition for /api/shutdown `GET` endpoint

        Raises:
            RuntimeError: If not running werkzeug server implementation under the `Flask` hood
        """
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        func()

    def __get_capabilities(self) -> Response:
        return self.build_response(HTTPStatus.OK, self.__capabilities)

    def __get_capability(self) -> Response:
        uuid = request.args.get("uuid")
        filename = ""
        try:
            filename = (
                Capability.BASE_DIRECTORY
                + (
                    [
                        capability
                        for capability in self.__capabilities
                        if capability.get_uuid() == uuid
                    ][0]
                ).get_js_file()
            )
        except:
            return self.build_response(HTTPStatus.NOT_FOUND)
        out = ""
        try:
            with open(filename, "r") as file:
                out = file.read()
        except FileNotFoundError:
            return self.build_response(HTTPStatus.NOT_FOUND)

        return self.build_response(HTTPStatus.OK, out, False)

    def build_response(
        self,
        response_code: int,
        response_obj: t.Dict[t.Any, t.Any] = None,
        package: bool = True,
    ) -> Response:
        """
        A nice simple way to put together a `Flask` `Response` object

        Args:
            response_code (int): The response code to send back to client
            response_obj (t.Dict[t.Any, t.Any]): The body of the response

        Returns:
            Response: A `Flask` `Response` object
        """

        response = (
            util.jsonify_data(response_obj)
            if package and response_code is not None
            else response_obj
            if response_code is not None
            else None
        )
        return Response(
            response=response,
            status=response_code,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            },
            mimetype="application/json",
        )

    def uptime(self) -> t.Dict[str, int]:
        """
        Diagnostics to see how long the server has been live for\n
        `!!!THIS WILL BE REMOVED!!!`

        Returns:
            t.Dict[str, int]: A human readable representation of the amount of time the server has been up
        """
        delta = time.time() - self.__start_time
        return {
            "year": math.floor(delta / 31536000),
            "month": math.floor(delta / 2629746) % 12,
            "day": math.floor(delta / 86400) % 30,
            "hour": math.floor(delta / 3600) % 24,
            "minute": math.floor(delta / 60) % 60,
            "second": math.floor(delta % 60),
        }

    def get_data_service(self) -> DataService:
        """
        Accessor for `DataService` instance variable

        Returns:
            DataService: The servers `DataService` reference
        """
        return self.__data_service

    def get_parent_peer(self) -> Peer:
        """
        Accessor for the parent `Peer` object

        Returns:
            Peer: The parent `Peer` object
        """
        return self.__parent_peer

    def add_capability(self, capability: Capability) -> None:
        return self.__capabilities.append(capability)

    def get_endpoints(self) -> t.Iterable[Endpoint]:
        return self.__endpoints
