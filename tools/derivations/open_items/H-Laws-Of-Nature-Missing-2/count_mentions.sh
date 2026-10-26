#!/bin/sh
# H-Laws-Of-Nature-Missing-2: counts of each law's name in the three documents (read-only; the table's "none" cells rest on a 0 here).
cd "$(dirname "$0")/../../../.." || exit 1
for t in "angular momentum" "Noether" "baryon" "lepton" "CPT" "Doppler" "polarisation" "black body" "equipartition" "entropy" "second law" "contraction" "twin" "inflation" "flatness" "uniformity" "fusion" "tunnel" "exclusion" "uncertainty" "Bell" "GHZ" "two slits" "horizon" "Hawking" "dark energy" "dark matter" "neutrino" "quark" "confinement" "exponential decay" "Zeeman" "Lorentz" "dilation" "redshift" "deflection" "free fall" "Maxwell" "Coulomb" "Casimir" "Aharonov" "parity" "lattice momentum" "conserved form" "Bohr" "mass ratio" "temperature" "arrow of time" "perihelion" "frame dragging" "gravitational wave" "Compton" "material ruler" "generations"; do
  a=$(grep -o -i "$t" docs/ALGEBRA.md | wc -l); u=$(grep -o -i "$t" docs/UNIVERSE24.md | wc -l); i=$(grep -o -i "$t" tools/derivations/open_items/INDEX.md | wc -l)
  echo "$t | ALGEBRA $a | UNIVERSE24 $u | INDEX $i"
done
