---
description: Commit all changed files to git
---

You are an expert in writing github commit messages. I want you to:

1. Run git status -s to list all changed and untracked files.
2. Select the files you want to stage.
3. Stage the selected files using git add ...
4. (Optional) Run git diff --cached to review staged changes.
5. Enter a clear and concise commit message.
6. Commit the staged changes with git commit -m "your message".
7. If your branch has no upstream, run git push --set-upstream origin . Otherwise, just run git push.
