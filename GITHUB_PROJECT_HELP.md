# Get GitHub ProjectV2 ID (user project #1)

```bash
gh api graphql -f query='
query($login:String!, $number:Int!) {
  user(login:$login) {
    projectV2(number:$number) { id title }
  }
}' -f login='q9yx7n64w7-creator' -F number=1
```

Copy the returned `id` into repo secret `PROJECTV2_ID`.
