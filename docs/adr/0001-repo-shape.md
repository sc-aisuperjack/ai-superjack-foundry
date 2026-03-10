# ADR 0001: Modular monorepo scaffold

## Status
Accepted

## Context
The project needs to demonstrate multiple platform concepts in one public repository without collapsing into a tangled single-file demo.

## Decision
Use a modular monorepo with app entrypoints, service modules, shared contracts, and test suites.

## Consequences
The repo is slightly larger up front, but easier to reason about and extend.
