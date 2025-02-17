# Averse Python Client

**Averse Python Client** is a Python library that provides a simple client for the Averse cache service via gRPC.

## Features

- Connects to a gRPC cache service
- Provides easy-to-use methods to get, set, set with TTL, delete, and dump cache data
- Wraps all gRPC calls with Pythonic methods

## Installation

Install the package from PyPI:

```bash
pip install averse-python-client
```

## Usage

```python
if __name__ == "__main__":
    with AverseClient(host="localhost", port=50051) as cache:
        cache.set("example_key", "example_value")

        value = cache.get("example_key")
        print(f"Got value: {value}")

        cache.set_with_ttl("temp_key", "temp_value", ttl_seconds=60)

        delete_response = cache.delete("example_key")
        print(f"Delete success: {delete_response}")
```

## Incoming

- **Async support**: Write an async client.
- **Pydantic implementation**: Add the possibility to automaticaly serialize and deserialize cached values.
- **Publish on PyPi**: Publish the package on PyPi.
- **Secure Channels**: Implement secure channels.

## Contributing

Contributions are welcome! Please open issues or submit pull requests if you have any ideas, bug fixes, or enhancements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.