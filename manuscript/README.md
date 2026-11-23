# Sharp tails for Bala's inverse-function conjectures

Revision 2. Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang
(National University of Singapore; ChronoAI Pte Ltd, Singapore).
Licensed under CC BY 4.0 (`cc-by-4.0`).

## Mathematical content

`note.tex` is the main source. `note.pdf` is the corresponding readable note.
For the integer coefficients `u(n) = (2n)! [x^(2n)] C_5(x)`, Theorem 1 proves
least eventual period 18 modulo 27 from the exact index 2, and a zero tail
modulo 385 from the exact index 6. The preceding residue is `u(5) = 105 mod 385`.
The zero tails modulo 5, 7 and 11 begin at the exact indices 3, 4 and 6.

The general modular assertions are credited to Lien-Hung Su,
*Quadratic Derivations and Uniform Modular Periods for Six Inverse-Function
Sequences*, v1, October 31, 2026, DOI `10.5281/zenodo.23835577`.
The note specializes Theorem 3.2 and Corollary 3.3 for the even flows and
Theorem 4.1 for the odd flow. Its modulo-27 origin 2 improves the sufficient
origin 3 from that theorem. No priority claim is made.

The companion results comprise seven least-period certificates, five row
multipliers, the constant A281181 residue 1 modulo 12, a full-index consequence
for A281182, Bala's tentative A281183 derivative identity, and two corrected
coefficient normalizations. Exact dated OEIS locators and the coverage table
are in the note. A281182 is not itself a posed modular conjecture.

## Rebuild

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively use a LaTeX installation with the packages named in the source:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; BibTeX is unnecessary.
The source archive contains this README, `note.tex`, `metadata.json`,
`coverage.json`, `verify.py`, `checks.json`, `LICENSE.txt`, and `SHA256SUMS`.
`coverage.json` records detailed scientific locators and declaration scope.

## Exact arithmetic

Python 3, with its standard library, suffices:

```sh
python3 verify.py --output checks-rebuilt.json
cmp checks.json checks-rebuilt.json
sha256sum -c SHA256SUMS
```

`checks.json` gives eight complete finite period certificates, five row
certificates, three prime zero-tail certificates, and the modulo-12 identity.
The rank is `ceil(m/2)` for modulus `m`. Proposition 2 proves that the stated
consecutive zero differences or zero values propagate to every later index
by Cayley–Hamilton; the certificates include least-period and onset witnesses.

Two integer coefficient algorithms agree at indices 0 through 256 for
A281184, and at indices 0 through 64 for eight additional parameter pairs.
Fourteen further moduli each have 64 modular comparisons. These are exact
finite checks, distinct from the all-index certificate argument and Su's
general theorems. There is no floating-point arithmetic or rounding.

## Lean declaration scope

The pinned file
https://github.com/the-omega-institute/trureturing/blob/92de86888730265f84e24d28bdb67546c543a966/D5/S1/Recurrence/Periodic/BalaA281184TotientSquarePeriod.lean
contains `result` in its matching namespace: existence of the source series,
integer normalized coefficients of `C^3`, and the eventual totient-square
shift for every positive modulus.

The pinned file
https://github.com/the-omega-institute/trureturing/blob/92de86888730265f84e24d28bdb67546c543a966/D5/S1/Recurrence/Periodic/BalaA281181TotientSquarePeriod.lean
contains `BalaPolynomialSystem.even_sequence_coefficient` and
`BalaPolynomialSystem.even_sequence_period`: coefficient correspondence and
the square-period conclusion for flow exponent `q+1`, `q=3` or `7`, and any
nonnegative observable exponent.

The pinned file
https://github.com/the-omega-institute/trureturing/blob/92de86888730265f84e24d28bdb67546c543a966/D5/S1/Recurrence/Residue/BalaQuarticEGFEventualDivisibility.lean
contains `result` in its matching namespace: source existence and eventual
integer-multiple divisibility for every positive modulus coprime to 6. Its
statement does not include the exact modulo-385 origin or the second
A281428 conjecture for moduli divisible by 2 or 3.

The half-square periods and the all-modulus odd-flow conclusions are the cited
Su theorems. The exact origins, finite certificates, full-index consequence
and normalization identities have the written proofs in the note.
