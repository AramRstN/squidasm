from netqasm.logging import get_netqasm_logger
from netqasm.sdk.toolbox import set_qubit_state
from netqasm.sdk import Qubit
from squidasm.sdk import NetSquidConnection
from squidasm.sim_util import get_qubit_state

from .sub_protocols import quantum_anonymous_tranmission, setup_sockets
from .conf import nodes

logger = get_netqasm_logger()


def anonymous_transmission(
    node_name,
    log_config=None,
    sender=False,
    receiver=False,
    phi=None,
    theta=None,
):

    # Setup sockets, epr_sockets and a broadcast_channel needed for the protocol
    sockets = setup_sockets(
        node_name=node_name,
        nodes=nodes,
        log_config=log_config,
    )

    # Initialize the connection to the backend
    conn = NetSquidConnection(
        name=node_name,
        log_config=log_config,
        epr_sockets=sockets.epr_sockets,
    )
    with conn:
        if sender:
            # Prepare the qubit to teleport
            qubit = Qubit(conn)
            set_qubit_state(qubit=qubit, phi=phi, theta=theta)
        else:
            qubit = None
        q = quantum_anonymous_tranmission(
            conn=conn,
            sockets=sockets,
            num_nodes=len(nodes),
            sender=sender,
            receiver=receiver,
            qubit=qubit,
        )
        if receiver:
            dm = get_qubit_state(q)
            output = {"qubit_state": dm.tolist()}
        else:
            output = None
    return output