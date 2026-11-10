#![no_std]
//! Small architecture-aware primitives for the hardware boundary.
//! This crate intentionally does not discover devices or map MMIO addresses.

use core::sync::atomic::{compiler_fence, fence, Ordering};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Architecture {
    X86,
    Arm,
    RiscV,
    Avr,
    Other,
}

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub const BUILD_ARCH: Architecture = Architecture::X86;
#[cfg(any(target_arch = "arm", target_arch = "aarch64"))]
pub const BUILD_ARCH: Architecture = Architecture::Arm;
#[cfg(any(target_arch = "riscv32", target_arch = "riscv64"))]
pub const BUILD_ARCH: Architecture = Architecture::RiscV;
#[cfg(target_arch = "avr")]
pub const BUILD_ARCH: Architecture = Architecture::Avr;
#[cfg(not(any(
    target_arch = "x86",
    target_arch = "x86_64",
    target_arch = "arm",
    target_arch = "aarch64",
    target_arch = "riscv32",
    target_arch = "riscv64",
    target_arch = "avr"
)))]
pub const BUILD_ARCH: Architecture = Architecture::Other;

/// Hint to the processor that the current thread is in a spin-wait loop.
/// This is a scheduling/power hint, not a synchronization primitive.
#[inline(always)]
pub fn cpu_relax() {
    #[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
    unsafe {
        core::arch::asm!("pause", options(nomem, nostack, preserves_flags));
    }

    #[cfg(any(target_arch = "arm", target_arch = "aarch64"))]
    unsafe {
        core::arch::asm!("yield", options(nomem, nostack, preserves_flags));
    }

    #[cfg(any(target_arch = "riscv32", target_arch = "riscv64"))]
    unsafe {
        core::arch::asm!("nop", options(nomem, nostack));
    }

    #[cfg(not(any(
        target_arch = "x86",
        target_arch = "x86_64",
        target_arch = "arm",
        target_arch = "aarch64",
        target_arch = "riscv32",
        target_arch = "riscv64"
    )))]
    core::hint::spin_loop();
}

/// Emits compiler and hardware ordering fences.
/// A fence does not make a data race valid and does not replace a lock.
#[inline]
pub fn full_memory_fence() {
    compiler_fence(Ordering::SeqCst);
    fence(Ordering::SeqCst);
    compiler_fence(Ordering::SeqCst);
}

/// Read a 32-bit memory-mapped register.
///
/// # Safety
/// address must be non-null, correctly aligned, mapped for reads, and point
/// to a register whose access semantics permit a 32-bit volatile read. The
/// caller must establish the device-specific ordering and lifetime rules.
#[inline]
pub unsafe fn mmio_read32(address: *const u32) -> u32 {
    // SAFETY: the caller guarantees the MMIO pointer contract above.
    unsafe { core::ptr::read_volatile(address) }
}

/// Write a 32-bit memory-mapped register.
///
/// # Safety
/// address must be non-null, correctly aligned, mapped for writes, and point
/// to a register whose access semantics permit a 32-bit volatile write. The
/// caller must establish the device-specific ordering and lifetime rules.
#[inline]
pub unsafe fn mmio_write32(address: *mut u32, value: u32) {
    // SAFETY: the caller guarantees the MMIO pointer contract above.
    unsafe { core::ptr::write_volatile(address, value) }
}

/// Read an 8-bit memory-mapped register.
///
/// # Safety
/// The pointer must satisfy the device-specific MMIO mapping and access rules.
#[inline]
pub unsafe fn mmio_read8(address: *const u8) -> u8 {
    // SAFETY: the caller guarantees the MMIO pointer contract above.
    unsafe { core::ptr::read_volatile(address) }
}

/// Write an 8-bit memory-mapped register.
///
/// # Safety
/// The pointer must satisfy the device-specific MMIO mapping and access rules.
#[inline]
pub unsafe fn mmio_write8(address: *mut u8, value: u8) {
    // SAFETY: the caller guarantees the MMIO pointer contract above.
    unsafe { core::ptr::write_volatile(address, value) }
}
