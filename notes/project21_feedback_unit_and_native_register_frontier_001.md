# Project 21 feedback-unit and native-register frontier 001

## Status

Project 21 has moved beyond the original slot/C axis-anchor search into a more precise feedback and closure-memory frontier.

The centroid-normalized local-I construction remains a bounded theorem candidate over the 6561-point slot/C register. It supplies a common comparison frame, but it does not determine an unlabeled axis, prove a unique native G15 embedding, admit a native generator, or close Gap A.

The current frontier concerns a narrower question:

> What is the smallest source-side distinction that can be carried by an admissible transition and return a nontrivial verdict on closure?

The working answer is no longer a raw packet value or provenance label. The strongest current candidate is a binary transition receipt derived from source-side role-hook change, accumulated by XOR around closed directed paths.

The native comparison surface is now also clearer. The x_sigma register has an exact radix-60 address law and an exact split between internal slot-fiber motion and external G15 carrier motion. The remaining bridge is a lawful assignment of the missing local sheet state.

## Keeper

The residue names the place. The sheet remembers how it was reached.

## 1. Starting point

The recent Project 21 chain began with the centroid-normalized local-I theorem candidate and the problem of axis anchoring.

For a candidate row

    p(x) = (from_slot, to_slot, from_C, to_C),

the full-register centroid C is preserved under the tested local-t extension

    p_t(x) = p(x) + t(p(x) - C).

This gives a stable proxy comparison frame. It does not by itself identify a native axis.

The initial axis-anchor results were:

- raw value profiles do not distinguish the four coordinates;
- centroid structure is invariant under all coordinate permutations;
- labels preserve the frame, while the unlabeled centroid does not;
- order signatures distinguish the coordinate sequences;
- order remains burdened by artifact-order risk because source-side birth order is not proven.

This motivated a search for a cleaner channel datum.

## 2. Channel candidates and the provenance-bit correction

The first channel-axis search reported three exact candidates:

- role_hooks
- support_sources
- native

That result required careful correction.

The native/non-native partition was not an independent row field. The original generator defined it by:

    ss = [str(v) for v in x.get("support_sources", [])]
    native = any("native_chain" in s for s in ss)

The audit `audit_native_channel_bit_as_provenance_projection_001` established:

- 48 packet rows;
- 24 native and 24 non-native;
- exact reproduction of the original partition;
- removal of support_sources erases the native bit;
- support_sources is the provenance carrier;
- native is a derived one-bit provenance projection.

Therefore:

> The native bit is a receipt bit, not a transport-feedback bit.

It records that a packet has native-chain support. It does not yet encode crossed versus parallel, preserve versus exchange, upstairs versus downstairs, or loop holonomy.

No upstairs/downstairs identification is admitted from this result.

## 3. Search for a genuine feedback unit

Once the provenance bit was removed as a false target, the search moved from row classification to transition structure.

The 48 packet rows collapse to 24 unique law-key states. A directed transition is admitted when the source endpoint of one state equals the starting point of the next in both slot and C coordinates.

This produced:

- 24 transition states;
- 28 directed transitions;
- 3 cyclic strongly connected components;
- component sizes 12, 6, and 6.

No directed 3-cycles occur.

The first transition-bit search therefore returned a clean negative:

- 14 tested binary features;
- no triangle substrate;
- no 3-cycle residue candidate.

The correct interpretation was not that no feedback exists. It was that the shortest tested closure surface did not exist.

## 4. Longer-cycle residue

The longer-cycle search enumerated the simple directed cycles of the observed transition graph.

Result:

- 7 simple directed cycles;
- cycle lengths 6, 10, and 12;
- four 6-cycles;
- one 10-cycle;
- two 12-cycles.

Eleven tested transition bits produced both even and odd closed-cycle residues.

The leading feature was:

    role_hook_change

defined by comparing the source-side role-hook sets at the endpoints of an admissible transition:

    f(u -> v) = 0 if H(u) = H(v)
                1 if H(u) != H(v)

The closed-path residue is:

    omega(C) = XOR over e in C of f(e)

For role_hook_change, the seven-cycle residue vector is:

    0000101

This means:

- the four 6-cycles close even;
- the 10-cycle closes odd;
- the two 12-cycles split, one even and one odd.

This is not a row classifier. It is a closure-sensitive transition residue.

## 5. Cycle-space and switching audit

The switching audit established that the seven observed cycles form a complete GF(2) cycle basis for the tested transition graph.

Counts:

    E = 28
    V = 24
    C = 3

so the expected cycle rank is:

    E - V + C = 7

The observed seven cycle vectors have GF(2) rank 7.

Therefore the recorded cycles span the tested cycle space.

All 11 longer-cycle candidate bits are:

- invariant under cycle rotation;
- invariant under the four tested vertex switchings;
- expressible as one of five cycle-residue signatures.

The five signature classes are:

    0000000
        source_cross_equal_xor
        source_delta_equal
        target_delta_equal

    0000100
        source_c_wrap
        target_c_wrap
        transition_c_wrap

    0000101
        role_hook_change

    0001000
        source_delta_parity_xor
        source_slot_c_order_xor
        target_delta_parity_xor
        transition_wrap_xor

    0001100
        source_slot_wrap
        target_slot_wrap
        transition_slot_wrap

The role-hook residue is unique in the tested feature family.

This is the first genuinely cohomological-looking Project 21 result.

Boundary:

- cocycle candidate found;
- no native cocycle admitted;
- no holonomy class admitted;
- no signed-lift identity established.

## 6. Source-side provenance of role_hook_change

The audit `audit_role_hook_change_feedback_candidate_native_provenance_001` established:

- 48 packet rows;
- 24 unique law-key states;
- 28 transitions;
- 48 role-hook occurrences;
- all role hooks come from source_payload;
- zero row-level role-hook occurrences;
- zero forbidden answer or downstream payload hits;
- exact reconstruction on all 28 transitions;
- all 24 law keys have native-chain support;
- expected cycle signature 0000101.

Thus role_hook_change is no longer merely a feature name.

It is exactly reconstructible from clean source-side role-hook sets.

Current status:

- source-side feedback-unit candidate found;
- exact transition replay achieved;
- switching-invariant closed-cycle residue achieved;
- feedback unit not admitted;
- transport rule not admitted;
- native signed-lift identity not proven.

## 7. Native signed-lift ruler

A minimal native G15 signed-lift receipt was imported from the signed-lift paper.

The imported table contains:

- 15 G15 vertices;
- 30 unique G15 edges;
- 10 parallel edges;
- 20 crossed edges;
- cocycle convention:
  - parallel = bit 0
  - crossed = bit 1
- one minimal-support representative with support size 6.

This puts the native comparison object in the Project 21 repository.

However, importing the ruler does not supply a bridge.

A valid comparison requires an independently defined map from the 28 Project 21 transition edges to native G15 edges. The map must not be selected using:

- role_hook_change values;
- native cocycle values;
- crossed or parallel labels;
- cycle-residue agreement.

## 8. Failed flat mappings

A blind low-complexity slot/C projection search tested 612 candidate maps from the four law-key coordinates into G15 vertex labels.

No exact map was found.

Best result:

- 14 of 28 transitions mapped to native G15 edges;
- 14 failed;
- 10 distinct mapped vertices;
- 13 distinct mapped edges.

Therefore:

> The Project 21 transition graph does not embed into the native G15 edge register through the tested low-complexity affine slot/C projections.

A second blind search tested all 360 ordered assignments of the four law-key coordinates to four distinct x_sigma fields chosen from:

- u_slot
- v_slot
- u_local
- v_local
- u_vertex
- v_vertex

At best:

- one of 24 nodes matched;
- one node projected uniquely;
- zero transitions mapped end-to-end.

Therefore the law-key coordinates are not merely renamed x_sigma fields.

## 9. The 30-column G15 register

The upstream source search recovered three important register surfaces:

    18-g900-kernel-admission/source/kernel_payload/g15_slot_edges.csv

    18-g900-kernel-admission/source/kernel_payload/x_sigma_edges.csv

    11-thalean-unification/lifts/g15_candidate_cocycle_edges.json

Their schemas are:

### g15_slot_edges.csv

- 30 rows;
- fields slot_u and slot_v;
- row order acts as the candidate 30-column index;
- all 30 rows are unique G15 slot edges.

### x_sigma_edges.csv

- 3600 rows;
- fields:
  - kind
  - u_slot
  - v_slot
  - u_local
  - v_local
  - u_vertex
  - v_vertex

### g15_candidate_cocycle_edges.json

- 30 records;
- symbolic endpoints e0 through e14;
- separate label alphabet;
- no explicit symbolic-to-numeric bridge found in that file.

Only two Project 21 states join directly to the G15 slot register by their slot pair:

    node 1
    law_key [0,5,5,0]
    column 2

    node 13
    law_key [5,4,4,5]
    column 13

Four states join by C pair.

No transition is fully mapped by those direct joins.

The two direct hits have swapped-pair form:

    (a,b,b,a)

and both coordinate pairs name the same register edge.

This is informative but not yet a general law.

## 10. Exact x_sigma register grammar

The audit `audit_x_sigma_radix60_and_kind_split_001` established an exact address law across all 3600 rows:

    u_vertex = 60*u_slot + u_local
    v_vertex = 60*v_slot + v_local

Thus:

- slot is a 15-valued base coordinate;
- local is a 60-valued fiber coordinate;
- vertex is the flattened 900-state address.

The observed x_sigma slot-pair surface contains exactly 45 pairs:

    30 registered G15 edges
    15 unregistered diagonal pairs

The 15 unregistered pairs are exactly:

    (0,0), (1,1), ..., (14,14)

The kind split is exact.

### internal_thalion_copy

- 1800 rows;
- exactly 15 slot pairs;
- every row is same-slot;
- every row is unregistered;
- all motion remains within a slot fiber.

### external_signed_carrier

- 1800 rows;
- exactly 30 slot pairs;
- every row is different-slot;
- every row lies on a registered G15 edge.

Therefore the x_sigma register decomposes exactly as:

    15 internal slot fibers
    disjoint union
    30 external G15 carriers

This is a native structural theorem candidate for the imported register surface, but it is currently recorded as an exact finite audit result rather than promoted into the Project 21 theorem boundary.

## 11. The missing sheet bridge

Project 21 C values occupy the observed set:

    {0,1,2,4,5,10,11,13,14}

The x_sigma local coordinate decomposes as:

    local = residue + 15*sheet

where:

    residue = local mod 15
    sheet = local // 15
    sheet in {0,1,2,3}

Project 21 C lies inside the full local residue domain modulo 15.

This suggests the next candidate bridge:

    local_from = from_C + 15*q_from
    local_to   = to_C   + 15*q_to

The missing information is the sheet assignment:

    q_from, q_to in {0,1,2,3}

This sheet state is a plausible carrier of the closure memory that the raw C residue lacks.

The current conceptual reading is:

> The residue names the place. The sheet remembers how it was reached.

This is only a search framing.

No local-sheet rule has been admitted.

No identification with the native signed-lift sheet has been proven.

## 12. Current candidate unit of feedback

The strongest current Project 21 feedback candidate is:

    one binary source-side role-hook-change receipt
    attached to an admissible transition

with closure residue:

    XOR of the transition receipts around a closed directed path.

It satisfies the following observed properties:

- binary;
- source-side;
- free of forbidden answer payload;
- exactly replayable on all 28 observed transitions;
- nonconstant on closed paths;
- invariant under cycle rotation;
- invariant under tested vertex switching;
- unique cycle signature within the tested coordinate feature family.

It does not yet satisfy the following admission requirements:

- independently derived native transition map;
- identity with the native G30 to G15 signed-lift cocycle;
- native local-sheet construction;
- generator law;
- unique native G15 embedding;
- theorem-level closure;
- Gap A closure.

## 13. Conceptual ladder

The current mathematical picture can be summarized as:

    point -> relation -> path -> cycle -> residue

A point supplies distinction.

An edge supplies relation.

A path carries ordered change.

A cycle supplies closure.

The residue distinguishes closure sectors.

In Project 21 language:

    packet state
        -> admissible transition
        -> role-hook-change bit
        -> closed directed cycle
        -> switching-invariant XOR residue

In native-register language:

    G15 slot
        -> 60-state local fiber
        -> radix-60 vertex address
        -> internal or external carrier edge
        -> signed-lift closure memory

The open problem is to build the lawful bridge between these two descriptions without selecting it by the desired output.

## 14. Locked boundaries

The following remain false:

- feedback_unit_admitted
- transport_feedback_rule_admitted
- native_signed_lift_identification_proven
- cocycle_admitted
- holonomy_class_admitted
- upstairs_downstairs_identification
- channel_axis_rule_admitted
- source_law_admitted
- native_generator_admitted
- unique_native_g15_embedding_proven
- full_theorem_admitted
- proof_claim
- gap_a_closure
- geometry_claim
- physics_claim
- force_claim

The centroid-normalized local-I theorem candidate remains bounded to proxy-coordinate status.

The role-hook residue remains a source-side cocycle candidate on the observed Project 21 transition graph.

The x_sigma radix-60 and kind-split results are exact finite register audits.

No claim currently identifies these candidate and native structures as the same object.

## 15. Next exact target

The next artifact is:

    search_project21_c_to_x_sigma_local_residue_sheet_map_001

Goal:

Search for a source-side, bit-blind rule assigning:

    q_from, q_to in {0,1,2,3}

such that:

    local_from = from_C + 15*q_from
    local_to   = to_C   + 15*q_to

and the resulting radix-60 endpoints land on exact x_sigma rows.

The search should test:

- whether one uniform sheet rule covers all 24 states;
- whether endpoint rows lie in internal_thalion_copy or external_signed_carrier as required;
- whether each state projects to a unique 30-column G15 edge;
- whether all 28 transitions map end-to-end;
- whether role-hook-change and cocycle values remain sealed until the map is frozen;
- whether the sheet rule is invariant under permitted relabeling;
- whether the two direct swapped-pair states emerge naturally rather than as exceptions.

The acceptable progression is:

    source-side sheet candidate
    -> exact x_sigma endpoint replay
    -> frozen structural map
    -> blind native cocycle comparison
    -> cycle-residue comparison
    -> admission review

No later stage should be skipped.

## Closing line

We found the receipt bit.

We found a source-side transition bit.

We found a complete closed-cycle residue surface.

We found the native signed-lift ruler.

We found the radix-60 register grammar.

The remaining question is whether the missing sheet assignment makes the candidate and the native lift the same lawful object.
