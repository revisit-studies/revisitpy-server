# Usage

`pip install revisitpy_server`

or

`uv add revisitypy_server`

```python
```

# Development

1. Pulling latest copy of the study repo
2. Changing env files to use "/" instead of "/study/"
3. `yarn run build`
4. Copy "dist" directory into "src/revisitpy_server"
5. Delete static directory
6. Rename dist to static
7. Update pyproject.toml with new version
8. build and push

## Publishing

Package major/minor versions follow ReVISit. Study release notifications must
include `client_payload.release_tag` (`vX.Y.Z`); the build uses that exact study
tag. A new study series starts at `X.Y.0`; another publication in that series
increments the package patch independently. Older study series are rejected.

For a manual publication or an independent package patch, run
`new_version.yml` on `main` with
`study_tag` (for example, `v3.0.0`). An optional `release_version` selects an exact
package version in the same major/minor series, including the current version
for retrying a failed publication. PyPI rejects duplicate artifacts.

Publishing runs are serialized and push their version, lockfile, and bundled
assets before publishing. If `main` changes during the build, the push fails and
publication stops; start a new run from the updated branch.
