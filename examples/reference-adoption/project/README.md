# Reference Tag Normalizer

This deliberately small, dependency-free Python module is the standalone software project used by the governed-delivery reference adoption.

The baseline behavior lowercases a tag, trims leading/trailing whitespace, and converts ordinary spaces to hyphens. The project exists to exercise the playbook against an inspectable code change rather than to provide production functionality.

Run its tests through the repository validation suite or directly with:

```bash
python3 -m unittest tests.test_reference_project -v
```
