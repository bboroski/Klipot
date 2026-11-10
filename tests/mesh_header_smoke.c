#include <stdint.h>
#include "mesh-envelope.h"
#include "kloz/platform.h"
#include "co/saintsi_bridge.h"
#include "saintsi/kloz_clock.h"
#include "reaper_kloz_clock.h"
#include "reaper_saintsi_bridge.h"

/* Compiled with all repository include roots; this is a header/API smoke test.
 * It intentionally does not link or execute hardware-facing callbacks. */
int nun_mesh_header_smoke(
    const nun_mesh_envelope_t *record,
    const nun_mesh_capabilities_t *capabilities,
    const saintsi_kloz_clock_t *clock,
    const co_runtime_t *co_runtime,
    const reaper_runtime_t *reaper_runtime,
    saintsi_supervisor_t *supervisor,
    reaper_kloz_clock_t *reaper_clock)
{
    uint32_t now = 0u;
    int32_t co_result;
    int32_t reaper_result;
    uint64_t monotonic_us;

    if (!nun_mesh_envelope_valid(record) ||
        !nun_mesh_capabilities_valid(capabilities)) {
        return -1;
    }
    (void)saintsi_kloz_read_now32(clock, &now);
    co_result = co_saintsi_refresh_runtime(co_runtime, supervisor, 1u, now);
    reaper_result = reaper_saintsi_refresh_runtime(
        reaper_runtime, supervisor, 2u, now);
    monotonic_us = reaper_kloz_monotonic_us(reaper_clock);
    (void)co_result;
    (void)reaper_result;
    (void)monotonic_us;
    return 0;
}
