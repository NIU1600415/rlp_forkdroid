import { useEffect, useState } from "react";
import machineApi, { type State } from "../api/machineApi";

export default function useMainLogic() {
  const [machineState, setMachineState] = useState<State>();
  const [amountTargets, setAmountTargets] = useState(1);

  useEffect(() => {
    machineApi.getState().then((response) => setMachineState(response));
  }, []);

  const requestTargetCalibration = () =>
    machineApi.sendCommand("CALIB_DATA_TARGET");
  const requestMachineStart = () => machineApi.sendCommand("START_MACHINE");
  const requestMachineStop = () => machineApi.sendCommand("STOP_MACHINE");

  const onTargetSliderChange = (_e: Event, newValue: number | number[]) => {
    setAmountTargets(newValue as number);
  };

  return {
    state: machineState,
    amountTargets,
    requestTargetCalibration,
    requestMachineStart,
    requestMachineStop,
    onTargetSliderChange,
  };
}
