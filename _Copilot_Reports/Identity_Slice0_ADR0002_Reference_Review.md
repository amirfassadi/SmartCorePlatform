> Revision note: original findings below describe the uploaded candidate; the publication review supersedes dispositions it explicitly corrects.

# Slice 0 evidence — ADR-0002 version-reference review

Prepared: 2026-10-04. Status: DRAFT review evidence; not an architectural acceptance, not implementation permission. The uploaded review was local-only. Its publication review and corrections are recorded in Identity_Slice0_Publication_Review.md.

Rule applied (ADR-0002:711–713): version-pinned references are reviewed against the version each document actually adopts; a historical version mention is not an inconsistency by itself; no global replacement with v1.8.0.

## Classification (candidate tree, 30 old-version mentions found by pattern)

| Class | Locations | Disposition |
|---|---|---|
| Historical changelog entries | 026:640, 648, 652; 027:601, 605; 057:432, 436; 059:644, 651, 658; Audit_ADR_Dependency_Alignment_2026-09-24.md:26, 49, 128; _Copilot_Reports ADR-0004 propagation validation:18 | Correct as history. No change. |
| "This revision references ADR-0002 v1.7" notes | 026:630; 027:591; 057:422; 059:628 | Correct as history of what each revision adopted. No change. |
| Contractual pins to v1.7 | 026:9; 027:10, 311, 377; 057:8, 272, 291; 059:9, 271 | Adopted-version record. Must be reviewed against v1.8.0 (what changed v1.7.1 to v1.8.0 is the sequencing text in PR #6). Update only after that review; do not replace in bulk. |
| Contractual pins to older versions in body text | 059:448 ("v1.3 Decision 5"); 059:688 ("v1.4 Decision 8") | Read in context. 059:448: Decision 5 grew from 777 to 3206 normalized characters between v1.3 and v1.7.1/v1.8.0, with the classification (LoginFailed = Security Event; nine Domain Events) unchanged; the pin is old but the stated rule still holds. 059:688: the statement (PersonRegistered after Ready) matches v1.8.0; v1.4 predates the v1.6 OccurredAt clarification. Both need an owner-visible adopted-version record, not a content change. |
| Rule text naming a version | ADR-0002:713 mentions "an older reference to v1.7" inside a v1.8.0 document | Probably intentional historical wording. Flag only. |

Result: of the mentions read in context (059:448, 059:688 and the changelog entries), none was wrong on content. The v1.7 contractual pins listed above were classified by location and wording only and have not yet been compared against the v1.8.0 text. 9 contractual pins to v1.7 and 2 older body pins need a documented adoption decision. No file was edited.
