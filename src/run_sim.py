from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from sim.sim_motion import SimMotion
from sim.sim_vision import SimVision
from client_messaging.client_messaging import ClientMessaging
from state_machine.state_machine import StateMachine

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.require("sim")

    client_messaging = ClientMessaging()
    motion = SimMotion(sim)
    vision = SimVision(sim)

    state_machine = StateMachine(client_messaging, motion, vision)

    state_machine.begin()
