name: API Section Update Report
description: Report incorrect or outdated parts of the API and suggest updated details
title: "[API Fix] <short summary of the issue>"
labels: [api, bug, documentation]
body:
  - type: markdown
    attributes:
      value: |
        ## API Section Correction Report

        Use this form to report incorrect, outdated, or misleading sections of the API and provide a corrected or updated version.

  - type: input
    id: section
    attributes:
      label: Affected Section
      description: What part of the API is incorrect or outdated?
      placeholder: e.g. `POST /user/register` response format
    validations:
      required: true

  - type: textarea
    id: current
    attributes:
      label: Current Behavior / Structure
      description: Paste or describe the current behavior or structure as it exists now.
      placeholder: |
        e.g.
        ```
        {
          "username": "string",
          "email": "string"
        }
        ```
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Correct or Updated Behavior
      description: Provide the correct version or structure you expect.
      placeholder: |
        e.g.
        ```
        {
          "username": "string",
          "email": "string",
          "user_id": "uuid"
        }
        ```
    validations:
      required: true

  - type: textarea
    id: reason
    attributes:
      label: Why This Update is Needed
      description: Briefly explain why the change is important or necessary.
      placeholder: e.g. The `user_id` is required to fetch data in other requests.
    validations:
      required: true

  - type: checkboxes
    id: impact
    attributes:
      label: Impact of the Inaccuracy
      description: What impact does the incorrect section have?
      options:
        - label: Causes client-side bugs
        - label: Causes data inconsistency
        - label: Causes confusion during integration
        - label: Minor documentation mismatch
        - label: Other (explain below)
    validations:
      required: true

  - type: textarea
    id: notes
    attributes:
      label: Additional Notes or References
      description: Include any logs, docs, links, or context if needed
      placeholder: Optional
    validations:
      required: false
