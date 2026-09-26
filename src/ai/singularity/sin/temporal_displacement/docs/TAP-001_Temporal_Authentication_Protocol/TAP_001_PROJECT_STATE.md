# TAP-001 Project State

**Project:** Temporal Authentication Protocol  
**Designation:** TAP-001  
**Document:** `TAP_001_PROJECT_STATE.md`  
**Status:** Working project-state artifact  
**Revision:** v27  
**Purpose:** Consolidated statement of the current TAP-001 architecture, frozen decisions, cryptographic lifecycle, optional historical-secret commitment, evidence model, completed Steps 6–15, current Step 16 specification work, and remaining open design questions.

---

# 1. Project Purpose

TAP-001 is a protocol for evaluating a future entity that claims to have established contact with the present through temporal displacement.

The protocol deliberately separates three questions:

1. **Immediate cryptographic authentication:** Can a received message be verified as having been produced with the designated historical secret?
2. **Historical event evidence:** Was the designated authentication material physically instantiated during a defined historical interval and subsequently destroyed under documented conditions?
3. **Temporal-contact assessment:** Do the authenticated information and independently obtained observations provide evidence consistent with the claimed temporal contact?

The protocol does **not** treat cryptographic authentication as mathematical proof of temporal displacement.

Core separation:

```text
AUTHENTICATION
    ≠
PHYSICAL VERIFICATION
    ≠
TEMPORAL-DISPLACEMENT CONCLUSION
```

---

# 2. Core TAP Architecture

```text
                    TAP
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 HISTORICAL AUTHENTICATION    FUTURE EVIDENCE
        │                         │
        │                         │
 Secret existed at                │
 (L₁,T₁)                          │
        │                         │
 Secret destroyed                │
        │                         │
        ▼                         ▼
Future entity possesses      Future observations
historical secret            X₁, X₂, X₃...
        │                         │
        ▼                         ▼
Cryptographic proof          Independent evidence
        │                         │
        └────────────┬────────────┘
                     ▼
             Temporal-contact
                 assessment
```

More precise causal model:

```text
HISTORICAL EVENT
      │
      ▼
Historical secret S
      │
      ▼
Physical instantiation
      │
      ▼
Physical destruction
      │                 FUTURE
      │                   │
      │                   ▼
      │          Claimant possesses S
      │                   │
      │                   ▼
      │          Authenticated message
      │                   │
      │          ┌────────┴────────┐
      │          │                 │
      │          ▼                 ▼
      │         X₁                X₂ ... Xₙ
      │          │                 │
      │          └────────┬────────┘
      │                   ▼
      │        Human independent testing
      │                   │
      │                   ▼
      │              V₁...Vₙ
      │                   │
      └──────────┬────────┘
                 ▼
       Temporal-contact assessment
```

---

# 3. HSIE — Historical Secret Instantiation Event

## TAP-D002 — HSIE Conceptual Definition — FROZEN

> **Historical Secret Instantiation Event (HSIE)**  
> A Historical Secret Instantiation Event is a deliberately created, bounded physical event in which designated cryptographic authentication material is physically instantiated at a specified physical location during a specified temporal interval, under documented custody and access conditions, and subsequently destroyed. The event establishes the historical provenance context of the authentication material; it does not, by itself, establish that no unauthorized copy was made. For long-term archival survival, the published HSIE artifact is the preferred durable archival root. The complete public verification material required for later TAP authentication SHALL be packaged directly within the published HSIE artifact, in its authentication-material component, including `key_identifier`, `public_key`, `signature_algorithm`, and `signature_parameters`. External keyservers, directories, locators, or other discovery infrastructure MAY supplement discovery, but SHALL NOT be required to recover the public verification key from the surviving HSIE artifact. The private signing key SHALL NOT be included in the published HSIE artifact.

Formal model:

```text
HSIE = (S, L, T_start, T_end, M, C, D)
```

Where:

- `S` = designated secret authentication material
- `L` = physical location
- `T_start` = event start epoch
- `T_end` = event end epoch
- `M` = physical medium containing `S`
- `C` = documented custody/access conditions
- `D` = destruction procedure

Lifecycle:

```text
UNINSTANTIATED
       │
       │ T_start
       ▼
 INSTANTIATED
       │
       │ T_end
       ▼
  DESTROYED
```

### Frozen HSIE boundaries

The HSIE is:

- deliberately created;
- spatially bounded;
- temporally bounded;
- an event in which designated authentication material is physically instantiated;
- subject to documented custody/access conditions;
- followed by destruction;
- a source of historical provenance context;
- the preferred durable archival root for the published HSIE artifact;
- self-contained with respect to the complete public verification material required for later TAP authentication, packaged in the authentication-material component as `key_identifier`, `public_key`, `signature_algorithm`, and `signature_parameters`.

The published HSIE artifact:

- MAY be supplemented by external keyservers, directories, locators, or other discovery mechanisms;
- MUST NOT require continued existence of such external infrastructure for a future verifier to recover the public verification key from the surviving HSIE artifact;
- MUST NOT contain the private signing key merely because the public verification key is embedded.

The HSIE does **not**:

- prove that no unauthorized copy was made;
- prove exclusive possession mathematically;
- prove temporal displacement.

### Existing historical HSIE instance

The project has documented a concrete historical event:

```text
Location:
    43.0389° N
    87.9065° W

Epoch:
    2026-09-21 05:03:00 UTC

Availability window:
    2026-09-21 05:03:00 – 05:03:10 UTC
```

Physical implementation discussed:

1. Generate a private signing key.
2. Print the designated secret authentication material on paper.
3. Place the paper in an envelope.
4. Place the envelope on a table in a back room.
5. Maintain sole personal custody during the approximately ten-minute event.
6. Remove and destroy the paper.
7. Destroy/delete the remaining digital copy.

These conditions document the historical event. They do not constitute mathematical proof that no copy was made.

### Location representation

The coordinate reference system has **not** been silently fixed to WGS84. A future TAP schema may explicitly identify the coordinate reference system, coordinate precision, and related location metadata.

---

# 4. TAP-001 Record Layering

## TAP-D013 — TAP-001 Record Layering — FROZEN

> A TAP-001 record shall distinguish the historical HSIE record, cryptographic authentication data, authenticated message contents, independently generated verification observations, and any subsequent temporal-contact assessment as separate semantic layers.

Conceptual structure:

```text
TAP-001
│
├── Historical HSIE record
├── Cryptographic authentication data
├── Authenticated message contents
│     └── X₁ ... Xₙ
├── Independent verification observations
│     └── V₁ ... Vₙ
└── Temporal-contact assessment
```

## TAP-D014 — Evidence Claims Are Authenticated Content — FROZEN

> Evidence claims `X₁...Xₙ` shall be represented as content of the authenticated TAP message. Cryptographic authentication of an `Xᵢ` establishes its provenance as authenticated message content but does not establish the physical truth of the claim.

Thus an `Xᵢ` is not merely a prediction. It is intended to be a self-contained, independently executable verification protocol or claim.

## TAP-D015 — Verification Results Are Independent — FROZEN

> Independent verification results `V₁...Vₙ` shall be distinguishable from the corresponding authenticated claims `X₁...Xₙ` and shall not be represented as though they originated from the authenticated claimant unless they actually did.

Causal ordering:

```text
authenticated claim
        │
        ▼
independent test
        │
        ▼
observation
        │
        ▼
analysis
```

The protocol must not reverse this relationship by allowing the claimant to define or reinterpret an observation after the fact.

---

# 5. Cryptographic Primitive and Lifecycle

## TAP-D016 — Asymmetric Digital-Signature Authentication — FROZEN

> TAP-001 shall use an asymmetric digital-signature primitive in which a secret signing key is associated with the historical authentication material and a corresponding public verification key is retained for independent verification. The future claimant shall authenticate TAP message content by generating a digital signature using the secret signing key. Verification shall be possible using the corresponding public verification key without disclosure of the secret signing key.

Abstract interface:

```text
KeyGen()
    │
    ├── public key PK
    └── secret key SK

Sign(SK, M) → σ

Verify(PK, M, σ) → VALID / INVALID
```

Where:

- `SK` = historical secret authentication material;
- `PK` = public verification material;
- `M` = exact TAP message content;
- `σ` = digital signature.

The fundamental mapping is:

```text
S = SK
```

in the HSIE formal model.

The public key is **not** secret authentication material.

### Why asymmetric authentication is required

The verifier must be able to authenticate future messages without possessing the historical secret.

A symmetric MAC would require the verifier to possess the same secret required to generate the authentication code. That would undermine the intended TAP topology because present-day verifiers would then possess the authentication secret.

TAP-001 therefore uses:

```text
Historical secret
       │
       └──► signing authority

Public key
       │
       └──► independent verification
```

---

## TAP-D017 — Historical Authentication Key Lifecycle — FROZEN

> The TAP authentication key pair shall be generated before or as part of preparation for the HSIE. The secret signing key shall be physically instantiated during the HSIE, subsequently destroyed as part of the HSIE, and shall not be required to remain available to present-day verifiers. The corresponding public verification key shall be retained independently so that future authenticated messages can be verified without access to the historical secret.

### Key lifecycle

```text
                 TAP KEY LIFECYCLE
                         │
                         ▼
                    KEY GENERATION
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
               SK                PK
                │                 │
                │                 └──────► retained
                │
                ▼
          HSIE instantiation
                │
                ▼
          physical SK exists
                │
                ▼
          HSIE destruction
                │
                ▼
       historical SK destroyed
                │
                │ FUTURE
                ▼
        claimant possesses SK
                │
                ▼
          Sign TAP message
                │
                ▼
                 σ
                │
                ▼
       present-day verification
                │
                │ PK
                ▼
     Verify(PK, M, σ)
```

The protocol deliberately creates the following historical condition:

```text
SK existed physically
        │
        ▼
SK was destroyed
        │
        ▼
PK remained available
        │
        ▼
future message verifies under PK
```

The intended evidentiary significance arises from the combination of the historical HSIE record and the later authenticated message. Neither component is, by itself, equivalent to a proof of temporal displacement.

Present-day verification should normally be possible with:

```text
PK + M + σ
```

and should not require:

```text
SK
```

---

# 6. Cryptographic Message Authentication

TAP-001 will authenticate the TAP message as a whole rather than treating each evidence claim as an independent cryptographic object by default.

Conceptual model:

```text
M = canonical TAP message
```

with:

```text
M
├── message metadata
├── protocol information
└── evidence claims
    ├── X₁
    ├── X₂
    └── Xₙ
```

The claimant produces:

```text
σ = Sign(SK, M)
```

A verifier performs:

```text
Verify(PK, M, σ)
```

This directly implements TAP-D014:

> The signature authenticates the exact message containing the `Xᵢ` claims. It does not authenticate the physical truth of those claims.

### Canonical representation

Cryptographic verification requires an unambiguous byte representation.

Conceptually:

```text
structured TAP message
        ↓
canonical representation
        ↓
bytes M
        ↓
Sign(SK, M)
```

The verifier must reproduce the same canonical representation before signature verification.

The exact serialization mechanism remains open.

---

# 7. Cryptographic Algorithm Selection

TAP-D016 and TAP-D017 define the **primitive class and lifecycle**, not a particular algorithm.

The following remain open:

- exact signature algorithm;
- classical versus post-quantum selection;
- parameter set;
- key-generation procedure;
- entropy requirements;
- public-key representation;
- signature representation;
- canonical serialization;
- key reuse policy;
- single-message versus multi-message lifecycle;
- use of multiple independent signature schemes;
- detailed cryptographic threat model.

The architectural requirement is therefore:

```text
REQUIRED:
    asymmetric digital signature

NOT YET FROZEN:
    specific signature algorithm
```

---

# 8. Cryptographic Threat Considerations

The project has identified a distinction between two different future capabilities.

### A. Cryptographic break

A future adversary may be capable of defeating the computational security assumption underlying the selected signature algorithm.

### B. Universal historical-secret reconstruction

A hypothetical future entity might be capable of recovering the exact historical secret signing key from public information.

These are related but are not logically identical claims.

TAP-001 must therefore avoid treating:

```text
"signature verifies"
```

as equivalent to:

```text
"only the historically instantiated entity could possibly have produced it."
```

Possible threat levels previously identified:

```text
A0  Ordinary present-day adversary
A1  Faster classical future computation
A2  Cryptanalytic breakthroughs / quantum capability
A3  Capability to reconstruct SK from PK
A4  Hypothetical arbitrary recovery of historical secrets
```

No threat level has yet been adopted as a formal TAP requirement.

---

# 9. Future Evidence — Xᵢ

## TAP-D010 — Evidence Claims Must Be Independently Testable — FROZEN

Future evidence claims `X₁...Xₙ` must be independently testable.

## TAP-D011 — Human Verification Should Be Freely Accessible — FROZEN

> Verification of an `Xᵢ` intended as temporal-displacement evidence shall be accessible using the **ordinary publicly accessible capability represented by a public library**. This requirement applies to all capabilities and conditions required to execute and evaluate the `Xᵢ`, including required physical space.

Operational interpretation adopted in Step 9:

```text
TAP-D011 — Human Accessibility
│
├── Capability baseline
│   └── ordinary publicly accessible capability
│       represented by a public library
│
└── Physical-space constraint
    └── ordinary publicly accessible capability
        represented by a public library
```

The public-library capability baseline is the single accessibility standard for all required conditions. No separate dwelling-size, household-resource, or personal-ownership baseline is imposed by TAP-D011.

Accessibility is assessed from the declared resources and dependencies of the `Xᵢ`; it is not established merely by asserting that an `Xᵢ` is accessible. Optional resources do not determine TAP-D011 compliance when at least one sufficient required configuration exists within the baseline.

The phrase **ordinary publicly accessible capability represented by a public library** is intentionally technology-neutral. Step 9 does not prescribe a statistical definition of a public library, a specific provider, particular equipment, software, or implementation technology.

## TAP-D012 — Evidence Claims Should Be Operationally Self-Contained — FROZEN

An `Xᵢ` should contain enough information to allow an independent investigator to execute the intended test without relying on the claimant to provide post hoc clarification.

Conceptual Xᵢ structure:

```text
Xᵢ
├── phenomenon
├── apparatus requirements
├── construction procedure
├── calibration procedure
├── measurement procedure
├── expected result
├── controls
├── uncertainty requirements
├── analysis procedure
└── falsification criteria
```

---

# 10. Desired Evidence Characteristics

Preferred `Xᵢ` characteristics:

- independently verifiable;
- quantitative;
- instrument-independent or measurable with multiple technologies;
- low interpretation;
- reproducible;
- precisely specified;
- pre-committed;
- difficult to predict through ordinary means;
- difficult to fabricate;
- archivable;
- statistically assessable;
- falsifiable;
- no-cost accessible.

No specific phenomenon has yet been selected.

---

# 10A. Step 8 — Detailed Xᵢ Schema — APPROVED

Step 8 defines the formal conceptual organization and field structure of authenticated evidence claims `X₁...Xₙ`.

The organization is intentionally conceptual and remains modifiable in later development if necessary. It does not freeze a serialization format or a particular physical phenomenon, apparatus, measurement technology, statistical framework, uncertainty framework, or other experimental methodology.

## TAP-D028 — Authenticated Evidence Claim Structure — APPROVED

Each `Xᵢ` is an authenticated, self-contained specification of an evidence claim. For the current protocol design, `Xᵢ` is formally organized into three branches:

```text
Xᵢ
│
├── claim
│   ├── claim_id
│   ├── claim_statement
│   └── phenomenon
│
├── experiment
│   ├── conditions
│   ├── apparatus
│   │   └── requirements
│   └── procedure
│       ├── construction
│       ├── calibration
│       ├── measurement
│       └── controls
│
└── evaluation_specification
    ├── expected_result
    ├── uncertainty_requirements
    ├── analysis_procedure
    └── falsification_criteria
```

The exact serialization and field-level syntax remain open.

## TAP-D029 — Claim / Experiment / Evaluation Separation — APPROVED

The three branches have distinct semantic roles:

- `claim` defines the proposition being asserted, including the phenomenon to which the proposition refers.
- `experiment` defines how an independent investigator can operationally test the claim.
- `evaluation_specification` defines the precommitted rules, criteria, and procedures by which future observations are evaluated with respect to the claim.

The `evaluation_specification` is a specification of evaluation, not an evaluation result.

## TAP-D030 — Independent Execution and Operational Self-Containment — APPROVED

An `Xᵢ` intended as temporal-displacement evidence must contain sufficient operational information for an independent investigator to perform the intended test without requiring post-hoc clarification from the claimant.

The experiment branch may specify conditions, apparatus requirements, construction, calibration, measurement, and controls as applicable to the particular Xᵢ.

The schema does not require every possible procedural component to be substantively applicable to every future Xᵢ.

## TAP-D031 — Precommitted Falsifiability — APPROVED

The evaluation specification must define falsification criteria before the future test is performed.

`falsification_criteria` specifies what future observations or results would count against the claim. It does not contain the later determination that the claim was or was not falsified.

## TAP-D032 — Accessibility Through Declared Resources and Dependencies — APPROVED

An `Xᵢ` must identify the resources and dependencies required for independent verification sufficiently to permit evaluation against TAP-D011.

Accessibility is not represented as an asserted boolean property of Xᵢ. The creator specifies required resources and dependencies; protocol compliance with TAP-D011 is assessed from those requirements.

The accessibility assessment uses the unified TAP-D011 baseline: the ordinary publicly accessible capability represented by a public library.

## TAP-D033 — Methodological Neutrality and Authenticated Precommitment — APPROVED

The Xᵢ schema does not mandate a particular physical phenomenon, apparatus, measurement technology, calibration methodology, statistical framework, uncertainty framework, or other experimental methodology.

However, information necessary to prevent post-observation redefinition of the claim, test, or evaluation rules must be included in the authenticated Xᵢ specification.

The authenticated Xᵢ therefore fixes, as applicable:

- the claim identity;
- the claim statement;
- the relevant phenomenon;
- experimental conditions;
- apparatus/resource requirements;
- construction procedure;
- calibration procedure;
- measurement procedure;
- control procedure;
- expected/result criterion;
- uncertainty requirements;
- analysis procedure;
- falsification criteria.

These are specifications established before future independent testing.

They do not include future observations, measurements, execution records, analysis results, or temporal-contact conclusions.

## Step 8 — Explicit Xᵢ / Vᵢ Boundary — APPROVED

The authenticated `Xᵢ` defines the claim, the test, and the rules by which the future test will be evaluated.

The independent `Vᵢ` records what actually occurred when the test was subsequently performed.

Conceptually:

```text
Xᵢ
│
├── claim
├── experiment
└── evaluation_specification
        │
        ▼
   future independent test
        │
        ▼
       Vᵢ
        │
        ├── actual execution
        ├── actual observations
        ├── actual measurements
        └── actual execution-related data
```

The following do not belong in Xᵢ:

- future observations;
- future measurements;
- actual experimental execution records;
- actual analysis results;
- temporal-contact conclusions.

The later relationship between `Xᵢ` and `Vᵢ` remains subject to the eventual evidence-analysis rules.

## Step 8 Field Disposition — APPROVED

The following conceptual fields are approved for the current design:

```text
Xᵢ
├── claim
│   ├── claim_id
│   ├── claim_statement
│   └── phenomenon
│
├── experiment
│   ├── conditions
│   ├── apparatus
│   │   └── requirements
│   └── procedure
│       ├── construction
│       ├── calibration
│       ├── measurement
│       └── controls
│
└── evaluation_specification
    ├── expected_result
    ├── uncertainty_requirements
    ├── analysis_procedure
    └── falsification_criteria
```

`apparatus.alternatives` is not a required field. Instrument independence and multiple-technology verification remain desired characteristics rather than universal requirements.

`accessibility` is not a required Xᵢ field. Resource and dependency requirements are specified as part of the operational test specification and evaluated against TAP-D011.

`analysis` is represented conceptually as `analysis_procedure` to distinguish the precommitted method from later analysis results.

The exact formal serialization of these fields remains open.

---

# 10C. Development-Boundary Change — Sender-Determined Verification Content

The project originally placed three research activities into the TAP-001 development sequence:

1. survey present-day and approximately 20-year no-cost verification techniques;
2. identify candidate physical phenomena;
3. develop falsifiable experimental protocols.

These are no longer treated as required TAP-001 development steps.

The rationale is architectural: TAP-001 defines the protocol and the authenticated `X_i` structure; it does not need to prescribe how a sender discovers or develops the substantive scientific content of an `X_i`. The sender/creator should be able to determine those matters from existing historical records and supporting information available to the sender.

This change does **not** weaken the already-frozen requirements that:

- `X_i` be independently testable;
- `X_i` contain sufficient operational information for independent execution;
- the experiment and evaluation specification be precommitted;
- falsification criteria be represented;
- accessibility be evaluated under TAP-D011.

Accordingly, the sender supplies the substantive verification design within the approved `X_i` framework, while TAP-001 focuses its remaining development work on representation, independent observations, and temporal-contact assessment.

# 10B. Step 9 — Human Accessibility Formalization — COMPLETE

Step 9 operationalizes TAP-D011 without replacing or reopening the underlying frozen accessibility principle. TAP-D032 continues to require each `Xᵢ` to declare the resources and dependencies needed for independent verification.

## State transition from v9

```text
v9:
    TAP-D011 principle                  FROZEN
    TAP-D032 declared dependencies     APPROVED
    Operational accessibility test     IN PROGRESS
    Baseline-resource boundary         OPEN

v10:
    TAP-D011 principle                  FROZEN
    TAP-D032 declared dependencies     APPROVED
    Operational accessibility test     COMPLETE
    Unified accessibility baseline      DEFINED
    Step 9                            COMPLETE
```

## 10B.1 Unified accessibility baseline

The Step 9 decision is that **all conditions required to execute and evaluate an `Xᵢ` are assessed against one accessibility baseline**:

> **the ordinary publicly accessible capability represented by a public library**

This applies to all required capabilities, including but not limited to:

- equipment and instrumentation;
- software;
- data;
- literature and reference information;
- institutional or infrastructure access;
- computational resources;
- materials and consumables; and
- physical space required to execute or evaluate the test.

The physical-space requirement is therefore not governed by a separate "average single-human dwelling" rule. It uses the same public-library capability baseline.

## 10B.2 Required versus optional resources

Accessibility remains an assessed property rather than an asserted boolean property. The `Xᵢ` declares its required resources and dependencies, and TAP-D011 compliance is determined from those requirements.

```text
REQUIRED DEPENDENCY
    ↓
Necessary to execute the prescribed test
or evaluate it according to the authenticated
evaluation specification.

OPTIONAL RESOURCE
    ↓
Not necessary to perform and evaluate the
prescribed test.
```

Where an `Xᵢ` explicitly permits multiple sufficient configurations, compliance may be established through any sufficient configuration whose required capabilities fall within the TAP-D011 baseline. Optional convenience, redundancy, improved performance, or alternative implementations do not independently make an otherwise compliant `Xᵢ` inaccessible.

## 10B.3 Operational compliance rule

For TAP-001 Step 9, an `Xᵢ` is TAP-D011-compliant when:

1. all resources and dependencies necessary to execute the authenticated experimental procedure and evaluate the authenticated evaluation procedure have been identified sufficiently for independent assessment; and
2. the required capability for each necessary condition, including required physical space, falls within **the ordinary publicly accessible capability represented by a public library**.

No separate rule for personal ownership, ordinary household resources, incremental monetary expenditure, transportation, or dwelling size is introduced by TAP-D011. Such factors are relevant only insofar as they affect whether a required capability falls within the unified baseline.

## 10B.4 Methodological neutrality

Step 9 does not select or require:

- a physical phenomenon;
- a particular apparatus;
- a measurement technology;
- a calibration methodology;
- a statistical framework;
- an uncertainty framework;
- a software implementation; or
- a specific resource provider.

The baseline is a protocol-level accessibility criterion that can be applied to later candidate `Xᵢ` designs without prematurely constraining the scientific methodology.

## 10B.5 Public-library baseline boundary

The phrase **ordinary publicly accessible capability represented by a public library** is retained as the governing formulation without introducing a numerical prevalence threshold, named institution, geographic population, or technology inventory at this stage. Those details are implementation or application questions only if a later `Xᵢ` requires a determination at a borderline case.

The Step 9 decision therefore defines the accessibility standard without prematurely freezing a provider-specific resource catalog.

## 10B.6 Step 9 completion boundary

Step 9 is complete because the protocol now has:

- a single baseline applicable to all required accessibility conditions;
- an explicit required-versus-optional distinction;
- an assessment model based on declared `Xᵢ` dependencies rather than an accessibility assertion;
- an explicit inclusion of required physical space within the same baseline; and
- a technology-neutral formulation that does not select a scientific method or resource provider.

The former working questions concerning ordinary baseline resources, incremental monetary cost, household space, transportation, and separate resource-class rules are therefore closed as Step 9 design questions.

The provisional discussion labels `D034–D038` remain **unapproved** and are not added to the frozen decision set. Their working material is superseded by the completed Step 9 formulation recorded above and by the existing TAP-D011/TAP-D032 decisions.

# 11. Independent Verification — Vᵢ

Independent verification observations `V₁...Vₙ` are generated after receipt of the authenticated message and execution of the relevant tests.

Step 13 establishes the detailed conceptual representation and relationship model for `Vᵢ`. The exact serialization and field-level syntax remain open.

## TAP-D039 — Vᵢ Is an Independent Execution / Observation Record — APPROVED

`Vᵢ` is an independent verification record describing what actually occurred when an independent investigator performed the test specified by `Xᵢ`.

`Vᵢ` is not another claim specification and shall not redefine the authenticated test after the observation exists.

Conceptually:

```text
Xᵢ
│
│ defines
├── claim
├── test
└── evaluation rules
        │
        ▼
independent execution
        │
        ▼
       Vᵢ
```

The semantic distinction is:

```text
Xᵢ = what was specified beforehand
Vᵢ = what independently happened afterward
Assessment = what the comparison means
```

## TAP-D040 — Exact Xᵢ Reference — APPROVED

Every `Vᵢ` shall identify the exact authenticated `Xᵢ` that it purports to test.

A human-readable claim identifier alone is not sufficient if it could ambiguously identify more than one authenticated version. The final representation shall provide an unambiguous reference to the authenticated `Xᵢ`; the exact reference mechanism remains open.

## TAP-D041 — Actual Execution and Observation Data — APPROVED

`Vᵢ` shall record actual execution information and actual observations rather than merely asserting a final PASS/FAIL result.

The conceptual `Vᵢ` record may contain:

```text
Vᵢ
├── verification_reference
├── investigator
├── execution
├── observations
└── execution_record
```

The observations branch may record, as applicable:

```text
observations
├── raw_observations
├── measurements
├── uncertainty_data
└── supporting_records
```

These are conceptual fields. Exact required fields and serialization remain open.

## TAP-D042 — Deviations Are Recorded, Not Automatically Interpreted — APPROVED

A deviation between the authenticated `Xᵢ` specification and the actual execution shall be representable as an execution fact.

A deviation shall not automatically be converted into an invalid observation or claim result merely because it occurred.

Whether a deviation affects the evidentiary relationship between `Xᵢ` and `Vᵢ` is determined by the applicable evaluation and evidence-analysis rules.

## TAP-D043 — Vᵢ / Xᵢ Semantic Separation — APPROVED

`Vᵢ` shall remain semantically distinct from `Xᵢ`.

The authenticated `Xᵢ` fixes the claim, test, and precommitted evaluation specification. `Vᵢ` records the subsequent independent execution and observations.

`Vᵢ` shall not be used to retroactively redefine the authenticated claim, experimental conditions, procedure, expected result, analysis procedure, or falsification criteria.

## TAP-D044 — Claim Status Is Downstream of Vᵢ — APPROVED

A claim status is an assessment of the relationship between `Xᵢ` and one or more `Vᵢ` records. It is not synonymous with the raw `Vᵢ` observation record.

```text
Xᵢ
 │
 ▼
Vᵢ
 │
 ▼
analysis / comparison
 │
 ▼
claim status
```

Therefore `Vᵢ` shall not be reduced to a field such as `status = SUPPORTED` or `status = FAIL` in place of the underlying execution and observation record.

## TAP-D045 — Multiple Vᵢ Records May Correspond to One Xᵢ — APPROVED

TAP-001 shall permit multiple independently generated `Vᵢ` records to correspond to the same authenticated `Xᵢ`.

```text
             ┌── V₁a
             ├── V₁b
X₁ ──────────┼── V₁c
             └── V₁d
```

The protocol does not require a one-to-one relationship between an authenticated claim and an independent observation record.

## TAP-D046 — Globally Unique Observation Identity — APPROVED

Every independent observation/execution record shall have its own globally unique identifier while retaining an explicit reference to the authenticated `Xᵢ` it tests.

```text
Vᵢ
├── observation_id      ← globally unique
└── x_reference         ← exact authenticated Xᵢ
```

The identifier-generation mechanism remains open. The identifier shall identify the individual observation/execution record rather than merely the claim being tested.

## TAP-D047 — Three-Level Xᵢ / Vᵢ Relationship — APPROVED

The relationship between `Xᵢ` and `Vᵢ` shall be evaluated at three conceptually distinct levels:

```text
1. Referential relationship
   Vᵢ → exact authenticated Xᵢ

2. Execution-conformance relationship
   actual Vᵢ execution ↔ Xᵢ experiment specification

3. Evidentiary relationship
   Vᵢ observations ↔ Xᵢ evaluation specification
```

These levels answer different questions:

```text
Referential:
    Which authenticated specification was tested?

Execution:
    How closely did the actual execution correspond
    to the specified test?

Evidentiary:
    What do the observations mean under the
    precommitted evaluation rules?
```

No level silently substitutes for another.

## TAP-D048 — Analysis Remains Downstream and Distinct from Raw Vᵢ Observation — APPROVED

Raw observations and measurements shall remain distinguishable from subsequent analysis.

A `Vᵢ` record may contain or reference an analysis record, but the analysis result shall not be treated as though it were itself a raw observation.

The final decision on whether analysis records are physically represented inside `Vᵢ` or as a separate downstream record remains open. The semantic distinction between observations and analysis is approved.

## Step 13 conceptual representation

The resulting conceptual `Vᵢ` structure is:

```text
Vᵢ
│
├── verification_reference
│   ├── observation_id
│   └── x_reference
│
├── investigator
│   ├── investigator_id
│   └── independence_statement
│
├── execution
│   ├── execution_id
│   ├── start_time
│   ├── end_time
│   ├── location
│   ├── actual_conditions
│   ├── actual_apparatus
│   ├── calibration
│   ├── procedure_execution
│   └── deviations
│
├── observations
│   ├── raw_observations
│   ├── measurements
│   ├── uncertainty_data
│   └── supporting_records
│
└── execution_record
    ├── data_references
    ├── analysis_record
    └── integrity_metadata
```

This is a conceptual representation, not yet a frozen serialization.

The investigator identity and independence model, exact field requirements, raw-data archival requirements, timestamp/location requirements, integrity mechanisms, and exact analysis-record placement remain open.

The established relationship is:

```text
Xᵢ = what was specified beforehand
Vᵢ = what independently happened afterward
Assessment = what the comparison between them means
```

A later evidence-analysis stage may characterize `Xᵢ ↔ Vᵢ` as supported, contradicted, unresolved, or otherwise according to the eventual TAP evidence-analysis rules.

# 11A. Step 14 — Future-Evidence Branch Formalization — IN PROGRESS

Step 14 formalizes the future-evidence branch as a distinct protocol pathway operating downstream of successful cryptographic authentication and upstream of the separate temporal-contact assessment.

```text
future TAP message
      ↓
cryptographic authentication
      ↓
authenticated X₁ ... Xₙ
      ↓
independent verification
      ↓
V₁ ... Vₙ
      ↓
downstream evidence analysis
      ↓
evidence characterization
      ↓
Temporal-contact assessment (Step 15)
```

## TAP-D049 — Future-Evidence Branch as a Distinct Semantic Pathway — APPROVED / NOT FROZEN

The future-evidence branch shall be represented as a distinct semantic pathway beginning with a future TAP message, passing through cryptographic authentication and authenticated evidence claims, then through independent execution, `Vᵢ` observations, downstream analysis, and evidence characterization, before reaching the separate temporal-contact assessment.

The approved conceptual branch is:

```text
Future TAP message
      ↓
Cryptographic authentication
      ↓
Authenticated X₁ ... Xₙ
      ↓
Independent execution
      ↓
V₁ ... Vₙ
      ↓
Downstream analysis
      ↓
Evidence characterization
      ↓
Temporal-contact assessment
          Step 15
```

It does not replace the historical HSIE layer, the cryptographic authentication layer, or the temporal-contact assessment layer.

The approved branch definition establishes the sequence and semantic boundaries only. The narrower Step 14 rules below remain subject to separate approval.

## TAP-D050 — Authentication Precedes Authenticated Future Evidence — APPROVED / NOT FROZEN

Only message content that successfully passes the applicable cryptographic authentication procedure shall be treated as authenticated Xᵢ content within the future-evidence branch.

```text
received M + σ
    ↓
Verify(PK, M, σ)
    ↓
 VALID ─────→ authenticated Xᵢ branch
 INVALID ───→ not authenticated as claimant content
```

A failed verification establishes failure of TAP-001 authentication for the message; it does not by itself determine every other property of the message.

## TAP-D051 — Authenticated Xᵢ Is Immutable Within the Future-Evidence Branch — APPROVED / NOT FROZEN

Once an Xᵢ has been extracted from an authenticated message, that authenticated specification is fixed for subsequent verification. Later observations, analyses, or claimant communications shall not retroactively modify it.

## TAP-D052 — Independent Verification Is Downstream of Xᵢ — APPROVED / NOT FROZEN

Execution of an authenticated Xᵢ shall proceed independently of claimant control over the resulting observation or interpretation. Logistical communication is not prohibited, but post-observation claimant control over the meaning of the authenticated specification is.

## TAP-D053 — One-to-Many Xᵢ to Vᵢ Relationship — APPROVED / NOT FROZEN

The branch shall permit zero, one, or multiple independent Vᵢ records for a given authenticated Xᵢ, preserving TAP-D045.

```text
Xᵢ ─────┬── Vᵢa
        ├── Vᵢb
        └── Vᵢc
```

The branch does not require every Xᵢ to receive an observation and does not require one observation to settle a claim.

## TAP-D054 — Execution and Observation Failures Are Recordable Branch Outcomes — APPROVED / NOT FROZEN

The branch shall represent states such as not executed, attempted but incomplete, executed with deviation, and executed with observations. These are execution/evidence states, not automatic temporal-contact conclusions.

A failed execution does not automatically mean claim falsified; successful execution does not automatically mean claim established.

## TAP-D055 — Raw Observation, Analysis, and Evidence Status Remain Separate — APPROVED / NOT FROZEN

The branch shall preserve at least:

```text
Vᵢ observations / measurements
          ↓
       analysis
          ↓
   evidence result/status
```

This preserves TAP-D044 and TAP-D048. Exact analysis-record placement remains open.

## TAP-D056 — Evidence-Branch Output Is Not a Temporal-Contact Conclusion — APPROVED / NOT FROZEN

The branch may produce evidence-level characterization of how observations compare with the authenticated Xᵢ evaluation specification. It shall not itself make the final temporal-displacement assessment.

```text
evidence characterization
          ↓
Temporal-contact assessment
          (Step 15)
```

## TAP-D057 — No Retroactive Evidence-Branch Feedback Into Authenticated Content — APPROVED / NOT FROZEN

Later observations and analysis shall not modify the authenticated claim, experimental specification, expected result, uncertainty requirements, analysis procedure, or falsification criteria contained in Xᵢ.

If later information exposes an ambiguity or defect, that shall be recorded as an evidentiary/specification fact rather than silently rewriting historical authenticated content.

## Step 14 Conceptual Boundary

```text
ENTRY
  successfully authenticated future message
          ↓
  authenticated Xᵢ

PROCESS
  independent execution → Vᵢ → analysis

OUTPUT
  evidence characterization

EXIT
  Step 15 temporal-contact assessment
```

Step 14 does not redefine the HSIE, perform cryptographic authentication itself, rewrite authenticated Xᵢ content, substitute claimant assertions for Vᵢ, collapse observations into analysis, or make the final temporal-contact determination.

### Step 14 Open Implementation / Formalization Questions

- exact serialization of the future-evidence branch;
- exact execution-status vocabulary;
- handling/archive status of unauthenticated future messages;
- detailed investigator independence requirements;
- raw-data and provenance requirements;
- exact analysis-record placement and serialization;
- evidence-status vocabulary and comparison rules;
- treatment of partial, repeated, dependent, or contradictory tests.

---

# 11B. Step 15 — Temporal-Contact Assessment — APPROVED (conceptual framework; not frozen)

Step 15 is approved at the conceptual framework level. The approved framework defines the final evidentiary assessment layer that follows the historical, cryptographic, authenticated-claim, independent-observation, and future-evidence-analysis layers. The conceptual framework and D058–D067 are approved but explicitly not frozen; remaining work is implementation and formalization.

Its purpose is to assess what the complete evidentiary record supports, contradicts, or leaves unresolved with respect to a specified temporal-contact hypothesis. It does not convert cryptographic authentication into proof of temporal displacement.

The conceptual relationship is:

```text
HSIE-related historical information and records ────────┐
                                                         │
Cryptographic authentication → Authenticated Xᵢ → Vᵢ   │
                                               → Analysis
                                               → Evidence characterization
                                                         │
                                                         ▼
                                          Temporal-contact assessment
```

The historical information and records associated with the HSIE are assessment inputs; they are not a separate TAP processing stage or protocol layer.

## TAP-D058 — Temporal-Contact Assessment Is a Distinct Downstream Layer — APPROVED / NOT FROZEN

Temporal-contact assessment shall be represented as a distinct downstream semantic layer following the future-evidence branch.

Conceptually:

```text
historical / cryptographic record
        +
future-evidence record
        ↓
temporal-contact assessment
```

The assessment is not:

- the HSIE record;
- the cryptographic authentication result;
- an `Xᵢ`;
- a `Vᵢ`;
- raw observation data; or
- an analysis record.

It is an assessment of the combined evidentiary record.

## TAP-D059 — Assessment Inputs Are Explicit and Traceable — APPROVED / NOT FROZEN

A temporal-contact assessment shall identify the evidentiary inputs on which it depends. Where historical information or records associated with the HSIE are material to the assessment, they shall be identified as historical assessment inputs rather than treated as a separate TAP protocol layer.

Conceptually:

```text
TEMPORAL_CONTACT_ASSESSMENT
│
├── hypothesis
├── historical_records
├── authentication_inputs
├── future_evidence_inputs
├── observation_analysis_inputs
├── alternative_explanations
└── uncertainty_and_limitations
```

Each material input should be traceable to its source record. A conclusion shall not depend on an unrecorded evidentiary fact merely because the fact appears plausible.

## TAP-D060 — Historical Authentication and Future Evidence Retain Separate Roles — APPROVED / NOT FROZEN

The assessment shall preserve the distinct evidentiary roles of historical authentication and future evidence.

```text
Historical authentication
    ↓
historical information and records associated with the HSIE

Future evidence
    ↓
independently obtained observations relevant to the claims

Temporal-contact assessment
    ↓
evaluation of the combined record
```

Neither branch silently substitutes for the other.

```text
valid signature
    ≠
physical truth of Xᵢ

valid signature + HSIE
    ≠
automatic temporal-contact conclusion
```

## TAP-D061 — Assessment Is Comparative Rather Than Automatically Deductive — APPROVED / NOT FROZEN

The temporal-contact assessment shall compare the observed evidentiary record with the specified temporal-contact hypothesis and documented alternative explanations rather than treating any single observation as logically dispositive by default.

Conceptually:

```text
H_TC
  ↕
observed evidence

H_A1
  ↕
observed evidence

H_A2
  ↕
observed evidence
```

where:

```text
H_TC = specified temporal-contact hypothesis
H_Ai = explicitly documented alternative explanation
```

The framework does not require every conceivable alternative explanation to be known or eliminated. It requires material alternatives considered by the assessment to be identified and their relationship to the evidence documented.

The absence of a presently identified alternative explanation shall not, by itself, be represented as proof of temporal contact.

## TAP-D062 — Evidence Can Support, Contradict, or Fail to Distinguish a Hypothesis — APPROVED / NOT FROZEN

The assessment shall permit individual and aggregate evidence to be characterized according to its relationship with the temporal-contact hypothesis.

At the conceptual level, permitted characterizations include:

```text
supports consistency with H_TC
contradicts consistency with H_TC
does not materially distinguish H_TC from alternatives
unresolved because evidence is insufficient or conflicting
```

The controlled vocabulary is formalized by TAP-D070 and applies at both the individual-evidence and aggregate-assessment levels.

No single `Vᵢ` result is required to determine the aggregate assessment.

## TAP-D063 — Uncertainty and Evidentiary Limitations Are First-Class Assessment Inputs — APPROVED / NOT FROZEN

A temporal-contact assessment shall explicitly record relevant uncertainty and limitations.

These may include:

- measurement uncertainty;
- execution deviations;
- incomplete observations;
- instrument limitations;
- environmental uncertainty;
- archival or provenance gaps;
- cryptographic assumptions;
- unresolved alternative explanations;
- dependencies among observations;
- insufficient sample size; and
- ambiguity or defect in an `Xᵢ` or its evaluation procedure.

Uncertainty or limitation shall not be silently converted into either support or contradiction.

## TAP-D064 — No Mandatory Single Numerical Evidence Score — APPROVED / NOT FROZEN

TAP-001 shall not require a single scalar score, probability, confidence number, or universal weighting function as the conceptual representation of temporal-contact assessment.

A later implementation may use quantitative methods where justified by the particular evidentiary design.

If quantitative inference is used, the assumptions, model, inputs, dependencies, uncertainty, and limitations shall be documented rather than hidden inside an unexplained score.

## TAP-D065 — Alternative Explanations Are Explicitly Assessed — APPROVED / NOT FROZEN

Where an authenticated future message or `Xᵢ` appears to contain information that is temporally significant, the assessment shall distinguish:

```text
evidence difficult to explain under a specified alternative
```

from:

```text
evidence impossible to explain under a specified alternative
```

TAP-001 shall not require a verifier to establish impossibility merely to document that evidence is difficult to explain under an alternative.

At the same time, unexplained evidence shall not automatically be treated as evidence of temporal contact.

The assessment shall record which alternatives were considered, what evidence bears on them, and what remains unresolved.

## TAP-D066 — Assessment Strength Is Bounded by the Evidentiary Record — APPROVED / NOT FROZEN

The temporal-contact assessment shall not state a stronger conclusion than is justified by the documented evidentiary record and its stated uncertainties and limitations.

Conceptually:

```text
documented evidence
      +
documented uncertainty
      +
documented alternatives
      ↓
permitted assessment characterization
```

A cryptographic verification result, HSIE record, commitment match, or single future-evidence result shall not independently be promoted to a temporal-contact conclusion.

## TAP-D067 — Assessment Is Reproducible and Auditable — APPROVED / NOT FROZEN

A temporal-contact assessment shall contain or reference enough information for the receiver, acting as the responsible assessor and reviewer, to determine:

```text
what hypothesis was assessed;
which evidence records were considered;
which alternative explanations were considered;
what analytical rules or methods were used;
what uncertainties and limitations were recognized;
and how the stated assessment characterization followed from those inputs.
```

The assessment record shall not require access to hidden claimant state, unstated assumptions, or private reasoning to reproduce the stated evidentiary pathway.

No separate independent third-party reviewer is required by TAP-001. The receiver may seek outside assistance, but TAP-001 does not require that assistance to be disclosed solely because it occurred.

## TAP-D068 — Minimum Temporal-Contact Hypothesis Representation — APPROVED / NOT FROZEN

A temporal-contact hypothesis used by an assessment shall have a minimum unambiguous representation consisting of:

```text
hypothesis_id
hypothesis_statement
assessment_scope
```

`hypothesis_id` shall uniquely identify the hypothesis record. The statement shall express the proposition being assessed, and `assessment_scope` shall identify the temporal, evidentiary, or other boundaries necessary to distinguish what the assessment does and does not address.

A materially different hypothesis shall receive a distinct `hypothesis_id` rather than silently modifying an existing hypothesis record.

## TAP-D069 — Simplified Alternative-Explanation Representation — APPROVED / NOT FROZEN

A material alternative explanation considered by an assessment shall be represented by:

```text
alternative_id
alternative_statement
```

`alternative_id` shall uniquely identify the alternative record. The statement shall describe the alternative sufficiently for its relationship to the evidence to be evaluated.

A materially different alternative shall receive a distinct `alternative_id` rather than silently modifying an existing alternative record.

The protocol does not require exhaustive enumeration of every conceivable alternative explanation.

## TAP-D070 — Controlled Assessment-Result Vocabulary — APPROVED / NOT FROZEN

Temporal-contact evidence characterization shall use the following controlled vocabulary at both the individual-evidence and aggregate-assessment levels:

```text
SUPPORTS
CONTRADICTS
DOES_NOT_DISTINGUISH
UNRESOLVED
```

The meanings are:

```text
SUPPORTS
    The characterized evidence is consistent with and provides
    evidentiary support for the specified hypothesis at the
    assessment scope being characterized.

CONTRADICTS
    The characterized evidence is inconsistent with and provides
    evidentiary evidence against the specified hypothesis at the
    assessment scope being characterized.

DOES_NOT_DISTINGUISH
    The characterized evidence does not materially distinguish
    the specified hypothesis from the relevant alternatives.

UNRESOLVED
    The relationship cannot be determined from the available
    record because the evidence is insufficient, conflicting,
    materially limited, or otherwise not adequately resolved.
```

`DOES_NOT_DISTINGUISH` and `UNRESOLVED` shall not be treated as equivalent to either support or contradiction.

No additional universal result state is required at the conceptual level. A future implementation may preserve finer-grained method-specific detail without changing the controlled TAP characterization.

## TAP-D071 — Dependent Evidence Shall Not Be Treated as Independent — APPROVED / NOT FROZEN

Evidence records that derive from, substantially reuse, or share a material underlying source with another evidence record shall be representable as dependent evidence.

A simple dependency representation is:

```text
evidence_reference
    └── depends_on: [evidence_reference, ...]
```

Where material dependency exists, the dependent records shall not be treated as independent pieces of evidence for purposes of evidentiary combination or statistical inference.

Where a validated analytical method explicitly models the dependency, that method may use the records separately. Otherwise, the assessment shall use a conservative treatment that avoids counting the same underlying evidence more than once for the same inferential purpose.

TAP-001 does not mandate a specific dependency model or statistical estimator.

## TAP-D072 — Assessment Is Append-Only and Versioned — APPROVED / NOT FROZEN

A completed temporal-contact assessment shall not be modified in place.

Each assessment shall have:

```text
assessment_id
assessment_version
```

with `assessment_version` beginning at `1` and increasing monotonically for later versions of the same assessment.

When new material `Vᵢ` evidence, analysis, or other assessment input is incorporated, the receiver shall create a new assessment version that:

```text
retains the same assessment_id
references the newly considered inputs
identifies the immediately preceding assessment version
supersedes that prior version for the current assessment state
```

Prior assessment versions remain part of the historical assessment record and shall not be overwritten.

Conceptually:

```text
Assessment A(v1)
        ↓ new material evidence
Assessment A(v2)
        ↓ additional material evidence
Assessment A(v3)
```

The same lifecycle applies when material historical or analytical information changes the evidentiary record, not only when a new `Vᵢ` arrives.

## TAP-D073 — Assessment Methodology Is Requirement-Based, Not Method-Prescriptive — APPROVED / NOT FROZEN

TAP-001 shall define requirements that any valid temporal-contact assessment methodology must satisfy without mandating one universal analytical method.

A method may be qualitative or quantitative, including likelihood-based, Bayesian, frequentist, or another justified approach, provided that the assessment record identifies, as applicable:

```text
method_type
method_description
assumptions
inputs
uncertainty_treatment
dependency_treatment
```

The method shall be reproducible from the recorded inputs and stated rules, shall not rely on unrecorded material assumptions, and shall produce a characterization using the TAP-D070 vocabulary.

Quantitative methods shall not conceal weighting, dependency assumptions, uncertainty, or model choices inside an unexplained scalar result.

No universal weighting function or mandatory numerical evidence score is required.

## TAP-D074 — Proposed Temporal-Contact Assessment Record Profile — APPROVED / NOT FROZEN

The existing conceptual assessment structure is retained. A proposed implementation profile adds explicit field syntax, identifiers, versioning, and source references while remaining unfrozen for Step 16 final specification work.

Proposed logical representation:

```text
TEMPORAL_CONTACT_ASSESSMENT
│
├── assessment_reference
│   ├── assessment_id
│   ├── assessment_version
│   └── schema_version
│
├── hypothesis
│   ├── hypothesis_id
│   ├── hypothesis_statement
│   └── assessment_scope
│
├── evidence_inputs
│   ├── historical_records
│   ├── cryptographic_authentication
│   ├── optional_secret_commitment
│   ├── authenticated_Xᵢ_records
│   ├── Vᵢ_records
│   └── analysis_records
│
├── comparative_assessment
│   ├── evidence_supporting
│   ├── evidence_contradicting
│   ├── evidence_non_discriminating
│   ├── unresolved_evidence
│   └── alternative_explanations
│       ├── alternative_id
│       └── alternative_statement
│
├── uncertainty_and_limitations
│   ├── measurement_uncertainty
│   ├── execution_limitations
│   ├── provenance_limitations
│   ├── model_assumptions
│   └── unresolved_dependencies
│
└── assessment_result
    ├── methodology
    │   ├── method_type
    │   ├── method_description
    │   ├── assumptions
    │   ├── inputs
    │   ├── uncertainty_treatment
    │   └── dependency_treatment
    ├── characterization
    ├── rationale
    ├── limitations
    └── unresolved_questions
```

A proposed source reference shall identify the exact source record and, where applicable, its version:

```text
record_ref
├── record_id
└── record_version
```

Repeatable evidence/input collections shall contain zero or more such references. A dependency may be represented on an evidence reference as:

```text
depends_on: [record_ref, ...]
```

### Proposed encoding and naming profile

The proposed assessment serialization is:

```text
encoding: UTF-8
logical serialization: JSON object
field naming: snake_case
repeatable items: JSON arrays
identifiers: globally unique opaque identifiers
version fields: positive monotonically increasing integers where versioning applies
```

This is a proposed implementation profile, not a frozen serialization requirement. Step 16 shall establish the final encoding and exact serialization consistently with the final TAP specification and any cross-layer canonicalization requirements.

No field in this profile silently changes the semantic boundaries already established by D013–D018, D028–D033, D039–D048, or D049–D067.

## TAP-D075 — Minimal Structured Uncertainty and Limitation Representation — APPROVED / NOT FROZEN

Each material uncertainty or limitation shall be representable as a structured item containing at least:

```text
uncertainty_id
category
description
source_refs
```

The existing conceptual categories remain available:

```text
measurement_uncertainty
execution_limitations
provenance_limitations
model_assumptions
unresolved_dependencies
```

Method-specific quantitative detail may be added where justified by the assessment method. Such detail shall not be required for qualitative uncertainty and shall not silently convert an uncertainty or limitation into `SUPPORTS` or `CONTRADICTS`.

The same representation may be used for unresolved evidentiary limitations that are not strictly measurement uncertainty.

## TAP-D076 — Receiver Responsibility and Optional Outside Assistance — APPROVED / NOT FROZEN

The receiver is responsible for performing and issuing the temporal-contact assessment and for the review required by TAP-D067.

The receiver may obtain outside assistance, including technical, scientific, statistical, or other assistance. TAP-001 does not require the receiver to document or disclose that assistance solely because it occurred.

Any substantive external material that the receiver independently relies upon remains subject to the ordinary assessment-input traceability requirements; the protocol does not create a separate assistance-disclosure record.

## TAP-D078 — Message Authentication Key Resolution Through HSIE Reference — APPROVED / NOT FROZEN

An authenticated TAP message SHALL resolve the public verification material required for signature verification through its exact `historical_reference.hsie_reference`. The referenced HSIE artifact contains the designated authentication-material component, including `key_identifier`, `public_key`, `signature_algorithm`, and `signature_parameters`.

The message SHALL NOT require a separate `authentication_key_reference` or a separately surviving `AUTHENTICATION_KEY_RECORD` in order to identify or recover the public verification key required for authentication. A deployment MAY maintain auxiliary key records for local indexing or implementation convenience, but such records are not part of the protocol's archival dependency chain.

The removal of a separate message-level authentication-key reference does not collapse TAP-D013 semantic layers. The cryptographic authentication data remains semantically distinct even though its durable public verification material is physically packaged within the HSIE artifact.

## TAP-D079 — Bidirectional Temporal Message Channel — APPROVED / NOT FROZEN

TAP-001 MAY support a bidirectional temporal message channel in which an outgoing message is physically instantiated as part of the HSIE. Its distinct message text is represented by `associated_outgoing_message.message_content` and SHALL be encrypted before packaging with the HSIE artifact. The outgoing message SHALL be cryptographically bound to the designated historical signing key, and its `message_content` SHALL be encrypted using the public encryption key material contained within the HSIE's embedded OpenPGP public key material. A D079-enabled HSIE SHALL therefore contain the public encryption material required for later decryption. For the supplied example key pair, this is the Cv25519/X25519 encryption subkey identified by `7C11A43BA5060409`. The historical private signing key and the corresponding private encryption key SHALL both be held on the same physical medium during the HSIE. Neither private key SHALL be included in the published HSIE artifact. **Both private keys are destroyed as part of the same physical destruction event of the medium.** For D079 channel operation, the future endpoint is intended to obtain that physical medium in the future state and recover both private keys from it. The private encryption key is used to decrypt the embedded message content; the historical private signing key retains its signing function and may be used by the future endpoint for an authenticated response. The future endpoint MAY decrypt the message content, process the request, and return a `MESSAGE_RECORD` response that identifies the exact embedded outgoing message and is cryptographically signed with the designated historical signing key.

The channel is a **logical protocol-layer capability** for authenticated and encrypted communication across temporally separated endpoints. It does not assert that a physical temporal transport mechanism exists, that a future responder exists, that a responder is a "superior intelligence," or that a cryptographically authenticated response is necessarily correct.

The outgoing request SHALL be constructed while the designated historical signing key is available. The outgoing request SHALL be signed with that historical signing key before the historical signing key is destroyed according to the HSIE lifecycle. The `associated_outgoing_message.message_content` SHALL be retained in the HSIE artifact as ciphertext produced using the public encryption key material embedded in the HSIE. The historical private signing key and the corresponding private encryption key SHALL reside on the same physical medium during the HSIE, and **both private keys are destroyed as part of the same physical destruction event of the medium**. Neither private key SHALL be included in the published HSIE artifact. For D079 channel operation, the future endpoint is intended to obtain the same physical medium in the future state and recover both private keys. The private encryption key decrypts the embedded message content; the historical private signing key may be used for future response signing.

A future response SHALL identify the exact request to which it responds. The response MAY include a returned computation, proof, derivation, certificate, measurement, or other application-defined result. Cryptographic signature validity establishes message authenticity/provenance under the designated key; it does not independently establish the semantic correctness of the result or the identity, capability, or temporal origin of the responder.

The channel MAY be used for application-level computation requests, including requests whose solution is unavailable using present-day capabilities. In such a case, the request SHOULD predeclare the problem statement, required output, acceptance criteria, and any required response format or verification material. Any conclusion that the response came from a future or technologically superior intelligence remains outside the cryptographic assertion of TAP-001 and requires separate assessment of the complete evidentiary record.

D079 does not modify the frozen HSIE definition in D002, the semantic separation required by D013, the authentication/evidence boundaries in D001, D005, D009, D014, or D015, the asymmetric-signature requirement in D016, the historical key lifecycle in D017, or the narrow commitment binding in D018.

## Step 15 Completion Boundary

Step 15 is complete at the approved design level because:

```text
conceptual framework             APPROVED / NOT FROZEN
D058–D067                        APPROVED / NOT FROZEN
D068–D076                        APPROVED / NOT FROZEN
remaining conceptual questions  CLOSED
```

The remaining work is Step 16 review/refinement: selecting and freezing the exact final serialization, integrating the approved requirements across all TAP layers, faithfully incorporating the frozen TAP-D002 archival packaging requirements, and completing `TAP_001_SPECIFICATION.md`.

## Step 15 Conceptual Assessment Record

The conceptual assessment record is:

```text
TEMPORAL_CONTACT_ASSESSMENT
│
├── assessment_reference
│   ├── assessment_id
│   └── assessment_version
│
├── hypothesis
│   ├── temporal_contact_hypothesis
│   └── assessment_scope
│
├── evidence_inputs
│   ├── historical_records
│   ├── cryptographic_authentication
│   ├── optional_secret_commitment
│   ├── authenticated_Xᵢ_records
│   ├── Vᵢ_records
│   └── analysis_records
│
├── comparative_assessment
│   ├── evidence_supporting
│   ├── evidence_contradicting
│   ├── evidence_non_discriminating
│   ├── unresolved_evidence
│   └── alternative_explanations
│
├── uncertainty_and_limitations
│   ├── measurement_uncertainty
│   ├── execution_limitations
│   ├── provenance_limitations
│   ├── model_assumptions
│   └── unresolved_dependencies
│
└── assessment_result
    ├── characterization
    ├── rationale
    ├── limitations
    └── unresolved_questions
```

This structure is conceptual and is not yet a frozen serialization. TAP-D074 supplies the approved-but-not-frozen logical field profile, including UTF-8/JSON as the proposed encoding, globally unique identifiers, assessment versioning, and exact source-record references.

## Step 15 Epistemic Boundary

The semantic meaning of each stage remains distinct:

```text
HSIE
    = historical event

HSIE-related historical information and records
    = historical assessment inputs associated with the HSIE

cryptographic authentication
    = authentication of message provenance

Xᵢ
    = precommitted claim/test/evaluation specification

Vᵢ
    = independent execution/observation record

analysis
    = interpretation of recorded observations under stated methods

evidence characterization
    = relationship of analyzed evidence to Xᵢ and considered alternatives

temporal-contact assessment
    = structured assessment of the complete evidentiary record
```

The final assessment does not become a mathematical proof merely because all preceding stages are valid.

# 12. Conceptual TAP-001 Record Schema

The following remains a **conceptual schema**, not a frozen serialization format:

```text
TAP-001 Record
│
├── protocol
│   ├── protocol_name
│   ├── protocol_version
│   └── record_id
│
├── historical_event
│   └── HSIE
│       ├── authentication_material
│       │   ├── key_identifier
│       │   ├── public_key
│       │   ├── signature_algorithm
│       │   └── signature_parameters
│       ├── location
│       ├── temporal_interval
│       ├── physical_medium
│       ├── custody
│       └── destruction
│
├── message
│   ├── message_id
│   ├── creation_time
│   ├── message_role
│   ├── historical_reference
│   ├── channel
│   │   ├── channel_id
│   │   ├── request_reference
│   │   └── request_nonce
│   ├── authenticated_content
│   ├── cryptographic_protection
│   │   ├── signature
│   │   └── optional encryption
│   └── evidence_claims
│       ├── X₁
│       ├── X₂
│       └── Xₙ
│
└── evidence
    ├── claim_status
    ├── independent_observations
    │   ├── V₁
    │   ├── V₂
    │   └── Vₙ
    └── temporal_contact_assessment
```

With D018, an optional commitment belongs to the cryptographic layer and MAY be physically packaged within the HSIE archival artifact without changing its semantic role.

The schema is constrained by TAP-D013 through TAP-D015 but does not yet freeze all serialization or field-level syntax.

---

# 13. Authentication / Evidence Boundary

```text
HISTORICAL LAYER
    │
    ├── HSIE
    ├── historical SK instantiation
    └── historical SK destruction
             │
             ▼
CRYPTOGRAPHIC LAYER
    │
    ├── PK
    ├── authenticated message M
    ├── signature σ
    └── optional commitment C
             │
             ▼
TEMPORAL MESSAGE-CHANNEL LAYER
    │
    ├── outgoing signed/encrypted request
    └── future authenticated response
             │
             ▼
EVIDENCE-CLAIM LAYER
    │
    ├── X₁
    ├── X₂
    └── Xₙ
             │
             ▼
INDEPENDENT-OBSERVATION LAYER
    │
    ├── V₁
    ├── V₂
    └── Vₙ
             │
             ▼
ASSESSMENT LAYER
    │
    └── temporal-contact assessment
```

No layer is permitted to silently substitute for another.

---

# 14. Current Frozen TAP Decisions

The following decisions are currently locked:

### TAP-D001 — Separate Historical Authentication and Future Evidence

Historical authentication and future evidence are separate evidentiary components.

### TAP-D002 — HSIE Is a Historical Event

The HSIE is a deliberately created historical physical event involving designated authentication material. The published HSIE artifact is the preferred durable archival root and SHALL package the complete public verification material required for later TAP authentication directly within its authentication-material component: `key_identifier`, `public_key`, `signature_algorithm`, and `signature_parameters`. External keyservers, directories, locators, or other discovery infrastructure MAY supplement discovery but SHALL NOT be required for a future verifier to recover the public verification key from the surviving HSIE artifact. The private signing key SHALL NOT be included in the published HSIE artifact.

### TAP-D003 — HSIE Is Bounded in Spacetime

The HSIE has defined physical and temporal boundaries.

### TAP-D004 — Secret Destruction Is Part of HSIE

Destruction of the designated secret authentication material is part of the HSIE.

### TAP-D005 — Immediate Cryptographic Authentication Is Independent of Future Evidence

Signature verification is a distinct operation from evaluating future evidence.

### TAP-D006 — HSIE Does Not Prove Absence of Copying

The HSIE does not establish that an unauthorized copy of the secret was not made.

### TAP-D007 — Temporal Displacement Is an Inference

Temporal displacement is an assessment arising from the total evidentiary record rather than a direct mathematical consequence of authentication.

### TAP-D008 — Do Not Silently Prescribe WGS84

The location coordinate reference system remains an explicit future schema decision.

### TAP-D009 — Future Evidence Is Delivered as Authenticated Message Content

Future evidence claims are contained within the authenticated message.

### TAP-D010 — Evidence Claims Must Be Independently Testable

`Xᵢ` claims must support independent testing.

### TAP-D011 — Human Verification Should Be Freely Accessible

The intended verification model avoids mandatory payment, institutional access, proprietary software, paid data, or proprietary equipment.

### TAP-D012 — Evidence Claims Should Be Operationally Self-Contained

An `Xᵢ` should contain the information required to perform the intended test.

### TAP-D013 — TAP-001 Record Layering

Historical, cryptographic, authenticated-content, independent-observation, and assessment layers are distinct semantic layers.

### TAP-D014 — Evidence Claims Are Authenticated Content

Cryptographic authentication establishes the provenance of `Xᵢ` as message content, not the physical truth of `Xᵢ`.

### TAP-D015 — Verification Results Are Independent

`Vᵢ` observations remain distinct from authenticated claimant content.

### TAP-D016 — Asymmetric Digital-Signature Authentication

TAP-001 uses an asymmetric digital-signature primitive with a secret signing key and independently retained public verification key.

### TAP-D017 — Historical Authentication Key Lifecycle

The signing key is physically instantiated during the HSIE, subsequently destroyed as part of the HSIE, and is not required for present-day verification; the public verification key is retained independently of the destroyed secret. The amended D002 definition clarifies that this independent retention does not require a separate surviving artifact: the public verification key is packaged directly into the published HSIE record.

### TAP-D018 — Optional Historical Secret Commitment — FROZEN

> TAP-001 MAY include a cryptographic commitment to the designated historical secret signing key. When present, the commitment shall be generated from the exact designated secret authentication material using a domain-separated cryptographic commitment construction and shall be retained independently of the secret signing key. The commitment shall provide an independently verifiable means of determining whether subsequently disclosed key material corresponds to the historically committed secret. The commitment shall not replace digital-signature authentication, shall not establish exclusive possession of the secret, and shall not by itself establish temporal displacement.

Conceptual construction:

```text
C = H(D || canonical_encoding(SK))
```

where:

- `H` = cryptographic hash function;
- `D` = TAP-001 domain-separation value;
- `SK` = exact designated historical secret signing key;
- `C` = optional public commitment.

If a future claimant discloses candidate key material:

```text
C' = H(D || canonical_encoding(SK_future))
```

then `C' == C` would establish correspondence to the committed secret, subject to the security properties of the selected construction and encoding.

It would **not** establish exclusive possession, absence of copying, or temporal displacement.

D018 does not modify D002, D016, D017, or the existing TAP-D013 through TAP-D015 record-layer boundaries.

---

# 15. Decisions Implemented in v6

This revision preserves the complete v5 architecture and frozen decisions and implements the remaining D018 construction proposals without changing the semantic meaning of TAP-D002, TAP-D013, TAP-D014, TAP-D015, TAP-D016, or TAP-D017.

Implemented and frozen in v6:

```text
D016  Asymmetric digital-signature authentication
      → FROZEN

D017  Historical authentication key lifecycle
      → FROZEN

D018  Optional historical-secret commitment architecture
      → FROZEN

D018 implementation construction
      → FROZEN at the protocol-requirement level
```

The D018 implementation decisions are algorithm-agile and technology-neutral. They specify what a compliant implementation must preserve while deliberately avoiding permanent dependence on a particular cryptographic algorithm, serialization technology, storage technology, or vendor.

The resulting cryptographic architecture is:

```text
                    KEY GENERATION
                          │
                   ┌──────┴──────┐
                   ▼             ▼
                  SK            PK
                   │             │
                   │             └──────────► retained independently
                   │
                   ├──────────► E(SK)
                   │              │
                   │              ▼
                   │       C = H(D || E(SK))
                   │              │
                   │              └──────────► retained independently
                   │
                   ▼
             HSIE instantiation
                   │
                   ▼
             physical SK exists
                   │
                   ▼
             HSIE destruction
                   │
                   ▼
          historical SK destroyed
                   │
                   │ FUTURE
                   ▼
           claimant possesses SK
                   │
             ┌─────┴─────┐
             ▼           ▼
       Sign(SK, M)    optional SK disclosure
             │           │
             ▼           ▼
             σ       H(D || E(SK))
             │           │
             ▼           ▼
       Verify(PK)       compare with C
```

The commitment remains separate from the signature:

```text
Digital signature:
    σ = Sign(SK, M)

Historical-secret commitment:
    C = H(D || E(SK))
```

The commitment does not become a second authentication mechanism.

---

# 16. D018 Implementation-Level Construction

TAP-D018 is frozen conceptually and its implementation-level requirements are now defined. These requirements do not replace or broaden the frozen D018 architecture.

## 16.1 Technology neutrality

TAP-001 shall not be normatively dependent on a particular key-management, storage, transport, archival, or container technology.

The protocol distinguishes three separate concepts:

```text
1. Cryptographic identity
   = the exact designated secret signing key SK

2. Canonical TAP representation
   = E(SK)

3. Storage / transport representation
   = any implementation technology used to retain or transport SK
```

Only the first two define the D018 commitment input.

A storage or transport technology such as OpenPGP, a hardware-backed key store, a raw archival file, or a future technology does not itself define the D018 commitment input.

### OpenPGP status

OpenPGP/PGP is an available present-day implementation and archival technology for the current experimental work. It is **not** a TAP-001 protocol requirement.

The appropriate relationship is:

```text
TAP-001
  D018 secret-key commitment
        │
        ├── TAP-defined requirements
        │
        └── current implementation
              └── OpenPGP available for storage/transport
```

A TAP-001 verifier shall not be required to implement OpenPGP merely to satisfy D018.

If OpenPGP is documented in experimental records, it should be identified as an implementation/historical note rather than a normative protocol dependency.

### Long-term archival packaging

The preferred archival model, now frozen as part of D002, is that the published HSIE artifact carries the complete public verification material needed for future authentication rather than depending on a surviving keyserver or other external discovery service. External services MAY provide additional discovery paths, but they are not a durability dependency for the TAP archive.

## 16.2 Frozen D018 commitment construction

The protocol-level construction is:

```text
C = H(D || E(SK))
```

where:

```text
SK = exact designated historical secret signing key
E  = canonical TAP representation of SK
D  = TAP-001/D018/SK-COMMITMENT/v1
H  = selected compliant cryptographic hash function or XOF
C  = commitment value
```

The commitment SHALL be computed from the exact designated secret authentication material itself.

The narrow binding target remains:

```text
SK only
```

The commitment SHALL NOT silently incorporate `PK`, HSIE metadata, timestamps, location, destruction records, protocol parameters, message contents, `Xᵢ`, or `Vᵢ`.

A future expansion of the binding scope would require an explicit new design decision rather than being inferred from D018.

## 16.3 Hash-algorithm selection

TAP-001 shall remain hash-algorithm agile. D018 shall not permanently mandate one hash algorithm.

The selected hash construction SHALL:

1. be a cryptographic hash function or XOF standardized or otherwise approved by a recognized contemporary cryptographic standards authority;
2. have no publicly known practical preimage attack applicable to the selected security level;
3. provide sufficient security against classical and relevant foreseeable quantum attacks;
4. provide at least the security strength required by the intended TAP-001 archival lifetime;
5. have a stable public specification;
6. have independently maintained implementations;
7. have publicly documented test vectors;
8. remain considered suitable for new cryptographic applications by the relevant standards authority at deployment time; and
9. have no known structural weakness making it inappropriate for long-term archival commitments.

The deployed commitment record SHALL identify the exact hash algorithm and relevant parameters used.

### Security target

The recommended protocol target is at least **256-bit classical preimage-security strength**, with the selected construction also assessed for relevant quantum preimage resistance.

This is a security requirement rather than a permanent algorithm selection.

The phrase "post-quantum hash algorithm" shall not be used as though it were a formal algorithm class equivalent to a post-quantum signature scheme. D018 instead requires an appropriate contemporary cryptographic hash/XOF construction whose classical and quantum security properties are acceptable for the intended archival lifetime.

## 16.4 Canonical secret-key representation

The D018 commitment SHALL be computed from a canonical representation of the designated cryptographic secret signing key itself.

The representation `E(SK)` SHALL be:

- deterministic;
- canonical;
- unambiguous;
- reproducible by an independent verifier;
- explicitly versioned or otherwise identified;
- defined independently of storage/container technology where practical.

The protocol does not permanently select one serialization technology at this stage.

Three implementation approaches were evaluated:

### Approach A — Algorithm-native canonical representation

```text
SK
 ↓
algorithm-specific canonical representation
 ↓
bytes
 ↓
H(D || bytes)
```

This is the preferred long-term conceptual architecture because it commits to the cryptographic key itself rather than to a particular container technology.

### Approach B — Generic protocol-defined structured representation

TAP-001 may define a technology-neutral structured representation containing the cryptographic algorithm identifier, relevant parameters, and secret-key material, followed by a deterministic canonical encoding.

A deterministic binary representation such as canonical CBOR is a possible implementation candidate, but no specific serialization technology is required by this current project state.

### Approach C — External technology/container with extraction of SK

A technology such as OpenPGP may be used to generate, store, transport, or archive the key. The exact designated `SK` is then extracted or otherwise identified and passed through the TAP canonical representation before commitment:

```text
external container
        ↓
exact designated SK
        ↓
E(SK)
        ↓
H(D || E(SK))
```

This is the practical model for the current experiment because OpenPGP is available now while TAP-001 remains technology-neutral.

### Critical distinction

The following must not be conflated:

```text
cryptographic key identity
        ≠
file/container identity
        ≠
storage technology identity
```

The D018 commitment is about the first item, represented canonically by the second-stage function `E(SK)`.

## 16.5 Domain separation

A domain separator identifies the semantic purpose of a cryptographic construction. It prevents a D018 commitment from being confused with another use of the same hash primitive.

The D018 domain separator is frozen as the UTF-8 encoding of:

```text
TAP-001/D018/SK-COMMITMENT/v1
```

Thus:

```text
D = UTF8("TAP-001/D018/SK-COMMITMENT/v1")
```

and:

```text
C = H(D || E(SK))
```

The domain separator is public. It is not a secret, password, key, or source of entropy.

The domain separator SHALL remain independent of the selected hash algorithm. The hash algorithm and parameters are recorded separately.

## 16.6 Commitment record

The initial D018 commitment record SHALL contain enough information to reproduce and verify the commitment construction later.

Conceptual structure:

```text
D018 Commitment Record
│
├── commitment_version
├── hash_algorithm
├── hash_parameters
├── domain_separator
├── secret_key_encoding
├── commitment_value
└── public_key_identifier
```

### Required cryptographic information

The record SHALL identify:

```text
commitment_version
hash_algorithm
hash_parameters (when applicable)
domain_separator
secret_key_encoding / encoding version
commitment_value
```

### Associated-key identification

The record SHOULD identify the associated public verification key, preferably through a stable public-key fingerprint or equivalent identifier.

The public-key identifier is metadata identifying the associated authentication key. It is **not** part of the D018 commitment input under the current narrow binding decision.

### Optional archival metadata

The broader TAP archival record may also carry information such as:

```text
record_id
creation_time
implementation_identifier
implementation_version
encoding_parameters
```

Such metadata is not part of the D018 commitment calculation unless a future explicit decision changes the binding scope.

## 16.7 Minimum information required for later cryptographic verification

For the D018 commitment itself, a later verifier minimally needs:

```text
1. commitment_value C
2. hash_algorithm
3. hash_parameters, when applicable
4. domain_separator D
5. secret_key_encoding identifier/version
6. the candidate secret signing key SK_future
```

The verifier then computes:

```text
C' = H(D || E(SK_future))
```

and compares:

```text
C' == C
```

If equal, the candidate key corresponds to the committed key, subject to the security and correctness properties of the selected hash construction and canonical encoding.

The D018 cryptographic minimum is distinct from the broader evidentiary archive. A complete TAP record additionally needs enough historical and protocol information to establish what the commitment means and how it relates to the HSIE and authentication record.

## 16.8 D018 correspondence boundary

A successful commitment match establishes:

```text
candidate SK
     │
     ▼
corresponds to committed SK
```

It does not establish:

```text
exclusive possession
absence of copying
historical custody by only one entity
temporal displacement
```

D018 therefore remains an auxiliary cryptographic correspondence mechanism, not a replacement for HSIE documentation or signature verification.

---

# 17. Current Claim Boundary

TAP-001 can currently be described as providing a framework in which:

1. designated secret authentication material can be associated with a bounded historical physical event;
2. that secret can be physically instantiated and subsequently destroyed as part of the HSIE;
3. a corresponding public verification key can remain available;
4. a future claimant possessing the secret can authenticate a message without disclosing the secret;
5. the authenticated message can contain independently testable evidence claims;
6. investigators can independently generate observations from those claims;
7. an optional commitment can provide an independently verifiable correspondence check for subsequently disclosed key material;
8. the complete evidentiary record can later be used for a temporal-contact assessment.

The protocol does **not** currently establish:

- that a future claimant actually exists;
- that temporal displacement is physically possible;
- that a signature proves temporal displacement;
- that a commitment proves temporal displacement;
- that historical custody proves exclusive possession;
- that no copy of the historical secret existed;
- that any particular future evidence phenomenon exists;
- that any specific cryptographic algorithm is appropriate;
- that any particular `Xᵢ` will successfully distinguish temporal contact from alternative explanations.

---

# 18. Conceptual Core

The current TAP-001 conceptual core is:

```text
                         HISTORICAL
                             │
                             ▼
                     ┌───────────────┐
                     │      HSIE     │
                     │               │
                     │ SK instantiated
                     │      ↓        │
                     │ SK destroyed  │
                     └───────┬───────┘
                             │
                       ┌─────┴─────┐
                       │           │
                       ▼           ▼
                      PK           C
                       │           │
                       │           └────► optional commitment
                       │
                       ▼
                 Future signature
                       │
                       ▼
                    M + σ
                       │
                       ▼
                  Verify(PK)
                       │
                       ▼
                Authenticated Xᵢ
                       │
                       ▼
                Independent test
                       │
                       ▼
                      Vᵢ
                       │
                       ▼
                    Analysis
                       │
                       ▼
             Evidence characterization
                       │
                       ▼
          Temporal-contact assessment
```

The central epistemic boundary remains:

```text
SIGNATURE VERIFICATION
        ↓
authenticity of message provenance
        ↓
NOT physical truth of message contents
        ↓
NOT automatic proof of temporal displacement
```

Similarly:

```text
COMMITMENT MATCH
        ↓
correspondence to committed SK
        ↓
NOT exclusive possession
        ↓
NOT absence of copying
        ↓
NOT automatic proof of temporal displacement
```

---

# 19. Current Project Status

## Frozen / Complete

```text
HSIE conceptual definition             COMPLETE
HSIE spacetime boundaries              COMPLETE
HSIE destruction requirement           COMPLETE
Historical-copy limitation             COMPLETE
Record-layer separation                COMPLETE
Authenticated Xᵢ model                 COMPLETE
Independent Vᵢ model                   COMPLETE
Human-accessibility principle          COMPLETE
Human-accessibility operational test  COMPLETE
Asymmetric signature primitive         COMPLETE
Historical key lifecycle               COMPLETE
Optional SK commitment architecture    COMPLETE
D018 hash-selection requirements       COMPLETE
D018 canonical SK representation rules COMPLETE
D018 domain separator                  COMPLETE
D018 commitment record minimum         COMPLETE
D018 cryptographic verification minimum COMPLETE
HSIE archival self-containment of public verification material COMPLETE (FROZEN IN D002)
```


## Approved but Not Frozen

```text
TAP-D049  Future-evidence branch as a distinct semantic pathway
TAP-D050  Authentication precedes authenticated future evidence
TAP-D051  Authenticated Xᵢ cannot be retroactively changed
TAP-D052  Verification remains independent of claimant control
TAP-D053  One Xᵢ may have zero, one, or many Vᵢ records
TAP-D054  Execution failures/deviations are recordable states,
          not automatic conclusions
TAP-D055  Raw observation, analysis, and evidence status remain distinct
TAP-D056  The branch does not itself make the temporal-contact conclusion
TAP-D057  Later evidence cannot rewrite the authenticated Xᵢ
```

These decisions are approved for the current conceptual protocol design but are **not frozen**.


## Approved but Not Frozen

```text
Step 15 temporal-contact assessment
    APPROVED at the approved-design level
    CONCEPTUAL FRAMEWORK NOT FROZEN

TAP-D058 through TAP-D076
    APPROVED / NOT FROZEN

TAP-D078
    Message authentication key resolution through exact HSIE reference
    APPROVED / NOT FROZEN

TAP-D079
    Bidirectional temporal message channel
    APPROVED / NOT FROZEN

```

The Step 15 conceptual framework and D058–D076 are approved for the current protocol design but remain deliberately unfrozen. D078 and D079 are approved but remain deliberately unfrozen. The HSIE archival self-containment requirements are frozen as part of TAP-D002. Final serialization and protocol-wide canonicalization continue in Step 16.

## Open

```text
Exact asymmetric signature algorithm
Exact asymmetric signature parameters
Final TAP canonical message serialization
Detailed HSIE documentation schema beyond the frozen archival self-containment requirements
Detailed authenticated-message field syntax
Outgoing-message signature/encryption composition and exact field syntax
Exact physical mechanism, timing, custody, and evidentiary conditions by which the future endpoint acquires the D079 key-bearing physical medium and recovers both private keys
Request/response binding, nonce/challenge, replay, and duplicate-response handling
Temporal-channel addressing/discovery and transport assumptions
Future-response delivery and archival-record handling
Exact Vᵢ serialization and field-level syntax
Vᵢ investigator identity / independence criteria
Vᵢ raw-data archival requirements
Vᵢ timestamp / location requirements
Vᵢ integrity and provenance mechanisms
Exact analysis-record representation
Future-evidence branch implementation/formalization details
Cross-layer final serialization and canonicalization for Step 16
Final TAP-001 specification
```

Step 15 is complete at the approved-design level. Final exact serialization and remaining Step 16 implementation-level details remain open.

# 20. Recommended Development Order

The development sequence reflects the current state through the Step 16 specification baseline, the v21 → v22 frozen HSIE archival-definition amendment, the v22 → v23 message-schema refinement, and the v23 → v24 bidirectional-channel extension:

1. ~~Freeze HSIE concept~~ — **COMPLETE**
2. ~~Define TAP-001 structural record layering~~ — **COMPLETE**
3. ~~Define crypto lifecycle/primitive~~ — **COMPLETE**
4. ~~Define optional cryptographic commitment~~ — **COMPLETE (D018 FROZEN)**
5. ~~Define remaining D018 commitment construction details~~ — **COMPLETE**
6. ~~Define location/time/destruction documentation requirements~~ — **COMPLETE**
7. ~~Define detailed authenticated message schema~~ — **COMPLETE**
8. ~~Define detailed `Xᵢ` schema~~ — **COMPLETE (D028–D033 APPROVED)**
9. ~~Formalize human accessibility~~ — **COMPLETE**
10. ~~Survey present-day and approximately 20-year no-cost verification techniques~~ — **REMOVED AS A REQUIRED TAP-001 DEVELOPMENT STEP**
11. ~~Identify candidate physical phenomena~~ — **REMOVED AS A REQUIRED TAP-001 DEVELOPMENT STEP**
12. ~~Develop falsifiable experimental protocols~~ — **REMOVED AS A REQUIRED TAP-001 DEVELOPMENT STEP**
13. ~~Define detailed `Vᵢ` representation and the `Xᵢ` / `Vᵢ` relationship~~ — **COMPLETE (D039–D048 APPROVED)**
14. ~~Define the future-evidence branch formally~~ — **COMPLETE (D049–D057 APPROVED / NOT FROZEN; implementation/formalization details remain open)**
15. ~~Define temporal-contact assessment~~ — **COMPLETE (APPROVED / NOT FROZEN; conceptual framework and approved implementation/formalization requirements complete)**
16. Produce `TAP_001_SPECIFICATION.md` — **IN PROGRESS (baseline produced; review/refinement ongoing)**

The Step 16 review/refinement now includes formalizing the optional bidirectional temporal message channel under TAP-D079, including the signed outgoing-request structure, encryption of the HSIE-embedded `associated_outgoing_message.message_content` using the public encryption material contained in the HSIE, the colocated historical private signing key and private encryption key on one physical medium, the joint physical destruction of both private keys as part of the same destruction event of that medium, corresponding future endpoint acquisition of that medium, future private-key decryption, exact request/response binding, and the distinction between cryptographic message provenance and any independent claim about responder identity, capability, temporal origin, or correctness.

The sender/creator of an authenticated `X_i` is responsible for determining the phenomenon, verification method, apparatus, procedure, evaluation rules, and falsification criteria from the sender's available historical records and other supporting information. TAP-001 therefore does not require the protocol designers to maintain a separate survey of present-day or approximately 20-year verification techniques, select candidate physical phenomena, or develop experimental protocols as mandatory development steps.

Those matters remain part of the content that may be supplied by an `X_i` creator under the already-approved TAP-D010, TAP-D012, and D028–D033 framework. Removing them from the protocol-development sequence does not remove the requirement that an `X_i` be independently testable and operationally self-contained.

Step 14 is complete at the conceptual decision level. Step 15 is complete at the approved-design level. The Step 16 specification baseline has been produced and is under review/refinement. The current active development boundary remains Step 16: review and refine `TAP_001_SPECIFICATION.md`, including final cross-layer serialization/canonicalization, faithful incorporation of the frozen HSIE archival packaging requirements in TAP-D002, formalization of the D078 message authentication-key resolution rule, and formalization of the D079 bidirectional temporal message channel, its HSIE-embedded outgoing-message content, and its single-medium dual-private-key lifecycle.

No step in this sequence implicitly modifies a frozen TAP decision.

---

# 21. Frozen-Definition Change Control

The following rule remains in force:

> Before adopting any future design decision that would alter the meaning or required properties of a frozen TAP decision, explicitly identify the conflict and obtain a deliberate decision to modify the affected frozen definition.

Future design work must distinguish:

```text
FITS WITHIN FROZEN DEFINITION
        versus
REQUIRES MODIFICATION OF FROZEN DEFINITION
```

The discipline applies to TAP-D002 through TAP-D018.

### D018 compatibility check

D018 adds an optional cryptographic artifact and its construction requirements to the existing cryptographic layer. It does not redefine the HSIE.

```text
D018 adds:
    commitment to exact historical SK
    canonical representation requirements
    algorithm-agile hash requirements
    domain separation
    commitment-record requirements

D018 does not redefine:
    what an HSIE is
```

Therefore:

```text
TAP-D002 remains unchanged.
```

The same compatibility result applies to D013, D014, D015, D016, and D017.

### D079 compatibility boundary

D079 extends the HSIE physical-event content and the future message layer with an optional request/response channel. The outgoing message content is intentionally part of the HSIE physical event and its packaged artifact, while retaining a distinct semantic message identity under TAP-D013. The `associated_outgoing_message.message_content` is stored as encrypted ciphertext produced from the public encryption key material contained in the HSIE, so that the corresponding private encryption key can be used by the future endpoint to recover the message content. For D079, the historical private signing key and corresponding private encryption key are colocated on the same physical medium during the HSIE. Neither private key is included in the published HSIE artifact. **Both private keys are destroyed as part of the same physical destruction event of the medium.** The future endpoint is intended to obtain the same physical medium in the future state and recover both private keys; the private encryption key decrypts the embedded outgoing content, while the historical private signing key can support future response signing. D079 does not change the destruction requirement or make cryptographic validity equivalent to physical or temporal conclusions.

```text
D079 adds:
    optional outgoing signed request
    encrypted HSIE-embedded outgoing message content
    required public encryption material in the HSIE when D079 is used
    future private-key decryption of embedded message content
    optional future authenticated response
    exact request/response binding
    application-level computation-request capability

D079 does not establish:
    physical temporal transport
    future responder existence
    responder identity or intelligence level
    correctness of a returned computation
    temporal displacement by cryptographic operation alone
```

Therefore:

```text
D002–D018 frozen semantics remain unchanged.
```

---

# 22. Current Open Design Questions

The open questions below reflect the current v27 state after approval of the Step 15 conceptual framework, D058–D076, the v22 amendment of TAP-D002, the v23 D078 message-schema refinement, the v24 D079 bidirectional-channel extension, the v25 HSIE-embedded outgoing-message refinement, and the v26 D079 encryption correction plus the v27 D079 key-bearing-medium clarification. Questions resolved by earlier approved design work are no longer listed as open.

## Cryptography

1. Which asymmetric signature algorithm should TAP-001 use?
2. Should TAP-001 use a post-quantum signature scheme?
3. Should multiple independent signature schemes be used?
4. What parameter set should be selected?
5. What entropy and key-generation controls are required?
6. What public-key and signature encodings should be used for the embedded archival public key and future signatures?
7. What canonical serialization should define `M`?
8. Should one historical signing key authenticate multiple future messages?
9. Should the protocol constrain the number or timing of authenticated messages?
10. What formal cryptographic threat model should TAP-001 adopt?

## Historical event

11. How should location be represented?
12. How should temporal precision be represented?
13. What custody documentation is required?
14. What destruction evidence should be recorded?
15. How should physical-medium characteristics be recorded?
16. What independent witness or audit mechanisms, if any, are appropriate?

## Authenticated message

17. What additional exact field syntax or representation is required beyond the approved message structure and HSIE-derived authentication-key resolution?
18. How are timestamps represented?
19. How is message identity generated?
20. How are protocol versions represented?
21. How are evidence claims referenced and ordered?

## Xᵢ

22. What exact serialization and field syntax should formalize the approved Xᵢ schema?
23. What constitutes sufficient self-containment?
24. What statistical requirements apply?
25. How should uncertainty and controls be represented?
26. What constitutes a valid falsification criterion?

## Vᵢ

27. What exact serialization and field syntax should formalize the approved `Vᵢ` conceptual representation?
28. What exact investigator identity and independence criteria should apply?
29. How should raw data be archived and referenced?
30. What timestamp, location, and integrity metadata are required?
31. Should analysis records be represented inside `Vᵢ` or as a separate downstream record?
32. What exact vocabulary and formal rules should govern the relationship/status assessment between `Xᵢ` and `Vᵢ`?

## Temporal-contact assessment

The Step 15 conceptual and implementation/formalization questions are resolved at the approved-but-not-frozen design level by TAP-D058 through TAP-D076. Remaining work is final Step 16 specification and cross-layer serialization/canonicalization.

---

# 23. Revision Notes — v22

### State transition from v21

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v21.md**.

```text
v21:
    D077 = APPROVED / NOT FROZEN
    D077 carried the HSIE archival self-containment requirements
        as a separate Step 16 packaging decision
    D002 itself did not yet include those archival requirements
    published HSIE was treated as the preferred durable archival root
    complete public verification material was packaged in the HSIE artifact
    external keyservers/directories were supplementary rather than archival requirements

v22:
    D002 is explicitly amended through frozen-definition change control
    the archival self-containment requirements are incorporated into D002
    published HSIE is the preferred durable archival root
    complete public verification material is packaged directly in the HSIE artifact
    key_identifier, public_key, signature_algorithm, and signature_parameters are
        part of the HSIE authentication-material component
    external keyservers/directories are supplementary discovery mechanisms only
    no external discovery infrastructure is required for long-term archival recovery
    D077 is absorbed into D002 and is no longer an active separate decision
```

### Frozen-definition amendment — TAP-D002

The v22 amendment explicitly incorporates the durable archival properties that had previously been represented separately during Step 16 review. This is a deliberate modification of a frozen definition and is therefore recorded here under frozen-definition change control.

The amended D002 requires, for the published HSIE artifact:

```text
1. The published HSIE artifact is the preferred durable archival root.
2. The complete public verification material required for later TAP authentication
   is packaged directly in the artifact's authentication-material component.
3. That component includes:
       key_identifier
       public_key
       signature_algorithm
       signature_parameters
4. External keyservers/directories/locators may supplement discovery but are not
   required for recovery of the public verification key from the surviving HSIE.
5. The private signing key remains excluded from the published artifact.
```

### D077 disposition

```text
D077 previous state: APPROVED / NOT FROZEN
D077 v22 state:      ABSORBED INTO TAP-D002
```

D077 no longer functions as an independent active design decision because its substantive requirements are now part of the frozen D002 definition.

### Semantic compatibility

```text
D002 historical-event meaning
    preserved

D002 spacetime boundaries
    preserved

D002 custody/access concept
    preserved

D002 destruction requirement
    preserved

D013 semantic record-layer separation
    preserved

D017 independent public-key retention
    preserved

D018 narrow SK-only commitment binding
    preserved
```

The amendment changes the durable packaging requirements of the published HSIE artifact but does not redefine the HSIE as a cryptographic operation, assessment, or temporal-displacement conclusion. Physical co-packaging of authentication material does not collapse the semantic record layers.

### Current-state reconciliation audit

```text
v21 used as immediately preceding canonical source                  → PASS
D002 archival requirements incorporated into frozen definition       → PASS
D002 amendment explicitly treated as deliberate frozen change        → PASS
published HSIE remains preferred durable archival root              → PASS
complete public verification material embedded in HSIE              → PASS
key_identifier embedded                                               → PASS
public_key embedded                                                    → PASS
signature_algorithm embedded                                           → PASS
signature_parameters embedded                                          → PASS
external keyservers/directories not required for archival recovery   → PASS
private signing key excluded from published HSIE                     → PASS
D013 semantic separation preserved                                    → PASS
D017 independent-retention meaning preserved                          → PASS
D018 narrow binding preserved                                         → PASS
D077 not simultaneously active and absorbed                             → PASS
Step 15 remains COMPLETE / APPROVED / NOT FROZEN                     → PASS
D058–D076 remain APPROVED / NOT FROZEN                               → PASS
Step 16 baseline remains produced and under review                    → PASS
final serialization/canonicalization remains open                    → PASS
no separate historical provenance protocol layer introduced          → PASS
no CGUM-001 material introduced                                       → PASS
```

### Independent contradiction / stale-state audit

```text
D002 simultaneously unchanged and amended
    → PASS / v21 is historical; v22 is the current amended frozen definition

D077 simultaneously active and absorbed
    → PASS / D077 is historical and no longer active

Public-key packaging interpreted as semantic layer collapse
    → PASS / physical packaging remains distinct from semantic identity

Independent public-key retention interpreted as requiring a separate file
    → PASS / independence is from the destroyed secret, not from the HSIE artifact

External keyserver treated as a durability dependency
    → PASS / supplementary discovery only

Published HSIE interpreted as containing the private signing key
    → PASS / private key expressly excluded

Step 16 treated as both unstarted and under review
    → PASS / baseline produced; review/refinement ongoing

Open HSIE questions imply the frozen archival packaging requirements are unresolved
    → PASS / remaining HSIE questions concern documentation/detail beyond the frozen requirement

No frozen D003–D018 decision altered without explicit change control
    → PASS / only D002 was deliberately amended in v22
```

### Revision delta

```text
v21 → v22

FROZEN-DEFINITION CHANGE
    TAP-D002 amended to incorporate durable archival self-containment
    of the published HSIE artifact.

ARCHIVAL MODEL
    Published HSIE = preferred durable archival root.

EMBEDDED PUBLIC VERIFICATION MATERIAL
    key_identifier
    public_key
    signature_algorithm
    signature_parameters

EXTERNAL INFRASTRUCTURE
    Keyservers/directories/locators remain supplementary discovery mechanisms.
    Long-term TAP verification does not depend on their survival.

D077 DISPOSITION
    Previous D077 archival-packaging decision absorbed into D002.
    No longer maintained as a separate active decision.

SEMANTIC BOUNDARY
    Physical co-packaging does not collapse TAP-D013 semantic layers.
    D017 remains satisfied because the public key is retained independently
    of the destroyed secret.

NO CHANGE
    D002 event/spacetime/custody/destruction core semantics
    D003–D018 except the explicit D002 archival amendment
    D018 narrow SK-only binding
    D028–D033
    D039–D048
    D049–D057
    D058–D076
    D011 accessibility baseline
    separation of TAP-001 from CGUM-001
```

# 26. Revision Notes — v23

### State transition from v22

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v22.md**.

```text
v22:
    TAP-D002 frozen definition includes durable HSIE archival self-containment
    published HSIE packages complete public verification material
    Step 16 specification baseline produced and under review/refinement
    message schema still carried a separate authentication-key reference

v23:
    redundant message-level authentication-key reference removed
    exact HSIE reference becomes the sole protocol path for resolving the
        public verification material required for message authentication
    no separately surviving AUTHENTICATION_KEY_RECORD is required by TAP
    D078 introduced as APPROVED / NOT FROZEN
    Step 16 message-schema refinement remains under review
```

### D078 decision

```text
TAP-D078
    Message Authentication Key Resolution Through HSIE Reference
    APPROVED / NOT FROZEN
```

The authenticated message now references the exact HSIE record version through `historical_reference.hsie_reference`. The referenced HSIE contains the durable authentication-material component with:

```text
key_identifier
public_key
signature_algorithm
signature_parameters
```

No separate `authentication_key_reference` is required in the message. No separately surviving `AUTHENTICATION_KEY_RECORD` is required for TAP authentication or archival recovery. Implementations may retain auxiliary key records for local convenience, but such records are not protocol archival dependencies.

### Compatibility audit

```text
D002 archival self-containment                    → PRESERVED
D013 semantic layer separation                    → PRESERVED
D016 asymmetric signature requirement             → PRESERVED
D017 public-key retention from destroyed SK       → PRESERVED
D018 narrow SK-only commitment binding             → PRESERVED
D078 introduces no second surviving key artifact  → PASS
Exact HSIE version identifies verification key    → PASS
Message no longer references absent key record    → PASS
External keyserver dependence remains prohibited → PASS
Private signing key remains excluded              → PASS
No separate historical provenance layer introduced → PASS
TAP-001 remains separate from CGUM-001            → PASS
```

### Independent contradiction / stale-state audit

```text
Message requires separate AUTHENTICATION_KEY_RECORD
    → PASS / removed in v23

Message authentication_key_reference points to surviving record
    → PASS / removed in v23

HSIE public key is merely a discovery pointer
    → PASS / complete public verification material is embedded

D078 collapses cryptographic and historical semantic layers
    → PASS / physical packaging and semantic identity remain distinct

D002 and D017 conflict over public-key retention
    → PASS / D017 retention is satisfied by embedded public verification material

D078 changes frozen D002 meaning without control
    → PASS / D078 refines message resolution and does not alter D002

Step 16 simultaneously complete and unstarted
    → PASS / specification baseline exists; review/refinement continues
```

### Revision delta

```text
v22 → v23

MESSAGE SCHEMA
    Removed `authentication_context.authentication_key_reference`.
    Exact `historical_reference.hsie_reference` now provides the sole
    protocol path to the authentication material required for verification.

RECORD MODEL
    An independently surviving `AUTHENTICATION_KEY_RECORD` is no longer
    required by TAP. Authentication-key data is physically packaged inside
    the published HSIE artifact as its authentication-material component.

NEW DECISION
    D078 — APPROVED / NOT FROZEN

OPEN WORK
    Exact message field syntax and final cross-layer serialization remain
    Step 16 review items.

NO CHANGE
    HSIE event definition and archival requirements in D002
    D003–D018 frozen semantics other than no semantic change
    D028–D033
    D039–D048
    D049–D057
    D058–D076
    D011 accessibility baseline
    TAP-001 / CGUM-001 separation
```

# 27. Revision Notes — v24

### State transition from v23

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v23.md**.

```text
v23:
    D078 = APPROVED / NOT FROZEN
    authenticated messages resolve their public verification material
        through the exact HSIE reference
    no separate AUTHENTICATION_KEY_RECORD is required
    Step 16 message-schema refinement remains in progress

v24:
    D079 = APPROVED / NOT FROZEN
    TAP-001 may support a logical bidirectional temporal message channel
    outgoing requests may be signed with historical SK and encrypted to
        the future endpoint's public encryption key
    future responses may reference the exact request and be signed with
        the corresponding historical signing key
    the channel is a protocol/message-layer capability, not proof of a
        physical temporal transport, responder identity, intelligence level,
        or computational correctness
    application-level computation requests are explicitly recognized as
        a use case, with correctness remaining independently assessable
```

### D079 decision

```text
TAP-D079
    Bidirectional Temporal Message Channel
    APPROVED / NOT FROZEN
```

The channel uses the existing TAP key hierarchy rather than introducing a second historical trust root. The historical Ed25519 private signing key signs the outgoing request and may sign a future response; the associated public encryption subkey may be used to address the future endpoint. The future endpoint's private encryption key is not included in the HSIE artifact.

The outgoing request is intended to be constructed and signed while the historical signing key is available, after which the historical signing key may be destroyed according to D004/D017. The future response references the exact embedded outgoing message through the HSIE record version and message identifier so that the response can be verified against the same durable public key material.

### Compatibility audit

```text
D001 historical/future-evidence separation            → PRESERVED
D002 HSIE historical-event definition                  → PRESERVED
D004 historical secret destruction                     → PRESERVED
D005 authentication/evidence separation                → PRESERVED
D009 future evidence remains authenticated content     → PRESERVED
D013 semantic record-layer separation                  → PRESERVED
D014 signature authenticates content provenance only   → PRESERVED
D016 asymmetric signature lifecycle                    → PRESERVED
D017 public-key retention                              → PRESERVED
D018 narrow SK-only commitment binding                  → PRESERVED
D078 exact HSIE-based key resolution                   → PRESERVED
D079 adds optional channel without new trust root      → PASS
D079 does not assert responder identity/intelligence   → PASS
D079 does not equate signature with correctness        → PASS
No separate physical-temporal transport asserted      → PASS
TAP-001 remains separate from CGUM-001                → PASS
```

### Independent contradiction / stale-state audit

```text
Outgoing request treated as post-HSIE signing operation
    → PASS / D079 requires construction and signing while SK is available

Outgoing encryption described as private-key encryption
    → PASS / schema distinguishes private-key signing from recipient-public-key encryption

Future response lacks binding to the outgoing request
    → PASS / exact request reference and response binding are required

Future response automatically proves a "superior intelligence"
    → PASS / responder identity/capability remains outside cryptographic assertion

Authenticated response automatically proves computational correctness
    → PASS / correctness remains subject to independent verification/assessment

D002 accidentally absorbs message semantics into HSIE event semantics
    → PASS / outgoing message content is intentionally part of the HSIE physical event while retaining distinct message-layer semantics under D013

D018 expands beyond exact historical SK
    → PASS / channel artifacts do not modify D018 input scope

D078 becomes redundant or contradictory
    → PASS / response verification still resolves through exact HSIE reference

Frozen definitions D001–D018 modified silently
    → PASS / D079 explicitly records compatibility with frozen boundaries
```

### Revision delta

```text
v23 → v24

MESSAGE / CHANNEL MODEL
    Added D079 defining an optional logical bidirectional temporal message channel.
    Added signed/encrypted outgoing-request semantics.
    Added exact request/response binding for future responses.

CRYPTOGRAPHIC SEMANTICS
    Historical private signing key remains the signing mechanism.
    Future-endpoint encryption uses the recipient public encryption key;
        the corresponding private encryption key remains outside HSIE.
    Future responses may reuse the historical signing key for authentication,
        preserving D078's exact-HSIE public-key resolution path.

APPLICATION CAPABILITY
    Added computation-request use case, including problems whose solutions
    are unavailable to the present implementation environment.
    Explicitly retained independent evaluation of answer correctness and
    responder identity/capability.

FROZEN-DECISION AUDIT
    D001–D018 unchanged.
    D078 retained and extended by D079 without a second trust root.

STEP 16
    Specification refinement scope expanded to include the bidirectional
    message-channel schema and its cryptographic/request-response rules.
```

---

# 24. Status Statement

**TAP-001 is currently a conceptual protocol design with frozen architectural and epistemic boundaries, a frozen optional D018 historical-secret commitment architecture, frozen protocol-level D018 construction requirements, approved Step 7 authenticated-message schema and Step 8 Xᵢ schema decisions D028–D033, a completed Step 9 human-accessibility operationalization, approved Step 13 conceptual `Vᵢ` / `Xᵢ`–`Vᵢ` relationship decisions D039–D048, an approved but not frozen Step 14 future-evidence branch with D049–D057, and frozen HSIE archival self-containment requirements incorporated into TAP-D002, plus the approved but not frozen D078 message authentication-key resolution rule and D079 bidirectional temporal message-channel rule, including the HSIE-embedded encrypted outgoing-message content model. Step 15 is **COMPLETE at the approved-design level and NOT FROZEN**. D058 through D076, D078, and D079 are **APPROVED / NOT FROZEN**. The `TAP_001_SPECIFICATION.md` baseline has been produced and is currently under review/refinement; it is not yet treated as the final frozen specification. The D079 key-bearing-medium clarification is part of the current approved-but-not-frozen design state.**

The approved future-evidence branch remains:

```text
Future TAP message
      ↓
Cryptographic authentication
      ↓
Authenticated X₁ ... Xₙ
      ↓
Independent execution
      ↓
V₁ ... Vₙ
      ↓
Downstream analysis
      ↓
Evidence characterization
      ↓
Temporal-contact assessment
          Step 15
```

The approved Step 15 temporal-contact assessment design is:

```text
HSIE-related historical information and records ────────┐
                                                         │
Cryptographic authentication → Authenticated Xᵢ → Vᵢ   │
                                               → Analysis
                                               → Evidence characterization
                                                         │
                                                         ▼
                                          Temporal-contact assessment
```

Historical information and records associated with the HSIE are assessment inputs. They are not a separate named TAP protocol layer.

Step 15 now has an approved, not-frozen design that includes:

```text
D058–D067
    approved conceptual temporal-contact framework

D068–D076
    approved implementation/formalization requirements
```

The Step 15 approved design establishes, at the current level:

```text
H_TC
    minimum unambiguous representation

H_Ai
    simple explicit alternative representation

assessment characterization
    SUPPORTS
    CONTRADICTS
    DOES_NOT_DISTINGUISH
    UNRESOLVED

dependent evidence
    explicitly identified and not double-counted as independent

assessment lifecycle
    append-only, monotonically versioned

assessment methodology
    requirement-based and method-non-prescriptive

assessment record
    conceptual structure retained with proposed UTF-8/JSON profile,
    globally unique identifiers, versioning, and exact source references

uncertainty
    structured and first-class

review
    receiver is responsible; no mandatory independent third-party
    reviewer or assistance disclosure
```

The remaining work is now Step 16 review/refinement. In particular, Step 16 must select/finalize the exact serialization and cross-layer canonicalization, reconcile all remaining protocol schemas into one final specification, ensure the final specification incorporates the frozen HSIE archival packaging requirements in TAP-D002, and complete `TAP_001_SPECIFICATION.md`.

The following remain open for Step 16:

```text
Exact asymmetric signature algorithm
Exact asymmetric signature parameters
Final TAP canonical message serialization
Detailed HSIE documentation schema
Detailed authenticated-message field syntax
Exact Vᵢ serialization and field-level syntax
Vᵢ investigator identity / independence criteria
Vᵢ raw-data archival requirements
Vᵢ timestamp / location requirements
Vᵢ integrity and provenance mechanisms
Exact analysis-record representation
Exact future-evidence serialization and execution-status vocabulary
Encrypted outgoing-message content representation and cryptographic-envelope serialization
Request/response binding and anti-replay semantics
Exact physical mechanism, timing, custody, and evidentiary conditions for future endpoint acquisition of the D079 key-bearing physical medium and recovery of both private keys
Temporal-channel addressing and delivery assumptions
Handling/archive status of unauthenticated future messages
Cross-layer final serialization/canonicalization
Final TAP-001 specification
```

The sender/creator determines the substantive phenomenon, verification technique, experimental procedure, and falsification criteria embodied in a particular `Xᵢ`, using the sender's historical records and supporting information. These are not separate TAP-001 development deliverables.

The current design boundary is:

> **Review and refine `TAP_001_SPECIFICATION.md` — Step 16.**

The specification baseline has been produced. Step 15 is complete at the approved-design level. Its conceptual framework and D058–D076 are approved but not frozen, D078 and D079 are approved but not frozen, and the HSIE archival self-containment requirements are frozen as part of TAP-D002. No frozen TAP definition should be modified without explicit frozen-definition change control. The active Step 16 boundary now includes formalization of the optional bidirectional temporal message channel, the HSIE-embedded encrypted outgoing-message content, corresponding future private-key decryption, and its request/response provenance rules.

# 28. Revision Notes — v25

The following section records the v25 state for historical traceability. Its confidentiality interpretation is superseded by v26.

### State transition from v24

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v24.md**.

```text
v24:
    D079 = APPROVED / NOT FROZEN
    outgoing request modeled as a distinct MESSAGE_RECORD associated with HSIE
    HSIE carried only an archival association to that message

v25:
    D079 retained as APPROVED / NOT FROZEN and semantically refined
    associated_outgoing_message.message_content becomes the distinct outgoing
        message text physically instantiated as part of the HSIE event
    the outgoing message content is packaged with the HSIE artifact
    future response remains a distinct MESSAGE_RECORD
    future response binds to the embedded outgoing message by exact HSIE record
        version and embedded message_id rather than a separate request record
```

### D079 refinement

```text
TAP-D079
    Bidirectional Temporal Message Channel
    APPROVED / NOT FROZEN

Refinement:
    associated_outgoing_message.message_content contains distinct message text
    that is packaged with the HSIE artifact and makes the outgoing message part
    of the HSIE physical event.
```

This refinement does not modify the frozen HSIE spacetime, custody, or destruction requirements. The outgoing message remains semantically distinct from the historical authentication material, independent observations, analysis, and temporal-contact assessment under TAP-D013, even though its message content is physically included within the HSIE event/artifact.

Because the message content is intentionally packaged in the HSIE artifact, the embedded message content is archival protocol content rather than confidential material. Where D079 uses encryption, the encrypted representation protects the outgoing transport form to the designated future endpoint; it does not make the already-packaged `message_content` confidential.

### Compatibility audit

```text
D001 historical/future-evidence separation                 → PRESERVED
D002 HSIE historical-event definition                       → PRESERVED
D003 HSIE spacetime boundaries                              → PRESERVED
D004 historical secret destruction                          → PRESERVED
D005 authentication/evidence separation                     → PRESERVED
D009 future evidence as authenticated content               → PRESERVED
D013 semantic record-layer separation                       → PRESERVED
D014 signature authenticates content provenance only        → PRESERVED
D015 independent observations remain distinct                → PRESERVED
D016 asymmetric signature requirement                       → PRESERVED
D017 public verification-key retention                      → PRESERVED
D018 narrow SK-only commitment binding                      → PRESERVED
D078 exact HSIE-based key resolution                        → PRESERVED
D079 embedded outgoing message content                       → PASS
No second historical trust root                             → PASS
Future response remains distinct MESSAGE_RECORD             → PASS
Exact response binding to embedded outgoing message         → PASS
No claim that encryption itself proves temporal transport   → PASS
No claim that response signature proves correctness         → PASS
TAP-001 remains separate from CGUM-001                      → PASS
```

### Independent contradiction / stale-state audit

```text
HSIE only archives a reference to the outgoing message
    → PASS / corrected in v25; message_content is embedded in HSIE

Outgoing request is still a distinct MESSAGE_RECORD
    → PASS / corrected in v25; embedded outgoing message is an HSIE component

Outgoing message is outside the HSIE physical event
    → PASS / corrected in v25; message_content is part of the HSIE physical event

D079 says encrypted content is confidential even though message_content is archived
    → PASS / encryption is transport protection; embedded message_content is archival

Future response references a non-existent request record
    → PASS / response binds to exact HSIE version + embedded message_id

D013 semantic separation is lost because message content is physically embedded
    → PASS / physical packaging and semantic identity remain distinct

D002 frozen event boundaries are changed silently
    → PASS / D079 refinement remains within existing bounded physical-event semantics

D018 commitment input expands to message content
    → PASS / D018 remains bound only to exact designated historical SK

No other frozen D001–D018 decision is altered
    → PASS
```

### Revision delta

```text
v24 → v25

HSIE-EMBEDDED OUTGOING MESSAGE
    previous associated outgoing message = archival association
        → associated_outgoing_message.message_content = distinct message text
          physically instantiated as part of the HSIE event and packaged with
          the HSIE artifact

D079 CHANNEL MODEL
    outgoing request = distinct MESSAGE_RECORD
        → outgoing request = embedded HSIE message component

RESPONSE BINDING
    future response → request MESSAGE_RECORD reference
        → future response → exact HSIE record/version + embedded message_id

CONFIDENTIALITY BOUNDARY
    outgoing-message encryption
        → encrypted transport form distinguished from intentionally archived
          message_content

NO CHANGE
    D001–D018 frozen meanings
    D018 narrow SK-only commitment scope
    D013 semantic separation
    D016/D017 historical signature lifecycle
    D078 HSIE-based authentication-key resolution
    TAP-001 / CGUM-001 separation
```

---

# 29. Revision Notes — v26

### State transition from v25

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v25.md**.

```text
v25:
    D079 treated `associated_outgoing_message.message_content` as
        intentionally archived plaintext and treated encryption as a
        transport-protection mechanism
    outgoing message content was physically part of the HSIE event
    future response remained a distinct MESSAGE_RECORD

v26:
    the v25 confidentiality interpretation is corrected
    `associated_outgoing_message.message_content` is encrypted before
        archival packaging using the public encryption key material
        contained in the HSIE
    the corresponding private encryption key is intended to become
        available to / be discovered by the future endpoint
    the future endpoint decrypts the embedded message content and may
        process the computation/request
    the outgoing request remains part of the HSIE physical event
    the future response remains a distinct MESSAGE_RECORD
    D079 remains APPROVED / NOT FROZEN and is semantically refined
```

### D079 correction

```text
TAP-D079
    Bidirectional Temporal Message Channel
    APPROVED / NOT FROZEN

Corrected outgoing-message confidentiality model:
    `associated_outgoing_message.message_content` is encrypted using
    the public encryption key material contained in the HSIE's embedded
    OpenPGP public key material. The corresponding private encryption key
    is intended to be available to, or discovered by, the future endpoint
    so that the embedded message content can be decrypted.

The outgoing message remains physically instantiated during the HSIE and
its encrypted form is packaged with the HSIE artifact. Encryption does not
remove the message from the HSIE physical event; it protects the message
content from plaintext disclosure until the corresponding future private
encryption key is available.

The historical signing key and the future decryption key have distinct
roles. The historical signing key authenticates the outgoing request; the
corresponding private encryption key decrypts the embedded message content
in the future. For the supplied example OpenPGP key pair, the encryption
role is represented by the Cv25519/X25519 subkey identified by
`7C11A43BA5060409`, while the Ed25519 primary key remains the signing key.
```

### Compatibility audit

```text
D001 historical/future-evidence separation                 → PRESERVED
D002 HSIE historical-event definition                       → PRESERVED
D003 HSIE spacetime boundaries                              → PRESERVED
D004 historical secret destruction                          → PRESERVED
D005 authentication/evidence separation                     → PRESERVED
D009 future evidence as authenticated content               → PRESERVED
D013 semantic record-layer separation                       → PRESERVED
D014 signature authenticates content provenance only        → PRESERVED
D015 independent observations remain distinct                → PRESERVED
D016 asymmetric signature requirement                       → PRESERVED
D017 public verification-key retention                      → PRESERVED
D018 narrow SK-only commitment binding                      → PRESERVED
D078 exact HSIE-based key resolution                        → PRESERVED
D079 outgoing message physically embedded in HSIE            → PRESERVED
D079 outgoing message content confidentiality               → CORRECTED
No requirement for plaintext archival disclosure            → PASS
Public encryption key is recoverable from HSIE               → PASS
Future private encryption key can decrypt outgoing content   → PASS
Historical signing key and future decryption key roles differ → PASS
Future response remains a distinct MESSAGE_RECORD             → PASS
No second historical trust root                             → PASS
No claim that encryption proves temporal transport           → PASS
No claim that response signature proves correctness           → PASS
TAP-001 remains separate from CGUM-001                      → PASS
```

### Independent contradiction / stale-state audit

```text
`message_content` is plaintext in the surviving HSIE artifact
    → PASS / corrected in v26; surviving `message_content` is encrypted ciphertext

Encryption is merely transport protection after archival publication
    → PASS / corrected in v26; encryption is applied to the outgoing message content before HSIE packaging

The HSIE lacks the public key needed for outgoing-message encryption
    → PASS / the required public encryption material is contained in the HSIE's embedded OpenPGP public key material

The future endpoint receives only plaintext archival content
    → PASS / future endpoint must obtain the corresponding private encryption key to decrypt the embedded content

Historical signing key and future decryption key are conflated
    → PASS / signing and decryption are explicitly distinct cryptographic roles

D004/D017 require the future endpoint to possess the destroyed historical signing secret
    → PASS / the future decryption key is a distinct encryption-key role; the historical signing key lifecycle remains unchanged

D018 commitment input expands to encrypted message content
    → PASS / D018 remains bound only to the exact designated historical signing key

Frozen definitions D001–D018 modified silently
    → PASS / D079 remains an approved, not-frozen refinement and no frozen definition is changed
```

### Revision delta

```text
v25 → v26

CONFIDENTIALITY MODEL
    v25: message content intentionally archived as plaintext; encryption
         treated as transport protection
    v26: message content is encrypted before HSIE packaging using the
         public encryption material contained in the HSIE; corresponding
         future private encryption key decrypts the content

D079 CRYPTOGRAPHIC ROLES
    historical signing key → signs outgoing request
    HSIE public encryption material → encrypts outgoing message content
    future private encryption key → decrypts outgoing message content

HSIE CONTENT
    outgoing message remains part of the HSIE physical event
    encrypted message content is part of the surviving HSIE artifact

TWO-WAY PROTOCOL
    outgoing encrypted request → future endpoint decrypts/processes →
    future authenticated response MESSAGE_RECORD

NO CHANGE
    D001–D018 frozen meanings
    D018 narrow SK-only commitment scope
    D013 semantic separation
    D016/D017 historical signing-key lifecycle
    D078 HSIE-based authentication-key resolution
    future response remains a distinct MESSAGE_RECORD
    TAP-001 / CGUM-001 separation

CORRECTIVE NOTE
    v25 contained an incorrect statement that the embedded message content
    was not confidential. That interpretation is superseded by v26.
```

The corrected D079 model is now the active project-state interpretation and supersedes the v25 confidentiality statement. The specification remains under Step 16 review and must be reconciled to this corrected D079 state before it is treated as final.


---

# 30. Revision Notes — v27

### State transition from v26

The immediately preceding canonical state was **TAP_001_PROJECT_STATE_v26.md**.

```text
v26:
    D079 outgoing message_content is encrypted before HSIE packaging
    using public encryption material contained in the HSIE
    corresponding private encryption key is intended to become available to /
        be discovered by the future endpoint for decryption
    historical signing key and future decryption key have distinct cryptographic roles
    the historical signing-key lifecycle remains otherwise described through D017

v27:
    D079 explicitly defines a single key-bearing physical medium for the two
        private keys used by the bidirectional channel:
            • historical private signing key (SK)
            • corresponding private encryption key
    both private keys are physically colocated on that same medium during the HSIE
    neither private key is included in the published HSIE artifact
    both private keys are destroyed as part of the same physical destruction event
        of the medium
    the future endpoint is intended to obtain the same physical medium in the
        future state and recover both private keys from it
    private encryption key → decrypts the embedded outgoing request
    historical private signing key → retains signing function and may sign the
        future response
    exact future acquisition mechanism, timing, custody, and evidentiary conditions
        remain open for Step 16 formalization
```

### D079 key-bearing-medium clarification

```text
TAP-D079
    Bidirectional Temporal Message Channel
    APPROVED / NOT FROZEN

D079 key-bearing physical medium:
    The historical private signing key and the corresponding private encryption
    key are held on the same physical medium during the HSIE.

    Neither private key is included in the published HSIE artifact.

    Both private keys are destroyed as part of the same physical destruction
    event of the medium.

    The future endpoint is intended to obtain the same physical medium in the
    future state and recover both private keys from it.

    The private encryption key is used to decrypt the embedded outgoing
    message content. The historical private signing key retains its signing
    function and may be used by the future endpoint to sign a future response.

    This clarification does not assert a physical temporal transport mechanism,
    responder identity, computational correctness, or temporal displacement.
```

### Compatibility audit

```text
D001 historical/future-evidence separation                    → PRESERVED
D002 HSIE historical-event definition                          → PRESERVED
D003 HSIE spacetime boundaries                                 → PRESERVED
D004 historical secret destruction                             → PRESERVED / jointly instantiated private keys now explicitly share the same physical destruction event under D079
D005 authentication/evidence separation                        → PRESERVED
D009 future evidence as authenticated content                  → PRESERVED
D013 semantic record-layer separation                          → PRESERVED
D014 signature authenticates content provenance only             → PRESERVED
D015 independent observations remain distinct                   → PRESERVED
D016 asymmetric signature requirement                            → PRESERVED
D017 public verification-key retention                           → PRESERVED / future SK availability is already represented by D017's lifecycle model
D018 narrow SK-only commitment binding                           → PRESERVED
D078 exact HSIE-based key resolution                             → PRESERVED
D079 outgoing message physically embedded in HSIE                 → PRESERVED
D079 outgoing message content confidentiality                    → PRESERVED
D079 historical SK and private encryption key physically colocated → CLARIFIED
D079 joint destruction of both private keys                       → CLARIFIED
D079 future endpoint acquisition of key-bearing medium             → CLARIFIED / exact physical mechanism remains open
No private key added to published HSIE artifact                    → PASS
Future private encryption key remains the decryption key           → PASS
Historical SK remains the signing key                              → PASS
Future response remains a distinct MESSAGE_RECORD                  → PASS
No second historical trust root                                    → PASS
No claim that encryption proves temporal transport                 → PASS
No claim that response signature proves correctness                 → PASS
TAP-001 remains separate from CGUM-001                             → PASS
```

### Independent contradiction / stale-state audit

```text
D079 says the private encryption key is external to the HSIE and separately provisioned
    → PASS / the private encryption key is physically on the same key-bearing medium as SK;
      neither private key is included in the published HSIE artifact

D079 says the future endpoint may discover only the private encryption key
    → PASS / current model requires future endpoint acquisition of the physical medium
      containing both private keys; the exact acquisition mechanism remains open

Historical SK is destroyed but later future-response signing requires it
    → PASS / D017 already models future claimant possession of SK; v27 clarifies
      that SK and the private encryption key share the same physical medium and
      joint physical destruction event

Private encryption key is described as the signing key
    → PASS / decryption and signing roles remain distinct

The two private keys have independent physical destruction events
    → PASS / v27 explicitly requires one common physical destruction event of the medium

The published HSIE artifact contains either private key
    → PASS / both private keys are excluded from the published artifact

The outgoing message is plaintext in the surviving HSIE artifact
    → PASS / v26 correction remains active; surviving content is encrypted ciphertext

D018 commitment scope expands to include the encryption key or medium
    → PASS / D018 remains bound only to the exact designated historical SK

Frozen D001–D018 definitions are silently modified
    → PASS / the clarification remains within approved-but-not-frozen D079 and
      does not amend frozen D001–D018

Historical v25/v26 revision text contains obsolete formulations
    → PASS / those statements remain explicitly retained as historical revision history;
      the v27 active state supersedes them
```

### Revision delta

```text
v26 → v27

KEY-BEARING MEDIUM
    v26: future private encryption key intended to become available to / be discovered
         by the future endpoint; historical SK lifecycle described separately
    v27: historical private signing key and private encryption key are explicitly
         colocated on one physical medium during the HSIE

DESTRUCTION
    v26: historical SK destruction remained explicit; encryption-key destruction
         was not physically coupled in the D079 text
    v27: both private keys are destroyed as part of the same physical destruction
         event of the medium

FUTURE ACQUISITION
    v26: future endpoint may obtain/discover the private encryption key
    v27: future endpoint is intended to obtain the same physical medium and recover
         both private keys from it

CRYPTOGRAPHIC ROLES
    historical SK → signs outgoing request and may sign future response
    private encryption key → decrypts embedded outgoing request

NO CHANGE
    D001–D018 frozen meanings
    D018 narrow SK-only commitment scope
    D013 semantic separation
    D078 HSIE-based authentication-key resolution
    encrypted outgoing message_content model established in v26
    future response remains a distinct MESSAGE_RECORD
    logical, rather than physically asserted, temporal transport boundary
    TAP-001 / CGUM-001 separation

OPEN WORK REMAINING
    exact physical medium representation
    exact physical destruction evidence
    exact timing and mechanism of future medium acquisition
    custody/evidentiary conditions for future recovery of both private keys
    all remaining Step 16 serialization and anti-replay details
```

The v27 clarification is now the active project-state interpretation of the D079 private-key lifecycle. It supersedes any earlier active wording that treated the future private encryption key as separately provisioned without stating that it shares the same physical medium as the historical private signing key. Historical revision sections remain retained for traceability and are not current state.
