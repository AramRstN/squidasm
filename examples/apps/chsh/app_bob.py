import numpy as np

from netqasm.sdk import EPRSocket
from netqasm.sdk import ThreadSocket as Socket
from netqasm.output import get_new_app_logger
from squidasm.sdk import NetSquidConnection


def measure_basis_0(bob, q):
    q.rot_Y(angle=-np.pi/4)
    return q.measure()


def measure_basis_1(bob, q):
    q.rot_Y(angle=np.pi/4)
    return q.measure()


def main(log_config=None, y=0):
    if not (y == 0 or y == 1):
        raise ValueError(f"y should be 0 or 1, not {y}")

    app_logger = get_new_app_logger(node_name="bob", log_config=log_config)
    app_logger.log(f"Bob received input bit y = {y}")

    socket = Socket("bob", "repeater", log_config=log_config)
    epr_socket = EPRSocket("repeater")

    bob = NetSquidConnection(
        "bob",
        log_config=log_config,
        epr_sockets=[epr_socket]
    )

    with bob:
        # Wait for entanglement with Alice through repeater
        epr = epr_socket.recv()[0]

        # Receive teleportation corrections
        msg = socket.recv()
        app_logger.log(f"Bob got teleportation corrections: {msg}")
        m1, m2 = eval(msg)
        if m2 == 1:
            epr.X()
        if m1 == 1:
            epr.Z()

        # CHSH strategy: measure in one of 2 bases depending on y.
        if y == 0:
            b = measure_basis_0(bob, epr)
        else:
            b = measure_basis_1(bob, epr)

    app_logger.log(f"Bob outputs b = {b}")
    return {'b': int(b)}


if __name__ == "__main__":
    main()