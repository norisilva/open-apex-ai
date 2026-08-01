# Changelog

## [2.0.0] - 2026-08-01 - OpenApex AI
### Added
- **Rebranding to OpenApex AI**: Official name change focusing on AI and open-source telemetry.
- **Smart HUD (Overlays)**:
  - Dynamic overlay displaying live car setups when on track.
  - Tyre Telemetry Overlay featuring mathematical wear predictions (pit window estimates).
- **Internationalization (i18n)**: Dynamic support for 6 languages (English, Portuguese, Spanish, German, Hindi, Arabic).
- **Customization**:
  - New Cyberpunk-themed Settings Interface.
  - Option to customize the Tyre HUD hotkey directly from the UI.

### Changed
- Major refactor on overlay injection and window capture logic, completely eliminating OS focus-stealing issues that previously interrupted gameplay.
- Build scripts and official repository updated to `open-apex-ai`.

## [1.1.0] - 2026-08-01
### Added
- New mathematical prediction module and Tyre wear overlay (`TyrePredictor` and `TyreOverlayApp`).

### Fixed
- Removed dead and broken code (`from_bytes`) inside `process_packet` that referenced non-existent objects.
- Fixed structural issue in F1 24/25 UDP packet reading: `m_currentLapNum` is now correctly read from byte 33 (and `m_lapDistance` from byte 20). This resolves a bug where the tyre overlay was stuck on "Waiting for full lap..." due to missed lap transitions.
