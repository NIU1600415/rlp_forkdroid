import Api from "./_api";

interface CalibrationData {
  lower: string;
  upper: string;
}

export interface State {
  machine_state: "IDLE" | "CALIBRATING" | "RUNNING"; // TODO
  calibrated: boolean;
  calibration_data: {
    target: CalibrationData;
    destination: CalibrationData;
  };
}

type MachineCommand = "CALIB_DATA_TARGET" | "CALIB_DATA_DESTINATION" | "START_MACHINE" | "STOP_MACHINE";

const machineApi = {
  getState: () => Api.get<State>("/state"),
  sendCommand: (command: MachineCommand) =>
    Api.post("/state/command", { command }),
};

export default machineApi;
