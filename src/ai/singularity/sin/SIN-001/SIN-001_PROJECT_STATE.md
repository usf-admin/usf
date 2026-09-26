# SIN-001 Project State

**Project:** SIN-001 — Temporal Experimental Language  
**Baseline:** SIN 0.0.1 Language Specification — SIN Development Baseline  
**State artifact:** `SIN-001_PROJECT_STATE.md`  
**Revision:** 0001  
**Status:** Initial canonical project-state artifact  
**Established:** 2026-09-24

---

## 1. Project Identity

SIN-001 is the programming-language and runtime project for expressing and executing the computational side of protocol/experiment work.

The organizing question for this project is:

> **How do we express and execute the protocol/experiment computationally?**

SIN is a separate project from TAP-001.

---

## 2. Project Boundary

### SIN-001 owns

- SIN language syntax and grammar;
- lexical structure;
- AST and semantic representation;
- type system;
- execution semantics;
- runtime behavior;
- `.sin` program format;
- compiler/toolchain architecture;
- SINC;
- standard-library architecture;
- USF framework/library implementation;
- capability and external-interface mechanisms;
- testing and executable conformance;
- implementation-specific tooling.

### TAP-001 owns

- protocol semantics;
- authentication;
- evidentiary architecture;
- HSIE semantics;
- message provenance;
- formal protocol requirements.

SIN may implement or expose an interface to TAP-001 concepts, but SIN must not silently redefine TAP-001.

Relationship:

```text
TAP-001
  protocol and evidentiary layer
          |
          v
     TAP/SIN interface
          |
          v
SIN-001
  language and runtime layer
          |
          v
   temporal experiment programs
```

---

## 3. Source and Evidence Discipline

The SIN 0.0.1 baseline establishes the following classifications:

- **Demonstrated / Existing** — directly evidenced by supplied SIN source.
- **Proposed** — introduced during development but not established by repository evidence.
- **Required** — necessary for the intended implementation but not evidence that it exists.
- **Theoretical** — named concept/version without established implementation evidence.

Source authority is ordered as:

1. actual source artifacts;
2. executable tests;
3. specifications/design documents;
4. `PROJECT_STATE.md`;
5. conversation history.

Documentation must not silently turn proposals into existing language features.

Historical/target metadata such as `SINC 0.0.1 / 20241020` is not implementation evidence unless implementation and test evidence establishes it.

---

## 4. Baseline Specification

The uploaded baseline is:

**SIN 0.0.1 Language Specification — SIN Development Baseline**

It is divided into six volumes covering Sections 1–30.

The baseline is the authoritative starting point for SIN-001 development unless an explicit subsequent project decision supersedes a provision.

The baseline itself states that it is a working specification and an onboarding/development baseline rather than proof that every proposed subsystem already exists.

---

## 5. Language Identity and Existing Syntax

SIN is intended to be a general-purpose programming language supporting a complete implementation of USF.

USF is intended to be implemented as a SIN framework/library rather than compiler-specific functionality.

The demonstrated syntax includes:

```sin
->lib:sin:default
->lib:sin:default:Observer
->lib:sin:default:Time
->lib:sin:default:Location
->lib:sin:USF

framework:USF;
self:Observer;

def name(parameters) {
    ...
}

ret 0;
ret 1, err;

~
    ...
~-> err {
    ...
}
```

Other demonstrated constructs include member/property access, method calls, assignment, arithmetic, concatenation, `wait(...)`, and classified function declarations.

The central compatibility rule is:

> Preserve demonstrated SIN syntax and extend it rather than silently replacing it.

---

## 6. Function Classification

The baseline demonstrates classified functions:

```text
name(parameters):function:internal -> Result
name(parameters):function:external -> Result
name(parameters):function:abstract
```

Current design meanings:

- `internal` — implementation detail used within the component;
- `external` — public callable capability;
- `abstract` — interface/contract whose implementation mechanism is unspecified.

The exact grammar and visibility semantics remain a formalization task.

---

## 7. Inline Semantic Prompt Layer

The syntax:

```text
#! ... !#
```

is a first-class semantic communication channel in the SIN design.

It is intended to remain adjacent to the declaration, function, interface, or semantic unit it governs.

Potential structured fields demonstrated by the baseline include:

- `ReferenceDefinition`
- `HumanModel`
- `HumanDeclaredReality` / `DeclaredReality`
- `ExpectedState`
- `ExpectedBehavior`
- `VerificationTolerance`

These blocks are not intended to be ordinary comments.

They communicate human-authored semantic contracts and are intended to be preserved in AST/IR and exposed to tooling.

They are not magical authority over executable behavior. Formal language rules, type checking, runtime invariants, and explicit authorization remain necessary.

No completed prompt-verification algorithm is established by the baseline.

---

## 8. USF Relationship

The intended architecture is:

```text
SIN
 |
 +-- Standard Library
 |
 +-- USF
 |
 +-- Applications
```

USF services such as logging and error handling remain framework responsibilities rather than compiler magic.

---

## 9. Current Working Grammar

The baseline provides the following working formalization:

```text
CompilationUnit ::= Import* Declaration*

Import ::= "->lib:" Path

Declaration ::= FrameworkDecl
              | VariableDecl
              | FunctionDecl
              | InterfaceDecl
              | RecordDecl

FrameworkDecl ::= Identifier ":" TypeName ";"

VariableDecl ::= Identifier ":" TypeName ";"

FunctionDecl ::= "def" Identifier "(" Parameters? ")" FunctionQualifier? Block

Parameters ::= Parameter ("," Parameter)*

Parameter ::= Identifier

FunctionQualifier ::= ":" "function" ":" ("internal" | "external" | "abstract")

Block ::= "{" Statement* "}"

Statement ::= Assignment
            | CallStmt
            | ReturnStmt
            | ErrorBlock
            | WaitStmt
            | DeclarationStmt
            | ...

ReturnStmt ::= "ret" ExpressionList? ";"

ErrorBlock ::= "~" Statement* "~->" Identifier Block

Assignment ::= Expression "=" Expression ";"

CallStmt ::= CallExpression ";"

WaitStmt ::= "wait" "(" ExpressionList ")" ";"
```

This is explicitly a **working formalization**, not a frozen final grammar.

The ellipsis is intentional.

---

## 10. Type-System Direction

The baseline proposes a progressively stronger type system.

Design/proposal areas include:

- primitive types;
- strings and bytes;
- structured records;
- interfaces;
- objects;
- enums;
- references;
- generics;
- ownership and lifetime;
- resource management;
- Result/error types.

Still open:

- type inference;
- coercion;
- nullability;
- mutability;
- generic constraints;
- variance;
- ownership/borrowing;
- aliasing;
- ABI representation.

The type system must support validating complete domain states before atomic transition.

---

## 11. Runtime and Concurrency Direction

The broader design proposes:

- deterministic resource management;
- explicit object/state semantics;
- threads/tasks/futures/promises;
- async/await;
- mutexes;
- read/write locks;
- atomics;
- channels;
- semaphores;
- reflection;
- runtime type information;
- compile-time evaluation;
- metaprogramming;
- FFI, including C ABI and interoperability with C++, Python, and other environments.

These are design targets, not claims that all are implemented.

Still unspecified:

- concurrency memory model;
- object representation;
- ownership implementation;
- garbage collection/reference counting strategy;
- thread-safety guarantees;
- FFI ABI rules.

---

## 12. Compiler and SINC Architecture

The proposed compiler pipeline is:

```text
SIN source
    |
    v
Lexer
    |
    v
Parser
    |
    v
AST
    |
    v
Semantic analysis
    |
    v
Typed AST
    |
    v
SIN IR
    |
    v
Optimizer
    |
    v
Backend
   / \
native LLVM strategy
        \
       potentially WASM
```

An intermediate representation is preferred to separate language semantics from backend implementation.

**SINC** is the intended compiler/toolchain name.

`SINC 0.0.1 / 20241020` remains historical/target metadata unless implementation and tests establish otherwise.

---

## 13. Standard Library and USF Architecture

The broader standard-library proposal includes facilities such as:

- Core
- Math
- Collections
- String
- Regex
- File
- IO
- Process
- Network
- HTTP
- JSON
- XML
- Time
- Thread
- Async
- Crypto
- Compression
- Database
- Graphics
- Audio
- Image
- scientific functionality

This is proposal-level architecture unless separately established.

USF remains a separate framework/library layer.

---

## 14. Conformance and Testing

Future SIN implementation testing is divided into:

1. syntax conformance;
2. semantic conformance;
3. standard-library conformance;
4. runtime conformance;
5. FFI conformance;
6. USF conformance.

Compiler tests should cover, at minimum:

- lexing;
- parsing;
- name resolution;
- imports;
- expressions;
- functions;
- returns;
- error blocks;
- member access;
- method calls;
- assignments;
- exact parsing of reference SIN files.

Runtime/semantic tests should cover:

- type checking;
- error propagation;
- object state;
- lifetime;
- ownership;
- concurrency;
- FFI boundaries;
- deterministic cleanup.

USF tests should cover:

- Observer construction;
- checkpoints;
- validation;
- atomic execution;
- failure preserving source state;
- recovery as displacement;
- negative temporal displacement as a domain operation.

---

## 15. Development Phases

### Phase 0 — Language specification

Includes:

- SIN Language Specification;
- SIN Grammar;
- SIN Type System Specification;
- SIN Runtime Specification;
- SIN Error Model;
- SIN Module Specification;
- USF integration specification;
- atomic displacement semantics.

Baseline status: substantially drafted.

### Phase 1 — Minimal SINC

Targets:

- lexer;
- parser;
- AST;
- functions;
- variables;
- expressions;
- blocks;
- conditionals;
- loops;
- return;
- basic types;
- imports;
- errors.

Status depends on the current bootstrap/reference artifact and executable verification.

### Phase 2 — Full type system

Objects, structs, enums, generics, references, ownership, resource management.

Status: design/proposal.

### Phase 3 — Standard library

Strings, collections, files, IO, math, time, regex, processes, networking.

Status: design/proposal.

### Phase 4 — Advanced language

Async, threads, channels, reflection, metaprogramming, FFI.

Status: design/proposal.

### Phase 5 — USF

USF, Observer, Time, Location, State, Transaction, TemporalDisplacement.

Status: architecture established; implementation incomplete.

### Phase 6 — Self-hosting

SINC written substantially in SIN.

Status: future.

---

## 16. Explicitly Unresolved Questions

The following remain open until explicit project decisions and, where appropriate, implementation/test evidence resolve them:

1. Exact formal SIN grammar.
2. Exact type-system rules.
3. Exact ownership, lifetime, and aliasing semantics.
4. Exact Result/error propagation semantics.
5. Exact module/package resolution rules.
6. Exact runtime representation of Observer state.
7. Exact API and implementation of TemporalDisplacement.
8. Exact semantics and implementation of USF.Log.
9. Exact semantics and implementation of USF.HandleError.
10. Exact implementation of Observer checkpoints.
11. Whether trajectory data is a first-class abstraction.
12. Exact concurrency memory model.
13. Exact FFI mechanisms and ABI rules.
14. Exact compiler backend strategy.
15. Exact standard-library API surface.
16. Initial SINC bootstrap strategy.
17. Which existing repository portions must be preserved unchanged for compatibility.

These questions must remain visibly open until explicitly resolved.

---

## 17. Locked Decisions Inherited from Baseline

The following decisions are carried into this project state as locked:

- **D001** — USF is implemented in SIN.
- **D002** — Preserve demonstrated SIN syntax.
- **D003** — Separate existing syntax from proposed semantics.
- **D004** — SINC 0.0.1 20241020 is not implementation evidence.
- **D005** — Temporal displacement is atomic.
- **D006** — Validation does not mutate Observer state.
- **D007** — Failed displacement preserves source state.
- **D008** — Recovery is atomic displacement.
- **D009** — Displacement operates on a complete destination state.
- **D010** — Negative temporal displacement is a domain axiom.
- **D011** — Do not invent unsupported physical mechanisms.
- **D012** — Inline prompts are first-class semantic metadata.

---

## 18. SIN/TAP Boundary

SIN-001 may provide computational mechanisms through which TAP-001 concepts are represented, invoked, authenticated, transported, or recorded.

However:

- TAP semantics remain owned by TAP-001;
- SIN implementation convenience does not modify TAP-001;
- a SIN representation of a TAP concept is not itself a new TAP requirement;
- any formal TAP change must be made in the TAP-001 project context.

---

## 19. Experimental Boundary

A `.sin` program is a program artifact.

Its execution is runtime behavior.

An observed value produced during execution is an observation.

Scientific interpretation of that observation is separate.

Therefore:

```text
SIN source
    |
    v
program execution
    |
    v
runtime observations
    |
    v
experimental record
    |
    v
scientific interpretation
```

A successful SIN execution is not automatically evidence of temporal displacement.

Actual temporal-displacement experiment results belong in the separate experiments context.

---

## 20. Feature Status Model

Every significant SIN feature should be tracked using:

```text
proposed
specified
implemented
tested
accepted
```

These states must not be conflated.

In particular:

- drafted code does not establish implementation;
- implementation does not establish specification;
- passing an implementation test does not automatically establish scientific validity;
- documentation does not establish repository evidence.

---

## 21. Immediate Engineering Priorities

The baseline identifies the immediate priorities as:

1. freeze the lexical model;
2. freeze the syntactic model;
3. define the AST;
4. define the semantic/type model;
5. formalize Result/error behavior;
6. establish module resolution;
7. continue SINC implementation against executable conformance tests.

These priorities should guide subsequent SIN-001 work unless explicitly revised.

---

## 22. Revision Discipline

Future revisions of this artifact should:

1. load the immediately preceding canonical state;
2. construct the proposed state transition;
3. reconcile the complete document;
4. audit contradictions and stale state;
5. verify identifiers and cross-references;
6. record the revision delta;
7. generate the new canonical artifact;
8. perform an independent final audit.

No design decision should become authoritative merely by appearing in implementation code.

---

## 23. Revision History

### Revision 0001 — Initial project state

Established the initial SIN-001 project-state artifact from the supplied SIN 0.0.1 six-volume language specification.

No new language semantics were introduced by this revision.

The uploaded specification is preserved as the baseline; unresolved questions remain unresolved.

## 25. Proposed `defined(E)` Presence Predicate

### Status

**Proposed** — not yet specified, implemented, tested, or accepted.

### Language-level operation

SIN proposes a built-in presence predicate:

```text
defined(E)
```

`defined(E)` evaluates `E` using **presence-aware resolution**.

If any binding or member required to resolve `E` is absent, the result is `false`.

If `E` resolves to `null`, the result is `false`.

If `E` resolves to any explicitly present value—including `0`, negative numbers, `false`, or an empty string—the result is `true`.

### Required three-way distinction

The SIN type/runtime model shall explicitly distinguish:

```text
MISSING ≠ NULL ≠ VALUE
```

Where:

- **MISSING** means that a required binding or member is absent.
- **NULL** means that the binding or member exists and explicitly contains the `null` value.
- **VALUE** means that the binding or member exists and contains an explicitly present value.

Accordingly:

```text
defined(missing) → false
defined(null)    → false
defined(0)       → true
defined(-1)      → true
defined(42.5)    → true
defined(false)   → true
defined("")      → true
```

### Member-resolution cases

The proposed semantics must distinguish all four cases:

```text
observer missing
    → defined(observer)    → false

observer exists
et missing
    → defined(observer.et) → false

observer.et exists
observer.et = null
    → defined(observer.et) → false

observer.et exists
observer.et = 0
    → defined(observer.et) → true
```

### Semantic purpose

`defined(E)` tests **presence** rather than truthiness, nonzero-ness, nonemptiness, validity, or any other value-quality predicate.

The operation is intended to provide one language-level mechanism usable by higher-level SIN constructs, including:

```text
verify_initial_state()
TemporalDisplacement.validate()
```

### Scope limitation

This proposal establishes the `defined(E)` operation and its required distinction between `MISSING`, `NULL`, and `VALUE`.

It does **not yet** fully specify where `MISSING` can exist throughout the SIN language/runtime, including the complete rules for bindings, record members, optional fields, function results, or other language constructs.

Ordinary member access must not be assumed to silently swallow missing values merely because `defined(E)` performs presence-aware resolution.

### Conformance requirements to be established

Once this proposal is formalized, executable conformance tests should verify at minimum:

1. missing binding → `false`;
2. missing member → `false`;
3. explicit `null` → `false`;
4. zero → `true`;
5. negative numeric value → `true`;
6. positive numeric value → `true`;
7. `false` → `true`;
8. empty string → `true`;
9. present nested member → `true`;
10. absent intermediate member/binding → `false`.

### Revision note

Revision 0002 adds this proposed language operation to the project state. No existing SIN syntax or previously locked decision is changed by this proposal.

### Revision 0002 — Proposed `defined(E)` presence predicate

Added the proposed `defined(E)` built-in presence predicate and the explicit `MISSING ≠ NULL ≠ VALUE` distinction. The proposal remains unaccepted and does not alter the baseline's locked decisions.
