# SIN 0.0.1 Language Specification

**USF / SIN Development Baseline**

> This Markdown file consolidates the six supplied `SIN_Language_Specification` PDF volumes. The PDF source identifies the volumes as a pagination artifact of the same working specification. Content has been consolidated without adding external material or silently resolving open questions.

---

## 1. Specification status and epistemic rules

This document is a working SIN language specification derived from the supplied USF/SIN artifacts and accumulated project decisions. It distinguishes:

- **Demonstrated / Existing** — syntax or behavior directly evidenced by the supplied SIN source.
- **Proposed** — a design introduced during development but not established by the repository.
- **Required** — necessary for the intended implementation but not evidence that the repository already contains it.
- **Theoretical** — a named concept/version without established implementation evidence.

Source authority is ordered as: actual source artifacts, executable tests, specifications/design documents, `PROJECT_STATE.md`, and conversation history. Documentation must not silently turn proposals into existing language features.

`SINC 0.0.1 / 20241020` is historical or target metadata unless implementation and test evidence establish otherwise. Do not rewrite metadata merely to imply a compiler existed.

## 2. What SIN is and intended to become

SIN is the programming language being developed to support a complete implementation of the Universal Software Framework (USF). USF is intended to be implemented as a SIN framework/library rather than compiler-specific functionality.

The language target is general-purpose. The present source establishes a compact syntax and several important semantic conventions, while the complete type system, runtime, standard library, compiler, concurrency model, FFI, and self-hosting remain development work.

The architecture is conceptually:

```text
SIN
├── Standard Library
├── USF
└── Applications
```

## 3. Design philosophy and syntax rationale

The central compatibility rule is to preserve demonstrated SIN syntax and extend it rather than silently replace it.

The syntax is intentionally compact and readable:

- `->lib:...` expresses library/component references.
- `name:Type;` provides a concise declaration form.
- `def name(...) { ... }` gives functions a familiar executable body.
- dotted access expresses properties and methods.
- `~ ... ~-> err { ... }` provides an explicit success/error region.
- `ret 0;` and `ret 1, err;` provide a compact status/result convention.
- `#! ... !#` provides a semantic layer for human-authored contract information.

SIN therefore has two complementary layers: executable/structural syntax and an adjacent semantic-contract layer.

## 4. Lexical and source-file model

A SIN source file is text containing library references, declarations, function definitions, statements, expressions, and semantic prompt blocks.

Demonstrated lexical forms include identifiers, integer literals, strings, punctuation, operators, parentheses, braces, semicolons, and the special delimiters `#!` and `!#`.

Whitespace is used for readability. The exact complete lexical grammar, comment grammar, escape rules, Unicode policy, numeric literal set, and tokenization edge cases remain to be frozen by the language specification.

The implementation should preserve the ability to associate an inline semantic prompt with the structural node it governs.

## 5. Imports and library references

The demonstrated import/reference forms include:

```text
->lib:sin:default
->lib:sin:default:Observer
->lib:sin:default:Time
->lib:sin:default:Location
->lib:sin:USF
```

These forms are direct evidence of the current source language. The complete package-resolution algorithm, visibility rules, namespace semantics, module format, version resolution, and cyclic-dependency rules are not yet established.

A future compiler should parse these references into explicit module/import AST nodes rather than treating them as opaque comments.

## 6. Declarations, framework references, and state

Demonstrated declarations include:

```text
framework:USF;
self:Observer;
```

State access and assignment include:

```text
self.et = Time.now.et;
```

The exact declaration grammar and typing rules are not yet final. The design direction is that declarations establish named typed entities while subsequent member access operates on structured values.

USF-level state is intended to represent complete domain state where atomic operations require it; displacement must not be modeled as independently committing individual coordinate fields.

## 7. Functions and function classification

The demonstrated function form is:

```text
def name(parameters) {
    ...
}
```

`TemporalDisplacement_v05.sin` additionally demonstrates classified declarations such as:

```text
validate(observer, target_state):function:internal -> ValidationResult
perform_atomic_transition(observer, target_state):function:abstract
displace(observer, target_state):function:external
```

The project uses these classifications to distinguish:

- **internal** — implementation detail used within the component.
- **external** — public callable capability.
- **abstract** — interface/contract whose implementation mechanism is unspecified.

The precise grammar and visibility semantics for classified functions remain a formalization task, but the distinction is part of the current design.

## 8. Parameters, returns, expressions, and calls

Parameters are comma-separated within function parentheses.

Expressions demonstrated by the supplied source include integers, strings, arithmetic, assignment, concatenation, property/member access, method calls, and nested calls.

Examples:

```text
self.et - 86400
"Atomic Observer displacement failed: " + err.msg
observer.commit()
observer.et.verify()
```

Return conventions demonstrated by the source are:

```text
ret 0;
ret 1, err;
```

The project intends to formalize this surface using a Result-like semantic model without discarding the demonstrated syntax.

## 9. Statements and control flow

The source demonstrates:

- assignments
- function calls
- explicit return
- blocks
- error-handling blocks
- conditional/control constructs in the broader language design
- `wait(hours, 3)` and `wait(minutes, 20)`

The complete grammar for `if/else`, loops, declarations, `break`/`continue`, `switch`/`match`, and other control constructs must be frozen before claiming complete language conformance.

`wait(...)` is demonstrated syntax; its scheduling and timing semantics are still language/runtime design.

## 10. Error handling and failure propagation

The demonstrated error form is:

```text
~
    ...
~-> err {
    ...
}
```

Example:

```text
~
    observer.commit();
    observer.et.verify();
~-> err {
    observer.recover();
    ret 1, err;
}
```

USF framework errors are intended to flow through:

```text
framework.HandleError(problem_code, problem_sub, problem_description);
```

The project separates error reporting from state mutation. In the temporal-displacement model, validation is non-mutating and failed execution preserves the complete source state.

## 11. Records and interfaces

`TemporalDisplacement_v05.sin` demonstrates:

```text
TemporalDisplacement:interface
```

It also demonstrates records named:

- `ValidationResult`
- `TransitionResult`
- `DisplacementResult`

These constructs establish the direction of interfaces and structured result records. The complete record syntax, field declarations, visibility, constructors, methods, inheritance/composition, and interface implementation rules are not yet completely frozen.

## 12. Inline semantic prompt system

The syntax:

```text
#! ... !#
```

is a first-class semantic communication channel in the language design.

A prompt may contain structured fields such as:

- `ReferenceDefinition`
- `HumanModel`
- `HumanDeclaredReality` / `DeclaredReality`
- `ExpectedState`
- `ExpectedBehavior`
- `VerificationTolerance`

The prompt is intended to remain adjacent to the exact declaration, function, interface, or semantic unit that it governs.

This adjacency permits tooling to associate the semantic contract with the corresponding AST node.

These blocks are not ordinary comments in the intended design. They carry meaningful semantic metadata. The current repository does not prove that an existing compiler already parses or verifies them.

## 13. Invention and rationale of inline prompts

Inline prompts were introduced because executable syntax can specify operations while still failing to communicate the complete human semantic model behind those operations.

Complex USF concepts require statements about:

- definitions and intended meanings
- assumptions
- declared reality/models
- evidence and uncertainty
- expected states
- expected behavior
- authorization boundaries
- atomicity
- failure invariants
- alternative explanations

Putting this information inline keeps the contract next to the syntax it governs and reduces semantic drift. Structured fields give tools stable anchors while natural-language content remains expressive enough for concepts that do not map naturally to executable statements.

The intended role is therefore a semantic bridge between human intent and machine/AI/tooling interpretation, not a replacement for formal language semantics.

## 14. Semantic contract fields and verification

A semantic prompt can describe the human model that a programmer expects an implementation to honor.

- `ReferenceDefinition` identifies the intended concept or reference.
- `HumanModel` describes the human-authored model of that concept.
- `HumanDeclaredReality` records a declared premise/model where relevant.
- `ExpectedState` identifies the state expected after an operation.
- `ExpectedBehavior` identifies required behavior.
- `VerificationTolerance` may describe acceptable uncertainty where appropriate.

The semantic layer should eventually be preserved in the AST/IR and exposed to compiler tooling.

A future verifier may compare executable semantics against these declarations, but the current source does not establish a finished verification algorithm.

Semantic prompts must not be treated as magical authority over executable behavior. Formal language rules, type checking, runtime invariants, and explicit authorization remain necessary.

## 15. USF as the reference semantic workload

USF supplies the principal domain in which SIN's semantic design is being exercised.

The conceptual USF abstractions are:

- `Observer`
- `Time`
- `Location`
- `Event`
- `State`
- `Transaction`
- `TemporalDisplacement`

Observer state proposed during the project includes identity, spacetime position (`et`, `x`, `y`, `z`), proper time, four-velocity, four-momentum, orientation, angular velocity, physical state, reference frame, and worldline. These are design proposals, not evidence that every field already exists in the repository.

TemporalDisplacement is modeled as:

```text
State A ----[ TemporalDisplacement ]----> State B
```

The model deliberately avoids exposing a sequence of partially updated Observer states.

## 16. Atomic temporal displacement

Temporal displacement is a locked USF domain design decision.

Atomicity invariant:

- success establishes the complete destination state;
- failure leaves the complete source state unchanged;
- no Observer-visible intermediate state exists.

Validation and execution are separate. Validation is non-mutating. Authorization is separate from validation: the Observer remains the final Authorizer.

The destination is a complete state rather than a set of independently committed coordinate changes.

Negative temporal displacement is permitted as a USF domain axiom. This is a property of the project model, not a claim about experimentally established physical reality.

## 17. Validation, authorization, execution, and recovery

The current temporal displacement example contains `validate_displacement`, `move_observer`, and `recover_observer`.

Validation:

```text
TemporalDisplacement.validate(observer, target_state);
```

Execution:

```text
TemporalDisplacement.displace(observer, target_state);
```

The semantic contract states that validation assesses a proposed complete source/destination transition without mutating Observer state. Validation does not authorize execution.

`move_observer` constructs a complete destination state, validates it, and then requests the atomic displacement. Errors are reported through `framework.HandleError` and failure returns an error result.

Recovery is a new atomic displacement from the current state to a checkpoint. It is not rollback of partial movement, undo of mutations, or automatic authorization.

## 18. Current SIN grammar — working formalization

The following is a working formalization, not a claim that the final grammar has been frozen.

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

Member access and calls are represented by dotted expressions.

The ellipsis is intentional: control flow, typing, operators, records, interfaces, prompt syntax, and complete lexical rules still require final grammar work.

## 19. Type-system direction

The language direction includes a progressively stronger type system.

Design/proposal areas:

- primitive types
- strings and bytes
- structured records
- interfaces
- objects
- enums
- references
- generics
- ownership and lifetime
- resource management
- Result/error types

Exact type inference, coercion, nullability, mutability, generic constraints, variance, ownership/borrowing, aliasing, and ABI representation remain open.

The type system should support the semantic requirement that complete domain states can be validated before atomic transition.

## 20. Runtime, memory, concurrency, and FFI direction

The broader design proposes:

- deterministic resource management
- explicit object/state semantics
- threads/tasks/futures/promises
- async/await
- mutexes, read/write locks, atomics
- channels and semaphores
- reflection and runtime type information
- compile-time evaluation and metaprogramming
- FFI, including C ABI and interoperability with C++, Python, and other environments

These are design targets, not all implemented language features.

The concurrency memory model, object representation, ownership rules, garbage collection/reference counting strategy, thread safety guarantees, and FFI ABI rules remain to be specified.

## 21. Compiler architecture and SINC

The proposed compiler architecture is:

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
native  LLVM strategy
          \
       potentially WASM
```

An intermediate representation is preferred because it separates language semantics from backend implementation.

SINC is the intended compiler/toolchain name.

Historical metadata identifying `SINC 0.0.1 20241020` must not be treated as proof of an existing compiler.

Where a bootstrap/reference implementation exists in project artifacts, its actual tested capability must be distinguished from the complete specification target.

## 22. Standard library and USF architecture

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

USF should remain a separate framework/library layer:

```text
SIN
|
+-- Standard Library
|
+-- USF
|
+-- Applications
```

USF services such as `Log` and `HandleError` are framework responsibilities rather than compiler magic.

## 23. Programmer workflow and contribution rules

A programmer joining the project should first identify whether a statement is demonstrated, proposed, required, or theoretical.

Recommended contribution sequence:

1. Read `USF.sin` and the temporal displacement source.
2. Read the language specification.
3. Preserve demonstrated syntax.
4. Do not silently convert open questions into decisions.
5. Add tests for every newly established language behavior.
6. Record locked decisions when design choices become authoritative.
7. Keep semantic prompts adjacent to the code they describe.
8. Separate compiler implementation from USF library implementation.
9. Treat atomicity and source-state preservation as explicit conformance requirements.
10. Update project state after substantial architectural changes.

## 24. Conformance and testing strategy

A future SIN implementation should distinguish:

1. syntax conformance
2. semantic conformance
3. standard-library conformance
4. runtime conformance
5. FFI conformance
6. USF conformance

Compiler tests should cover:

- lexing
- parsing
- name resolution
- imports
- expressions
- functions
- returns
- error blocks
- member access
- method calls
- assignments
- exact parsing of the reference SIN files

Runtime/semantic tests should cover:

- type checking
- error propagation
- object state
- lifetime
- ownership
- concurrency
- FFI boundaries
- deterministic cleanup

USF tests should cover:

- Observer construction
- checkpoints
- validation
- atomic execution
- failure preserving source state
- recovery as displacement
- negative temporal displacement as a domain operation

## 25. Development phases

### Phase 0 — Language specification

Includes:

- SIN Language Specification
- SIN Grammar
- SIN Type System Specification
- SIN Runtime Specification
- SIN Error Model
- SIN Module Specification
- USF integration specification
- Atomic displacement semantics

**Status:** substantially drafted.

### Phase 1 — Minimal SINC

Targets:

- lexer
- parser
- AST
- functions
- variables
- expressions
- blocks
- conditionals
- loops
- return
- basic types
- imports
- errors

**Status:** implementation/verification depends on the current bootstrap/reference artifact.

### Phase 2 — Full type system

Objects, structs, enums, generics, references, ownership, resource management.

**Status:** design/proposal.

### Phase 3 — Standard library

Strings, collections, files, IO, math, time, regex, processes, networking.

**Status:** design/proposal.

### Phase 4 — Advanced language

Async, threads, channels, reflection, metaprogramming, FFI.

**Status:** design/proposal.

### Phase 5 — USF

USF, Observer, Time, Location, State, Transaction, TemporalDisplacement.

**Status:** architecture established; implementation incomplete.

### Phase 6 — Self-hosting

SINC written substantially in SIN.

**Status:** future phase.

## 26. Known gaps and open questions

The following are intentionally unresolved:

1. Exact formal SIN grammar.
2. Exact type-system rules.
3. Exact ownership, lifetime, and aliasing semantics.
4. Exact Result/error propagation semantics.
5. Exact module/package resolution rules.
6. Exact runtime representation of Observer state.
7. Exact API and implementation of TemporalDisplacement.
8. Exact semantics and implementation of `USF.Log`.
9. Exact semantics and implementation of `USF.HandleError`.
10. Exact implementation of Observer checkpoints.
11. Whether trajectory data is exposed as a first-class abstraction.
12. Exact concurrency memory model.
13. Exact FFI mechanisms and ABI rules.
14. Exact compiler backend strategy.
15. Exact standard-library API surface.
16. How the initial SINC implementation will be bootstrapped.
17. Which portions of the existing repository should be preserved unchanged for compatibility.

These questions must remain visibly open until resolved by an explicit project decision and, where appropriate, implementation/test evidence.

## 27. Design decisions and rationale

### D001 — USF is implemented in SIN. LOCKED.

USF should be a SIN framework/library rather than compiler-specific functionality.

### D002 — Preserve demonstrated SIN syntax. LOCKED.

New language features extend the demonstrated syntax rather than silently replacing it.

### D003 — Separate existing syntax from proposed semantics. LOCKED.

Documentation must distinguish repository evidence from design.

### D004 — SINC 0.0.1 20241020 is not implementation evidence. LOCKED.

The identifier remains historical/target metadata unless implementation and tests establish otherwise.

### D005 — Temporal displacement is atomic. LOCKED.

Observer transitions from complete source state to complete destination state with no Observer-visible intermediate state.

### D006 — Validation does not mutate Observer state. LOCKED.

A failed validation leaves source state unchanged.

### D007 — Failed displacement preserves source state. LOCKED.

Displacement is all-or-nothing from the Observer perspective.

### D008 — Recovery is atomic displacement. LOCKED.

Recovery is a new displacement to a checkpoint, not rollback.

### D009 — Complete destination state. LOCKED.

Displacement operates on a complete destination state.

### D010 — Negative temporal displacement. LOCKED AS DOMAIN AXIOM.

Permitted by the USF theoretical model; not an established physical fact.

### D011 — Do not invent unsupported physical mechanisms. LOCKED.

Do not introduce temporal energy, temporal charge, temporal phase, or similar mechanisms without a specific later requirement.

### D012 — Inline prompts are first-class semantic metadata. LOCKED.

The `#! ... !#` layer is intended to convey human-authored semantic contracts adjacent to governed syntax and to be available to future tooling.

## 28. Worked SIN examples

### Example — minimal function

```text
def hello(name) {
    framework.Log("Hello, " + name);
    ret 0;
}
```

### Example — error block

```text
def verify(observer) {
    ~
    observer.et.verify();
    ~-> err {
        framework.HandleError(0, "verify", err.msg);
        ret 1, err;
    }
    ret 0;
}
```

### Example — semantic contract

```text
#!
ReferenceDefinition:
Atomic Observer displacement
ExpectedBehavior:
On success, the Observer occupies the complete destination state.
On failure, the complete source state remains unchanged.
ExpectedState:
No Observer-visible intermediate state exists.
!#
```

### Example — temporal movement

```text
def move_observer(observer, target_et, target_x, target_y, target_z) {
    ~
    let target_state = destination_state(
        observer,
        target_et,
        target_x,
        target_y,
        target_z
    );
    validate_displacement(observer, target_state);
    TemporalDisplacement.displace(observer, target_state);
    ~-> err {
        framework.HandleError(
            0,
            "move_observer",
            ("Atomic Observer displacement failed: " + err.msg)
        );
        ret 1, err;
    }
    framework.Log("Observer displaced atomically to destination state.");
    ret 0;
}
```

## 29. Quick-reference cheat sheet

### Core demonstrated forms

**Library:**

```text
->lib:sin:default
->lib:sin:default:Observer
```

**Declarations:**

```text
framework:USF;
self:Observer;
```

**Function:**

```text
def name(parameters) {
    ...
}
```

**Classified function:**

```text
name(parameters):function:internal -> Result
```

**Return:**

```text
ret 0;
ret 1, err;
```

**Error block:**

```text
~
    ...
~-> err {
    ...
}
```

**Member/method:**

```text
self.et
observer.commit()
observer.et.verify()
```

**Expressions:**

```text
self.et - 86400
"message: " + err.msg
```

**Semantic prompt:**

```text
#!
ExpectedBehavior:
...
!#
```

**Core USF invariant:**

```text
source state --[atomic displacement]--> destination state
```

**Failure:**

```text
destination not established; source remains unchanged.
```

## 30. Specification status and contribution boundary

This multi-volume export is a pagination artifact of the same working specification. The content is intentionally divided into evenly sized volumes so that no later section is lost during PDF export.

The specification should be treated as a baseline for immediate programmer onboarding, not as proof that every proposed subsystem already exists.

When implementation evidence changes the status of a feature, update the classification and add tests/specification text together.

When a design decision is made, record the decision explicitly rather than allowing it to emerge implicitly from implementation.

The immediate engineering priority remains to freeze the lexical and syntactic model, define the AST and semantic/type model, formalize Result/error behavior, establish module resolution, and then continue the SINC implementation against executable conformance tests.
