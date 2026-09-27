# TAP-001 Specification

**Project:** Temporal Authentication Protocol  
**Designation:** TAP-001  
**Document:** `TAP_001_SPECIFICATION.md`  
**Specification version:** 1.0  
**Source project state:** `TAP_001_PROJECT_STATE.md`  
**Status:** Formal protocol specification  

---

## 1. Purpose and Scope

TAP-001 is a protocol for evaluating a future entity that claims to have established contact with the present through temporal displacement.

TAP-001 deliberately separates three questions:

1. **Immediate cryptographic authentication:** Can a received message be verified as having been produced with the designated historical secret signing key?
2. **Historical event evidence:** Was the designated authentication material physically instantiated during a defined historical interval and subsequently destroyed under documented conditions?
3. **Temporal-contact assessment:** What does the complete authenticated and independently generated evidentiary record support, contradict, or leave unresolved with respect to a specified temporal-contact hypothesis?

TAP-001 does not treat cryptographic authentication, an HSIE record, a commitment match, an `X_i`, a `V_i`, a D079 channel exchange, or any single future observation as mathematical proof of temporal displacement.

This specification formalizes the approved TAP-001 design through Step 15 and extends the Step 16 protocol-wide record, serialization, traceability, assessment, and conformance rules to include the optional bidirectional temporal message channel defined by D079.

The project-state distinction between **approved** and **frozen** remains external to this document's semantic content. In the project state, D049–D076, D078, and D079, together with the Step 15 conceptual framework, are approved but not frozen. Future project-state revisions may therefore refine these provisions without implying a change to the historical meaning of this specification version.

---

## 2. Normative Language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, and **MAY** are normative requirements.

Where a field is marked optional, its absence MUST NOT be interpreted as evidence of failure unless another applicable rule requires it.

---

## 3. Core Epistemic Separation

TAP-001 uses the following separation throughout the protocol:

```text
AUTHENTICATION
    ≠
PHYSICAL / HISTORICAL EVENT EVIDENCE
    ≠
INDEPENDENT OBSERVATION
    ≠
ANALYSIS
    ≠
TEMPORAL-CONTACT ASSESSMENT
```

The central semantic distinctions are:

```text
HSIE
    = historical physical event

HSIE-related historical information and records
    = assessment inputs associated with that event

cryptographic authentication
    = authentication of message provenance

X_i
    = authenticated, precommitted claim / test / evaluation specification

V_i
    = independent execution / observation record

analysis
    = interpretation of recorded observations under stated methods

evidence characterization
    = relationship of analyzed evidence to an X_i and considered alternatives

temporal-contact assessment
    = structured assessment of the complete evidentiary record
```

The phrase **historical provenance context** may be used descriptively in explanatory prose, including in the HSIE definition, but it is **not** a TAP record type, protocol layer, processing stage, or required field.

---

## 4. Protocol Architecture

The protocol is organized as follows:

```text
                    TAP-001
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
     HISTORICAL                 FUTURE
       BRANCH                   BRANCH
          │                         │
          ▼                         ▼
        HSIE                Future TAP message
          │                         │
          │                         ▼
          │              Cryptographic authentication
          │                         │
          │                         ▼
          │                 Authenticated X_1...X_n
          │                         │
          │                         ▼
          │                 Independent execution
          │                         │
          │                         ▼
          │                       V_i
          │                         │
          │                         ▼
          │                      Analysis
          │                         │
          │                         ▼
          │               Evidence characterization
          │                         │
          └────────────┬────────────┘
                       ▼
             Temporal-contact assessment
```

An optional message-channel path may be present alongside the existing future-evidence branch:

```text
HISTORICAL SIDE
    HSIE
      │
      ├── historical public verification material
      ├── associated outgoing request
      │        │
      │        ├── sign with historical SK
      │        └── encrypt to future endpoint public encryption key
      │
      ▼
PUBLISHED HSIE / MESSAGE ARTIFACT
      │
      ▼
FUTURE ENDPOINT
      │
      ├── decrypt outgoing request
      ├── verify historical signature
      ├── execute requested computation/process
      └── create authenticated response
                │
                └── sign with corresponding historical signing key
                         │
                         ▼
                 PRESENT-DAY VERIFIER
```

The temporal-message-channel path is a logical protocol capability. At the architectural level, it is the TAP-001 two-way temporal networking protocol: a present-side outgoing request can be addressed to a future endpoint, and a future response can be cryptographically bound back to that request. TAP-001 does not define or prove the physical mechanism by which a future endpoint would receive or return bytes across time.

No branch may silently substitute for another.

---

## 5. TAP Record Model

A TAP deployment consists of semantically distinct records. Records MAY be physically stored together or separately, but their semantic identities MUST remain distinct.

Every TAP record SHALL use the following envelope:

```json
{
  "record_type": "...",
  "record_id": "UUID",
  "record_version": 1,
  "schema_version": "1.0",
  "payload": {}
}
```

### 5.1 Record types

The specification defines these primary record types:

```text
HSIE_RECORD
MESSAGE_RECORD
OBSERVATION_RECORD
ANALYSIS_RECORD
TEMPORAL_CONTACT_ASSESSMENT_RECORD
```

An implementation MAY define additional ancillary record types provided that they do not redefine or collapse the semantic roles above.

A `MESSAGE_RECORD` MAY represent an ordinary authenticated future message or a future response to an outgoing temporal-channel request. A D079 outgoing request is represented as the `associated_outgoing_message` component of its HSIE and is not a separate `MESSAGE_RECORD`. The message role is explicit in the applicable message structure and MUST NOT be inferred solely from transport direction.

An implementation MAY retain an unauthenticated received message as an ancillary record. Such a record MUST NOT be treated as authenticated claimant content merely because it was retained.

### 5.2 Record identifiers

`record_id` MUST be a globally unique opaque identifier.

The TAP reference profile uses UUID version 4 identifiers in their canonical textual form.

`record_version` MUST be a positive integer beginning at `1` for the first version of a record and increasing monotonically for later versions of the same record.

A new semantic record MUST receive a new `record_id`. A changed version of an existing versioned record MUST retain the same `record_id` and increment `record_version`.

### 5.3 Record references

A reference to an exact record version SHALL have this form:

```json
{
  "record_id": "UUID",
  "record_version": 1
}
```

References to a versioned record MUST identify the exact version relied upon by the referring record.

A reference to `record_id` without `record_version` MUST NOT be used where the exact record state is material to the assessment.

---

## 6. Canonical Serialization and Encoding

The TAP reference serialization profile is:

```text
character encoding: UTF-8
logical serialization: JSON
canonical serialization for cryptographic operations: RFC 8785 JCS
field naming: snake_case
binary values: base64url without padding
identifiers: UUIDv4 canonical textual form
version numbers: positive integers
current HSIE schema extension: 1.2
current MESSAGE_RECORD schema extension: 1.2
```

The canonicalization method SHALL be applied to the exact JSON object that is to be hashed or signed. No field may be silently omitted, reordered semantically, normalized, or rewritten before cryptographic processing.

RFC 8785 JCS provides the deterministic JSON representation used for cryptographic operations; its restrictions and canonicalization rules are part of the TAP reference profile.

For timestamp strings, TAP uses the Internet date/time form described in RFC 3339 with an uppercase `T` and `Z` and UTC as the required protocol representation.

JSON strings MUST be preserved exactly for cryptographic purposes; implementations MUST NOT perform implicit Unicode normalization before canonicalization.

---

## 7. HSIE — Historical Secret Instantiation Event

### 7.1 Definition

A **Historical Secret Instantiation Event (HSIE)** is a deliberately created, bounded physical event in which designated cryptographic authentication material is physically instantiated at a specified physical location during a specified temporal interval, under documented custody and access conditions, and subsequently destroyed.

Formal model:

```text
HSIE = (S, L, T_start, T_end, M, C, D)
```

where:

```text
S = designated secret authentication material
L = physical location
T_start = event start time
T_end = event end time
M = physical medium containing S
C = documented custody/access conditions
D = destruction procedure
```

The HSIE is a historical event. It is not a cryptographic algorithm, an assessment, or a conclusion about temporal displacement.

### 7.2 Required properties

An HSIE record SHALL document, as applicable to the event:

- the designated secret authentication material or an exact secret reference;
- its physical instantiation;
- the event start and end time;
- the physical location;
- the physical medium;
- custody and access conditions;
- the destruction procedure;
- supporting documentation references;
- integrity metadata for the HSIE record itself.

The HSIE record MUST be sufficient to establish the intended historical event boundaries.

### 7.3 Location representation

The location representation SHALL identify:

```json
{
  "latitude": "decimal string",
  "longitude": "decimal string",
  "coordinate_reference_system": "identifier",
  "coordinate_precision": "description"
}
```

TAP-001 MUST NOT silently assume WGS84 when the applicable CRS is not otherwise established. A deployed record SHOULD explicitly identify its CRS.

Latitude and longitude SHOULD be represented as decimal strings rather than binary floating-point values when exact preservation of the declared decimal representation is required.

### 7.4 Temporal representation

Timestamps SHALL be UTC RFC 3339 date-time strings using `Z`.

Example:

```text
2026-09-21T05:03:00Z
```

The protocol does not infer event precision beyond the precision actually documented.

### 7.5 Historical-copy limitation

The HSIE does **not** establish:

- that no unauthorized copy of the secret was made;
- mathematical exclusive possession;
- that no alternate possession history exists;
- temporal displacement.

### 7.6 HSIE record structure

```text
HSIE_RECORD
│
├── record metadata
│   ├── record_type
│   ├── record_id
│   ├── record_version
│   └── schema_version
│
└── payload
    ├── authentication_material
    │   ├── key_identifier
    │   ├── public_key
    │   ├── signature_algorithm
    │   └── signature_parameters
    ├── temporal_interval
    │   ├── start_time
    │   └── end_time
    ├── location
    │   ├── latitude
    │   ├── longitude
    │   ├── coordinate_reference_system
    │   └── coordinate_precision
    ├── physical_medium
    ├── custody_access
    ├── destruction
    ├── supporting_records
    ├── associated_outgoing_message
    │   ├── message_id
    │   ├── creation_time
    │   ├── message_role
    │   ├── message_content
    │   ├── channel
    │   └── cryptographic_protection
    ├── integrity_metadata
    └── optional_secret_commitment
```

The exact field values depend on the actual HSIE. TAP-001 specifies the semantic requirements, not a particular historical implementation.

---

### 7.7 HSIE record structure JSON template

The following is a complete artificial example of an `HSIE_RECORD` using the current TAP-D002 archival model. The `authentication_material` component contains the complete public verification material required for later TAP authentication. The public key shown is the public key supplied for the example OpenPGP key pair; all event metadata, record identifiers, and commitment values are illustrative.

The private signing key MUST NOT appear in the published HSIE artifact.

```json
{
  "record_type": "HSIE_RECORD",
  "record_id": "3a8f6c21-7d45-4b92-ae16-509c2f784bd3",
  "record_version": 1,
  "schema_version": "1.1",
  "payload": {
    "authentication_material": {
      "key_identifier": "OPENPGP-FPR-1DF22F90D9050EF641E7014FA1AA19A0D52680B6",
      "public_key": "-----BEGIN PGP PUBLIC KEY BLOCK-----\nxjMEarS9UhYJKwYBBAHaRw8BAQdA1NCPSQ6b0zLlcHZBb1wVPtBwXRFKXZ9f\nSeypONgeI33NO1RvbW15VGhlVGltZVRyYXZlbGVyIDx0dHR0QHRlbXBvcmFs\nLWRpc3BsYWNlbWVudC5zcGFjZXRpbWU+wsATBBMWCgCFBYJqtL1SAwsJBwkQ\noaoZoNUmgLZFFAAAAAAAHAAgc2FsdEBub3RhdGlvbnMub3BlbnBncGpzLm9y\nZ0rQCE7egFKTw3J26KbxF7OtVJzhB5DlIX4q3ymYDad2BRUKCA4MBBYAAgEC\nGQECmwMCHgEWIQQd8i+Q2QUO9kHnAU+hqhmg1SaAtgAAcPcBAMzmEd1WLQSL\nasKuhu4FlUzcsZMfa6X0D8t/6GbnNo3qAQCPnvaApkI+Z/RcxA2hsYpA47Jm\nXBoTBQpjqmhblN5HAM44BGq0vVISCisGAQQBl1UBBQEBB0AbRL1Htn+aw0vQ\nTjBxP8Vz9gkB++00kjDUaQjvQ7/LYQMBCAfCvgQYFgoAcAWCarS9UgkQoaoZ\noNUmgLZFFAAAAAAAHAAgc2FsdEBub3RhdGlvbnMub3BlbnBncGpzLm9yZ42/\nbgfxXcUud9MD4QXVgDgS1Iu7qyVsHhIOuBd9M0n3ApsMFiEEHfIvkNkFDvZB\n5wFPoaoZoNUmgLYAAG7GAQCOX8pyY1wcPAEOVIUebg7VzwpnMiKOop9NUHNZ\nQytijgEAzTOuyZQJ4PHW0f8ULAKWP0/S90O2BczWtt7/FTkKkgA=\n=fbKn\n-----END PGP PUBLIC KEY BLOCK-----",
      "signature_algorithm": "Ed25519",
      "signature_parameters": {}
    },
    "temporal_interval": {
      "start_time": "2026-09-24T06:10:00Z",
      "end_time": "2026-09-24T06:20:00Z"
    },
    "location": {
      "latitude": "43.07472",
      "longitude": "-89.38417",
      "coordinate_reference_system": "EPSG:4326",
      "coordinate_precision": "0.0001 degree"
    },
    "physical_medium": "The designated Ed25519 private signing key was physically instantiated as printed secret authentication material on archival paper and sealed in a tamper-evident envelope.",
    "custody_access": "Single-person custody; the sealed envelope remained in the creator's direct physical possession for the full documented HSIE interval, with no authorized access by another person.",
    "destruction": "The printed secret authentication material was physically burned at the end of the documented custody interval. Any temporary digital working copy used to produce the printed material was securely deleted.",
    "supporting_records": [
      {
        "record_id": "6d2e914b-53a7-4c80-bf16-28e9457a31cd",
        "record_version": 1
      }
    ],
    "associated_outgoing_message": {
      "message_id": "84d2a6e1-5b39-47c8-91f0-2d7a6e4b3c58",
      "creation_time": "2026-09-24T06:15:00Z",
      "message_role": "outgoing_request",
      "message_content": "-----BEGIN PGP MESSAGE-----\nVersion: PGP Desktop 10.3.2 (Build 15230)\n\nhQGMA058xXw2N+eTAQv/Vd7P4W8Q1yG5fK2v9xL8mP4zQ3sW2v1xL8mP4zQ3sW2v\n1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4z\nQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v\n1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4z\nQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v\n1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4z\nQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v\n1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4zQ3sW2v1xL8mP4z\nQ3sW2v1xL8mP4zQ3sW2v==9XyL\n-----END PGP MESSAGE-----"
    },
    "integrity_metadata":  "sha256:8c4f2e7a1b6d9f3054c8e217a93b5d6f8012c4e7a5b9d3f6172e8a40c6b1d954",
    "optional_secret_commitment": {
      "commitment_version": 1,
      "hash_algorithm": "SHA-256",
      "hash_parameters": {
        "output_length_bits": 256
      },
      "domain_separator": "TAP-001/D018/SK-COMMITMENT/v1",
      "secret_key_encoding": "TAP-SK-CANONICAL-v1",
      "commitment_value": "7e1d4a9c3f8052b6d174e8a039cf51b27a6d490f3e8c2147b5d9a063f81c2e47",
      "public_key_identifier": "OPENPGP-FPR-1DF22F90D9050EF641E7014FA1AA19A0D52680B6"
    }
  }
}
```

The D018 `commitment_value` above is artificial. In an operational record, it MUST be calculated from the exact designated historical secret signing key using the selected D018 construction and canonical secret-key encoding.

The embedded `public_key` is archival verification material. Its presence does not alter the D018 commitment input, which remains narrowly bound to the designated historical secret signing key under TAP-D018.

The optional `associated_outgoing_message.message_content` contains distinct message text that is packaged with the HSIE artifact and makes the outgoing message part of the HSIE physical event. It is encrypted using the secret authentication material that was subsequently destroyed.

The published HSIE artifact MAY be supplemented by external discovery infrastructure, but TAP verification MUST NOT depend on the continued existence of any external keyserver, directory, or locator because the complete public verification material is already embedded in the surviving HSIE artifact.

## 8. Cryptographic Authentication

### 8.1 Primitive class

TAP-001 SHALL use an asymmetric digital-signature primitive with:

```text
secret signing key SK
public verification key PK
```

The secret signing key is the designated historical authentication material.

The public verification key MUST be retained independently of the destroyed historical secret material so that present-day verification does not require the secret key.

The core specification is cryptographically algorithm-agile. A deployment profile MUST identify the exact signature algorithm and parameters in use. A project-wide single algorithm is not mandated by this core specification.

### 8.2 Message signing

The signed object SHALL be the exact canonical `MESSAGE_RECORD` representation designated as the authenticated message, excluding any signature value that would create circular input.

Conceptually:

```text
canonical_message = JCS(authenticated_message_object)
σ = Sign(SK, canonical_message)
Verify(PK, canonical_message, σ)
```

The signature result SHALL be represented as a binary value using the TAP base64url encoding profile.

### 8.3 Authentication result

Authentication status SHALL be one of:

```text
VALID
INVALID
```

`VALID` means the supplied signature verifies under the identified public key and exact canonical message bytes.

`INVALID` means the signature verification operation does not validate the supplied message under the identified verification key.

Authentication status does not determine the physical truth of the authenticated content.

### 8.4 Authentication material in the HSIE artifact

The complete public verification material required for later TAP authentication SHALL be carried directly in the published HSIE artifact as the `authentication_material` component defined in Section 7.6.

The component contains:

```text
authentication_material
├── key_identifier
├── public_key
├── signature_algorithm
└── signature_parameters
```

TAP-001 does not require a separately surviving `AUTHENTICATION_KEY_RECORD`. An implementation MAY maintain an auxiliary key record for local indexing or operational convenience, but such a record is not part of the protocol's archival dependency chain.

### 8.5 Historical key lifecycle

The general historical signing-key lifecycle is:

```text
Key generation
    ↓
SK + PK
    ↓
HSIE physically instantiates SK
    ↓
HSIE destruction destroys historical SK
    ↓
PK retained independently
    ↓
Future claimant may use SK
    ↓
Future message signed
    ↓
Present-day verification uses PK
```

For D079 specifically, the historical private signing key and the corresponding
private encryption key are held on the same physical medium during the HSIE.
Neither private key is included in the published HSIE artifact. **Both private keys
are destroyed as part of the same physical destruction event of the medium.** The
future endpoint is intended to obtain the same physical medium in the future state
and recover both private keys from it. The private encryption key is used for
decryption of the embedded outgoing request; the historical private signing key
retains its signing function and may be used for future response signing.

A future claimant MUST NOT need to disclose `SK` merely to authenticate a message by signature.

### 8.6 Signed-and-encrypted outgoing message composition

When the optional D079 temporal-message channel is used, the outgoing request SHALL be constructed and signed while the designated historical signing key is available. The request content SHALL then be encrypted using the public encryption key material contained in the HSIE artifact before the encrypted message is packaged into the HSIE. The historical private signing key and the corresponding private encryption key SHALL be held on the same physical medium during the HSIE. Neither private key SHALL be included in the published HSIE artifact. **Both private keys are destroyed as part of the same physical destruction event of the medium.** The future endpoint is intended to obtain the same physical medium in the future state and recover both private keys from it.

The intended cryptographic construction is:

```text
R = canonical plaintext outgoing request object
σ = Sign(SK_historical, JCS(R))
S = {R, σ}
K = designated future endpoint public encryption key
E = Encrypt(K, JCS(S))
```

The published HSIE artifact SHALL contain the encrypted representation `E` of the outgoing request content rather than the plaintext request content when D079 confidentiality is used. The corresponding future private encryption key is used to decrypt `E`, recover the signed request object `S`, recover `R`, and verify `σ` using the public verification material contained in the HSIE.

The historical private signing key and the future private encryption key have distinct roles:

```text
historical private signing key
    → signs the outgoing request before HSIE completion

HSIE-embedded public encryption material
    → encrypts the signed outgoing request for the future endpoint

future private encryption key
    → decrypts the encrypted outgoing request in the future
```

For the example OpenPGP key pair supplied for TAP-001, the primary signing key identifier is `A1AA19A0D52680B6` and the encryption subkey identifier is `7C11A43BA5060409`.

The `associated_outgoing_message` component SHALL preserve sufficient metadata to identify the signing key through the exact HSIE reference and the recipient encryption key within the HSIE public key material. The plaintext request object MUST NOT be included elsewhere in the published HSIE artifact merely for convenience when D079 encrypted confidentiality is being used.

The exact encryption algorithm, parameters, OpenPGP packet/container format, and canonical encryption serialization remain deployment/profile questions unless separately frozen. The public encryption material required by the selected profile SHALL be recoverable from the HSIE's embedded public key material.
---

## 9. D018 — Optional Historical-Secret Commitment

TAP-001 MAY include an independent cryptographic commitment to the exact designated historical secret signing key.

### 9.1 Construction

```text
C = H(D || E(SK))
```

where:

```text
SK = exact designated historical signing key
E  = canonical representation of SK
D  = TAP-001/D018/SK-COMMITMENT/v1
H  = compliant cryptographic hash function or XOF
C  = commitment
```

The commitment input SHALL bind the exact designated secret key and SHALL NOT silently include:

- `PK`;
- HSIE metadata;
- timestamps;
- location;
- destruction records;
- protocol parameters;
- message contents;
- `X_i`;
- `V_i`.

### 9.2 Domain separation

The domain separator is:

```text
D = UTF8("TAP-001/D018/SK-COMMITMENT/v1")
```

The domain separator is public and is not secret material.

### 9.3 Hash agility

The core specification remains hash-algorithm agile.

A deployed commitment record MUST identify:

```text
commitment_version
hash_algorithm
hash_parameters, when applicable
domain_separator
secret_key_encoding
commitment_value
```

The selected construction SHOULD meet or exceed the project target of at least 256-bit classical preimage-security strength and SHOULD be evaluated for relevant quantum preimage resistance over the intended archival lifetime.

### 9.4 Canonical secret representation

`E(SK)` MUST be:

- deterministic;
- canonical;
- unambiguous;
- reproducible by an independent verifier;
- versioned or otherwise identified;
- independent of storage/container identity where practical.

A storage technology such as OpenPGP MAY be used operationally but is not itself the TAP commitment input.

### 9.5 Commitment correspondence

A later verifier MAY calculate:

```text
C' = H(D || E(SK_future))
```

and compare `C'` with `C`.

A matching commitment establishes correspondence between the candidate key and the committed key, subject to the security and correctness properties of the selected construction.

It does not establish:

```text
exclusive possession
absence of copying
historical custody by only one entity
temporal displacement
```

---

## 10. Authenticated Message

### 10.1 Message structure

A TAP authenticated message SHALL have the following logical structure:

```text
MESSAGE_RECORD
│
├── record metadata
│
└── payload
    ├── protocol
    │   ├── protocol_name
    │   ├── protocol_version
    │   └── message_schema_version
    ├── message
    │   ├── message_id
    │   ├── creation_time
    │   ├── message_role
    │   └── message_content (role-specific schema)
    ├── historical_reference
    │   └── hsie_reference
    ├── channel (required for D079 channel messages)
    │   ├── channel_id
    │   ├── request_reference
    │   └── request_nonce, when used
    ├── cryptographic_protection
    │   ├── signature
    │   │   ├── signing_key_identifier
    │   │   ├── signature_algorithm
    │   │   ├── signature_parameters
    │   │   └── signature
    │   └── encryption, when applicable
    │       ├── mode
    │       ├── recipient_key_identifier
    │       ├── encryption_algorithm
    │       ├── encryption_parameters
    │       └── ciphertext
    └── evidence_claims
        ├── X_1
        ├── X_2
        └── X_n
```

`message_content` is the content authored by the sender and authenticated as part of the message. For D079 channel messages, the request or response branch supplies the application-level content. `message_purpose` is not a required protocol field.

The `message_role` field SHALL distinguish at minimum:

```text
future_evidence_message
outgoing_request
future_response
```

A deployment MAY add more roles provided they do not alter the meaning of the existing roles.

### 10.2 Message creation time

`creation_time` SHALL represent the actual creation time of the authenticated message by its creator.

It MUST NOT be interpreted automatically as:

- HSIE time;
- target state time;
- message arrival time;
- verification time;
- observation time.

### 10.3 Authentication-key resolution

The message does not require a separate `authentication_context` or `authentication_key_reference`. The public verification material required for signature verification SHALL be resolved by following the exact `historical_reference.hsie_reference` to the corresponding HSIE record version and using that record's `authentication_material` component.

The HSIE authentication-material component identifies the designated verification key and provides the complete public key, signature algorithm, and signature parameters required by the deployment.

An implementation MAY maintain auxiliary local key indexes, but message authentication MUST NOT depend on a separately surviving authentication-key record or external keyserver.

### 10.4 Historical reference

`historical_reference.hsie_reference` SHALL identify the exact HSIE record version that the message claims to be associated with and from which the public verification material required for message authentication is resolved.

The reference itself does not prove the HSIE historical event.

### 10.5 Multiple future messages

A TAP deployment MAY permit more than one authenticated future message under a retained public verification key, and MAY permit multiple D079 outgoing requests and future responses. Each message MUST have a distinct `message_id`; each response MUST identify the exact request to which it responds.

---

### 10.6 Message structure JSON template

The following is a complete artificial example of a `MESSAGE_RECORD` using the exact element names defined by the authenticated message structure and the `X_i` structure. The values are illustrative only and MUST NOT be reused operationally.

Each member of `evidence_claims` is an `X_i` record following the structure defined in Section 11. The `X_1` and `X_2` members below are illustrative instances; additional claims MAY be represented using the same `X_i` structure.

```json
{
  "record_type": "MESSAGE_RECORD",
  "record_id": "9c1e7a4b-6d32-4f85-a109-3b7e5c2d8f64",
  "record_version": 1,
  "schema_version": "1.1",
  "payload": {
    "protocol": {
      "protocol_name": "TAP-001",
      "protocol_version": "1.2",
      "message_schema_version": "1.1"
    },
    "message": {
      "message_id": "b8e2c4f6-1a93-47d5-8c20-6f4b9d7e3a15",
      "creation_time": "2046-04-18T16:27:35Z",
      "message_role": "future_evidence_message",
      "message_content": "This message identifies the historical authentication event and supplies two independently testable evidence claims for future evaluation under TAP-001."
    },
    "historical_reference": {
      "hsie_reference": {
        "record_id": "3a8f6c21-7d45-4b92-ae16-509c2f784bd3",
        "record_version": 1
      }
    },
    "cryptographic_protection": {
      "signature": {
        "signing_key_identifier": "OPENPGP-KID-A1AA19A0D52680B6",
        "signature_algorithm": "Ed25519",
        "signature_parameters": {},
        "signature": "BASE64URL_SIGNATURE"
      }
    },
    "evidence_claims": {
      "X_1": {
        "claim": {
          "claim_id": "c2f7a1d9-5e34-4b68-9a20-7d3f8c6e1b52",
          "claim_statement": "Under the declared experimental conditions, the specified material system will produce the stated measurable response within the declared uncertainty bounds.",
          "phenomenon": "Temperature-dependent electrical resistance change in the specified material system"
        },
        "experiment": {
          "conditions": "Laboratory ambient pressure with the temperature sweep and environmental controls specified by the procedure",
          "apparatus": {
            "requirements": "Four-wire resistance measurement system, calibrated temperature sensor, controlled thermal chamber, and data acquisition system"
          },
          "procedure": {
            "construction": "Assemble the stated specimen and connect the four-wire measurement path exactly as documented.",
            "calibration": "Verify the resistance and temperature measurement channels against their declared calibration references before measurement.",
            "measurement": "Perform the prescribed temperature sweep and record the resistance response at each specified measurement point.",
            "controls": "Run the declared blank, baseline, and repeatability controls in the same session."
          }
        },
        "evaluation_specification": {
          "expected_result": "The measured resistance response follows the precommitted response envelope over the specified temperature interval.",
          "uncertainty_requirements": "Report combined measurement uncertainty and preserve all uncertainty components required by the precommitted procedure.",
          "analysis_procedure": "Apply the predeclared fitting and residual-analysis procedure to the recorded measurements.",
          "falsification_criteria": "The claim is falsified when the observed response falls outside the precommitted acceptance envelope after applying the declared uncertainty treatment."
        }
      },
      "X_2": {
        "claim": {
          "claim_id": "d5a9e3c1-7f24-4b68-8e30-2c6f1a9d5b47",
          "claim_statement": "The specified optical configuration will produce the declared interference pattern under the stated alignment and environmental conditions.",
          "phenomenon": "Interference fringe geometry produced by the specified optical configuration"
        },
        "experiment": {
          "conditions": "Stable laboratory illumination, controlled path geometry, and the environmental limits stated in the procedure",
          "apparatus": {
            "requirements": "Declared light source, beam-forming optics, detector surface, alignment fixture, and distance reference"
          },
          "procedure": {
            "construction": "Assemble and align the optical path using the declared fixture geometry.",
            "calibration": "Verify detector scale and alignment references before collecting the test image.",
            "measurement": "Capture the interference pattern at the specified detector plane using the declared acquisition settings.",
            "controls": "Record the baseline illumination and alignment-control observations before the primary measurement."
          }
        },
        "evaluation_specification": {
          "expected_result": "The measured fringe spacing and geometry fall within the precommitted geometric acceptance interval.",
          "uncertainty_requirements": "Report detector-scale, alignment, and geometric measurement uncertainties required by the declared analysis.",
          "analysis_procedure": "Extract fringe positions using the predeclared image-analysis procedure and compare the resulting geometry with the acceptance interval.",
          "falsification_criteria": "The claim is falsified when the measured fringe geometry remains outside the declared acceptance interval after the prescribed uncertainty treatment."
        }
      }
    }
  }
}
```

The example demonstrates the record structure only. In an authenticated deployment, the `MESSAGE_RECORD` object designated for signing MUST be canonicalized under the TAP RFC 8785 JCS profile before signature generation and verification.

### 10.7 Bidirectional temporal message channel

D079 defines an optional request/response channel across temporally separated endpoints. The outgoing request is physically instantiated as part of the HSIE event. Its message content is encrypted before archival packaging, and the future response is a distinct `MESSAGE_RECORD`.

The minimum channel semantics are:

```text
PRESENT / HISTORICAL CREATOR
    │
    │ construct plaintext request while SK_historical is available
    ▼
outgoing_request
    │
    ├── signature = Sign(SK_historical, canonical plaintext request)
    └── encryption = Encrypt(PK_encryption embedded in HSIE,
                             signed request)
    │
    ▼
HSIE PHYSICAL EVENT
    │
    └── associated_outgoing_message.message_content
            = encrypted ciphertext
    │
    ▼
PUBLISHED HSIE ARTIFACT
    │
    └── preserves ciphertext, not plaintext request content
    │
    ▼
FUTURE ENDPOINT
    │
    ├── obtain the same key-bearing physical medium
    ├── recover historical private signing key and private encryption key
    ├── use private encryption key to decrypt ciphertext
    ├── recover signed request
    ├── verify historical signature using HSIE public verification material
    └── execute/process request
    │
    ▼
future_response
    │
    ├── request_reference = exact HSIE record/version + embedded message_id
    └── signature = Sign(SK_historical, canonical response)
    │
    ▼
PRESENT-DAY VERIFIER
    │
    └── resolve PK through exact HSIE reference and verify response signature
```

The outgoing request is represented by the HSIE `associated_outgoing_message` component. Its `message_content` is the encrypted representation of distinct outgoing message text and is physically instantiated as part of the HSIE event and packaged with the HSIE artifact. The plaintext message content is not required to remain in the published HSIE artifact when D079 encrypted confidentiality is used. The historical private signing key and the corresponding private encryption key are colocated on the same physical medium during the HSIE, and **both private keys are destroyed as part of the same physical destruction event of the medium**. The future endpoint is intended to obtain that physical medium in the future state and recover both private keys.

The future response is a distinct `MESSAGE_RECORD`. The response SHALL identify the exact embedded outgoing message to which it responds using the exact HSIE record version together with the embedded `message_id`. A response SHOULD also carry or echo a request nonce/challenge when the application requires protection against replay, substitution, or response confusion.

The channel provides protocol-level message semantics. TAP-001 does not specify a physical temporal transport mechanism, routing fabric, or guarantee of delivery.

### 10.8 Outgoing request requirements

A D079 `outgoing_request` SHALL:

1. be constructed while the designated historical signing key is available;
2. have its plaintext request object signed with the designated historical signing key before the key is destroyed;
3. identify the exact HSIE record version and embedded outgoing message by `message_id`;
4. contain a complete application-level request before encryption;
5. encrypt the signed request using the designated future endpoint public encryption key contained in the HSIE's embedded public key material;
6. preserve the encrypted ciphertext in `associated_outgoing_message.message_content`;
7. retain enough canonical data and cryptographic metadata for the future endpoint to use the recovered private encryption key to decrypt the ciphertext and verify the recovered historical signature;
8. use the exact HSIE record version together with the embedded `message_id` so that a future response can refer to the request unambiguously.

For a computation request, the application payload SHOULD declare:

```text
request_type
problem_statement
required_output
acceptance_criteria
response_format, when material
verification_material_requirements, when material
```

The protocol does not require the requested problem to be impossible for all present technology. It merely permits a request whose solution is beyond the present sender's available capability.

### 10.9 Future response requirements

A D079 `future_response` SHALL:

1. identify the same exact HSIE record version through `historical_reference.hsie_reference`;
2. reference the exact HSIE record version and embedded outgoing `message_id` to which it responds;
3. identify its own `message_id` and `creation_time`;
4. contain the application-level response;
5. be digitally signed under the historical signing-key material recovered by the future endpoint from the D079 key-bearing physical medium;
6. preserve the exact canonical response object used as signature input.

The response MAY contain:

```text
computed_result
proof_or_derivation
certificate_or_verification_artifact
measurements
explanation
```

The response signature establishes cryptographic provenance of the response bytes under the designated key. It does not by itself establish the correctness of the returned result, the identity or intelligence level of the responder, the responder's temporal origin, or the physical mechanism by which the response reached the present.

### 10.10 Request/response provenance chain

A conforming D079 channel can be traced as:

```text
HSIE
  ↓
exact HSIE public verification material
  ↓
associated_outgoing_message
  ├── embedded message_id
  ├── exact HSIE version
  ├── signed request
  └── encrypted message_content
        ↓
future endpoint obtains the same key-bearing physical medium
        ↓
recovers both private keys
        ↓
private encryption key decrypts embedded message_content
        ↓
recovers and verifies signed request
        ↓
future processing
        ↓
future_response
  ├── response_id
  ├── exact HSIE version + embedded message_id reference
  ├── same HSIE reference
  └── signature under the designated signing key
```

This gives the protocol a durable cryptographic provenance chain for the request and response messages. It is not, by itself, a provenance proof of temporal transport or the responder's claimed origin.

### 10.11 Computation-request use case and epistemic boundary

D079 permits an application to issue a computation request into the future for a problem that the present sender cannot solve with its available capabilities. The request may be encrypted into the HSIE using the public encryption material embedded in that HSIE, and the future endpoint is intended to obtain the same key-bearing physical medium and recover the corresponding private encryption key so that it can decrypt the request and process it. The future endpoint also recovers the historical private signing key from that same medium for the future response-signing operation. A future response can then return a result together with any application-defined proof, derivation, certificate, or other verification material.

The protocol deliberately separates three propositions:

```text
1. The response is cryptographically authentic under the designated key.
2. The returned computation/result is correct under independently testable criteria.
3. The responder is a future entity possessing capabilities unavailable to the present sender.
```

TAP-001 directly addresses the first proposition through cryptographic authentication. The second requires independent evaluation under the response's declared acceptance/verification criteria. The third is a temporal-contact inference and remains subject to the existing TAP evidentiary and assessment framework.

The expression "superior intelligence" MAY appear in an application hypothesis or message content, but it is not a cryptographic role, authentication result, or TAP-defined entity class.

### 10.12 Optional response encryption

D079 does not require the future response to be encrypted. A deployment MAY later define a return-encryption profile, provided that such a profile does not alter the authentication, request-binding, or semantic boundaries already defined here.

### 10.13 Associated outgoing computation-request JSON template

The following is a complete artificial D079 example of the `associated_outgoing_message` component inside an `HSIE_RECORD`. The message content is intentionally part of the HSIE physical event. The plaintext request is signed with the historical signing key, the signed request is encrypted using the public encryption material contained in the HSIE, and the encrypted ciphertext is packaged with the HSIE artifact.

```json
{
  "associated_outgoing_message": {
    "message_id": "84d2a6e1-5b39-47c8-91f0-2d7a6e4b3c58",
    "creation_time": "2026-09-24T06:15:00Z",
    "message_role": "outgoing_request",
    "message_content": {
      "content_encoding": "base64url",
      "content_representation": "encrypted_signed_message",
      "ciphertext": "BASE64URL_CIPHERTEXT"
    },
    "channel": {
      "channel_id": "0a7e4c2d-91f5-43b8-a6d0-2c7e9b5f1a34",
      "request_nonce": "TAP-D079-EXAMPLE-NONCE"
    },
    "cryptographic_protection": {
      "signature": {
        "location": "inside_encrypted_message_content",
        "signing_key_identifier": "OPENPGP-KID-A1AA19A0D52680B6",
        "signature_algorithm": "Ed25519",
        "signature_parameters": {}
      },
      "encryption": {
        "mode": "OpenPGP",
        "recipient_key_identifier": "OPENPGP-KID-7C11A43BA5060409",
        "encryption_algorithm": "Cv25519",
        "encryption_parameters": {}
      }
    }
  }
}
```

The `message_content.ciphertext` value SHALL represent the encryption of the signed plaintext request object `S = {R, σ}` under the selected D079 encryption profile. The actual plaintext request object `R` is not persisted in the published HSIE artifact when encrypted D079 confidentiality is used.

The encryption recipient key identifier SHALL correspond to public encryption material contained in the HSIE's embedded OpenPGP public key material. The corresponding private encryption key is not included in the published HSIE artifact. It is held on the same physical medium as the historical private signing key during the HSIE, and **both private keys are destroyed as part of the same physical destruction event of the medium**. The future endpoint is intended to obtain the same physical medium in the future state and recover the private encryption key for decryption and the historical private signing key for future signing operations.

The signature is generated before encryption and is carried within the encrypted signed message so that the future endpoint can decrypt first and then verify the historical signature. The example identifiers and placeholders MUST NOT be reused operationally.


### 10.14 Future-response JSON template

```json
{
  "record_type": "MESSAGE_RECORD",
  "record_id": "5c8e2a71-4d36-49f0-b2a7-1e6c3d8f9b54",
  "record_version": 1,
  "schema_version": "1.1",
  "payload": {
    "protocol": {
      "protocol_name": "TAP-001",
      "protocol_version": "1.2",
      "message_schema_version": "1.1"
    },
    "message": {
      "message_id": "7b3d9f1e-6a42-4c85-b0d7-2e5f8a1c3d69",
      "creation_time": "2046-04-18T16:27:35Z",
      "message_role": "future_response",
      "message_content": {
        "response_type": "computation_result",
        "result": "[Returned result]",
        "proof_or_derivation": "[Optional independently verifiable proof or derivation]",
        "verification_material": "[Optional certificate, executable test, derivation data, or other verification artifact]"
      }
    },
    "historical_reference": {
      "hsie_reference": {
        "record_id": "3a8f6c21-7d45-4b92-ae16-509c2f784bd3",
        "record_version": 1
      }
    },
    "channel": {
      "channel_id": "0a7e4c2d-91f5-43b8-a6d0-2c7e9b5f1a34",
      "request_reference": {
        "hsie_reference": {
          "record_id": "3a8f6c21-7d45-4b92-ae16-509c2f784bd3",
          "record_version": 1
        },
        "message_id": "84d2a6e1-5b39-47c8-91f0-2d7a6e4b3c58"
      },
      "request_nonce": "TAP-D079-EXAMPLE-NONCE"
    },
    "cryptographic_protection": {
      "signature": {
        "signing_key_identifier": "OPENPGP-KID-A1AA19A0D52680B6",
        "signature_algorithm": "Ed25519",
        "signature_parameters": {},
        "signature": "BASE64URL_SIGNATURE"
      }
    }
  }
}
```

The future response is verified against the same public verification material resolved from the exact HSIE reference. Its correctness is a separate question from signature validity.

---

## 11. X_i — Authenticated Evidence Claim / Test Specification

### 11.1 General rule

Each `X_i` SHALL be an authenticated, self-contained specification of an evidence claim.

The authenticated `X_i` defines what was specified beforehand. It MUST NOT contain future observations, future measurements, future execution records, later analysis results, or a temporal-contact conclusion.

### 11.2 X_i structure

```text
X_i
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

### 11.3 Claim branch

`claim_id` MUST uniquely identify the claim within the authenticated message.

`claim_statement` SHALL state the proposition being asserted.

`phenomenon` SHALL identify the phenomenon to which the claim refers with enough specificity for independent evaluation.

### 11.4 Experiment branch

The `experiment` branch SHALL contain sufficient operational information for an independent investigator to perform the intended test without requiring post-observation clarification from the claimant.

Required resources and dependencies SHALL be declared as part of `apparatus.requirements` or an equivalent operational field within the experiment description.

### 11.5 Evaluation specification

The evaluation specification SHALL be precommitted.

It SHALL define, as applicable:

- expected result;
- uncertainty requirements;
- analysis procedure;
- falsification criteria.

`falsification_criteria` describes what future observations or results would count against the claim. It does not contain the later result of applying those criteria.

### 11.6 Accessibility

An `X_i` intended as temporal-displacement evidence SHALL be accessible using the ordinary publicly accessible capability represented by a public library.

This includes all capabilities and conditions required to execute and evaluate the test, including required physical space.

Accessibility SHALL be assessed from declared required resources and dependencies. `accessibility` is not represented as a simple boolean claim of compliance within `X_i`.

### 11.7 Methodological neutrality

TAP-001 does not mandate a particular physical phenomenon, apparatus, measurement technology, calibration method, statistical framework, uncertainty framework, or scientific methodology.

The sender/creator is responsible for the substantive verification design embodied in each `X_i`.

---

## 12. Future-Evidence Branch

Only successfully authenticated message content SHALL enter the authenticated future-evidence branch.

```text
received message + signature
        ↓
cryptographic verification
        │
        ├── INVALID → not authenticated claimant content
        │
        └── VALID
              ↓
       authenticated X_i
              ↓
       independent execution
              ↓
              V_i
              ↓
           analysis
              ↓
      evidence characterization
              ↓
     temporal-contact assessment
```

### 12.1 Immutable authenticated X_i

Once an `X_i` has been extracted from an authenticated message, that exact authenticated specification is fixed for subsequent verification.

Later observations, analysis, or claimant communications MUST NOT rewrite it.

### 12.2 Independent execution

Execution of an authenticated `X_i` MUST proceed independently of claimant control over the resulting observations or their interpretation.

Logistical communication is permitted. Post-observation claimant control over the meaning of the authenticated specification is not.

### 12.3 Multiple observations

One `X_i` MAY correspond to zero, one, or multiple independently generated `V_i` records.

A single `V_i` is not required to determine the aggregate status of the claim.

---

## 13. V_i — Independent Execution / Observation Record

### 13.1 Semantic definition

`V_i` records what independently happened when an investigator performed the test specified by an authenticated `X_i`.

The fundamental distinction is:

```text
X_i = what was specified beforehand
V_i = what independently happened afterward
Assessment = what the comparison means
```

### 13.2 Exact X_i reference

Every `OBSERVATION_RECORD` SHALL identify the exact authenticated `X_i` tested.

The reference SHALL contain:

```json
{
  "message_ref": {
    "record_id": "UUID",
    "record_version": 1
  },
  "claim_id": "UUID"
}
```

### 13.3 Observation record structure

```text
OBSERVATION_RECORD
│
├── record metadata
│
└── payload
    ├── verification_reference
    │   ├── observation_id
    │   ├── message_ref
    │   └── claim_id
    ├── investigator
    │   ├── investigator_id
    │   └── independence_statement
    ├── execution
    │   ├── execution_id
    │   ├── execution_status
    │   ├── start_time
    │   ├── end_time
    │   ├── location
    │   ├── actual_conditions
    │   ├── actual_apparatus
    │   ├── calibration
    │   ├── procedure_execution
    │   └── deviations
    ├── observations
    │   ├── raw_observations
    │   ├── measurements
    │   ├── uncertainty_data
    │   └── supporting_records
    └── execution_record
        ├── data_references
        ├── analysis_record_reference
        └── integrity_metadata
```

### 13.4 Observation identity

`observation_id` MUST be globally unique.

`execution_id` SHOULD uniquely identify the actual execution instance represented by the observation record.

### 13.5 Execution status

The reference profile defines these execution statuses:

```text
NOT_EXECUTED
ATTEMPTED_INCOMPLETE
EXECUTED_WITH_DEVIATION
EXECUTED_WITH_OBSERVATIONS
```

These statuses describe execution state. They are not temporal-contact conclusions.

A failed execution MUST NOT automatically be characterized as falsification of the claim.

A successful execution MUST NOT automatically be characterized as establishment of the claim.

### 13.6 Deviations

A deviation from the authenticated `X_i` specification SHALL be recorded as an execution fact.

A deviation MUST NOT automatically invalidate the observation or convert it into a claim result.

The evidentiary effect of a deviation is determined downstream by analysis and assessment.

### 13.7 Independence

The investigator field SHALL identify the investigator responsible for the observation record and include an independence statement sufficient to record that the investigator was acting independently with respect to the test and observation.

TAP-001 does not require a third-party auditor merely because an observation exists.

---

## 14. Analysis Record

### 14.1 Separation from raw observation

Analysis SHALL remain semantically distinct from raw observations and measurements.

An implementation MAY associate an analysis record with a `V_i`, but the analysis result MUST NOT be represented as though it were raw observational data.

### 14.2 Analysis record structure

```text
ANALYSIS_RECORD
│
├── record metadata
│
└── payload
    ├── subject_references
    ├── method
    │   ├── method_type
    │   ├── method_description
    │   ├── assumptions
    │   ├── inputs
    │   ├── uncertainty_treatment
    │   └── dependency_treatment
    ├── outputs
    ├── limitations
    └── integrity_metadata
```

### 14.3 Methodological neutrality

An analysis method MAY be:

- qualitative;
- quantitative;
- likelihood-based;
- Bayesian;
- frequentist;
- another justified analytical method.

TAP-001 does not mandate one universal analytical method.

A method used in a temporal-contact assessment MUST be reproducible from recorded inputs and stated rules and MUST NOT depend on hidden material assumptions.

If quantitative inference is used, weighting, dependency treatment, uncertainty treatment, model assumptions, and relevant inputs MUST be documented rather than hidden inside an unexplained scalar result.

---

## 15. Temporal-Contact Assessment

### 15.1 Purpose

The temporal-contact assessment is the final downstream evidentiary assessment layer.

It evaluates the complete record against:

```text
H_TC = specified temporal-contact hypothesis
H_Ai = material alternative explanations
```

It is comparative rather than automatically deductive.

### 15.2 Assessment inputs

A temporal-contact assessment SHALL identify the material inputs on which it depends, including as applicable:

```text
historical records associated with the HSIE
cryptographic authentication records
optional D018 commitment records
authenticated X_i records
V_i records
analysis records
```

These inputs are traceable records, not a new protocol layer called "historical provenance context."

### 15.3 Hypothesis representation

A temporal-contact hypothesis SHALL have the minimum unambiguous representation:

```text
hypothesis_id
hypothesis_statement
assessment_scope
```

Example logical form:

```json
{
  "hypothesis_id": "UUID",
  "hypothesis_statement": "...",
  "assessment_scope": "..."
}
```

A materially different hypothesis MUST receive a distinct `hypothesis_id`.

An existing hypothesis MUST NOT be silently rewritten after an assessment has relied upon it.

### 15.4 Alternative explanations

A material alternative explanation SHALL have the minimum representation:

```text
alternative_id
alternative_statement
```

Example:

```json
{
  "alternative_id": "UUID",
  "alternative_statement": "..."
}
```

The protocol does not require exhaustive enumeration of every conceivable alternative explanation.

A materially different alternative explanation MUST receive a distinct `alternative_id`.

### 15.5 Assessment-result vocabulary

The controlled TAP vocabulary is:

```text
SUPPORTS
CONTRADICTS
DOES_NOT_DISTINGUISH
UNRESOLVED
```

Definitions:

**SUPPORTS** — the characterized evidence is consistent with and provides evidentiary support for the specified hypothesis at the assessment scope being characterized.

**CONTRADICTS** — the characterized evidence is inconsistent with and provides evidentiary evidence against the specified hypothesis at the assessment scope being characterized.

**DOES_NOT_DISTINGUISH** — the characterized evidence does not materially distinguish the specified hypothesis from the relevant alternatives.

**UNRESOLVED** — the relationship cannot be determined from the available record because the evidence is insufficient, conflicting, materially limited, or otherwise not adequately resolved.

`DOES_NOT_DISTINGUISH` and `UNRESOLVED` MUST NOT be treated as equivalent to either support or contradiction.

The vocabulary applies both to individual-evidence characterization and to aggregate assessment characterization.

No universal additional result state is required by TAP-001.

### 15.6 Comparative assessment

The assessment SHALL compare the evidence with the specified temporal-contact hypothesis and the material alternatives considered by the receiver.

The absence of an identified alternative explanation MUST NOT by itself be represented as proof of temporal contact.

Evidence that is unexplained under an alternative MUST NOT automatically be represented as impossible under that alternative.

Likewise, unexplained evidence MUST NOT automatically become `SUPPORTS` merely because no satisfactory alternative is presently known.

### 15.7 Dependent evidence

Evidence that derives from, substantially reuses, or shares a material underlying source with another evidence record SHALL be representable as dependent evidence.

Dependency representation:

```json
{
  "evidence_reference": {
    "record_id": "UUID",
    "record_version": 1
  },
  "depends_on": [
    {
      "record_id": "UUID",
      "record_version": 1
    }
  ]
}
```

Where material dependency exists, dependent records MUST NOT be treated as independent pieces of evidence for the same inferential purpose unless a validated analytical method explicitly models the dependency.

Absent such a model, the assessment SHALL use a conservative treatment that avoids counting the same underlying evidence more than once for the same inferential purpose.

### 15.8 No mandatory evidence score

TAP-001 does not require a single scalar evidence score, probability, confidence number, or universal weighting function.

A quantitative method MAY be used where justified and adequately documented.

---

## 16. Uncertainty and Limitations

Uncertainty and evidentiary limitations are first-class assessment inputs.

Examples include:

```text
measurement uncertainty
execution limitations
incomplete observations
instrument limitations
environmental uncertainty
archival / provenance gaps
cryptographic assumptions
unresolved alternative explanations
dependent evidence
insufficient sample size
X_i ambiguity or defect
```

Each material uncertainty or limitation SHALL be representable as:

```text
uncertainty_id
category
description
source_refs
```

The reference categories are:

```text
measurement_uncertainty
execution_limitations
provenance_limitations
model_assumptions
unresolved_dependencies
```

Method-specific quantitative detail MAY be added.

An uncertainty or limitation MUST NOT be silently converted into `SUPPORTS` or `CONTRADICTS` merely because it exists.

---

## 17. Temporal-Contact Assessment Record

### 17.1 Exact logical structure

The reference assessment record SHALL be represented logically as:

```text
TEMPORAL_CONTACT_ASSESSMENT_RECORD
│
├── record metadata
│
└── payload
    ├── assessment_reference
    │   ├── assessment_id
    │   ├── assessment_version
    │   └── schema_version
    ├── responsibility
    │   └── receiver_id
    ├── hypothesis
    │   ├── hypothesis_id
    │   ├── hypothesis_statement
    │   └── assessment_scope
    ├── evidence_inputs
    │   ├── historical_records
    │   ├── cryptographic_authentication
    │   ├── optional_secret_commitment
    │   ├── authenticated_X_i_records
    │   ├── V_i_records
    │   └── analysis_records
    ├── comparative_assessment
    │   ├── evidence_supporting
    │   ├── evidence_contradicting
    │   ├── evidence_non_discriminating
    │   ├── unresolved_evidence
    │   ├── evidence_characterizations
    │   └── alternative_explanations
    ├── uncertainty_and_limitations
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

### 17.2 Assessment identifiers

`assessment_id` MUST be globally unique.

`assessment_version` begins at `1` and increases monotonically for later versions of the same assessment.

### 17.3 Evidence input references

Each evidence input collection contains zero or more exact `record_ref` values.

For example:

```json
"V_i_records": [
  {
    "record_id": "UUID",
    "record_version": 1
  }
]
```

### 17.4 Individual evidence characterization

For cases where individual evidence requires an explicit characterization beyond the classification lists, `evidence_characterizations` SHALL use:

```json
{
  "evidence_ref": {
    "record_id": "UUID",
    "record_version": 1
  },
  "characterization": "SUPPORTS",
  "rationale": "...",
  "alternative_refs": [
    {
      "alternative_id": "UUID"
    }
  ]
}
```

Each evidence item MUST have at most one individual TAP characterization within the assessment version.

The summary collections:

```text
evidence_supporting
evidence_contradicting
evidence_non_discriminating
unresolved_evidence
```

MUST be consistent with the individual characterizations where individual characterization is supplied.

### 17.5 Alternative representation

`alternative_explanations` SHALL contain objects of the form:

```json
{
  "alternative_id": "UUID",
  "alternative_statement": "..."
}
```

### 17.6 Methodology

The `methodology` object records the assessment method actually used.

`method_type` is a descriptive string such as:

```text
qualitative
quantitative
likelihood
bayesian
frequentist
custom
```

The list is descriptive rather than a closed universal taxonomy.

`method_description` SHALL explain the method sufficiently for reproduction.

`assumptions`, `inputs`, `uncertainty_treatment`, and `dependency_treatment` SHALL document the material analytical basis.

### 17.7 Aggregate characterization

`assessment_result.characterization` SHALL contain exactly one value from:

```text
SUPPORTS
CONTRADICTS
DOES_NOT_DISTINGUISH
UNRESOLVED
```

The aggregate characterization SHALL describe the relationship of the complete assessed record to the specified temporal-contact hypothesis within the declared assessment scope.

---

## 18. Assessment Lifecycle and Revision

### 18.1 Append-only rule

A completed temporal-contact assessment MUST NOT be modified in place.

When new material evidence or analytical information is incorporated, the receiver MUST create a new assessment version.

Lifecycle:

```text
Assessment A(v1)
        ↓ new material evidence
Assessment A(v2)
        ↓ additional material evidence
Assessment A(v3)
```

### 18.2 Versioning requirements

Each later assessment version SHALL:

- retain the same `assessment_id`;
- increment `assessment_version`;
- identify the newly considered inputs;
- identify the immediately preceding assessment version;
- supersede the prior version for the current assessment state;
- preserve all prior assessment versions as historical records.

The recommended explicit predecessor field is:

```json
"previous_assessment_reference": {
  "assessment_id": "UUID",
  "assessment_version": 1
}
```

### 18.3 What triggers a new version

A new assessment version is required when material new information changes the assessed record, including:

- a new `V_i`;
- a new analysis record;
- material new HSIE-related historical information or records;
- a material new cryptographic record;
- a correction that changes an assessed fact;
- another material evidentiary dependency.

A purely administrative retrieval or presentation operation that does not change the assessed record does not create a new assessment version.

---

## 19. Receiver Responsibility and Optional Assistance

The receiver is responsible for performing and issuing the temporal-contact assessment and for the review required by TAP-001.

The receiver MAY seek outside assistance, including scientific, technical, statistical, legal, or other assistance.

TAP-001 does **not** require the receiver to disclose or record that outside assistance merely because it occurred.

Any substantive external material that the receiver independently relies upon becomes an ordinary assessment input and SHALL be traceable under the normal input-reference rules.

The protocol does not require a separate assistance-disclosure record.

---

## 20. Historical Information and Records Associated with the HSIE

Historical information and records associated with the HSIE are ordinary assessment inputs.

They are not a separately named TAP protocol layer.

Relevant records MAY include:

- HSIE documentation;
- custody records;
- destruction records;
- contemporaneous records;
- supporting physical-event documentation;
- integrity-protected archival records.

Their evidentiary significance is determined during assessment rather than assumed from their existence.

The assessment SHALL identify material historical records by exact record reference.

---

## 21. Claim Status and Evidence Characterization Boundaries

A claim status SHALL remain downstream from `V_i` and any applicable analysis.

```text
X_i
 ↓
V_i
 ↓
analysis / comparison
 ↓
claim characterization
 ↓
aggregate temporal-contact assessment
```

`V_i` SHALL NOT be reduced to a final claim status in place of the underlying execution and observations.

Similarly, a temporal-contact assessment SHALL NOT rewrite authenticated `X_i` content.

---

## 22. Prohibited Semantic Shortcuts

A conforming implementation MUST NOT make any of the following substitutions:

```text
valid signature
    → temporal-contact proof

HSIE record
    → exclusive possession proof

D018 commitment match
    → exclusive possession proof

successful V_i
    → automatic claim establishment

failed execution
    → automatic claim falsification

unexplained evidence
    → automatic temporal contact

absence of a known alternative
    → proof of temporal contact

multiple dependent observations
    → independent evidence merely by counting records

assessment revision
    → destruction / overwriting of earlier assessment versions
```

---

## 23. Conformance Requirements

A TAP-001 implementation conforms to this specification only if it preserves all of the following semantic boundaries:

1. HSIE remains a distinct historical event.
2. Cryptographic authentication remains distinct from physical or temporal conclusions.
3. `X_i` remains authenticated, precommitted test specification content.
4. `V_i` remains independent execution/observation data.
5. Analysis remains distinct from raw observations.
6. Temporal-contact assessment remains a downstream comparative assessment.
7. Historical HSIE-related information and records are assessment inputs, not a separate protocol layer.
8. Alternative explanations are explicitly representable.
9. Uncertainty and limitations are explicitly representable.
10. Dependent evidence is not silently treated as independent.
11. Assessment versions are append-only.
12. The receiver is responsible for the assessment and review.
13. Outside assistance is optional and need not be separately disclosed.
14. The controlled result vocabulary is preserved.
15. No mandatory universal evidence score is introduced.
16. D079 channel messages preserve exact request/response references where applicable.
17. D079 outgoing requests distinguish signing from recipient-public-key encryption.
18. D079 key material is physically colocated on one key-bearing medium during the HSIE, while the two private keys retain distinct cryptographic roles.
19. D079 future responses do not receive stronger epistemic status solely from cryptographic authentication.
19. The embedded outgoing message content is part of the HSIE physical event while retaining distinct message semantics; future-response MESSAGE_RECORDs remain distinct records.

### 23.1 Record validation

At minimum, a validator SHALL verify:

- required envelope fields are present;
- `record_id` and `record_version` are well formed;
- references identify exact record versions where material;
- schema versions are supported;
- authenticated message canonicalization is performed before signature verification;
- `X_i` is immutable after authentication;
- every `V_i` identifies its exact `X_i`;
- dependency references are valid;
- assessment result characterization uses the TAP vocabulary;
- assessment version history is append-only;
- no assessment version depends on hidden claimant state or unstated material assumptions;
- a D079 future response references an exact outgoing request where one exists;
- D079 signatures are verified over the exact canonical signed object;
- D079 encryption recipient identifiers resolve within the required public key material;
- a D079 deployment records the physical-medium lifecycle assumptions for both private keys;
- a D079 cryptographic result is not treated as proof of computational correctness or responder identity.

---

## 24. Security and Evidentiary Considerations

TAP-001 recognizes at least two distinct cryptographic threat classes:

```text
cryptographic break of the selected signature system
        ≠
universal historical-secret reconstruction capability
```

A valid signature establishes that the signature verification operation succeeded under the selected cryptographic assumptions and exact message bytes.

It does not establish that no other party ever possessed or copied the secret.

D018 adds a correspondence mechanism for candidate disclosed key material but does not eliminate the copying or possession limitation.

Long-term archival deployments SHOULD review the cryptographic algorithms, parameters, implementations, and security assumptions periodically. A change of cryptographic profile does not by itself change the historical meaning of an already created HSIE or authenticated message.

For D079, confidentiality and authenticity are separate properties. Encryption to a future endpoint does not establish that the future endpoint is the intended responder, and successful response signature verification does not establish the semantic correctness of the returned result. The D079 model intentionally places the historical private signing key and private encryption key on the same physical medium while keeping their cryptographic roles distinct. Both private keys are destroyed as part of the same physical destruction event of the medium, and the future endpoint is intended to obtain that medium and recover both keys. A future response signed by the historical key establishes correspondence to the verification key anchored in the HSIE, subject to the same copying/possession limitations already recognized by TAP-D006 and D018.

---

## 25. Reference JSON Structures

### 25.1 Generic record envelope

```json
{
  "record_type": "OBSERVATION_RECORD",
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "record_version": 1,
  "schema_version": "1.0",
  "payload": {}
}
```

The example UUID is illustrative only and MUST NOT be reused operationally.

### 25.2 Hypothesis object

```json
{
  "hypothesis_id": "UUID",
  "hypothesis_statement": "Specified temporal-contact proposition",
  "assessment_scope": "Temporal and evidentiary scope of this assessment"
}
```

### 25.3 Alternative explanation object

```json
{
  "alternative_id": "UUID",
  "alternative_statement": "Material alternative explanation"
}
```

### 25.4 Uncertainty item

```json
{
  "uncertainty_id": "UUID",
  "category": "measurement_uncertainty",
  "description": "Description of uncertainty or limitation",
  "source_refs": [
    {
      "record_id": "UUID",
      "record_version": 1
    }
  ]
}
```

### 25.5 Assessment-result skeleton

```json
{
  "assessment_result": {
    "methodology": {
      "method_type": "qualitative",
      "method_description": "Description of analytical method",
      "assumptions": [],
      "inputs": [],
      "uncertainty_treatment": "Description",
      "dependency_treatment": "Description"
    },
    "characterization": "SUPPORTS",
    "rationale": "Reasoning traceable to the recorded inputs",
    "limitations": [],
    "unresolved_questions": []
  }
}
```

---

## 26. Assessment Procedure

The receiver SHOULD execute the following procedure for each temporal-contact assessment:

```text
1. Identify H_TC.
       ↓
2. Identify the assessment scope.
       ↓
3. Identify material HSIE-related historical records.
       ↓
4. Verify applicable cryptographic authentication.
       ↓
5. Identify the authenticated X_i records.
       ↓
6. Identify the available V_i records.
       ↓
7. Identify and review applicable analysis records.
       ↓
8. Identify material alternative explanations H_Ai.
       ↓
9. Identify evidence dependencies.
       ↓
10. Record material uncertainties and limitations.
       ↓
11. Characterize individual evidence where useful.
       ↓
12. Determine the aggregate characterization.
       ↓
13. Record rationale and unresolved questions.
       ↓
14. Create an append-only versioned assessment record.
```

This procedure does not require a particular scientific or statistical method. The method selected by the receiver MUST satisfy the methodology requirements of this specification.

---

## 27. Final Epistemic Boundary

The protocol's final evidentiary chain is:

```text
HSIE
    ↓
HSIE-related historical information and records
    ↓
Cryptographic authentication
    ↓
Authenticated X_i
    ↓
Independent V_i
    ↓
Analysis
    ↓
Evidence characterization
    ↓
Temporal-contact assessment
```

The meaning of the chain is:

```text
historical event
    +
authentication
    +
precommitted future test specification
    +
independent observation
    +
analysis
    +
explicit alternatives / uncertainty
    ↓
structured assessment of the complete record
```

The chain does not contain a hidden inference step that converts authentication into proof of temporal displacement.

---

## 28. Change Control and Specification Evolution

This version defines the current formal protocol baseline.

Future changes SHALL distinguish among:

```text
clarification
implementation-profile change
schema-compatible extension
semantic change
frozen-definition change
```

A change that alters the meaning or required properties of a frozen TAP decision MUST explicitly identify the affected decision and undergo frozen-definition change control.

Approved-but-not-frozen project decisions MAY be refined through ordinary project development, provided the refinement does not silently alter an unrelated frozen definition.

Existing historical records SHALL remain interpretable under the schema version under which they were created.

---

## 29. Requirements Traceability

The following maps the core specification to the approved TAP design decisions:

```text
TAP-D001–D007
    historical authentication, HSIE boundaries,
    cryptographic / temporal assessment separation

TAP-D008
    explicit CRS handling

TAP-D009
    authenticated future-message content

TAP-D010–D012
    independent testability, public-library accessibility,
    operational self-containment

TAP-D013–D018
    semantic layers, asymmetric signatures,
    key lifecycle, optional D018 commitment

TAP-D039–D048
    exact X_i / V_i relation, observation identity,
    independence, downstream analysis

TAP-D049–D057
    future-evidence branch sequencing and boundaries

TAP-D058–D067
    temporal-contact assessment framework

TAP-D068
    minimum temporal-contact hypothesis representation

TAP-D069
    alternative-explanation representation

TAP-D070
    controlled assessment-result vocabulary

TAP-D071
    dependent-evidence treatment

TAP-D072
    append-only versioned assessment lifecycle

TAP-D073
    requirement-based, method-non-prescriptive methodology

TAP-D074
    assessment-record profile, field syntax, references,
    versioning, JSON / UTF-8 profile

TAP-D075
    minimal structured uncertainty / limitation representation

TAP-D076
    receiver responsibility and optional outside assistance

TAP-D078
    message authentication-key resolution through exact HSIE reference;
    no separate authentication-key record required

TAP-D079
    optional bidirectional temporal message channel;
    outgoing message content physically embedded in HSIE;
    outgoing message_content encrypted before HSIE archival packaging
        using public encryption material contained in the HSIE;
    historical private signing key and private encryption key colocated on one
        physical medium during the HSIE;
    both private keys destroyed as part of the same physical destruction event
        of that medium;
    future endpoint acquisition of that key-bearing physical medium and recovery
        of both private keys;
    future private encryption key decryption;
    signed request and exact embedded-message / response binding;
    future authenticated response;
    computation-request use case and epistemic boundary
```

---

## 30. Specification Revision 1.4

This revision corrects the D079 confidentiality model established in Specification 1.3 and aligns the formal specification with `TAP_001_PROJECT_STATE_v26.md`.

The D079 outgoing message is physically instantiated as part of the HSIE event and represented by `HSIE_RECORD.payload.associated_outgoing_message`. Its `message_content` is encrypted before archival packaging using the public encryption key material contained in the HSIE's embedded OpenPGP public key material. The published HSIE therefore retains ciphertext rather than plaintext request content when D079 encrypted confidentiality is used.

The intended construction is:

```text
plaintext outgoing request
        ↓
historical Ed25519 signature
        ↓
signed request object
        ↓
encryption using HSIE public encryption material
        ↓
encrypted message_content ciphertext
        ↓
HSIE physical event / packaged HSIE artifact
        ↓
future endpoint obtains the same key-bearing physical medium
        ↓
recovers both private keys
        ↓
private encryption key decrypts ciphertext
        ↓
historical signature verification
        ↓
request processing
        ↓
future authenticated response
```

This preserves the bidirectional temporal-message-channel model while providing confidentiality for the embedded outgoing request until the corresponding future private encryption key becomes available.

The future response remains a distinct `MESSAGE_RECORD` and continues to identify the exact embedded outgoing message by HSIE record/version and embedded message identifier.

This revision supersedes the Specification 1.3 statement that the embedded plaintext message content was archival and non-confidential. That statement was incorrect and is retained only as revision history.

This revision does not alter the frozen D001–D018 semantic boundaries. In particular, D018 remains narrowly bound to the designated historical secret signing key; the outgoing-message ciphertext, encryption key, and future response do not become D018 commitment inputs.

---

## 31. Specification Revision 1.5

Specification 1.5 aligns the formal D079 key-lifecycle model with `TAP_001_PROJECT_STATE_v27.md`.

The clarification is physical rather than cryptographic: the historical private signing key and the corresponding private encryption key are distinct private keys, but they are held on the **same physical medium** during the HSIE. Neither private key is included in the published HSIE artifact. **Both private keys are destroyed as part of the same physical destruction event of the medium.**

The intended future endpoint lifecycle is:

```text
SINGLE KEY-BEARING PHYSICAL MEDIUM
    │
    ├── historical private signing key (SK_historical)
    └── private encryption key (SK_encryption)
            │
            ▼
    HSIE physical event
            │
            ├── outgoing request signed with SK_historical
            ├── signed request encrypted with PK_encryption
            └── encrypted ciphertext packaged in HSIE
            │
            ▼
    same physical medium is destroyed
            │
            └── both private keys are destroyed as part of the same
                physical destruction event of the medium
            │
            ▼
    FUTURE ENDPOINT
            │
            ├── obtains the same physical medium
            ├── recovers SK_encryption → decrypts outgoing request
            └── recovers SK_historical → may sign future response
```

This does not change the cryptographic distinction between the two keys. The private encryption key performs decryption of the embedded outgoing request. The historical private signing key performs signing. Their shared physical custody and shared destruction event are a property of the D079 physical-medium lifecycle, not a merger of their cryptographic roles.

The protocol still does not specify the physical mechanism by which the future endpoint acquires the key-bearing medium. Exact acquisition mechanism, timing, custody documentation, destruction evidence, and other implementation details remain part of Step 16 refinement.

The response-signing model is therefore coherent with the current D079 design: the future endpoint is intended to recover the historical private signing key from the same key-bearing medium. The historical public verification material remains recoverable directly from the HSIE artifact, as required by TAP-D002 and D078.

No frozen D001–D018 definition is changed by this clarification. D017 already records the historical signing-key lifecycle through physical instantiation, destruction, and future claimant possession; Specification 1.5 makes explicit that D079 pairs that historical signing key with a distinct private encryption key on the same physical medium and binds both to the same physical destruction event.

---

## 32. Implementation Notes

The sender/creator determines the substantive scientific content of each `X_i`, including the phenomenon, apparatus, procedure, measurement method, evaluation method, and falsification criteria.

TAP-001 does not require the protocol designers to maintain a catalog of candidate phenomena or verification methods. Those matters belong to the authenticated `X_i` supplied by the creator.

The TAP specification instead defines the structural, evidentiary, cryptographic, independence, traceability, assessment, archival, and optional temporal-message-channel requirements under which that creator-supplied content is evaluated.

The D079 computation-request capability is intentionally application-general. TAP-001 does not need to know in advance whether the requested problem is scientific, mathematical, engineering, informational, or another computational task. It only defines the provenance, binding, authentication, and confidentiality structures needed to carry such a request and to verify a corresponding future response.

---

## 33. Summary of Normative Core

A conforming TAP-001 system SHALL preserve the following chain:

```text
HISTORICAL
    HSIE
      ↓
    historical record
      │
      └── associated_outgoing_message.message_content
              ↓
        signed plaintext request
              ↓
        encrypted ciphertext packaged in HSIE

BIDIRECTIONAL TEMPORAL CHANNEL
    outgoing_request
      ↓
    encrypted ciphertext in HSIE
      ↓
    future endpoint obtains key-bearing physical medium
      ↓
    private encryption key decrypts request
      ↓
    historical private signing key may sign response
      ↓
    future_response
      ↓
    authenticated response linked to exact request

CRYPTOGRAPHIC
    PK + authenticated MESSAGE_RECORD
      ↓
    authenticated X_i

FUTURE EVIDENCE
    independent execution
      ↓
    V_i
      ↓
    analysis
      ↓
    evidence characterization

ASSESSMENT
    H_TC
      ↕
    evidence
      ↕
    H_Ai
      ↓
    SUPPORTS / CONTRADICTS /
    DOES_NOT_DISTINGUISH / UNRESOLVED
```

The final assessment SHALL be no stronger than the documented evidentiary record, its uncertainties, its dependencies, and its limitations justify.

---

## 34. Reference Sources for Serialization Profile

The TAP reference profile uses the following external specifications:

- RFC 8785, **JSON Canonicalization Scheme (JCS)**, for deterministic canonical JSON representation used in cryptographic operations.
- RFC 3339, **Date and Time on the Internet: Timestamps**, for the protocol's UTC timestamp representation.
- RFC 9562, **Universally Unique IDentifiers (UUIDs)**, for UUID identifiers used by the reference profile.

These external specifications govern only the corresponding serialization mechanisms. They do not alter TAP-001's epistemic definitions or evidentiary boundaries.

---

## 35. Specification Boundary

This document is the Step 16 formal specification baseline for TAP-001.

It fully specifies the currently approved protocol architecture and the required semantic behavior of the protocol records and assessment process while retaining cryptographic algorithm agility where the project state deliberately left the exact algorithm choice open.

The following are therefore parameters of a conforming deployment rather than unresolved semantic gaps in the TAP architecture:

```text
exact asymmetric signature algorithm
exact signature parameters
exact hash algorithm selected for D018
exact outgoing-message encryption profile and parameters
exact request/response anti-replay parameters
```

A deployment MUST record those selected parameters explicitly wherever required by the corresponding record types.

The protocol does not require those choices to alter the historical event model, the `X_i` / `V_i` / assessment separation, or the temporal-contact assessment framework.

---

**End of `TAP_001_SPECIFICATION.md`**
