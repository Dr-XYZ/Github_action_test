name: Fix Chinese-English spacing in Markdown

on:
  push:
    branches:
      - main  # 或是你的目標分支

jobs:
  fix-spacing:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 拉取完整的 commit history

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies (if any)
        run: pip install --upgrade pip

      - name: Get the list of changed .md files
        id: get_files
        run: |
          files=$(git diff --name-only ${{ github.event.before }} ${{ github.sha }} | grep '\.md$')
          echo "changed_files=$files" >> $GITHUB_ENV

      - name: Run spacing fixer on changed files
        run: |
          for file in ${{ env.changed_files }}; do
            echo "Fixing spacing in $file"
            python .github/scripts/fix_spacing.py $file
          done

      - name: Commit and push changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "chore: auto-fix spacing in Markdown files"
            git push
          fi
