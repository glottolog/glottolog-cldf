# Releasing glottolog-cldf

- Edit the changelog:
  ```shell
  vi CHANGELOG.md
  ```
- Recreate the CLDF data from the appropriate version of glottolog/glottolog: (about 15mins)
  ```shell
  cldfbench makecldf --with-cldfreadme --with-zenodo --glottolog-version v<version> cldfbench_glottolog.py
  cldfbench readme cldfbench_glottolog.py
  ```
- Make sure the data is valid:
  ```shell
  pytest
  ```
- Commit, tag and push:
  ```shell
  git commit -a -m"release <release>"
  git tag -a v<version> -m "release <version>"
  git push origin
  git push --tags origin
  ```
- Publish the release on Zenodo.
