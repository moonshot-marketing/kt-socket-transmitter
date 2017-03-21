# kt-socket-transmitter

TCP message transmitter module.

## Implement

1. added module via pip install
```
$ pip install git+https://github.com/moonshot-marketing/kt-socket-transmitter.git
```
2.
import all from kt_socket_transmitter
```python
from kt_socket_transmitter import *
```

3. implement transmitter class and build custom message

#### for example: bid service
```python
class BidSocketTransmitter(SocketTransmitter):

    def build_message(self, tracking_id, rows, status, message):
        message = {
            "tracking_id": tracking_id,
            "rows": rows,
            "status": 1 if status else 0,
            "message": message
        }

        return json.dumps(message)
```

4. send message when service finish / success or failed
```python
s = BidSocketTransmitter(SERVER_IP, SERVER_PORT, 1024)
s.execute(s.build_message(12, 1515, True, ''))
```