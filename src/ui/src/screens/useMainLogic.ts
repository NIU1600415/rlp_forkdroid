import { useEffect, useState } from "react";
import machineApi, { type State } from "../api/machineApi";

export default function useMainLogic() {
  const [machineState, setMachineState] = useState<State>();

  useEffect(() => {
    machineApi.getState().then((response) => setMachineState(response));
  }, []);

  const requestTargetCalibration = () =>
    machineApi.sendCommand("CALIB_DATA_TARGET");

  return {
    state: machineState,
    requestTargetCalibration,
  };
}
