from phys.phys_motion import PhysMotion
from phys.phys_vision import PhysVision
from client_messaging.client_messaging import ClientMessaging
from state_machine.state_machine import StateMachine

if __name__ == "__main__":
    client_messaging = ClientMessaging()
    motion = PhysMotion()
    vision = PhysVision()

    state_machine = StateMachine(client_messaging, motion, vision)

    state_machine.begin()
