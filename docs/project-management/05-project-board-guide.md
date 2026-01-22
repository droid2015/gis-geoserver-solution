# HƯỚNG DẪN SỬ DỤNG PROJECT BOARD

## 📊 Tổng quan

GitHub Project Board là công cụ Kanban để visualize và track tiến độ dự án. 

**Project URL:** https://github.com/droid2015/gis-geoserver-solution/projects/1

---

## 🎯 Project Board Structure

### Views

#### 1. **Board View** (Kanban)

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  📋 Backlog │  📝 To Do   │ 🔄 In Progress│ 👀 In Review│  ✅ Done   │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Issue #20   │ Issue #1    │ Issue #2    │ Issue #4    │ Issue #7    │
│ Issue #21   │ Issue #3    │ Issue #5    │             │ Issue #8    │
│ Issue #22   │ Issue #6    │             │             │ Issue #9    │
│ ...          │             │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Column definitions:**

| Column | Meaning | When to use |
|--------|---------|-------------|
| 📋 **Backlog** | Not started, not assigned | Issues created but not planned for current sprint |
| 📝 **To Do** | Planned for current sprint | Issues assigned and ready to start |
| 🔄 **In Progress** | Active work | Actively coding/working on |
| 👀 **In Review** | Code complete, awaiting review | PR created, waiting for approval |
| ✅ **Done** | Completed and merged | Issue closed, code merged |

#### 2. **Table View**

```
Title                    | Assignee   | Status      | Priority | Milestone  | Labels
-------------------------|------------|-------------|----------|------------|----------
[NV A] Setup Docker      | @nhanvien_a| Done ✅     | High     | Week 1-2   | backend
[NV B] QGIS setup        | @nhanvien_b| Done ✅     | High     | Week 1-2   | gis
[NV A] PostgreSQL        | @nhanvien_a| In Progress | High     | Week 1-2   | database
[NV C] React setup       | @nhanvien_c| To Do       | Medium   | Week 1-2   | frontend
```

**Use cases:**
- Bulk editing (assign multiple issues at once)
- Filtering (show only high priority)
- Sorting (by due date, priority)
- Export to CSV

#### 3. **Roadmap View** (Timeline)

```
Week 1-2      Week 3-4      Week 5-6      Week 7-8
|-------------|-------------|-------------|-------------|
█████████                                                Setup
              █████████████                             Backend API
                            ███████                     GeoServer
                                        ███████████     Frontend
```

**Use cases:**
- Visualize sprint timeline
- See dependencies
- Track milestone progress

---

## 🔄 Moving Cards (Issues)

### Method 1: Drag & Drop (Desktop)

```
1. Go to Board view
2. Click and hold issue card
3. Drag to target column
4. Release to drop
```

### Method 2: Issue Menu (Mobile-friendly)

```
1. Click "..." on issue card
2. Select "Move to column"
3. Choose target column
```

### Method 3: Automation (Automatic)

**Configured automations:**

```
Trigger: Issue opened
→ Action: Add to Backlog

Trigger: Issue assigned
→ Action: Move to To Do

Trigger: PR opened
→ Action: Move linked issue to In Review

Trigger: Issue closed
→ Action: Move to Done
```

**Set up automation:**
```
1. Project → Settings (⚙️)
2. Workflows
3. Enable pre-built workflows or create custom
```

---

## 📋 Daily Usage

### Morning Routine (Team Member)

```markdown
9:15 AM - After standup

1. Open Project Board
   https://github.com/droid2015/gis-geoserver-solution/projects/1

2. Filter to your issues:  
   Click your avatar → "Assigned to me"

3. Review "In Progress" column
   - Continue yesterday's work
   - Or move completed to "In Review" (if PR created)

4. Check "To Do" column
   - Identify next issue to work on
   - Move to "In Progress"
   - Comment in issue:  "🔄 Started working on this"

5. Start coding! 
```

### End of Day (Team Member)

```markdown
5:00 PM - Before leaving

1. Open Project Board

2. Update card positions: 
   - Completed work → Move to "In Review" (PR created)
   - Still working → Keep in "In Progress", comment progress
   - Blocked → Move to "Backlog", add label "blocked"

3. Add status comment in each active issue:
   ## EOD Update - [Date]
   ✅ Completed:  [items]
   🔄 In Progress: [items]
   ⏱️ Time spent: X hours

4. Check "In Review" column
   - If your PR got review comments → Address tomorrow
```

### Throughout Day (PM)

```markdown
Check every 2-3 hours: 

Morning (10:00 AM):
- Review "In Progress" column
  - Check if any cards stuck too long (> 2 days)
  - Identify bottlenecks
- Review "To Do" column
  - Ensure enough work for team
  - Prioritize if needed

Afternoon (2:00 PM):
- Review "In Review" column
  - Review PRs (target < 4 hours)
  - Merge approved PRs
  - Move to "Done"
- Reply to issue comments

Evening (5:00 PM):
- Review overall progress
  - Count cards in each column
  - Update milestone %
  - Plan tomorrow's standup
```

---

## 🎯 Filtering & Sorting

### Filter by Assignee

```
Method 1: Click avatar/username
Method 2: Search bar:   assignee:@username
Method 3: Table view → Filter → Assignee → Select person
```

### Filter by Label

```
Search bar: label:"backend"
Or: label:"priority:  high"

Multiple labels (AND): label:"backend" label:"week1-2"
Multiple labels (OR): label:"backend,frontend"
```

### Filter by Milestone

```
Search bar: milestone:"Tuần 1-2: Setup & Preparation"

Or: Table view → Filter → Milestone → Select
```

### Filter by Status

```
Board view: Already filtered by column
Table view: Filter → Status → Select
```

### Sort Cards

```
Table view → Click column header to sort

Sort by: 
- Priority (High → Low)
- Updated (Recently → Oldest)
- Created (Newest → Oldest)
- Due date (Soonest → Latest)
```

### Saved Filters

```
Create custom filter:
1. Apply filters
2. Click "Save view"
3. Name: "My High Priority Issues"
4. Access from sidebar
```

---

## 📊 Tracking Progress

### Sprint Progress

**View milestone progress:**

```
1. Go to Milestones tab
2. Click milestone (e.g., "Tuần 1-2: Setup & Preparation")
3. See progress bar:  
   
   ████████░░ 80% complete (8 of 10 issues closed)
   
   Due: January 15, 2025 (3 days remaining)
```

**Calculate manually:**

```markdown
## Week 1-2 Progress

Total issues: 9
- ✅ Done: 7
- 🔄 In Progress: 2
- 📝 To Do: 0
- 📋 Backlog: 0

Progress: 7/9 = 78% ✅

Velocity: 7 issues / 5 days = 1.4 issues/day
Projected completion: 2 days (within sprint ✅)
```

### Burndown Chart (Manual)

**Track daily:**

```markdown
| Date | Remaining Issues | Notes |
|------|------------------|-------|
| Mon  | 9 | Sprint start |
| Tue  | 8 | #1 completed |
| Wed  | 6 | #2, #3 completed |
| Thu  | 4 | #4, #5 completed |
| Fri  | 2 | #6, #7 completed |

Target: 0 issues by Friday EOD
Actual: 2 issues remaining (carry to next week)
```

**Visualize:**

```
Issues
  9 ┤ ●
  8 ┤   ●
  7 ┤     ╲
  6 ┤       ●
  5 ┤         ╲
  4 ┤           ●
  3 ┤             ╲
  2 ┤               ●  ← Current
  1 ┤                 ╲
  0 ┤___________________●___ Target
    Mon Tue Wed Thu Fri
```

### Cumulative Flow Diagram

**Track card distribution over time:**

```
Cards in each column by day: 

       Mon  Tue  Wed  Thu  Fri
Done    0    1    3    5    7
Review  0    1    2    1    0
Progress 2    3    2    2    1
To Do   7    4    2    1    1
Backlog 0    0    0    0    0
```

---

## 🚀 Advanced Features

### Custom Fields

**Add custom fields to track more data:**

```
1. Project → Settings → Fields
2. Add field:
   - Field name: "Estimate (hours)"
   - Type: Number
   - Options: 1, 2, 4, 8, 16

3. Add field:
   - Field name:  "Actual (hours)"
   - Type: Number

4. Use in Table view to track time
```

### Insights (Beta)

```
Project → Insights

View:
- Issues opened vs closed over time
- Burndown/burnup charts
- Velocity trends
- Time in each status
```

### Iteration Planning

**Set up sprints:**

```
1. Project → Settings → Fields
2. Add "Iteration" field
3. Create iterations:
   - Sprint 1 (Week 1-2)
   - Sprint 2 (Week 3-4)
   - Sprint 3 (Week 5-6)
   ... 

4. Assign issues to iterations
5. View by iteration in Table view
```

### Dependencies

**Show issue dependencies:**

```
Issue #10 depends on Issue #2

In Issue #10: 
- Add field "Blocked by":  #2
- Or comment: "Depends on #2"

Visual on board:
- Custom view with "Blocked by" column visible
```

---

## 👥 Team Collaboration

### Assigning Work

**During sprint planning:**

```
1. PM opens Project Board
2. Drag issues from Backlog → To Do
3. Discuss with team who takes what
4. Assign each issue: 
   - Click issue → Assignees → Select person
5. Team members self-assign remaining issues
```

**Balance workload:**

```
Table view → Group by:  Assignee

@nhanvien_a:   3 issues (12 hours)
@nhanvien_b:  3 issues (10 hours)
@nhanvien_c:  3 issues (14 hours)

✅ Balanced workload
```

### Pair Programming

```
Issue #15:   Complex spatial query optimization

Assigned to: @nhanvien_a (primary), @nhanvien_b (secondary)

Comment: 
"Pair programming session: 
- @nhanvien_a drives (writes code)
- @nhanvien_b navigates (reviews, suggests)
- Switch roles every 30 min"
```

### Code Review Workflow

```
Board columns:
- In Progress (coding)
- In Review (PR created, waiting review)
- Changes Requested (review comments, fixing)
- Approved (review passed, waiting merge)
- Done (merged)

Automation:
- PR created → Move to "In Review"
- Review approved → Move to "Approved"
- PR merged → Move to "Done"
```

---

## 🔧 Customization

### Custom Views

**Create view for each team member:**

```
View: "Backend Issues"
Filter: label:"backend"
Sort: priority (High → Low)
Saved as:  Favorite

View: "This Week"
Filter: milestone:"Tuần 1-2"
Group by:  Assignee
```

### Custom Workflows

**Example: Staging deployment workflow**

```
Trigger: Issue moved to "Approved" column
Action: 
  1. Deploy to staging environment
  2. Add comment: "Deployed to staging:  https://staging.example.com"
  3. Add label: "on-staging"
```

### Board Templates

**Save board configuration as template:**

```
1. Configure board (columns, fields, filters)
2. Project → ...  → Save as template
3. Name: "GIS Sprint Board Template"
4. Reuse for future projects
```

---

## 📱 Mobile Usage

### GitHub Mobile App

**View Project Board on mobile:**

```
1. Download GitHub app (iOS/Android)
2. Login
3. Repositories → gis-geoserver-solution
4. Projects tab
5. Select project

Features on mobile: 
✅ View board
✅ Move cards
✅ Comment on issues
✅ Assign/unassign
❌ Create custom views (desktop only)
```

### Mobile Workflow

```
Morning commute:
- Check "To Do" column
- Review assigned issues
- Read issue descriptions

During day:
- Update issue status
- Comment progress
- Move cards

Before leaving:
- Move completed to "In Review"
- Add EOD comments
```

---

## 🎯 Best Practices

### Do's ✅

```
✅ Update board daily (morning & evening)
✅ Move cards immediately when status changes
✅ Keep "In Progress" column small (max 3 per person)
✅ Comment before moving card (explain status)
✅ Use filters to focus on your work
✅ Review board during standup
✅ Close issues promptly after merge
✅ Archive completed milestones
```

### Don'ts ❌

```
❌ Let cards sit in "In Progress" > 3 days
❌ Skip updating board ("I'll do it later")
❌ Move cards without commenting why
❌ Work on issues in "Backlog" (not prioritized)
❌ Have too many "In Progress" (focus!)
❌ Ignore "In Review" column (review promptly)
❌ Forget to link PRs to issues
```

### Column Limits (WIP Limits)

```
Recommended Work-in-Progress (WIP) limits:

Per person:
- In Progress: Max 2 issues
- In Review: Max 3 PRs

Team total (3 people):
- In Progress: Max 6 issues
- In Review: Max 5 PRs

If column is full → Finish current work before starting new
```

---

## 🆘 Troubleshooting

### Issue not appearing on board

```
Problem: Created issue but not on board

Solution:
1. Check if issue is in project: 
   - Issue page → Projects (sidebar)
   - If not in project → Click "Add to project"

2. Check filters:
   - Remove all filters (clear search)
   - Check if issue appears

3. Refresh page (Ctrl+F5)
```

### Cannot move card

```
Problem: Card stuck, cannot drag

Solution:
1. Check permissions (need write access)
2. Try Issue menu method instead of drag-drop
3. Try different browser
4. Clear browser cache
```

### Board not syncing

```
Problem: Changes not reflected

Solution:
1. Refresh page
2. Check internet connection
3. Check GitHub status:  https://www.githubstatus.com
4. Try incognito mode (rule out extensions)
```

### Automation not working

```
Problem: Issue not auto-moving

Solution:
1. Check workflow enabled: 
   - Project → Settings → Workflows
   - Toggle ON if OFF

2. Check workflow rules match:
   - Example: "Issue opened" → Check issue actually opened

3. Manual fallback:  Move card manually
```

---

## 📊 Metrics & Reporting

### Weekly Project Report

**Generate from Project Board:**

```markdown
## Week 1 Report

### Issues Completed:  7/9 (78%)
✅ #1 - Server setup
✅ #2 - PostgreSQL
✅ #3 - Git repo
✅ #4 - QGIS setup
✅ #5 - Data collection
✅ #7 - React setup
✅ #8 - UI mockups

### In Progress: 2
🔄 #6 - Database schema (90% done)
🔄 #9 - Basic map (50% done)

### Blockers: 0

### Next Week:
9 issues planned for Week 3-4 (Backend API development)

### Velocity: 
7 issues completed / 5 days = 1.4 issues/day
```

### Sprint Metrics

```markdown
## Sprint Metrics - Week 1-2

| Metric | Value |
|--------|-------|
| Planned issues | 9 |
| Completed | 7 |
| In Progress | 2 |
| Completion rate | 78% |
| Avg time per issue | 8. 5 hours |
| PRs merged | 7 |
| Avg PR review time | 3.2 hours ✅ |
| Blockers encountered | 1 (resolved in 4 hours) |
| Carryover to next sprint | 2 issues |
```

---

## 🔗 Integration

### Slack/Teams Integration

```
Setup:
1. Slack → Apps → GitHub
2. /github subscribe droid2015/gis-geoserver-solution projects

Notifications:
- Issue moved to "In Review" → Notify #dev channel
- Issue moved to "Done" → Celebrate 🎉
- Issue stuck in "In Progress" > 3 days → Alert PM
```

### Automation with GitHub Actions

```yaml
# .github/workflows/project-board.yml
name: Update Project Board

on:
  issues:
    types: [opened, closed]
  pull_request:
    types: [opened, closed]

jobs:
  update-board: 
    runs-on: ubuntu-latest
    steps:
      - name: Move issue to In Review when PR opens
        if: github.event_name == 'pull_request' && github.event.action == 'opened'
        uses: actions/github-script@v6
        with:
          script: |
            // Move linked issue to In Review column
            // (implementation details)
```

---

## 🎯 Quick Reference

### Keyboard Shortcuts

```
Board view:
- j/k:   Move up/down between cards
- o:  Open selected card
- /:  Focus search
- c:  Create new issue

Table view:
- Ctrl+Click: Select multiple cards
- Shift+Click: Select range
```

### Common Filters

```
My issues:           assignee:@me is:open
High priority:       label:"priority:  high" is:open
This sprint:         milestone:"Week 1-2" is:open
Blocked:              label:"blocked" is:open
Needs review:        label:"needs review" is:open
No assignee:         no:assignee is:open
```

### Status Updates

```
Start work:           Move to "In Progress", comment "🔄 Started"
EOD update:          Comment progress, keep in current column
Create PR:           Move to "In Review", link PR
Address comments:    Keep in "In Review", comment "Addressing feedback"
Complete:            PM merges, auto-moves to "Done"
```

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
