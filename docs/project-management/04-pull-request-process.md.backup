# QUY TRÌNH PULL REQUEST

## 📖 Overview

Pull Request (PR) là cơ chế để review code trước khi merge vào codebase chính. 

**Benefits:**
- ✅ Code review → Catch bugs early
- ✅ Knowledge sharing
- ✅ Maintain code quality
- ✅ Documentation (PR history)

---

## 🚀 Creating a Pull Request

### Step 1: Prepare Your Branch

```bash
# 1. Ensure branch is up to date with develop
git checkout develop
git pull origin develop

# 2. Rebase your feature branch
git checkout feature/issue-2-postgresql-setup
git rebase develop

# If conflicts: 
#   - Resolve conflicts in files
#   - git add <resolved-files>
#   - git rebase --continue

# 3. Run tests locally
npm test              # Frontend
pytest               # Backend
flake8 app/          # Linting

# 4. Push branch
git push origin feature/issue-2-postgresql-setup --force-with-lease
```

### Step 2: Create PR on GitHub

```
1. Go to GitHub repository
2. Tab "Pull requests"
3. Click "New pull request"
4. Base:   develop (or main) ← Compare: feature/issue-2-postgresql-setup
5. Click "Create pull request"
```

### Step 3: Fill PR Template

**Title:**
```
[Issue #2] Setup PostgreSQL + PostGIS

Format:  [Issue #X] Short description
```

**Description:**

```markdown
## 📝 Description
Setup PostgreSQL 15 + PostGIS 3.4 on database server với performance configuration

Closes #2

## 🔧 Type of change
- [x] 🛠️ Infrastructure
- [ ] ✨ New feature
- [ ] 🐛 Bug fix
- [ ] 📚 Documentation
- [ ] ♻️ Refactoring

## 📦 Changes Made
- Installed PostgreSQL 15 from official repository
- Installed PostGIS 3.4 extension
- Created database `gisdb` and user `gisuser`
- Configured postgresql.conf:
  - shared_buffers = 8GB (25% of RAM)
  - effective_cache_size = 24GB (75% of RAM)
  - work_mem = 128MB
  - maintenance_work_mem = 2GB
- Enabled PostGIS extension
- Created spatial index on geometry columns
- Added connection test script

## 🧪 Testing
- [x] PostgreSQL service running:  `systemctl status postgresql`
- [x] PostGIS extension enabled: `SELECT PostGIS_version();`
- [x] Connection from app server successful
- [x] Spatial query test: `SELECT ST_AsText(ST_MakePoint(106.7, 10.8));` ✅
- [x] Performance test: Query 100K points < 1s ✅

## 📸 Screenshots
![PostgreSQL version](https://user-images.githubusercontent.com/. ../postgresql-version.png)
![PostGIS functions](https://user-images.githubusercontent.com/.../postgis-test. png)

## ✅ Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [x] Tests added/updated
- [x] Documentation updated (README. md, setup guide)
- [x] No console errors or warnings
- [x] Linting passed
- [x] All tests passing

## 🔗 Related Issues
- Closes #2
- Blocks #10 (Authentication API - can now proceed)

## 📝 Additional Notes
Chose PostgreSQL 15 over 14 for better performance with large spatial datasets.
PostGIS 3.4 required for new ST_MakeValid() function. 

Estimated vs Actual time:  8h estimated, 9h actual (1h spent on troubleshooting pg_hba.conf)

## 🔍 Reviewers
@droid2015 please review configuration settings
```

### Step 4: Assign Reviewers & Labels

```
**Right sidebar:**

Reviewers:  
- @droid2015 (PM - required)
- @teammate (Peer review - optional)

Assignees:
- @yourself

Labels:
- backend
- database
- needs review

Projects:
- GIS System - 12 Week Sprint

Milestone: 
- Tuần 1-2: Setup & Preparation

Linked issues:
- Closes #2 (auto-detected from description)
```

### Step 5: Notify Team

**In Issue #2:**
```markdown
@droid2015 PR is ready for review:  #45

All checklist items completed.  PostgreSQL and PostGIS working as expected. 
```

**In Slack/Teams (optional):**
```
PR #45 ready for review:  Setup PostgreSQL + PostGIS
https://github.com/droid2015/gis-geoserver-solution/pull/45
```

---

## 👀 Code Review Process

### For PR Author:  Preparing for Review

**Self-review checklist:**

```markdown
Before requesting review:
- [ ] Read your own code changes (line by line)
- [ ] Check for: 
  - [ ] Commented-out code → Remove
  - [ ] console.log() / print() debug → Remove
  - [ ] Hardcoded values → Use config
  - [ ] Magic numbers → Use constants
  - [ ] TODO comments → Create issues or resolve
  - [ ] Formatting inconsistencies
  - [ ] Missing error handling
  - [ ] Missing input validation
- [ ] Run linter:  flake8, eslint
- [ ] Run tests: All passing
- [ ] Update documentation if needed
- [ ] Add comments for complex logic
```

### For Reviewers: How to Review

#### Step 1: Check PR Overview

```
1. Read PR description
2. Understand what problem it solves
3. Check linked issue
4. Note testing done by author
```

#### Step 2: Review Code Changes

```
1. Click "Files changed" tab
2. Review each file:
   - Click line number to add comment
   - Use "Add single comment" for specific feedback
   - Use "Start a review" to batch comments
```

**What to look for:**

✅ **Functionality**
- Does code solve the problem?
- Does it handle edge cases?
- Are there potential bugs?

✅ **Code Quality**
- Is code readable?
- Are functions/variables named clearly?
- Is code DRY (Don't Repeat Yourself)?
- Is complexity reasonable?

✅ **Performance**
- Are there performance issues?
- Can queries be optimized?
- Are there memory leaks?

✅ **Security**
- Are inputs validated?
- Are SQL injections prevented?
- Are secrets hardcoded? 
- Is authentication/authorization correct?

✅ **Tests**
- Are tests adequate?
- Do tests cover edge cases?
- Are tests passing?

✅ **Documentation**
- Are comments clear?
- Is documentation updated?
- Are API endpoints documented?

#### Step 3: Leave Review Comments

**Types of comments:**

**1. Required changes (blocking):**
```markdown
**🔴 Required:**  Please add error handling for database connection failure. 

If PostgreSQL is down, the app will crash.  Add try-catch block: 

\```python
try:
    conn = psycopg2.connect(...)
except psycopg2.OperationalError as e:
    logger.error(f"Database connection failed: {e}")
    raise HTTPException(status_code=503, detail="Database unavailable")
\```
```

**2. Suggestions (non-blocking):**
```markdown
**💡 Suggestion:** Consider using environment variable for `shared_buffers` value.

This allows easier configuration per environment (dev/staging/prod) without code changes. 

\```python
SHARED_BUFFERS = os.getenv('PG_SHARED_BUFFERS', '8GB')
\```
```

**3. Questions:**
```markdown
**❓ Question:** Why did you choose `work_mem = 128MB`?

Does this value work for our expected query complexity?
```

**4. Praise (important!):**
```markdown
**✅ Nice! **  Great documentation in the setup script.  This will help future developers.
```

**5. Nitpicks:**
```markdown
**🔧 Nitpick:** Typo in comment:   "cofiguration" → "configuration"
```

#### Step 4: Submit Review

```
1. Click "Review changes" (top right)
2. Add summary comment
3. Choose: 
   - ✅ **Approve** - LGTM (Looks Good To Me)
   - 💬 **Comment** - General feedback, no approval
   - ❌ **Request changes** - Must fix before merge
4. Click "Submit review"
```

**Review summary template:**

```markdown
## Review Summary

**Overall:** Good work!   PostgreSQL setup looks solid.

**✅ Strengths:**
- Excellent documentation
- Comprehensive testing
- Good error handling
- Performance configuration well thought out

**🔴 Required Changes:**
- Add error handling for connection failure (line 45)
- Remove hardcoded password (line 78) - use environment variable

**💡 Suggestions:**
- Consider using connection pooling (non-blocking)
- Add monitoring for slow queries (nice-to-have)

**Estimated time to address:** ~1 hour

Please address required changes and re-request review.  Thanks!
```

---

## 🔄 Addressing Review Comments

### Author Response

**For each comment:**

```markdown
**Reviewer:** 
> Add error handling for connection failure

**Your reply:**
✅ **Done.**  Added try-catch block in `database.py` line 45-50.  
Updated in commit `abc1234`.

---

**Reviewer:**
> Consider using connection pooling

**Your reply:**
💡 **Good idea.**  Created issue #50 to implement connection pooling in Week 3.  
Will keep current implementation for now to unblock Week 2 work.

---

**Reviewer:**
> Typo:  "cofiguration"

**Your reply:**
✅ **Fixed** in commit `def5678`.
```

### Making Changes

```bash
# Make requested changes
git checkout feature/issue-2-postgresql-setup

# Edit files
# ... 

# Commit changes
git add .
git commit -m "fix(database): Address review comments

- Add error handling for connection failure
- Use env var for passwords
- Fix typo in comments

Addresses review comments in PR #45"

# Push
git push origin feature/issue-2-postgresql-setup
```

### Re-request Review

```
1. Reply to all comments
2. Click "Re-request review" button (reviewer's name, circular arrow icon)
3. Or comment: 
   ```
   @droid2015 All review comments addressed. Ready for re-review.
   ```
```

---

## ✅ Approving & Merging

### Approval

**Reviewer clicks "Approve":**

```markdown
## ✅ Approved

All comments addressed. Code looks good! 

**LGTM** (Looks Good To Me)

Approving and merging. 
```

### Merge Options

**Option 1: Merge commit (default)**
```
Preserves all commits from feature branch
History:  All commits visible

Use when: Want full history
```

**Option 2: Squash and merge (recommended)**
```
Combines all commits into one
History: Clean, linear

Use when: Feature has many WIP commits

Final commit message:
[Issue #2] Setup PostgreSQL + PostGIS (#45)

* Install PostgreSQL 15
* Install PostGIS 3.4
* Configure for production
* Add tests
```

**Option 3: Rebase and merge**
```
Rebases feature branch commits onto base
History: Linear, preserves individual commits

Use when: Feature has meaningful commit history
```

**Our project standard:  Squash and merge ✅**

### Merge Checklist

```markdown
Before merging:
- [ ] All required reviewers approved
- [ ] All CI/CD checks passing (GitHub Actions green)
- [ ] No merge conflicts
- [ ] Branch up to date with base
- [ ] All review comments addressed
- [ ] Linked issue exists and correct
```

### After Merge

**Automatic:**
- ✅ PR marked as merged
- ✅ Linked issue auto-closed (if "Closes #X" used)
- ✅ Branch can be deleted

**Manual:**
- ✅ Delete branch (click button on PR page)
- ✅ Update Project Board (move issue to "Done")
- ✅ Notify team if needed

**Author:**
```bash
# Pull latest
git checkout develop
git pull origin develop

# Delete local branch
git branch -d feature/issue-2-postgresql-setup

# Start next issue
git checkout -b feature/issue-3-git-repo-setup
```

---

## 🚨 Handling Merge Conflicts

### Cause

```
Your branch:         A → B → C → D (your commits)
Develop branch:     A → B → E → F (others' commits)

Conflict:  C and E modified same lines
```

### Resolution

#### Method 1: Rebase (Recommended)

```bash
# 1. Update develop
git checkout develop
git pull origin develop

# 2. Rebase feature branch
git checkout feature/issue-2-postgresql-setup
git rebase develop

# 3. Git will stop at conflicts
# CONFLICT (content): Merge conflict in app/database.py

# 4. Open conflicted files, look for: 
<<<<<<< HEAD (develop)
current code in develop
=======
your code
>>>>>>> feature/issue-2-postgresql-setup

# 5. Edit files to resolve conflicts
# Remove conflict markers, keep correct code

# 6. Mark as resolved
git add app/database.py

# 7. Continue rebase
git rebase --continue

# 8. Force push (rebase rewrites history)
git push origin feature/issue-2-postgresql-setup --force-with-lease
```

#### Method 2: Merge (Alternative)

```bash
# 1. Update develop
git checkout develop
git pull origin develop

# 2. Merge develop into feature branch
git checkout feature/issue-2-postgresql-setup
git merge develop

# 3. Resolve conflicts (same as rebase steps 4-6)

# 4. Commit merge
git commit -m "Merge develop into feature/issue-2"

# 5. Push
git push origin feature/issue-2-postgresql-setup
```

#### Method 3: GitHub UI (Simple conflicts only)

```
1. On PR page, click "Resolve conflicts"
2. Edit files in web editor
3. Click "Mark as resolved"
4. Click "Commit merge"
```

### Preventing Conflicts

```
✅ Do: 
- Pull develop frequently
- Rebase feature branch regularly
- Keep PRs small (< 500 lines)
- Communicate with team about files you're editing

❌ Don't:
- Work on feature branch for weeks without syncing
- Edit same files as teammates without coordination
- Have multiple features in one PR
```

---

## 📏 PR Best Practices

### Size Guidelines

| Size | Lines Changed | Review Time | Recommended |
|------|---------------|-------------|-------------|
| XS | < 10 | < 10 min | ✅ Ideal |
| S | 10-100 | < 30 min | ✅ Good |
| M | 100-300 | < 1 hour | ✅ OK |
| L | 300-500 | 1-2 hours | ⚠️ Consider splitting |
| XL | > 500 | > 2 hours | ❌ Too large, split |

**If PR > 500 lines:**
- Split into multiple PRs
- Each PR is independently mergeable
- Link PRs together

### Commit Messages

✅ **Good:**
```
feat(auth): Add JWT authentication

- Implement login endpoint
- Add token generation
- Add middleware for protected routes

Refs #10
```

❌ **Bad:**
```
update
fix stuff
WIP
asdfasdf
```

**Convention:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Build, dependencies

### PR Description

✅ **Good:**
```markdown
## Description
Clear summary of what and why

## Changes
- Bullet list of changes
- Each change is atomic

## Testing
Specific test cases, screenshots

## Checklist
All items checked
```

❌ **Bad:**
```
did some stuff
```

### Review Turnaround Time

| Priority | Target | Maximum |
|----------|--------|---------|
| Critical | 1 hour | 2 hours |
| High | 2 hours | 4 hours |
| Normal | 4 hours | 1 day |
| Low | 1 day | 2 days |

**Reviewer SLA:**
- Check PRs 3x per day:  Morning, after lunch, before EOD
- Prioritize `priority:  high` PRs
- If can't review in time → delegate to another reviewer

---

## 🔒 Branch Protection Rules

### Main Branch Protection

```
Settings → Branches → Branch protection rules → main

☑ Require pull request reviews before merging
  Reviewers required: 1
  ☑ Dismiss stale reviews when new commits pushed
  ☑ Require review from Code Owners (if CODEOWNERS file exists)

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date
  Required checks: 
    - CI/CD (GitHub Actions)
    - Tests
    - Linting

☑ Require conversation resolution before merging

☑ Require signed commits (optional)

☑ Include administrators (optional - PM can bypass)

☐ Allow force pushes (disabled)
☐ Allow deletions (disabled)
```

### Develop Branch Protection

```
Same as main, but: 
☐ Include administrators (PM can bypass for hotfixes)
```

---

## 🎯 Quick Reference

### PR Workflow

```
1. Create branch:    git checkout -b feature/issue-X
2. Code & commit:  git commit -m "type(scope): message"
3. Push:  git push origin feature/issue-X
4. Create PR:  GitHub → New PR
5. Fill template:  Description, testing, checklist
6. Assign reviewers:   @droid2015
7. Address comments:  Make changes, push
8. Get approval:  LGTM from reviewer
9. Merge:  Squash and merge
10. Cleanup:  Delete branch, pull develop
```

### Common Commands

```bash
# Create feature branch
git checkout -b feature/issue-X

# Rebase with develop
git pull origin develop --rebase

# Force push after rebase
git push origin feature/issue-X --force-with-lease

# Update branch with develop
git checkout develop && git pull
git checkout feature/issue-X
git rebase develop

# Resolve conflicts
git add <file>
git rebase --continue

# Abort rebase
git rebase --abort
```

### Review Checklist

```markdown
Code Reviewer:
- [ ] Solves the problem described in issue
- [ ] Code is readable and maintainable
- [ ] Tests cover main scenarios
- [ ] No obvious bugs
- [ ] Performance is acceptable
- [ ] Security best practices followed
- [ ] Documentation updated
```

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
