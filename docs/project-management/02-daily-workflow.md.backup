# QUY TRÌNH LÀM VIỆC HÀNG NGÀY

## 📅 Daily Schedule

### 9:00 AM - Daily Standup (15 phút)

**Format:**

```markdown
## Daily Standup - [Date]

### Nhân viên A (@username_a)
- ✅ Yesterday:  Hoàn thành #1, #2. Bắt đầu #3
- 🔄 Today: Tiếp tục #3, dự kiến hoàn thành.  Bắt đầu #4
- 🚫 Blockers: Không có

### Nhân viên B (@username_b)
- ✅ Yesterday: Hoàn thành #4.  Import 30 substations vào DB
- 🔄 Today: Tiếp tục #5, thu thập data power lines
- 🚫 Blockers: Cần access vào database cũ - chờ phòng KT

### Nhân viên C (@username_c)
- ✅ Yesterday: Hoàn thành UI mockups (#8)
- 🔄 Today: Implement map component (#9)
- 🚫 Blockers: Không có

### Action Items: 
- [ ] PM: Contact phòng KT cho database access (NV B)
- [ ] NV A: Review PR #12 từ NV C
```

**Quy tắc:**
- ⏰ Đúng giờ - Start 9:00 AM sharp
- ⏱️ Ngắn gọn - Max 15 phút
- 🎯 Focus - Yesterday, Today, Blockers
- 💬 Discussions → After standup (breakout)

**Location:**
- Online:  Google Meet / Zoom
- Offline: Meeting room

---

## 🔄 Workflow trong ngày

### 1. Morning (9:00 - 12:00)

#### Sau Standup: 

**Team Members:**
```
9:15 - Check assigned issues
     - Mở Project Board:  https://github.com/droid2015/gis-geoserver-solution/projects/1
     - Filter:  assignee:@me is:open
     - Prioritize: urgent → high → medium → low

9:30 - Start working on issue
     - Move issue to "In Progress" column
     - Comment: "🔄 Started working on this"
     - Create branch: git checkout -b feature/issue-X-description

10:00 - Focus work
     - Code/design/document
     - Commit regularly (every 30-60 min)
     - Update checklist trong issue

11:30 - Update progress
     - Comment progress trong issue
     - Example: "✅ Completed 3/5 checklist items.  PostgreSQL installed và running."
```

**PM:**
```
9:30 - Review Project Board
     - Check "In Progress" column
     - Identify potential bottlenecks
     - Reply urgent comments

10:00 - Remove blockers
     - Contact phòng KT, IT, stakeholders
     - Provide resources/guidance

11:00 - Review Pull Requests
     - Check new PRs
     - Assign reviewers if needed
     - Review code changes
```

---

### 2. Lunch Break (12:00 - 13:00)

⏸️ Pause work, relax

---

### 3. Afternoon (13:00 - 17:00)

**Team Members:**
```
13:00 - Continue work
     - Resume từ morning
     - Focus on completing current task

15:00 - Coffee break (15 min)

15:15 - Final push
     - Complete checklist items
     - Write tests
     - Update documentation

16:30 - Wrap up
     - Commit & push code
     - Create Pull Request (if ready)
     - Update issue status
     - Comment EOD progress
```

**PM:**
```
13:00 - Review progress
     - Check Project Board
     - Reply comments

14:00 - Review PRs (priority)
     - Aim:  < 4 hours turnaround time
     - Provide feedback
     - Approve & merge if OK

15:00 - Planning for tomorrow
     - Review upcoming issues
     - Prepare sprint planning (if Friday)

16:30 - EOD update
     - Update milestone progress
     - Send quick status update to stakeholders (if needed)
```

---

## 📝 Issue Update Guidelines

### Comment Progress

**Template:**
```markdown
## Progress Update - [Date]

✅ **Completed:**
- Setup Docker on App server
- Install PostgreSQL 15
- Create database `gisdb`

🔄 **In Progress:**
- Installing PostGIS extension (70% done)
- Configuring postgresql.conf

⏭️ **Next:**
- Test connection from app server
- Performance tuning

⏱️ **Time spent today:** 6 hours
⏱️ **Total time:** 10 hours / 16 hours estimated

🚫 **Blockers:** None
```

### Update Checklist

```markdown
Issue #2:  Setup PostgreSQL + PostGIS

## Checklist
- [x] Install PostgreSQL 15
- [x] Install PostGIS 3.4
- [x] Create database `gisdb`
- [x] Create user `gisuser`
- [x] Enable PostGIS extension
- [ ] Configure postgresql.conf (performance tuning)  ← Working on this
- [ ] Test connection from app server
```

---

## 🚀 Pull Request Workflow

### 1. When to Create PR

```
✅ When: 
- Feature/task completed
- All checklist items done
- Code tested locally
- No console errors
- Documentation updated

❌ Don't create PR when:
- Work in progress (create Draft PR instead)
- Tests failing
- Merge conflicts
```

### 2. Create PR

```bash
# 1. Ensure branch is up to date
git checkout develop
git pull origin develop
git checkout feature/issue-X-description
git rebase develop

# 2. Push branch
git push origin feature/issue-X-description

# 3. Go to GitHub → Pull Requests → New PR
# 4. Fill PR template
# 5. Link issue:  "Closes #X" in description
# 6. Assign reviewers
# 7. Add labels
# 8. Create PR
```

### 3. PR Description Template

```markdown
## Description
Implement PostgreSQL + PostGIS setup on database server

Closes #2

## Changes
- Installed PostgreSQL 15
- Installed PostGIS 3.4
- Created database and user
- Configured performance settings
- Added connection test script

## Type of change
- [x] Infrastructure setup
- [ ] Bug fix
- [ ] New feature

## Testing
- [x] PostgreSQL service running
- [x] PostGIS extension enabled
- [x] Connection from app server successful
- [x] Sample spatial query working

## Screenshots
[Add screenshots if applicable]
```

### 4. Wait for Review

```
Notifications:
- GitHub sẽ notify reviewers
- Check email / GitHub notifications

Expected review time: 
- < 4 hours (working hours)
- < 1 day (maximum)

During review:
- Reply to comments
- Make requested changes
- Push updates to same branch
```

### 5. After Approval

```
PM/Reviewer will:
1. Approve PR
2. Merge to develop (or main)
3. Delete branch
4. Close linked issue (or auto-close)

You will: 
1. Delete local branch:  git branch -d feature/issue-X-description
2. Pull latest:  git checkout develop && git pull
3. Start next issue
```

---

## 📊 End of Day (EOD) Checklist

### Team Members

```markdown
- [ ] Commit all changes
- [ ] Push code to GitHub
- [ ] Update issue progress (comment)
- [ ] Update Project Board (move cards)
- [ ] Reply to any pending comments
- [ ] Log time spent
- [ ] Plan tomorrow (check next issue)
```

### PM

```markdown
- [ ] Review all PRs (target:  0 pending)
- [ ] Reply all comments
- [ ] Update milestone % in tracker
- [ ] Check for blockers
- [ ] Send EOD summary to stakeholders (if Friday)
- [ ] Plan tomorrow's standup agenda
```

---

## 📅 Weekly Workflow

### Monday

**9:00 AM - Week Planning (30 min sau standup)**

```markdown
## Week [X] Planning

### Sprint Goal: 
Tuần 1-2: Complete infrastructure setup

### This Week's Issues:
- [ ] #1 - Server setup (NV A) - Target: Monday
- [ ] #2 - PostgreSQL (NV A) - Target: Tuesday
- [ ] #3 - Git & CI/CD (NV A) - Target: Wed-Thu
- [ ] #4 - QGIS setup (NV B) - Target: Monday
- [ ] #5 - Data collection (NV B) - Target:  Tue-Wed
- [ ] #6 - Database schema (NV B) - Target: Thu-Fri
- [ ] #7 - React setup (NV C) - Target: Monday
- [ ] #8 - UI mockups (NV C) - Target:  Tue-Wed
- [ ] #9 - Basic map (NV C) - Target: Thursday

### Success Criteria:
- 9/9 issues completed
- All infrastructure ready for Week 3-4
- No critical blockers

### Risks:
- Database access cho NV B
- GeoServer installation complexity
```

---

### Friday

**4:00 PM - Sprint Review (1 hour)**

#### Agenda: 

**1. Review Completed Work (30 min)**

```markdown
## Sprint Review - Week [X]

### Completed Issues:  8/9 (89%)

✅ #1 - Server setup (NV A)
✅ #2 - PostgreSQL (NV A)
✅ #3 - Git & CI/CD (NV A)
✅ #4 - QGIS setup (NV B)
✅ #5 - Data collection (NV B)
✅ #7 - React setup (NV C)
✅ #8 - UI mockups (NV C)
✅ #9 - Basic map (NV C)

🔄 #6 - Database schema (NV B) - 90% done, carry over to Monday

### Demo: 
- NV A: Show Docker, PostgreSQL, CI/CD pipeline
- NV B: Show QGIS connected to PostGIS
- NV C:  Show React app with OSM map
```

**2. Retrospective (15 min)**

```markdown
### What went well?  ✅
- Team collaboration excellent
- Docker setup faster than expected
- UI mockups approved by stakeholders

### What didn't go well? ❌
- PostgreSQL config issues (4 hours lost)
- Data collection delayed due to phòng KT
- React dependencies conflict

### What to improve? 📈
- Document troubleshooting steps
- Contact phòng KT earlier
- Lock dependency versions (package-lock.json)

### Action Items:
- [ ] PM: Create troubleshooting wiki
- [ ] NV B: Setup meeting with phòng KT for Week 3
- [ ] NV C: Commit package-lock.json
```

**3. Plan Next Sprint (15 min)**

```markdown
### Week 3-4 Planning

Issues: 
- #10 - Authentication API (NV A)
- #11 - Substations CRUD (NV A)
- #12 - Power Lines CRUD (NV A)
- #14 - SLD Styles (NV B)
- #15 - Enrich data (NV B)
- #16 - Spatial queries doc (NV B)
- #17 - WMS map (NV C)
- #18 - Layer control (NV C)
- #19 - Measure tools (NV C)

Priorities:
1. Authentication API (blocker cho các API khác)
2. Database schema completion (#6)
3. WMS integration
```

---

## 🎯 Best Practices

### Communication

✅ **Do:**
- Update progress daily trong issues
- Tag people bằng @username
- Use clear, concise language
- Add screenshots khi cần
- Reply trong 2 hours (working hours)

❌ **Don't:**
- Silent > 1 day
- Vague comments:  "Có vấn đề" → Specify what
- Skip standup
- Work on unassigned issues
- Push directly to main/develop

### Time Management

```
Focus Time: 
- Morning: 9:30-12:00 (2. 5h focus)
- Afternoon: 13:00-15:00 (2h focus)
Total: 4.5h deep work / day

Meeting Time:
- Daily standup: 15 min
- Sprint review (Friday): 1h
- Ad-hoc: < 1h/day

Admin Time:
- Update issues: 30 min/day
- Code review: 30 min/day
- Planning: 30 min/week
```

### Code Quality

```
Before Commit:
- [ ] Code follows style guide
- [ ] No commented code
- [ ] No console. log / print() debug
- [ ] Tests passing
- [ ] No linting errors

Before PR:
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Rebase with develop
- [ ] No merge conflicts
```

---

## 🆘 Emergency Procedures

### Critical Bug in Production

```
1. Create issue: 
   - Title: [CRITICAL BUG] Description
   - Label: bug, priority: critical
   - Assign:  All hands

2. Immediate action:
   - PM:  Assess impact
   - Team: Drop current work
   - Focus: Fix bug ASAP

3. Hotfix branch:
   - Create from main
   - Fix bug
   - Test thoroughly
   - Deploy immediately

4. Post-mortem:
   - Document root cause
   - Update tests
   - Add monitoring
```

### Team Member Unavailable

```
If sick/emergency:
1. Notify PM ASAP (Slack/phone)
2. PM reassign urgent issues
3. Update Project Board
4. Document current work status

If planned leave:
- Notify 1 week advance
- Complete current issues
- Document WIP
- Handover to teammate
```

---

## 📱 Tools & Links

### Daily Use

| Tool | Purpose | Link |
|------|---------|------|
| GitHub Issues | Task tracking | [Issues](https://github.com/droid2015/gis-geoserver-solution/issues? q=is%3Aissue+is%3Aopen+assignee%3A%40me) |
| Project Board | Kanban | [Board](https://github.com/droid2015/gis-geoserver-solution/projects/1) |
| Pull Requests | Code review | [PRs](https://github.com/droid2015/gis-geoserver-solution/pulls) |
| Actions | CI/CD | [Actions](https://github.com/droid2015/gis-geoserver-solution/actions) |

### Communication

| Tool | Purpose | When |
|------|---------|------|
| GitHub Comments | Issue discussions | Primary |
| Email | Weekly reports | Friday |
| Slack/Teams | Urgent matters | Real-time |
| Google Meet | Standup, reviews | Daily/weekly |

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
