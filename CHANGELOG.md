# Changelog

All notable changes to this project will be documented in this file (beginning with version 0.2.2).

## [Unreleased]

Nothing to see yet.

## [0.2.2 HOTFIX] - 2023-02-04

### Fixed

 - Fixed issue where program would throw an error if the NEOCP json file did not exist on the system (due to array generator function being called too early).

### Changed

 - Moved array column names to conf YAML file to fix function call order issue.
 - Renamed changelog.md to CHANGELOG.md

## [0.2.2] - 2023-02-03

### Added

 - Added `-c` option to allow isolation of specific columns in `-l` printout.
 - Added changelog to track updates.

### Changed

 - Moved some configurations to a separate YAML file. 
 - Updated --version output.
 - Updated README