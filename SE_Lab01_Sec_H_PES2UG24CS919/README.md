# SE Lab 1 - Requirements Engineering and UML Use Case Modelling

PES University, Department of CSE
Aniyath Amrita Pradeep, PES2UG24CS919, Section H

## Problem Statement

**Community Lost & Found Matching Network** (Domain: Media, Events & Community)

A platform where community members report lost or found items, get automatically matched against
opposite reports through category, location, and keyword similarity, and go through an identity
verification step before contact details are exchanged. A community admin moderates flagged
listings and keeps the platform trustworthy.

**Actors:** Finder / Owner, Community Admin

## Contents

| File | Description |
|---|---|
| `SE_Lab1_Requirements_UML_PES2UG24CS919.pdf` | Full submission: problem overview, 5 functional requirements, 2 non-functional requirements, UML use case diagram, and a detailed flow specification for the Claim Item use case |
| `usecase_diagram.png` | Standalone export of the UML use case diagram used in the PDF |

## Requirements Summary

**Functional**
- FR-001 Report a lost or found item with photos
- FR-002 Generate ranked match suggestions across listings
- FR-003 Claim a match through an identity verification step
- FR-004 Admin moderation of flagged listings
- FR-005 Notify users on new matches and claim status changes

**Non-Functional**
- NFR-001 Match queries return in under 2 seconds at p95 across 500,000 listings
- NFR-002 Contact details stay hidden until verification and are encrypted at rest

## Use Case Diagram

The diagram models both actors against ten use cases, with two `<<include>>` relationships tied to
mandatory sub-steps (photo upload, identity verification, match notification) and one `<<extend>>`
relationship for the optional flag-while-browsing path.

## Use Case Flow Specification

The PDF includes a full preconditions, postconditions, main success scenario, and alternate flow
writeup for **Claim Item**, the core use case that ties FR-002, FR-003, and FR-005 together.

## Tools Used

Requirements and flow specification drafted directly. Diagram built as a vector illustration
following standard UML use case notation (actors, system boundary, association, include, extend).
