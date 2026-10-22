# Sutadhana Course

Reading app for Sutadhana online Pāḷi course groups: lessons, a word-by-word reader,
spaced-repetition word review and a grammar guide. Plain static site (GitHub Pages).

## Content

- `data/groups/index.json` – the list of groups and which one is current.
- `data/groups/<id>.json` – one course group: schedule, links, earlier recordings,
  lessons (each a list of texts and grammar items, `published` true/false) and teacher notes.
- `data/library/` – shared texts, built from `tools/texts/*.py` by `tools/build_library.py`.
- `data/grammar/index.json` – grammar guide, built by `tools/build_grammar.py`.

Unpublished lessons can be checked by adding `?preview` to the address.

## Building texts

The library builder reads an index made from the Digital Pāḷi Dictionary sources
(`dpd-db`, `db/backup_tsv` headwords and `db/inflections/inflection_templates.xlsx`):

    python3 tools/build_library.py /path/to/dpd_idx.pkl

Word meanings come from the Digital Pāḷi Dictionary by Bodhirasa Bhikkhu (CC BY-NC-SA 4.0).
Translations are credited in each text.
