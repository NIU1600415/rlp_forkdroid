import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Header from "../components/Header";
import useMainLogic from "./useMainLogic";

export default function Main() {
  const { state, requestTargetCalibration, requestMachineStart, requestMachineStop } = useMainLogic();

  return (
    <>
      <Header />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <p>{JSON.stringify(state || "LOADING...")}</p>
          <Button onClick={requestTargetCalibration}>Calibrate target</Button>
          <Button onClick={requestMachineStart}>Start</Button>
          <Button onClick={requestMachineStop}>Stop</Button>
        </Box>
      </Container>
    </>
  );
}
