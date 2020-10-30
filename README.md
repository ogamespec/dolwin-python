# dolwin-python

Python scripts for the GameCube Dolwin emulator.

This section contains examples of interaction with the emulator through python scripts.

Dolwin contains a custom debug and service interface called JDI (Json Debug Interface). All scripts interact with the emulator through this interface (see jdi.py).

JDI description: https://github.com/ogamespec/dolwin-docs/blob/master/EMU/JsonDebugInterface.md

## Data

This folder contains important files that the DolwinEmu core uses.

## DolwinEmuForPlayground

The Dolwin core itself, in a version with Null backends (no graphics, sound, etc.). Used to test emulation of Gekko processor, Flipper chipset or DSP.

This DLL is used for binding with python scripts, for further experiments with the emulator.

Sorry for the binary format (DLL), but it's easier for a quick start. If you are interested in building DolwinPlayground yourself, you can do this in the main repository (https://github.com/ogamespec/dolwin, DolwinPlayground_VS2019.sln).

## pong.dol

An old friend of the emulator is the PONG demo by DesktopMan. Ideal for testing.

## Example command line

```
py -3 dolwin.py pong.dol
```

With autorun script:

```
py -3 dolwin.py pong.dol autorun.txt
```
