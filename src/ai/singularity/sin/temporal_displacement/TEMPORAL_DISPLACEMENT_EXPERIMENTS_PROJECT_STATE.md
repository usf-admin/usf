# EXPERIMENTS_PROJECT_STATE.md — Temporal-Displacement Experiments

**Status:** Current experimental project state

**Source authority:**
- `TemporalDisplacement.sin`
- `TMTE.sin`
- `temporal-displacement-demo.sin`

The uploaded `.sin` source files are the current implementation authority for this project. This document records the current experimental architecture, implemented behavior, and the semantic decisions established during the design discussion. Where a design decision is not yet represented in the uploaded implementation, it is identified explicitly rather than presented as implemented fact.

---

## 1. Project Scope

This project is the experimental context for designing, executing, documenting, and analyzing temporal-displacement experiments.

The three project layers remain distinct:

```text
TAP-001
What must the protocol mean?

SIN-001
What must the language/runtime mean?

Experiments
What did we actually do, observe, and learn?
```

This project state therefore records the experimental implementation and the semantic decisions currently being exercised by the experiments. It is not the authoritative definition of TAP-001 or SIN-001.

---

# 2. Current Source Baseline

## `TemporalDisplacement.sin`

The current source identifies itself as the **Version 0.4 semantic model and interface definition**.

The current experimental architecture now separates the logical atomic-transition transaction from the technology-dependent physical mechanism. It defines the following internal behaviors:

```text
validate_current_state(observer)
validate_proposed_displacement(observer, target_state)
physical_transition(source_state, destination_state)
perform_atomic_transition(observer, target_state)
```

The public operation is:

```text
displace(observer, target_state)
```

The source also defines:

```text
ValidationResult
PhysicalTransitionResult
TransitionResult
DisplacementResult
```

`PhysicalTransitionResult` is the explicit technology-boundary result. Its fields are:

```text
available
successful
failure_reason
evidence
```

The `evidence` field is intentionally untyped and technology-defined. The TemporalDisplacement layer treats it as opaque mechanism-provided evidence.

`TransitionResult` now also contains:

```text
physical_transition_result
```

This preserves the logical transition result while exposing the underlying mechanism result to callers.

## `temporal-displacement-demo.sin`

The demonstration source initializes an Observer, establishes home and recovery checkpoints, constructs destination states through `observer.state(...)`, validates proposed transitions, invokes TemporalDisplacement, and provides recovery through the Observer's recovery checkpoint.

The demonstration explicitly exercises negative temporal displacement by subtracting one day from the current epoch time and positive temporal displacement by adding one day.

## `TMTE.sin`

`TMTE.sin` is now the current experimental interface definition for the **Temporal Metric Translation Engine (TMTE)**.

TMTE is defined as the hypothetical physical mechanism responsible for producing, controlling, and terminating a genuine temporal-spatial transition between a defined source spacetime state and a defined destination spacetime state.

The TMTE is explicitly a **physical-system boundary**, not a software operation. It must establish a physically traversable connection or equivalent transition geometry rather than merely changing the Observer's recorded state.

The current `TMTE.sin` interface exposes:

```text
execute_transition(observer, source_state, destination_state)
    → TMTE.DeviceResult
```

The mechanism-level result is:

```text
DeviceResult
    available
    successful
    failure_reason
    evidence
```

The current TMTE execution architecture defines the following supporting external operations:

```text
capture_source_state(...)
verify_destination_state(...)
establish_chronometric_references(...)
calculate_transition_geometry(...)
establish_field_configuration(...)
verify_transition_geometry(...)
establish_state_transfer_envelope(...)
open_transition_channel(...)
transfer_observer(...)
verify_destination_establishment(...)
verify_causal_transition(...)
verify_conservation_accounting(...)
perform_independent_verification(...)
terminate_transition(...)
preserve_transition_evidence(...)
```

These functions are physical-system boundary operations. They are declared as external because no physical TMTE implementation currently exists in the experiment.

The current `execute_transition(...)` sequence is:

```text
capture source state
        ↓
validate destination state
        ↓
establish chronometric references
        ↓
calculate transition geometry
        ↓
establish field configuration
        ↓
verify transition geometry
        ↓
establish state-transfer envelope
        ↓
open transition channel
        ↓
transfer Observer
        ↓
verify destination establishment
        ↓
verify causal transition
        ↓
verify conservation accounting
        ↓
independent verification
        ↓
terminate transition
        ↓
preserve transition evidence
        ↓
DeviceResult
```

A successful TMTE result is therefore not defined as merely "the mechanism changed the Observer state." The execution contract requires physical transition evidence and independent verification stages before `successful = true` is reported.

The TMTE interface remains implementation-agnostic. No specific wormhole, negative-energy, quantum-resonator, metamaterial, or other physical implementation is currently asserted by this project state.

---

# 4. Observer State Model

The Observer state is a complete representation of the Observer at a particular point in spacetime.

The current state model consists of:

```text
reference_entity
et
x
y
z
```

The `reference_entity` provides the reference object or coordinate context needed to interpret the spatial coordinates.

The state is treated as a complete state rather than as independently mutable coordinate fields for purposes of temporal displacement.

The fundamental displacement model is:

```text
source_state
     ↓
atomic transition
     ↓
destination_state
```

A successful transition places the Observer in the complete destination state. A failed transition leaves the Observer in the complete source state.

---

# 5. `defined(E)` Presence Semantics

## Status

`defined(E)` is a proposed SIN-001 built-in presence predicate and is adopted as the presence-aware semantic basis of the current experiment.

## Semantics

`defined(E)` evaluates `E` using presence-aware resolution.

If any binding or member required to resolve `E` is absent, the result is `false`.

If `E` resolves to `null`, the result is `false`.

If `E` resolves to an explicitly present value, the result is `true`.

Therefore explicitly present values including:

```text
0
negative numbers
false
""
```

are present.

The predicate tests **presence**, not:

- truthiness,
- nonzero-ness,
- nonemptiness,
- validity,
- or semantic correctness.

The intended runtime distinction is:

```text
MISSING
NULL
VALUE
```

Recursive member resolution follows the same semantics. For example:

```text
missing observer              → defined(observer)       == false
missing observer.et           → defined(observer.et)   == false
observer.et = null            → defined(observer.et)   == false
observer.et = 0               → defined(observer.et)   == true
observer.x = 0                → defined(observer.x)    == true
```

This is important because zero-valued coordinates and other zero-valued state members must not be rejected as missing.

---

# 6. Current Observer Validation

The canonical current-state validation operation is:

```sin
TemporalDisplacement.validate_current_state(observer)
```

It is declared internal to TemporalDisplacement.

Its contract is to determine whether the Observer currently contains a complete and logically valid state under the current state model.

Validation is explicitly non-mutating.

## Implemented validation layers

The current source checks:

1. Observer existence.
2. Observer state existence.
3. Presence of:
   - `et`
   - `reference_entity`
   - `x`
   - `y`
   - `z`
4. Final non-mutation integrity.

The source uses `defined(...)` for state-member presence.

The validation captures the current state before validation and compares the Observer's state against that captured state before returning.

## Important source-level detail

Negative `et` values are explicitly valid. `et` is a temporal coordinate whose domain includes negative, zero, and positive values.

Therefore `validate_current_state()` requires `et` to be present, but imposes no non-negative constraint on its value. A negative `et` is not an invalid state and must not be treated as an implementation gap or unresolved validation rule.

---

# 7. Proposed Displacement Validation

The canonical proposed-transition validation operation is:

```sin
TemporalDisplacement.validate_proposed_displacement(observer, target_state)
```

It evaluates the proposed source → destination transition without modifying the Observer.

## Validation layers

### Layer 1 — Input and state existence

The implementation checks:

- Observer existence.
- Source state existence.
- Destination state existence.

### Layer 2 — Source-state completeness

The source state must contain:

```text
et
reference_entity
x
y
z
```

Presence is tested using `defined(...)`.

### Layer 3 — Destination-state completeness

The destination state must contain:

```text
et
reference_entity
x
y
z
```

A destination is a complete Observer state, not merely a set of coordinate mutations.

### Layer 4 — Reference consistency

The current implementation requires:

```text
source_state.reference_entity == target_state.reference_entity
```

A differing reference entity is rejected because the current experimental model does not define cross-reference-frame transformation semantics as part of one temporal-displacement transition.

### Layer 5 — Displacement validity

An identical source and destination state is rejected as zero displacement.

Negative temporal displacement is explicitly permitted.

Therefore:

```text
target_state.et < source_state.et
```

is not itself a validation failure.

### Non-mutation

The Observer state is compared with the source state after validation. A change during validation causes validation to fail.

---

# 8. Reference-Entity Semantics

A central decision has been refined during the current design discussion.

The `reference_entity` is part of the complete Observer state and gives meaning to the spatial coordinates.

## During an individual displacement

The reference entity is invariant across the transition:

```text
source.reference_entity == target.reference_entity
```

A temporal displacement therefore changes the Observer's temporal/spatial state **within the reference context used by that transition**.

Cross-reference-frame transformation is not currently defined.

## After successful displacement

The Observer may intentionally establish a different reference entity as a separate state operation.

This is not itself a temporal displacement.

The intended semantic rule is:

> The reference entity must remain consistent throughout an individual temporal-displacement transition, but the Observer may intentionally change its reference entity after successful displacement as a separate state operation.

This permits an Observer to adopt a more accurate reference entity, or a completely different reference entity, after arrival.

The danger is therefore not that a reference entity ever changes. The dangerous condition is an unexpected or inconsistent reference-entity change that is not an intentional separate state operation.

---

# 9. `observer.state(...)` Semantics

The current experiment uses:

```sin
self.state(
    reference_entity=gc_milky_way,
    et=Time.now.et,
    x=Location.4d.x(Location.here.galactic_coordinates),
    y=Location.4d.y(Location.here.galactic_coordinates),
    z=Location.4d.z(Location.here.galactic_coordinates)
);
```

The established semantic meaning is:

> `observer.state(...)` constructs and establishes a complete Observer state from the supplied state components. It does not itself constitute temporal displacement or authorize temporal displacement.

For destination construction, the experimental helper uses:

```sin
ret observer.state(
    observer.reference_entity,
    target_et,
    target_x,
    target_y,
    target_z
);
```

Thus destination-state construction explicitly supplies the Observer's current reference entity together with the target temporal and spatial coordinates.

This keeps state construction owned by the Observer rather than inventing a separate `TemporalDisplacement.state(...)` constructor.

## Important distinction

The following concepts remain distinct:

```text
observer.state
    → current state

observer.state(...)
    → construct/establish a complete state

TemporalDisplacement.validate_proposed_displacement(...)
    → validate a proposed transition

TemporalDisplacement.displace(...)
    → execute the displacement operation
```

State construction does not authorize displacement.

---

# 10. Destination-State Construction

The experimental `destination_state(...)` helper constructs a complete destination state before displacement.

Its documented semantics are:

- destination is a complete Observer state;
- construction occurs before displacement;
- coordinate-by-coordinate mutation is not the displacement mechanism;
- construction does not establish validity;
- construction does not authorize displacement;
- the destination must be evaluated before displacement;
- the Observer remains the final Authorizer.

The current helper delegates construction to:

```sin
observer.state(
    observer.reference_entity,
    target_et,
    target_x,
    target_y,
    target_z
)
```

Errors are passed through `framework.HandleError(...)` and a failed construction is not represented as a successfully constructed valid destination.

---

# 11. Verification, Validation, Authorization, and Execution

These are intentionally distinct concepts.

## Construction

Constructs the proposed destination state.

## Verification

Provides the evidence, assumptions, inference, uncertainty, and other justification relevant to whether a state or transition can be established as valid.

## Validation

Evaluates the logical constraints represented by the current experimental model.

## Authorization

The Observer is the final Authorizer for temporal displacement.

## Execution

Performs the atomic transition after the necessary validation and authorization requirements have been satisfied.

The intended conceptual chain is:

```text
construct destination
        ↓
verification / validation
        ↓
Observer authorization
        ↓
atomic execution
```

Neither construction nor validation independently constitutes authorization.

---

# 12. Atomic Transition Model

The atomic transition architecture now separates two responsibilities:

```text
logical atomic transaction
        ↓
perform_atomic_transition(...)
        ↓
physical mechanism boundary
        ↓
physical_transition(...)
```

`physical_transition(source_state, destination_state)` is the technology-dependent boundary. It is responsible for invoking whatever actual physical temporal-displacement mechanism may eventually become available. The current implementation does not invent or simulate such a mechanism.

## `PhysicalTransitionResult`

The physical mechanism reports a structured result:

```text
available
successful
failure_reason
evidence
```

The meanings are:

- `available`: an actual physical displacement mechanism was available to invoke;
- `successful`: an available mechanism reports that the requested transition succeeded;
- `failure_reason`: why the mechanism could not complete the transition, or `null` on success;
- `evidence`: mechanism-provided evidence, intentionally untyped and technology-defined.

The required invariant is:

```text
available == false → successful == false
```

The architecture therefore distinguishes three mechanism outcomes:

```text
unavailable
    available = false
    successful = false

available but failed
    available = true
    successful = false

available and successful
    available = true
    successful = true
```

## `perform_atomic_transition(...)`

`perform_atomic_transition(observer, target_state)` is the logical transaction coordinator. It:

1. captures the source state;
2. invokes `physical_transition(...)`;
3. distinguishes mechanism unavailability from mechanism failure and mechanism success;
4. verifies the atomicity contract after the mechanism reports its result; and
5. returns `TransitionResult`.

`TransitionResult` contains:

```text
success
source_state
destination_state
failure_reason
physical_transition_result
```

The physical mechanism result is therefore preserved without making the logical transition result identical to it.

## Atomicity contract

The required Observer-state invariants remain:

```text
success
    → Observer state equals destination_state

failure
    → Observer state equals source_state
```

No intermediate Observer state is exposed. The complete state is transitioned atomically rather than through a sequence of independently visible coordinate mutations.

If a mechanism reports success but the destination state is not established, the logical operation fails with an atomic-transition integrity failure.

If a mechanism reports failure but the source state is not preserved, the logical operation fails with an atomic-transition integrity failure. The implementation does not attempt to simulate physical rollback through ordinary Observer state assignment.

## Current implementation boundary

The current `physical_transition(...)` implementation explicitly reports:

```text
available = false
successful = false
failure_reason = "Temporal displacement mechanism unavailable."
evidence = null
```

It does not modify Observer state. Consequently, the current experiment still does **not** implement physical temporal displacement. It now represents that limitation explicitly as a technology dependency rather than as an abstract placeholder that could be mistaken for a transition mechanism.

---

# 13. `TemporalDisplacement.displace(...)`

The external displacement operation:

```sin
TemporalDisplacement.displace(observer, target_state)
```

performs the logical displacement workflow:

1. Capture the source state.
2. Validate the proposed destination.
3. If validation fails, return a failed `DisplacementResult` without attempting transition.
4. Attempt `perform_atomic_transition(...)`.
5. If transition fails, return a failed `DisplacementResult`.
6. On success, return a successful `DisplacementResult`.

The transition stage is now explicitly composed of the logical transaction coordinator and the physical mechanism boundary described in Section 11.

`DisplacementResult` contains:

```text
success
source_state
destination_state
failure_reason
validation_result
transition_result
```

The result records the outcome and does not itself mutate state.

---

# 14. Recovery Checkpoint

The Observer supports:

```sin
self.set_recovery_checkpoint();
```

and recovery obtains the checkpoint with:

```sin
observer.get_recovery_checkpoint();
```

The recovery checkpoint is an explicitly established return state.

## Persistence

A successful displacement does **not** implicitly replace the recovery checkpoint.

If the Observer moves to a new state and wants that state to become the new recovery point, the Observer must explicitly call:

```sin
self.set_recovery_checkpoint();
```

again.

This is intentional safety behavior.

It means an accidental post-displacement corruption of coordinates or `reference_entity` does not automatically destroy the previously established recovery state.

---

# 15. Recovery Is a New Displacement

The experimental `recover_observer(observer)` operation is explicitly defined as a new atomic displacement.

Its conceptual flow is:

```text
current Observer state
        ↓
retrieve recovery checkpoint
        ↓
validate checkpoint as proposed destination
        ↓
Observer authorization
        ↓
atomic displacement
        ↓
checkpoint state
```

Recovery is **not**:

- rollback,
- undo,
- reversal of the previous displacement event.

A recovery displacement has its own source state, destination state, validation, authorization, and transition result.

A failed recovery must leave the Observer at the state from which recovery was attempted.

The fact that a checkpoint was previously established does not automatically authorize recovery.

---

# 16. Home Checkpoint

The Observer now supports:

```sin
self.set_home_checkpoint();
```

Home is distinct from the recovery checkpoint.

## Home semantics

The home checkpoint is:

- explicitly established;
- independently persistent;
- not automatically changed by temporal displacement;
- not automatically changed by recovery;
- intentionally replaceable by the Observer.

Calling:

```sin
self.set_home_checkpoint();
```

after the first establishment replaces the current home checkpoint with the Observer's current state.

The Observer is therefore free to intentionally move its home location.

Home is persistent, but it is not immutable.

---

# 17. Immutable Internal Origin Checkpoint

A further safety layer has been established as a design decision for the Observer library implementation.

The first successful call to:

```sin
self.set_home_checkpoint();
```

will also establish an internal checkpoint named:

```text
origin_checkpoint
```

## Origin semantics

`origin_checkpoint` is:

- established only on the first successful home establishment;
- immutable thereafter;
- never replaced by subsequent calls to `set_home_checkpoint()`;
- independent of the mutable home checkpoint;
- independent of the mutable recovery checkpoint;
- always available through the Observer library implementation.

The experiment source does not expose or manipulate `origin_checkpoint` directly. Its implementation belongs to the Observer library.

The semantic meaning is:

> The first deliberately established home becomes the Observer's `origin_checkpoint`.

This provides a deepest return state even if the Observer later moves home, changes recovery checkpoints, changes reference entities, or otherwise corrupts its current state.

---

# 18. Return-State Hierarchy

The resulting conceptual safety hierarchy is:

```text
origin_checkpoint
    │
    │ immutable
    │
    ▼
home_checkpoint
    │
    │ explicitly replaceable
    │
    ▼
recovery_checkpoint
    │
    │ explicitly replaceable
    │
    ▼
current_state
```

Home and recovery are independent checkpoints. The hierarchy represents increasing depth of intended recovery, not automatic synchronization between the checkpoints.

The important invariant is that ordinary current-state changes do not silently overwrite the established return anchors.

---

# 19. Initial Experimental State

The current demonstration initializes the Observer as follows:

```sin
self:Observer;

self.state(
    reference_entity=gc_milky_way,
    et=Time.now.et,
    x=Location.4d.x(Location.here.galactic_coordinates),
    y=Location.4d.y(Location.here.galactic_coordinates),
    z=Location.4d.z(Location.here.galactic_coordinates)
);
self.set_home_checkpoint();
self.set_recovery_checkpoint();
```

This establishes the current Observer state using the Milky Way Galactic Center as the initial reference entity and uses the current local galactic-coordinate location for the initial spatial coordinates.

The first home checkpoint therefore establishes the initial home and, under the new Observer-library design, also establishes the immutable internal origin checkpoint.

The recovery checkpoint is then explicitly established at that same initial state.

---

# 20. Current Demonstration Behavior

The demonstration's `main()` currently:

1. Calls `TemporalDisplacement.validate_current_state(self)`.
2. Stops if current-state validation fails.
3. Moves the Observer one day into the past by subtracting `86400` seconds from `self.state.et`.
4. Keeps the spatial coordinates unchanged for that displacement.
5. Waits three hours.
6. Recovers to the recovery checkpoint.
7. Waits ten minutes.
8. Moves the Observer one day into the future by adding `86400` seconds to `self.state.et`.
9. Waits three hours.
10. Recovers to the recovery checkpoint again.

The demonstration therefore explicitly exercises both negative and positive temporal displacement and demonstrates that recovery uses a previously established checkpoint rather than automatically changing the checkpoint after each displacement.

---

# 21. Important Current Implementation Caveats

The project state must distinguish the intended semantic model from what the current source can actually execute.

## Physical transition mechanism remains unavailable

`physical_transition(...)` is now the explicit technology boundary for the physical state transition. The current implementation reports mechanism unavailability rather than simulating physical displacement.

`perform_atomic_transition(...)` implements the logical transaction around that boundary, including mechanism-result handling and atomicity-integrity checks.

Consequently, the source now provides a complete logical execution architecture while the actual physical temporal-displacement mechanism remains unavailable.

## Authorization is part of the semantic contract

The source documentation repeatedly states that the Observer is the final Authorizer, including for recovery. The current experiment source does not yet expose a distinct authorization API in `TemporalDisplacement.sin`.

Therefore authorization is currently a documented semantic requirement rather than a fully represented implementation stage.

## Recovery currently uses the recovery checkpoint

The experiment source explicitly calls `get_recovery_checkpoint()` and proposes that state as a new displacement destination.

The new home/origin semantics are a design decision for the Observer library and are not directly exposed in the current demonstration source beyond `set_home_checkpoint()`.

## Reference-entity reassignment is not yet demonstrated in the uploaded experiment

The semantic decision permits an intentional post-displacement change of `reference_entity`, but the current uploaded demonstration does not itself perform such a reassignment.

The current displacement validator correctly rejects a source/destination reference-entity mismatch within a single displacement. Negative temporal displacement remains explicitly valid.

---

# 22. Established Decisions

The following are current project decisions:

1. An Observer state is a complete state consisting of temporal position, spatial position, and reference context.
2. A destination is represented as a complete Observer state.
3. `observer.state(...)` is the Observer-owned mechanism for constructing/establishing a complete state.
4. Destination construction is distinct from displacement.
5. Destination construction does not authorize displacement.
6. Validation does not mutate Observer state.
7. Validation uses presence semantics through `defined(E)`.
8. Present zero-valued members are valid candidates and are not treated as missing.
9. `et` may be negative, zero, or positive; negative temporal displacement is explicitly permitted.
10. Zero displacement is rejected.
11. Source and destination reference entities must match during an individual displacement.
12. Cross-reference-frame transformation is not currently defined.
13. A reference entity may intentionally be changed after successful displacement as a separate state operation.
14. A reference-entity change does not itself constitute temporal displacement.
15. Temporal displacement is modeled as an atomic transition between complete states.
16. A successful transition must leave the Observer in the complete destination state.
17. A failed transition must leave the Observer in the complete source state.
18. No intermediate Observer state is exposed by the displacement model.
19. Recovery is a new displacement, not rollback, undo, or reversal.
20. Recovery requires the checkpoint to be treated as a proposed destination and independently evaluated.
21. The Observer remains the final Authorizer for recovery and displacement.
22. A successful displacement does not automatically replace the recovery checkpoint.
23. Recovery checkpoints are changed only through explicit checkpoint operations.
24. Home is distinct from recovery.
25. Home may be explicitly replaced by the Observer.
26. Home is not automatically changed by displacement.
27. The first successful `set_home_checkpoint()` establishes the immutable internal `origin_checkpoint`.
28. `origin_checkpoint` can never be changed and remains available through the Observer library implementation.
29. The experiment does not expose `origin_checkpoint` directly.
30. Current state, recovery, home, and origin are distinct concepts with distinct persistence semantics.

31. The logical atomic transition is separated from the physical temporal-displacement mechanism.
32. `physical_transition(source_state, destination_state)` is the explicit technology boundary.
33. `PhysicalTransitionResult` distinguishes mechanism availability from mechanism success.
34. `PhysicalTransitionResult.evidence` is intentionally untyped and technology-defined.
35. `TransitionResult` preserves the corresponding `physical_transition_result`.
36. A mechanism-unavailable result cannot be successful.
37. A mechanism-reported success must be verified against actual destination-state establishment before logical success is reported.
38. A failed or unavailable mechanism must preserve the source state; otherwise the logical operation reports an atomic-transition integrity failure.
39. The logical layer must never simulate physical rollback through ordinary Observer state assignment.
40. The current physical mechanism implementation explicitly reports unavailability and does not mutate Observer state.
41. `TMTE.sin` is the current experimental interface boundary for the hypothetical Temporal Metric Translation Engine.
42. TMTE is a physical-system boundary and is not itself a software state mutation or coordinate assignment.
43. `TMTE.execute_transition(observer, source_state, destination_state)` is the mechanism-level execution entry point.
44. `TMTE.DeviceResult` distinguishes mechanism availability, mechanism-reported success, failure reason, and mechanism-provided evidence.
45. A mechanism-reported success is not by itself sufficient evidence that the Observer physically reached the destination state.
46. The TMTE execution architecture includes destination, causal, conservation, and independent verification stages before successful completion is reported.
47. TMTE supporting operations are external physical-boundary functions because no physical implementation currently exists.
48. The TMTE interface remains implementation-agnostic and does not currently assert a specific physical realization such as a wormhole, negative-energy system, quantum resonator, or metamaterial mechanism.
49. The logical TemporalDisplacement layer remains responsible for evaluating the TMTE result and enforcing the atomic-transition contract.

---

# 23. What Is Still Undefined

The current experimental model intentionally does not establish:

- an available physical mechanism of temporal displacement;
- a concrete technology implementation that can successfully perform the physical transition;
- cross-reference-frame transformation mathematics;
- the physical process by which a post-displacement reference entity is established;
- the internal storage and implementation of Observer home/recovery/origin checkpoints;
- whether checkpoint state is persisted outside the Observer instance;
- the complete physical verification apparatus needed to establish a destination as physically attainable;
- a concrete authorization API exposed by the current TemporalDisplacement interface.

These are not to be inferred merely from the current source model.

---

# 24. Source-vs-Semantics Discipline

Future changes should distinguish four categories:

```text
SOURCE IMPLEMENTATION
What the current `.sin` files actually implement.

SEMANTIC DECISION
What the experiment currently intends the system to mean.

OBSERVATION
What an executed experiment actually demonstrates.

HYPOTHESIS / PROPOSAL
What remains to be tested or formally incorporated.
```

A semantic decision must not be represented as an observed experimental result until an experiment actually establishes it.

Likewise, an implementation detail must not silently redefine a semantic contract without an explicit project decision.

---

# 25. Next Baseline

The uploaded `.sin` files are now the baseline for the next experimental iteration.

Before another project-state revision, changes should be reviewed against this document with particular attention to:

- `defined(E)` presence behavior;
- `observer.state(...)` construction semantics;
- current-state and proposed-displacement validation;
- reference-entity invariance during displacement;
- intentional post-displacement reference-entity reassignment;
- recovery checkpoint persistence;
- mutable home semantics;
- immutable internal origin semantics;
- Observer authorization;
- the TMTE physical-system boundary and its supporting external operations;
- TMTE destination, causal, conservation, and independent verification requirements;
- and the eventual concrete implementation of atomic transition.

---

# 26. Review Item — Error Semantics and Atomicity-Fault Containment

**Status:** Review required before implementation changes

**Origin:** Review of `TemporalDisplacement.sin` and `temporal-displacement-demo.sin`, including external Gemini review and subsequent project assessment.

This section records the current assessment of three proposed hardening changes. It is intentionally a **review item**, not an assertion that the proposed behavior has already been implemented.

## 26.1 `problem_code` / `problem_sub` relationship

The current framework error interface includes both a `problem_code` and a `problem_sub` value.

The established interpretation for this project is:

> `problem_code` and `problem_sub` describe the same problem classification. `problem_code` is an integer representation of the same semantic value represented by `problem_sub` as a string.

Therefore, `problem_code` is **not** a separate error taxonomy from `problem_sub`.

Conceptually:

```text
                    same problem
                         │
              ┌──────────┴──────────┐
              │                     │
       problem_sub             problem_code
        string form             integer form
```

For example, a future defined problem classification could conceptually be represented as:

```text
problem_sub  = "INTEGRITY_VIOLATION"
problem_code = <integer assigned to that classification>
```

The exact integer assignments are not currently defined by this project state and should not be invented merely to satisfy an external review recommendation.

### Assessment

Gemini's recommendation to replace the existing use of `framework.HandleError(0, ...)` with a new set of independently defined numeric error codes is therefore **not adopted as stated**.

The useful question for later review is narrower:

> Are the currently supplied `problem_code` values and corresponding `problem_sub` classifications sufficiently defined and consistently used for the error conditions produced by the temporal-displacement experiment?

If not, the project should define the classification semantics first and assign integer representations second.

No new error taxonomy should be introduced solely for implementation convenience.

---

## 26.2 TMTE retry / backoff

**Decision for current architecture:** Do not add generic retry/backoff behavior to `TemporalDisplacement`.

The current architecture deliberately places the technology-dependent operation behind:

```text
physical_transition(source_state, destination_state)
                    │
                    ▼
             TMTE.execute_transition(...)
```

`TemporalDisplacement` is responsible for the logical atomic-transition contract. It is not currently defined as the controller for the physical mechanism's operational state machine.

A mechanism reporting:

```text
available = false
successful = false
```

does not by itself establish that retrying is physically meaningful or safe.

A retry policy would require mechanism-specific semantics such as:

- whether the failure is transient;
- whether the mechanism is still armed or partially engaged;
- whether another attempt is physically safe;
- whether calibration or stabilization is required;
- whether repeating the transition could change the physical state;
- how many attempts are permissible;
- and what evidence must be revalidated after a retry.

Those questions belong to the physical mechanism/controller layer unless a future specification explicitly elevates them into the TemporalDisplacement contract.

### Rejected generic pattern

The following should **not** be introduced merely as error handling:

```text
TMTE unavailable
      │
      ▼
   wait N ms
      │
      ▼
   retry
      │
      └── repeat until success
```

Such a loop could accidentally turn a physical safety condition into an ordinary software retry condition.

### Future mechanism-layer pattern

If a future TMTE implementation establishes a well-defined transient failure mode, retry could instead be modeled explicitly inside the mechanism controller:

```text
             TMTE controller
                   │
          mechanism state machine
                   │
       ┌───────────┴───────────┐
       │                       │
   transient              non-retryable
    failure                  fault
       │                       │
   controlled                 fail
   recovery                   safely
       │
   re-verify
       │
   execute
```

The TemporalDisplacement layer would receive the resulting mechanism outcome rather than inventing a retry policy.

---

## 26.3 Atomicity integrity failure and fault containment

**Decision for current architecture:** This recommendation warrants a substantive future design review.

The current implementation already detects conditions in which the atomic-transition contract has been contradicted.

The relevant invariant is:

```text
                 Atomic transition invariant

        success  ───────────────► destination_state

        failure  ───────────────► source_state

        unavailable ────────────► source_state
```

An integrity failure occurs when the observed Observer state contradicts the required result.

Examples include:

```text
mechanism unavailable
        +
Observer state changed
        =
ATOMICITY INTEGRITY FAILURE
```

or:

```text
mechanism reports failure
        +
Observer state != source_state
        =
ATOMICITY INTEGRITY FAILURE
```

or:

```text
mechanism reports success
        +
Observer state != destination_state
        =
ATOMICITY INTEGRITY FAILURE
```

These are categorically different from ordinary mechanism failure.

### Ordinary mechanism failure

```text
Attempt transition
      │
      ▼
Mechanism cannot perform it
      │
      ▼
Source state preserved
      │
      ▼
Normal failed result
```

The system remains semantically coherent.

### Atomicity integrity failure

```text
Attempt transition
      │
      ▼
Observed state contradicts
atomic transition contract
      │
      ▼
Integrity invariant violated
      │
      ├──────────────┐
      ▼              ▼
 preserve         diagnose /
 evidence         contain
      │              │
      └──────┬───────┘
             ▼
       explicit fault state
```

The important distinction is that the second condition is not merely "the transition failed." It means the software's assumptions about indivisible state transition have been contradicted by the observed system state.

---

## 26.4 Why automatic rollback must remain prohibited

An integrity violation must not be handled by simply assigning:

```text
observer.state = source_state
```

The current architecture explicitly rejects software simulation of physical rollback.

If the Observer actually changed state during a supposedly atomic operation, assigning the old coordinates back would create a new software state without establishing that the physical system returned to the original physical state.

Therefore:

```text
observed integrity violation
          │
          X
          │
software coordinate rollback
```

must remain prohibited unless a future physical recovery mechanism independently establishes that the physical Observer has actually returned to the required state.

This is a critical safety and epistemic boundary.

---

## 26.5 Candidate fault-containment architecture

The exact response is not yet established, but a future design should evaluate a dedicated integrity-fault state rather than an ordinary error path.

A conceptual state machine is:

```text
                  NORMAL
                    │
                    │ displacement
                    ▼
                TRANSITION
                /         \
               /           \
       success              failure
         │                    │
         ▼                    ▼
   DESTINATION             SOURCE
                             │
                             │ preserved
                             ▼
                           NORMAL


             Any invariant contradiction
                       │
                       ▼
              INTEGRITY FAULT
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      preserve      prevent       preserve
      evidence      further       diagnostic
                    unsafe        context
                    transition
```

A future implementation should determine whether this fault state is:

- local to one Observer;
- global to the displacement subsystem;
- latched until explicit authorization;
- recoverable only through a physical diagnostic procedure;
- or some combination of these.

The current project state does **not** choose among those alternatives.

---

## 26.6 Forensic evidence requirements

The existing result architecture already provides a useful foundation because `TransitionResult` retains:

```text
physical_transition_result
```

and `PhysicalTransitionResult` retains:

```text
available
successful
failure_reason
evidence
```

If an atomicity integrity failure is detected, the future fault-containment design should consider preserving, at minimum:

```text
source_state
requested_destination_state
observed_state
physical_transition_result
mechanism evidence
failure classification
verification results
```

Conceptually:

```text
source ───────────────┐
                      │
requested destination│
                      ├──► Integrity-fault record
observed state ───────┤
                      │
mechanism evidence ───┤
                      │
verification results ─┘
```

The purpose is reconstruction, not automatic correction.

The system should preserve enough information to answer:

> What state did the software believe it was transitioning from, what destination was requested, what did the physical mechanism report, and what state was actually observed afterward?

---

## 26.7 Diagnostic/safe-mode question

Gemini recommended forcing diagnostic safe mode after an atomicity integrity failure.

The project assessment is that the underlying principle is worth reviewing, but the phrase "safe mode" is not yet a defined semantic construct in the current architecture.

The future review should therefore define the behavior rather than simply add a mode name.

Candidate requirements for an integrity-fault containment state include:

1. No additional temporal displacement is attempted automatically.
2. The fault record is preserved.
3. The Observer's observed state is treated as authoritative evidence of current software-visible state.
4. No software-only rollback is attempted.
5. Further displacement requires an explicitly defined authorization/recovery path.
6. Diagnostic operations must not silently mutate the Observer state.
7. Recovery, if physically possible, must itself satisfy the atomic-transition contract.

These are review candidates, not yet implemented requirements.

---

## 26.8 Recommended future review sequence

Before implementing fault containment, review the problem in this order:

```text
1. Define integrity invariant
          │
          ▼
2. Define integrity-fault classifications
          │
          ▼
3. Define evidence that must be retained
          │
          ▼
4. Define containment behavior
          │
          ▼
5. Define authorization required to leave fault state
          │
          ▼
6. Define physical recovery semantics
          │
          ▼
7. Implement mechanism-specific behavior
```

This preserves the project's separation between semantic definition and implementation.

---

## 26.9 Current assessment of Gemini's three recommendations

| Recommendation | Current assessment | Action |
|---|---|---|
| Replace generic `problem_code` usage with new domain-specific numeric codes | Mischaracterized because `problem_code` and `problem_sub` represent the same classification | **Do not adopt as stated. Review classification completeness/consistency later.** |
| Add TMTE retry/backoff | Not appropriate at the current TemporalDisplacement abstraction boundary | **Disregard for current implementation. Revisit only as TMTE mechanism/controller design.** |
| Lock down after atomicity integrity failure | Identifies a real architectural concern: invariant violation requires more than ordinary error handling | **Retain as a formal review item. Define fault containment before implementation.** |

### Overall assessment

Gemini's review is therefore best treated as a **hardening review**, not evidence that the current atomic-transition architecture is incorrect.

The most consequential finding is the third recommendation. The current implementation already detects atomicity contradictions; the unresolved design question is what the system must do **after detecting one**.

The next review should focus on:

```text
atomicity invariant
        ↓
integrity-fault definition
        ↓
evidence preservation
        ↓
fault containment
        ↓
explicit recovery/authorization
```

No retry loop or ad hoc numeric error taxonomy should be introduced as a substitute for that semantic work.

---

# 27. Review Status

The material in Section 25 is a **future-review item** and does not change the current source baseline unless a subsequent project decision explicitly adopts an item.

Current implementation remains governed by Sections 1–24 and the uploaded `.sin` source files.

The review is considered resolved only when the project explicitly decides whether to define and implement an atomicity-integrity fault state and its containment/recovery semantics.
