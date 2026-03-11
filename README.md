# Platform CLI

Command line interface for the Deterministic AI Governance Platform.

## Installation

pip install platform-cli

or

pip install -e .

## Authentication

platform login

## Example Usage

Submit intent:

platform intent create intent.yaml

Inspect plan:

platform plan show <plan_id>

Run execution:

platform execution start <plan_id>

List artifacts:

platform artifact list
