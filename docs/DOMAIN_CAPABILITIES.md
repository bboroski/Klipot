# Domain Capabilities

Klipot converts the supplied cycle, preservation, evolutionary and synthetic-intelligence
vocabulary into deterministic control-plane planning helpers.

## Implemented functions

| Engineering concept | Function |
|---|---|
| Harvest cycle / hibernation cycle | `advance_cycle(state, event)` — explicit lifecycle graph |
| Core reconstruction / recovery snapshot | `plan_recovery(...)` — bounded recommendation for resume, hold, rollback or escalation |
| Evolutionary guidance / genetic drift | `evaluate_evolution(...)` — evidence and rollback gate |
| Relay network / hive-network sequence | `validate_event_sequences(...)` — per-producer monotonic event validation |
| Collective consciousness / Geth consensus | Use the SAMBU consensus adapter or a project-specific quorum provider; the portal does not implement network transport |

## Verification

```sh
python -m unittest tests.test_domain_capabilities
```

All operations are deterministic planning functions. They do not execute a deployment,
perform a rollback, write firmware, communicate with devices, or authorize privileged actions.
