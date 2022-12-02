# Threading Communication Server

Simple tcp/udp server based on multithreading. This simple tool can read from setting and listen on given port. It can only reply to client with given message right now.  Planning to let it support more protocol model, such as http, https, ftp, etc.

## Usage

### run in python

```python
python3 main.py
```

### run in docker

```bash
docker-compose up -d
```

## settings example

```python
PORT_MAP = {
    "Modbus": {
        "TCP": 502,
        "UDP": None,
    },
    "S7COMM": {
        "TCP": 102,
    },
    "FINS": {
        "TCP": 9600,
    },
    "DNP3": {
        "TCP": 20000,
    },
    "OpcUA": {
        "TCP": 48400,
    },
    "IEC104": {
        "TCP": 2404,
    },
    "BACnet": {
        "UDP": 47808,
    },
    "MQTT": {
        "TCP": 1883
    }
}
```

## TODO

- [ ] Add more protocol support