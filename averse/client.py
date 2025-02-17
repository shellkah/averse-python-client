import grpc
import cache_pb2_grpc
import cache_pb2


class AverseClient:
    """
    A client for the Averse Cache.
    """

    def __init__(self, host="localhost", port=50051, secure=False, options=None):
        """
        Initializes the CacheClient.

        :param host: Server hostname or IP address.
        :param port: Server port.
        :param secure: Whether to use a secure channel (TLS). Currently, secure channels are not implemented.
        :param options: Additional channel options as a list of tuples.
        """
        self.target = f"{host}:{port}"

        if options is None:
            options = []

        if secure:
            # TODO
            # with open('server.crt', 'rb') as f:
            #     trusted_certs = f.read()
            # credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
            # self.channel = grpc.secure_channel(self.target, credentials, options=options)
            raise NotImplementedError("Secure channels are not implemented.")
        else:
            self.channel = grpc.insecure_channel(self.target, options=options)

        self.stub = cache_pb2_grpc.CacheServiceStub(self.channel)

    def get(self, key: str) -> str | None:
        """
        Retrieves the value for a given key.
        :param key: The key to retrieve.
        :return: The value if it was found, None otherwise.
        """
        request = cache_pb2.GetRequest(key=key)
        try:
            response = self.stub.Get(request)
            return response.value if response.found else None
        except grpc.RpcError as e:
            print(f"gRPC Get error: {e.details()}")
            raise

    def set(self, key: str, value: str) -> bool:
        """
        Sets the value for a given key.
        :param key: The key to set.
        :param value: The value to store.
        :return: is success.
        """
        request = cache_pb2.SetRequest(key=key, value=value)
        try:
            return self.stub.Set(request).success
        except grpc.RpcError as e:
            print(f"gRPC Set error: {e.details()}")
            raise

    def set_with_ttl(self, key: str, value: str, ttl_seconds: int) -> bool:
        """
        Sets the value for a given key with a time-to-live (TTL).
        :param key: The key to set.
        :param value: The value to store.
        :param ttl_seconds: Time to live in seconds.
        :return: is success.
        """
        request = cache_pb2.SetWithTTLRequest(
            key=key, value=value, ttl_seconds=ttl_seconds
        )
        try:
            return self.stub.SetWithTTL(request).success
        except grpc.RpcError as e:
            print(f"gRPC SetWithTTL error: {e.details()}")
            raise

    def delete(self, key: str) -> bool:
        """
        Deletes the given key.
        :param key: The key to delete.
        :return: Averse_pb2.DeleteResponse object.
        """
        request = cache_pb2.DeleteRequest(key=key)
        try:
            return self.stub.Delete(request).success
        except grpc.RpcError as e:
            print(f"gRPC Delete error: {e.details()}")
            raise

    def dump(self) -> bool:
        """
        Dumps the current cache state.
        :return: Averse_pb2.DumpResponse object.
        """
        request = cache_pb2.DumpRequest()
        try:
            return self.stub.Dump(request).success
        except grpc.RpcError as e:
            print(f"gRPC Dump error: {e.details()}")
            raise

    def close(self) -> None:
        """
        Closes the channel.
        """
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False
