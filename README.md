# README

my tools for making [HSC1](https://ajfarkas.dev/hyperspeedcube) filters. `filters.py` converts a piece mask string to an int and back, so you can use python's bitwise operations on them. `filters_oop.py` is intended for building up the entire filter sequence programmatically from atoms, though you can still use a raw piece mask string taken from HSC1.

also check out milo's [hscfilter](https://milojacquet.com/hscfilter), which compiles a reasonable filter language to HSC1 filters. its expressiveness lies between `filters.py` and `filters_oop.py`, though it cannot be used for editing existing HSC1 filters; you must start from scratch.

note that for 4^4+, editing the raw piece mask allows you to obtain filters that the UI can't express, such as ones that distinguish indistinguishables. but if you start with valid piece masks and only use set operations, you cannot obtain illegal filters.

separately, i believe that the filters UI can express all legal filters.

## `filters.py` usage

### import piece mask strings from HSC1

1. open piece filters in HSC1, under `Tools > Pieces filters`.
2. using the `Types` and `Colors` dropdown, select some pieces.
3. under the `Presets` dropdown, enable `Edit presets`.
4. add a new preset with a new name (HSC1 behaves weirdly with duplicated names).
5. click `Edit as plaintext`.
6. find your preset and copy its `visible_pieces` (which i've been calling a piece mask string).

### operate on piece masks

1. in `filters.py` use the `to_int` function to convert the piece mask strings to python ints.
2. use python's bitset operations on them (`~`, `&`, `|`).
3. use the `to_string` function to convert the piece mask to a `str`.

### export piece mask strings to HSC1

figure it out.

## `filters_oop.py` usage

basically the same as `filters.py` except there's a `Filter` class with methods, and you can export an entire filter sequence at once.

it's more heavy duty bc
i was generating many variations of CFOP filters
and wanted masks for individual pieces to build with
but didn't want to make and export masks in the UI for all of them,
so i exported masks just for the cells
and generated piece (and F2L pair) masks from them.

## TODO

if you want some feature added, ping me in the hypercubes discord server.

- check whether puzzles other than 3^4 work.
- make puzzles other than 3^4 work.
