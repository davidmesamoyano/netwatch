import socket
import threading

from netwatch.measure import take_samples, tcp_rtt_ms


def test_mide_un_servidor_local():
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen()
    port = srv.getsockname()[1]
    threading.Thread(target=lambda: [srv.accept() for _ in range(3)], daemon=True).start()

    samples = take_samples("127.0.0.1", port, count=3, timeout=1, pause=0)
    assert all(s is not None and s >= 0 for s in samples)
    srv.close()


def test_puerto_cerrado_cuenta_como_perdida():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()  # nadie escucha en ese puerto
    assert tcp_rtt_ms("127.0.0.1", port, timeout=1) is None
