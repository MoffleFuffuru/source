# Upload this Stella source-review package to GitHub

## Recommended: GitHub Desktop (Windows)

1. Extract `Stella-V5-GitHub-Patched-Source-20261029.zip` into a new local folder. The extracted folder should contain `mako/`, `tests/`, `backend/`, `avatar/`, `README.md`, etc.
2. Install [GitHub Desktop](https://desktop.github.com/) and sign in.
3. If you already made an **empty** repository on GitHub, choose `File > Clone repository` in GitHub Desktop, select that repository, and clone it to your PC. Otherwise, use `File > New repository` and then `Publish repository` later.
4. Open the local clone folder via `Repository > Show in Explorer`.
5. **Copy the extracted files and folders** into the clone folder. Do not copy the ZIP itself as a substitute for extracting the source.
6. Back in GitHub Desktop, confirm the changes, enter a commit summary such as `Add Stella source review with verified fixes`, and click `Commit to main`.
7. Click `Push origin`. If you created the repo locally, click `Publish repository` and choose its visibility.

## Using the GitHub website instead
In the repository page, click `uploading an existing file` in Quick setup, or `Add file > Upload files`. Drag the **extracted files**, not the ZIP. GitHub's browser upload may limit batch size; upload in multiple batches or use GitHub Desktop for this ~200-file project.

## Privacy
If public, **anyone can download and copy the source**. This package intentionally removes logs, memories, recordings, heavy art and known example Discord IDs. It has undergone basic automated secret screening, but only you can determine whether usernames, project logic, and the remaining test examples are okay to publish. Prefer a private repository when in doubt. Ensure repository collaborators have permission to view the code and conversation material.
