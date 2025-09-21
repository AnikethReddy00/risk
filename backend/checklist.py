from __future__ import annotations

# Minimal clause checklist (extend as needed)
CLAUSE_CHECKLIST = [
"Parties & Effective Date",
"Scope of Services / Deliverables",
"Payment Terms (amount, due date, late fees)",
"Term & Termination (for cause / convenience)",
"Confidentiality / NDA",
"Intellectual Property (ownership, license, background IP)",
"Warranties & Disclaimers",
"Liability Cap (amount, exclusions)",
"Indemnification (mutual / one-way, scope)",
"Governing Law & Venue",
"Dispute Resolution (mediation/arbitration)",
"Assignment / Subcontracting",
"Change Order / Amendment process",
"Force Majeure",
"Notices",
]

# Quick heuristic red-flag patterns (lowercase compare)
RISK_PATTERNS = [
("unlimited liability", "Unlimited liability"),
("indemnify and hold harmless", "Broad indemnity obligation"),
("sole discretion", "Counterparty has unilateral/sole discretion"),
("perpetual, irrevocable, worldwide, royalty-free", "Overbroad IP license grant"),
("assign this agreement without", "Unrestricted assignment by counterparty"),
("automatic renewal", "Auto-renewal without clear opt-out"),
("liquidated damages", "Liquidated damages risk"),
("injunctive relief", "Injunctive relief without balance"),
("at any time and for any reason", "Unilateral termination or change"),
("without notice", "Actions without notice"),
]
