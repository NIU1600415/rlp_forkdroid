interface CalibrationData {
  lower: string;
  upper: string;
}

interface State {
  machine_state: 'IDLE' | 'CALIBRATING' | 'RUNNING';
  calibrated: boolean;
  calibration_data: {
    target: CalibrationData;
    destination: CalibrationData;
  };
}

type StateCommand = 'CALIB_DATA_TARGET' | 'CALIB_DATA_DESTINATION' | 'START_MACHINE' | 'STOP_MACHINE';

type MessageFromMachineTypes = 'CALIB_DATA_TARGET' | 'CALIB_DATA_DESTINATION' | 'START_MACHINE' | 'STOP_MACHINE';

interface MessageFromMachine {
  type: MessageFromMachineTypes;
  data: CalibrationData;
}

type MessageToMachineTypes = 'CALIBRATE_TARGET' | 'CALIBRATE_DESTINATION' | 'START_MACHINE' | 'STOP_MACHINE';

interface MessageToMachine {
  type: MessageToMachineTypes;
  data: number | null;
}

export class StateService {
  static instance: StateService;
  state: State = {
    machine_state: 'IDLE',
    calibrated: false,
    calibration_data: {
      target: {
        upper: '#FFFFFF',
        lower: '#FFFFFF',
      },
      destination: {
        upper: '#FFFFFF',
        lower: '#FFFFFF',
      },
    },
  };
  messagesToMachineFIFO: MessageToMachine[] = [];

  constructor() {
    // Singleton pattern
    if (StateService.instance) {
      return StateService.instance;
    }
    StateService.instance = this;
  }

  // Process command from UI
  processStateCommand(command: StateCommand) {
    if (command === 'CALIB_DATA_TARGET') {
      this.messagesToMachineFIFO.push({
        type: 'CALIBRATE_TARGET',
        data: null,
      });

      this.state.calibrated = false;
    } else if (command === 'CALIB_DATA_DESTINATION') {
      this.messagesToMachineFIFO.push({
        type: 'CALIBRATE_DESTINATION',
        data: null,
      });

      this.state.calibrated = false;
    } else if (command === 'START_MACHINE') {
      this.messagesToMachineFIFO.push({
        type: 'START_MACHINE',
        data: null,
      });
    } else if (command === 'STOP_MACHINE') {
      this.messagesToMachineFIFO.push({
        type: 'STOP_MACHINE',
        data: null,
      });
      this.state.machine_state = 'IDLE';
    }
  }

  // Process message from machine
  processMachineMessage(message: MessageFromMachine) {
    console.log('Procesing:', message);
    if (message.type === 'CALIB_DATA_TARGET') {
      this.state.calibration_data.target = message.data;
    } else if (message.type === 'CALIB_DATA_DESTINATION') {
      this.state.calibration_data.destination = message.data;
    } else if (message.type === 'START_MACHINE') {
      this.state.machine_state = 'RUNNING';
    } else if (message.type === 'STOP_MACHINE') {
      this.state.machine_state = 'IDLE';
    }
    if (
      this.state.calibration_data.destination.lower !== '#FFFFFF' &&
      this.state.calibration_data.target.lower !== '#FFFFFF'
    ) {
      this.state.calibrated = true;
    }
  }

  // Read up to 1 pending message for machine
  readMachineFIFO(): MessageToMachine | undefined {
    return this.messagesToMachineFIFO.shift();
  }

  // Get machine state
  getState() {
    return this.state;
  }
}
