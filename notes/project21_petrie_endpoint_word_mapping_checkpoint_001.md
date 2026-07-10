# Project 21 Petrie endpoint-word mapping checkpoint 001

## Canonical status

The bounded Petrie endpoint-word mapping theorem is admitted.

Canonical admission commit:

    813db27 Admit Petrie endpoint word mapping theorem

The repository was clean after push.

## Theorem symbols

    E_TC21
    E_PW21

## E_TC21

For the admitted AC36 Project 21 carrier

    6 <- 5 -> 8 -> 15

under the user-declared orientation

    t = 5
    I = 15

a minimal tested monomial transport class carries the continuation tangent

    v_5_8

exactly to

    v_8_15

while the alternate tangent

    v_5_6

remains outside the output parallel class.

Perfect tangent alignment gives continuity of passage without identity of Eidrons.

## Exact Klein-four chamber action

The four minimal transport representatives form one exact

    V4 = Z2 x Z2

orbit preserving the common continuation filament.

The nontrivial relative actions are commuting involutions.

Generator cycles:

    within flip:  (0 1)(2 3)
    class flip:   (0 2)(1 3)
    product flip: (0 3)(1 2)

The alternate images split into two classes:

    [0, 0, -5, 2]
    [5, 0, 0, 2]

## E_PW21

Under the paper-defined Petrie chamber construction, the exact Klein-four chamber action is resolved into two independent binary axes:

    within axis = endpoint polarity
    class axis = FV versus VF word order
    product axis = endpoint polarity XOR FV/VF word order

Endpoint polarity generates the class-preserving action.

FV versus VF word order generates the class-changing action.

Their product generates the third nontrivial involution.

All four chamber realizations preserve one common continuation filament.

## Native chamber basis

The manuscript construction starts from dodecahedral flags with generators:

    S = edge-endpoint flip
    F = face-boundary rotation
    V = vertex rotation

The two branching transport words are:

    w- = FV
    w+ = VF

Each word acts on both endpoint representatives of a chamber.

Thus the native four-state basis is:

    endpoint polarity x FV/VF word order

## Four-state square

The Project 21 basis is:

    transport 0 = (0, 0)
    transport 1 = (1, 0)
    transport 2 = (0, 1)
    transport 3 = (1, 1)

where the first bit is endpoint polarity and the second bit is FV/VF word order.

## Admitted

    eidronic_tangent_continuity_theorem_admitted = true
    exact_klein_four_action_found = true
    transport_equivalence_class_admitted = true
    endpoint_polarity_axis_admitted = true
    FV_VF_word_order_axis_admitted = true
    four_state_chamber_square_admitted = true
    common_filament_preservation_admitted = true
    project21_petrie_endpoint_word_mapping_theorem_admitted = true

## Not admitted

    indexed_executable_provenance_derived = false
    petrie_parity_shadow_admitted = false
    face_chirality_theorem_admitted = false
    four_chambers_per_edge_theorem_admitted = false
    literal_534_honeycomb_claim = false
    higgs_analogue_claim = false
    higgs_mechanism_claim = false
    physics_claim = false
    force_claim = false
    gap_a_closure = false

## Canonical commits

    d55d408 Admit Eidronic tangent continuity theorem
    9196cb1 Record Eidronic tangent continuity theorem checkpoint
    d7ff28d Test four chamber Klein transport action
    9ec7072 Classify Klein transport generator effects
    17dd788 Test Project 21 V4 against Petrie basis
    c28b6a7 Resolve Petrie endpoint word axis assignment
    813db27 Admit Petrie endpoint word mapping theorem

## Final lines

Perfect alignment is perfect continuity, not identity.

The filament stays. Endpoint polarity selects the representative. FV versus VF selects the chamber side.
