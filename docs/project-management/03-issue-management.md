# QUẢN LÝ ISSUES

## 📋 Tổng quan

GitHub Issues là công cụ chính để quản lý tasks, bugs, và feature requests trong dự án. 

---

## 🔍 Xem Issues của mình

### Cách 1: Filter trên GitHub

```
1. Vào repo → Issues tab
2. Trong search bar, nhập: 
   is:open is:issue assignee:@me

3. Hoặc click "Assigned to you" trong sidebar
```

### Cách 2: Sử dụng URL trực tiếp

```
https://github.com/droid2015/gis-geoserver-solution/issues?q=is%3Aopen+is%3Aissue+assignee%3A%40me
```

Bookmark URL này để truy cập nhanh! 

### Cách 3: GitHub Mobile App

```
1. Mở GitHub app
2. Repositories → gis-geoserver-solution
3. Issues → Filter:  Assigned to me
```

---

## 📝 Anatomy of an Issue

### Issue Structure

```markdown
Title: [NV A] Setup PostgreSQL + PostGIS

Labels: backend, database, week1-2, priority: high
Milestone:  Tuần 1-2: Setup & Preparation
Assignees: @droid2015
Projects: GIS System - 12 Week Sprint

## 🎯 Mục tiêu
Install PostgreSQL 15 + PostGIS 3.4 và cấu hình database

## ✅ Checklist
- [x] Install PostgreSQL 15
- [x] Install PostGIS 3.4
- [x] Create database `gisdb`
- [ ] Configure postgresql.conf
- [ ] Test connection

## 📦 Deliverables
- ✅ PostgreSQL running
- ✅ PostGIS extension enabled

## ⏱️ Time estimate
8 hours (1 ngày)

## 🔗 Dependencies
- Depends on: #1 (Server setup)
- Blocks: #10 (Backend API)
```

---

## 🎯 Working on an Issue

### Step 1: Claim the Issue

Khi bắt đầu work: 

```markdown
**Comment:**
🔄 Started working on this issue. 

**Actions:**
1. Self-assign (nếu chưa được assign)
2. Move to "In Progress" trên Project Board
3. Add label "in progress"
```

### Step 2: Create Branch

```bash
# Naming convention: feature/issue-NUMBER-short-description
git checkout develop
git pull origin develop
git checkout -b feature/issue-2-postgresql-setup

# For bugs:  bugfix/issue-NUMBER-description
git checkout -b bugfix/issue-15-login-error
```

### Step 3: Work & Commit

```bash
# Make changes
# ... 

# Commit with meaningful message
git add .
git commit -m "feat(database): Install PostgreSQL 15 and PostGIS 3.4

- Install PostgreSQL from official repo
- Install PostGIS extension
- Create gisdb database and gisuser role
- Configure basic postgresql.conf settings

Refs #2"

# Push regularly
git push origin feature/issue-2-postgresql-setup
```

**Commit Message Convention:**

```
<type>(scope): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```
feat(auth): Add JWT authentication

- Implement login endpoint
- Add JWT token generation
- Add authentication middleware

Refs #10
```

### Step 4: Update Checklist

```markdown
## ✅ Checklist
- [x] Install PostgreSQL 15
- [x] Install PostGIS 3.4
- [x] Create database `gisdb`
- [x] Create user `gisuser`
- [x] Enable PostGIS extension
- [ ] Configure postgresql.conf (IN PROGRESS) ← Update này
- [ ] Test connection
```

Click vào checkbox để toggle status. 

### Step 5: Comment Progress

**Daily update template:**

```markdown
## Progress Update - 2025-12-30

✅ **Completed today:**
- Installed PostgreSQL 15 successfully
- Installed PostGIS 3.4
- Created database and user

🔄 **Currently working on:**
- Configuring postgresql.conf for performance
- Setting shared_buffers = 8GB
- Configuring work_mem = 128MB

⏭️ **Next:**
- Test connection from app server
- Verify PostGIS functions

⏱️ **Time spent:** 5 hours (out of 8 estimated)

🚫 **Blockers:** None

📸 **Screenshots:**
![PostgreSQL version](screenshot.png)
```

### Step 6: Log Time

```markdown
## Time Log

| Date | Hours | Activity |
|------|-------|----------|
| 2025-12-30 | 2h | Install PostgreSQL |
| 2025-12-30 | 2h | Install PostGIS |
| 2025-12-30 | 1h | Create database & user |
| 2025-12-31 | 2h | Configure performance settings |
| 2025-12-31 | 1h | Test connection |
| **Total** | **8h** | **As estimated ✅** |
```

---

## 🚀 Completing an Issue

### Step 1: Final Checklist

```markdown
Before creating PR:
- [ ] All checklist items completed
- [ ] Code tested locally
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console errors
- [ ] Code formatted
- [ ] Self-review done
```

### Step 2: Create Pull Request

```bash
# Ensure branch is up to date
git checkout develop
git pull origin develop
git checkout feature/issue-2-postgresql-setup
git rebase develop

# Fix conflicts if any
# ...

# Push
git push origin feature/issue-2-postgresql-setup --force-with-lease

# Go to GitHub → Create Pull Request
```

**PR Title:**
```
[Issue #2] Setup PostgreSQL + PostGIS
```

**PR Description:**
```markdown
Closes #2

## Changes
- Installed PostgreSQL 15
- Installed PostGIS 3.4
- Created database `gisdb` and user `gisuser`
- Configured postgresql.conf for performance
- Added connection test script

## Testing
- [x] PostgreSQL service running
- [x] PostGIS extension enabled
- [x] Connection from app server successful
- [x] Sample spatial query:  `SELECT PostGIS_version();` working

## Screenshots
![PostgreSQL running](screenshot1.png)
![PostGIS enabled](screenshot2.png)
```

### Step 3: Link PR to Issue

**Method 1: Trong PR description**
```markdown
Closes #2
```

**Method 2: Trong issue comment**
```markdown
Created PR #45 to resolve this issue. 
```

**Method 3: Trong commit message**
```bash
git commit -m "feat(database): Complete PostgreSQL setup

Closes #2"
```

### Step 4: Request Review

```
1. Assign reviewers:  @droid2015 hoặc peer reviewer
2. Add labels:   needs review
3. Notify in issue comment: 
   ```
   @droid2015 PR is ready for review:  #45
   ```
```

### Step 5: Address Review Comments

```markdown
**Reviewer comment:**
> Can you add error handling for database connection?

**Your reply:**
✅ Added try-catch block in connection. py.   Updated in commit abc123.
```

```bash
# Make changes
git add .
git commit -m "fix(database): Add error handling for connection"
git push origin feature/issue-2-postgresql-setup
```

### Step 6: After Merge

```
1. PM merges PR
2. Issue auto-closes (if "Closes #2" was used)
3. Delete branch (GitHub will prompt)
4. Update Project Board (move to "Done")
5. You:  Pull latest develop
   ```bash
   git checkout develop
   git pull origin develop
   git branch -d feature/issue-2-postgresql-setup
   ```
```

---

## 🆘 Handling Blockers

### Identifying a Blocker

**Blocker = Cannot proceed without external help**

Examples:
- ❌ Waiting for database access from IT
- ❌ Dependency on another team's API
- ❌ Missing requirements/specifications
- ❌ Infrastructure not ready
- ❌ Critical bug in dependency

**NOT blockers:**
- ✅ Don't know how to code X → Ask teammate
- ✅ Bug in own code → Debug
- ✅ Test failing → Fix test

### Reporting a Blocker

**Step 1: Comment in issue**

```markdown
@droid2015 **🚫 BLOCKER**

**Issue:** Cannot connect to database server from app server

**Tried:**
- Checked firewall:  Port 5432 is closed
- Pinged server:   Timeout
- Checked pg_hba.conf: Looks correct

**Need:** 
- Firewall rule to allow app server IP (192.168.1.10) to access DB server port 5432
- Or VPN access to database server

**Impact:**
- Cannot proceed with #2 (PostgreSQL setup)
- Blocking #10 (Backend API) which depends on this

**Urgency:** High - blocking sprint progress
```

**Step 2: Add label**

```
Add label: blocked
```

**Step 3: Update Project Board**

```
Move card to "Blocked" column (if exists)
Or add 🚫 emoji to card title
```

**Step 4: Work on other tasks**

```
While waiting: 
- Switch to another non-blocked issue
- Help teammate with their issue
- Write documentation
- Refactor code
```

### PM Response to Blocker

```markdown
**PM Reply:**
@nhanvien_a Thanks for reporting.  I'll contact IT now. 

**Action items:**
- [ ] Email IT for firewall rule
- [ ] Escalate to manager if needed
- [ ] ETA:   Within 2 hours

**Meanwhile:**
Can you start working on #3 (Git repo setup)? 

**Update [1 hour later]:**
✅ IT opened firewall port 5432.  You can proceed now.
```

---

## 🏷️ Using Labels

### Category Labels

| Label | Use When | Example |
|-------|----------|---------|
| `backend` | Backend code | API, database, server |
| `frontend` | Frontend code | React, UI, components |
| `gis` | GIS-specific | QGIS, GeoServer, spatial |
| `database` | Database work | Schema, queries, optimization |
| `documentation` | Writing docs | README, user guide, API docs |

### Priority Labels

| Label | Use When | SLA |
|-------|----------|-----|
| `priority: critical` | Production down, data loss | < 4 hours |
| `priority: high` | Blocks sprint, urgent | < 1 day |
| `priority: medium` | Important but not urgent | < 3 days |
| `priority: low` | Nice to have | < 1 week |

### Status Labels

| Label | Use When |
|-------|----------|
| `blocked` | Cannot proceed |
| `needs review` | Code ready for review |
| `in progress` | Actively working |
| `on hold` | Paused temporarily |

### Type Labels

| Label | Use When |
|-------|----------|
| `bug` | Something broken |
| `feature` | New functionality |
| `enhancement` | Improve existing |
| `question` | Need clarification |

### Adding Labels

**Method 1: On issue page**
```
Right sidebar → Labels → Click labels to add/remove
```

**Method 2: In comment**
```
/label bug
/label priority: high
```

---

## 🔗 Issue Relationships

### Dependencies

**Issue #10 depends on Issue #2:**

```markdown
## Issue #10:  Authentication API

## Dependencies
- **Depends on:** #2 (PostgreSQL setup must complete first)

@droid2015 Waiting for #2 to complete before starting this. 
```

**In Issue #2:**
```markdown
## Issue #2: PostgreSQL Setup

## Blocks
- **Blocks:** #10 (Authentication API)

Note:   #10 is waiting on this, prioritizing completion. 
```

### Related Issues

```markdown
## Related Issues
- Related to #3 (uses same server)
- See also #5 (similar configuration)
```

### Sub-tasks

For large issues, create sub-tasks:

```markdown
## Issue #20: Spatial Query API

**Sub-tasks:**
- [ ] #21 - Nearby features API
- [ ] #22 - Intersect API
- [ ] #23 - Buffer API
- [ ] #24 - Nearest features API
```

Create separate issues for each sub-task and link back to parent.

---

## 🔍 Searching Issues

### Basic Search

```
# My open issues
is:open is:issue assignee:@me

# My closed issues
is:closed is: issue assignee:@me

# Issues with specific label
is:open is:issue label:"backend"

# Issues in milestone
is:open is:issue milestone:"Tuần 1-2: Setup & Preparation"

# High priority issues
is:open is: issue label:"priority: high"
```

### Advanced Search

```
# Unassigned issues
is:open is:issue no:assignee

# Issues mentioning me
is:open is:issue mentions:@me

# Issues created by me
is:open is: issue author:@me

# Issues with no labels
is:open is:issue no:label

# Issues updated recently
is:open is:issue updated:>2025-12-25

# Issues with comments from specific user
is:open is:issue commenter:@droid2015
```

### Search Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `is:` | `is:open` | Issue state |
| `label:` | `label:bug` | Has label |
| `assignee:` | `assignee:@me` | Assigned to |
| `author:` | `author:@me` | Created by |
| `mentions:` | `mentions:@me` | Mentions user |
| `milestone:` | `milestone:"Week 1"` | In milestone |
| `created:` | `created:>2025-12-01` | Created date |
| `updated:` | `updated:<2025-12-25` | Updated date |
| `no:` | `no:assignee` | Missing attribute |

---

## 📊 Issue Templates

### Using Issue Templates

```
1. Click "New issue"
2. Choose template:
   - 📋 Task
   - 🐛 Bug Report
   - 💡 Feature Request
3. Fill in template
4. Create issue
```

### Task Template

```markdown
---
name: 📋 Task
about: Standard task for team members
---

## 🎯 Mục tiêu
<!-- Describe the goal -->

## ✅ Checklist
- [ ] Step 1
- [ ] Step 2

## 📦 Deliverables
- Item 1
- Item 2

## ⏱️ Time estimate
X hours

## 🔗 Dependencies
- Depends on: #
- Blocks: #

## 📚 Resources
- [Link]
```

### Bug Report Template

```markdown
---
name: 🐛 Bug Report
about: Report a bug
---

## 🐛 Description
<!-- What's the bug? -->

## 📋 Steps to Reproduce
1. Go to... 
2. Click...
3. See error

## ✅ Expected
<!-- What should happen -->

## ❌ Actual
<!-- What happens -->

## 🖼️ Screenshots
<!-- If applicable -->

## 🌐 Environment
- Browser: 
- OS:
- Version: 
```

---

## 💡 Best Practices

### Issue Titles

✅ **Good:**
```
[NV A] Setup PostgreSQL + PostGIS
[NV C] Implement authentication UI
[BUG] Login button not working
[FEATURE] Export map to PDF
```

❌ **Bad:**
```
Setup stuff
Fix bug
Need help
TODO
```

**Format:**
```
[WHO/TYPE] Clear, specific description

Examples:
[NV A] Install Docker on app server
[BUG] Map not loading on mobile
[FEATURE] Add password reset
```

### Issue Descriptions

✅ **Good:**
```markdown
## Goal
Install PostgreSQL 15 + PostGIS 3.4 on database server

## Steps
1. Add PostgreSQL repository
2. Install packages
3. Create database
4. Configure for production

## Success Criteria
- PostgreSQL running
- PostGIS extension working
- Connection from app server successful
```

❌ **Bad:**
```
Install database
```

### Comments

✅ **Good:**
```markdown
## Progress - 2025-12-30

✅ Completed:  PostgreSQL installed
🔄 In Progress: PostGIS configuration
⏱️ Time: 3 hours

Encountered issue with PostGIS 3.3 compatibility.
Upgraded to 3.4, now working.

Next: Test spatial queries
```

❌ **Bad:**
```
Done some stuff
```

### Closing Issues

✅ **Good:**
```markdown
✅ All checklist items completed
✅ PR #45 merged
✅ Tested on staging
✅ Documentation updated

Closing issue as complete.
```

❌ **Bad:**
```
Done
```

---

## 🎯 Quick Reference

### Issue Lifecycle

```
Created → Assigned → In Progress → PR Created → In Review → Merged → Closed
```

### Key Actions

| Action | How |
|--------|-----|
| **Claim issue** | Self-assign, comment "Working on this" |
| **Update progress** | Comment daily with ✅🔄⏱️ |
| **Report blocker** | Comment `@pm BLOCKER: ` + add label |
| **Link PR** | PR description:  `Closes #X` |
| **Close issue** | Merge PR (auto) or manual close |

### Time Estimates

| Size | Hours | Days |
|------|-------|------|
| XS | 1-2h | 0. 25 day |
| S | 2-4h | 0.5 day |
| M | 4-8h | 1 day |
| L | 8-16h | 2 days |
| XL | 16-40h | 1 week |

If > 40h → Break into smaller issues

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
