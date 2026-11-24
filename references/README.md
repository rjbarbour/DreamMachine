# References

Everything the project cites is recorded here so that a claim in the docs can be
traced to a source someone actually opened.

| Path | Committed | Contents |
|------|-----------|----------|
| `manifest.jsonl` | yes | One JSON record per source: identifiers, the URL opened, whether it was opened, what we use it for, and the checksum of any downloaded copy |
| `notes/` | yes | Our own research notes and the prior-art reports, which cite manifest keys |
| `cache/` | **no** (git-ignored) | Raw downloaded copies of sources |

## Why the cache is not committed

This repository is public and most of the sources are copyrighted journal articles
or web pages with no stated licence (Izhikevich's `spnet.m` carries none). The
manifest keeps the URL and SHA-256 of each cached file, so the cache can be rebuilt
and checked on any machine:

```bash
python scripts/refs.py fetch     # download every source that has a fetch_url
python scripts/refs.py verify    # compare cached files with recorded checksums
python scripts/refs.py list      # one line per source
```

A source whose licence permits redistribution may be committed under `open/` and
noted in its manifest record; none has been so far.

## Manifest fields

| Field | Meaning |
|-------|---------|
| `key` | Stable short name used to cite the source from docs and backlog tasks |
| `type` | `paper`, `software`, `dataset` or `webpage` |
| `title`, `authors`, `year`, `venue`, `doi`, `pmid` | Bibliographic details; empty when not seen on the page |
| `url` | The page that was opened |
| `opened` | `true` only if someone loaded the page or abstract. `false` means the citation is second-hand and must be checked before anything depends on it |
| `open_access`, `licence` | As stated by the source |
| `used_for` | Why the project cares |
| `source_report` | Which notes file introduced the record |
| `added` | Date the record was added |
| `fetch_url`, `local_file`, `sha256`, `bytes`, `retrieved` | Set when a raw copy is kept in the cache |

## Rules

1. A source enters the docs only through the manifest.
2. A record with `opened: false` may be listed as a lead but not used to support a
   requirement, a parameter value or a validation target.
3. New sources are added with `python scripts/refs.py import FILE.jsonl --report NAME`
   rather than by editing the manifest by hand, so duplicates are merged.
