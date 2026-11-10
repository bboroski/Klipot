#ifndef NUN_MESH_ENVELOPE_H
#define NUN_MESH_ENVELOPE_H
/* Portable wire-neutral envelope. This is a reference ABI, not a serializer.
 * Fields are host-endian until a transport defines canonical encoding. */
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define NUN_MESH_ABI_VERSION UINT16_C(1)
#define NUN_MESH_ENVELOPE_VERSION UINT16_C(1)
typedef enum nun_mesh_record_kind {
 NUN_MESH_RECORD_CAPABILITY=1, NUN_MESH_RECORD_HEALTH=2,
 NUN_MESH_RECORD_LIFECYCLE=3, NUN_MESH_RECORD_TELEMETRY=4,
 NUN_MESH_RECORD_DIAGNOSTIC=5, NUN_MESH_RECORD_MANUFACTURING=6
} nun_mesh_record_kind_t;
typedef struct nun_mesh_envelope {
 uint16_t version; uint16_t kind; uint32_t struct_size;
 uint32_t producer_id; uint32_t sequence; uint64_t monotonic_ticks;
 uint32_t flags; int32_t status;
} nun_mesh_envelope_t;
typedef struct nun_mesh_capabilities {
 uint16_t abi_version; uint16_t struct_size;
 uint32_t provided; uint32_t required; uint32_t optional;
} nun_mesh_capabilities_t;
static inline int nun_mesh_envelope_valid(const nun_mesh_envelope_t *r) {
 return r != 0 && r->version == NUN_MESH_ENVELOPE_VERSION &&
 r->struct_size >= (uint32_t)sizeof(nun_mesh_envelope_t) &&
 r->kind >= NUN_MESH_RECORD_CAPABILITY &&
 r->kind <= NUN_MESH_RECORD_MANUFACTURING;
}
static inline int nun_mesh_capabilities_valid(const nun_mesh_capabilities_t *c) {
 return c != 0 && c->abi_version == NUN_MESH_ABI_VERSION &&
 c->struct_size >= (uint16_t)sizeof(nun_mesh_capabilities_t) &&
 (c->required & ~c->provided) == 0u;
}
#ifdef __cplusplus
}
#endif
#endif
