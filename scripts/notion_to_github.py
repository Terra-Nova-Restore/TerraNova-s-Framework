name: notion_to_github

on:
  workflow_dispatch:
  schedule:
    - cron: "*/10 * * * *"

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Export secrets to env
        run: |
          echo "NOTION_TOKEN=${{ secrets.NOTION_TOKEN }}" >> $GITHUB_ENV
          echo "NOTION_DATABASE_ID_CHANGES=${{ secrets.NOTION_DATABASE_ID_CHANGES }}" >> $GITHUB_ENV
          echo "GITHUB_TOKEN=${{ secrets.GH_PAT }}" >> $GITHUB_ENV

      - name: Run Notion to GitHub sync
        run: |
          python scripts/notion_to_github.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46

      - name: Commit and push changes
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Auto-update from Notion" || echo "No changes to commit"
          git push
