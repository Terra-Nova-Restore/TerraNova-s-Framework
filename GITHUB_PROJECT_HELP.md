# GitHub Projects v2 note

The Notion-to-GitHub controller does not currently read `PROJECTV2_ID` or mutate
GitHub Projects v2. Do not add `PROJECTV2_ID` as part of the sync setup unless a
separate project automation is implemented.

For manual project administration, this command can still fetch a user project id:

```bash
gh api graphql -f query='
query($login:String!, $number:Int!) {
  user(login:$login) {
    projectV2(number:$number) { id title }
  }
}' -f login='q9yx7n64w7-creator' -F number=1
```
