# README

my tools for making [HSC1](https://ajfarkas.dev/hyperspeedcube) filters. `filters.py` converts a filter string to an int and back, so you can use python's bitwise operations on them. `filters_oop.py` is intended for building up the entire filter sequence programmatically from atoms, though you can still use a raw filter string not constructed from atoms.

also check out milo's [hscfilter](https://milojacquet.com/hscfilter), which compiles a reasonable filter language to HSC1 filters. its expressiveness lies between `filters.py` and `filters_oop.py`, though it cannot be used for editing existing HSC1 filters; you must build them from scratch.
