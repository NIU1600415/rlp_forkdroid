import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Slider from "@mui/material/Slider";
import Header from "../components/Header";
import useMainLogic from "./useMainLogic";

export default function Main() {
  const {
    state,
    amountTargets,
    requestTargetCalibration,
    requestMachineStart,
    requestMachineStop,
    onTargetSliderChange,
  } = useMainLogic();

  return (
    <>
      <Header />
      <Container maxWidth="sm">
        <Box sx={{ my: 4 }}>
          <p>Calibration status: Calibrated</p>
          <Button variant="contained" onClick={requestTargetCalibration}>
            Calibrate target
          </Button>
          &nbsp;&nbsp;&nbsp;
          <Button variant="contained" onClick={requestTargetCalibration}>
            Calibrate destination
          </Button>
          <br />
          <br />
          <p>State: {state?.machine_state}</p>
          <Box width={250} mb={2}>
            <Slider
              defaultValue={2}
              step={1}
              min={1}
              max={10}
              onChange={onTargetSliderChange}
            />
            <span>Amount of targets: {amountTargets}</span>
          </Box>
          <Button variant="contained" onClick={requestMachineStart}>
            Start
          </Button>
          &nbsp;&nbsp;&nbsp;
          <Button variant="contained" onClick={requestMachineStop}>
            Stop
          </Button>
        </Box>
      </Container>
    </>
  );
}
