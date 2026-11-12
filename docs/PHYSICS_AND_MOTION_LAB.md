# Physics and motion model boundary

The ecosystem exposes two complementary reference layers:

- **SAMBU:** pure Python equations for force, energy, spring-damper response, constant-acceleration kinematics, first-order thermal/RC response and quintic motion samples.
- **ReaperCripple:** portable C11 quintic trajectory validation and sampling for embedded motion planning.

Both models are deterministic and bounded. They return desired numerical samples, not hardware commands.

## Contract

All models must state units and assumptions, reject invalid domains and non-finite values, and expose limits before motion is accepted. Animatronic joints require explicit position, velocity and acceleration envelopes. Platform drivers and sensor feedback are separate adapters that own interlocks, watchdogs, calibration and emergency stop.

## Animation

Animation is a time-indexed view of a validated trajectory. Renderers choose a sampling cadence and may interpolate only within the validated time span. Reduced-motion preferences and a visible paused state belong to the UI layer. UI animation never proves the physical actuator moved.

## Physical evidence

A hardware result requires timestamped sensor feedback, sensor identity/calibration, units, board revision and a traceable test. A mathematical simulation is a model result, not measurement evidence.
