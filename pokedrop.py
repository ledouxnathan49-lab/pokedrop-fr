name: PokéDrop Pro

on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: |
          pip install requests beautifulsoup4 lxml

      - name: Lancer PokéDrop
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: python pokedrop.py

      - name: Sauvegarder l'état
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add state.json
          git diff --cached --quiet || git commit -m "update state"
          git push || true