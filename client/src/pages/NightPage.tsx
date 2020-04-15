import React from "react";
import {
  AppBar,
  Typography,
  Toolbar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Container,
  makeStyles,
  createStyles,
  Theme,
  FormHelperText,
  TextField,
  Button,
} from "@material-ui/core";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    formControl: {
      width: "100%",
      marginBottom: theme.spacing(3),
    },
  })
);

function NightPage() {
  const classes = useStyles();

  const [iso, setIso] = React.useState(400);
  const [shutterSpeed, setShutterSpeed] = React.useState("1");
  const [fStop, setFStop] = React.useState("F3.5");

  const [delay, setDelay] = React.useState("1");
  const [takes, setTakes] = React.useState("10");

  // Functions
  const takeTestPhoto = () => {
    fetch("http://raspberrypi:8080/capture-preview")
      .then((res) => {
        console.log(res);
      })
      .catch((reason) => {
        alert(reason);
      });
  };

  // The UI
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Night Photography</Typography>
        </Toolbar>
      </AppBar>

      <br />

      <Container>
        <FormControl className={classes.formControl} variant="standard">
          <InputLabel id="select-iso-label">ISO</InputLabel>
          <Select
            labelId="select-iso-label"
            id="select-iso"
            value={iso}
            onChange={(v) => setIso(v.target.value as number)}
          >
            <MenuItem value={100}>100</MenuItem>
            <MenuItem value={200}>200</MenuItem>
            <MenuItem value={400}>400</MenuItem>
            <MenuItem value={800}>800</MenuItem>
            <MenuItem value={1600}>1600</MenuItem>
            <MenuItem value={3200}>3200</MenuItem>
            <MenuItem value={6400}>6400</MenuItem>
            <MenuItem value={12800}>12800</MenuItem>
            <MenuItem value={25600}>25600</MenuItem>
          </Select>
        </FormControl>

        <FormControl className={classes.formControl} variant="standard">
          <InputLabel id="select-shutter-speed-label">Shutter Speed</InputLabel>
          <Select
            labelId="select-shutter-speed-label"
            id="select-shutter-speed"
            value={shutterSpeed}
            onChange={(v) => setShutterSpeed(v.target.value as string)}
          ></Select>
        </FormControl>

        <FormControl className={classes.formControl} variant="standard">
          <InputLabel id="select-f-stop-label">FStop</InputLabel>
          <Select
            labelId="select-f-stop-label"
            id="select-f-stop"
            value={fStop}
            onChange={(v) => setFStop(v.target.value as string)}
          ></Select>
        </FormControl>

        <FormControl className={classes.formControl} variant="standard">
          <TextField
            label="Delay (seconds)"
            id="select-delay"
            value={delay}
            onChange={(v: any) => setDelay(v.target.value as string)}
          />
          <FormHelperText>The delay in-between each photo</FormHelperText>
        </FormControl>

        <FormControl className={classes.formControl}>
          <TextField
            label="Takes"
            id="select-takes"
            value={takes}
            onChange={(v: any) => setTakes(v as string)}
          />
          <FormHelperText>How many photos to take</FormHelperText>
        </FormControl>

        <FormControl className={classes.formControl}>
          <Button variant="contained" color="primary">
            Start
          </Button>
        </FormControl>

        <FormControl className={classes.formControl}>
          <Button variant="outlined" onClick={takeTestPhoto}>
            Take test photo
          </Button>
        </FormControl>
      </Container>
    </>
  );
}

export default NightPage;
