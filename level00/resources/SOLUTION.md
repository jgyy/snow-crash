# Level00 Solution

## Objective
Find the password to access the flag00 account and retrieve the token.

## Solution

### Step 1: Discover the Encoded Password
The password hint is hidden in a file with unusual permissions: `/usr/sbin/john`

```bash
cat /usr/sbin/john
# Output: cdiiddwpgswtgt
```

### Step 2: Decode the Password
The string `cdiiddwpgswtgt` is encoded using a Caesar cipher with shift 15.

**Decryption Method:**
Apply Caesar cipher shift 15 (or shift -11) to decrypt:
- `cdiiddwpgswtgt` > `nottoohardhere`

**Decoded Password:** `nottoohardhere`

### Step 3: Access flag00 Account
```bash
su flag00
# Enter password: nottoohardhere
```

### Step 4: Get the Flag Token
```bash
getflag
# Output: Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```

## Key Points
1. **Information Disclosure**: The encoded password is stored in a readable file (`/usr/sbin/john`) owned by flag00
2. **Weak Encryption**: The Caesar cipher is a simple substitution cipher that's easy to break
3. **Token**: The flag token for level01 is `x24ti5gi3x0ol2eh4esiuxias`

## Final Answer
**Flag00 Password:** `nottoohardhere`
**Level00 Token:** `x24ti5gi3x0ol2eh4esiuxias`
**Token for Level01:** `x24ti5gi3x0ol2eh4esiuxias`

## Decryption Details
Caesar cipher shift 15 transformation:
```
a->p, b->q, c->r, ..., p->e, q->f, ..., z->o
```

Applying to `cdiiddwpgswtgt`:
```
c->n, d->o, i->t, i->t, d->o, d->o, w->h, p->a, g->r, s->d, w->h, t->e, g->r, t->e
Result: nottoohardhere
```
