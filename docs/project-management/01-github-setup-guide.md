# HƯỚNG DẪN SETUP GITHUB CHO DỰ ÁN

## 1. Tạo GitHub Personal Access Token

### Bước 1: Truy cập Settings

```
1. GitHub. com → Click avatar (góc trên phải)
2. Settings → Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
```

### Bước 2: Cấu hình Token

```
Note: GIS Project Management Token
Expiration: 90 days (hoặc Custom)

Scopes (chọn các quyền sau):
☑ repo (Full control of private repositories)
  ☑ repo:status
  ☑ repo_deployment
  ☑ public_repo
  ☑ repo:invite
☑ workflow
☑ write:packages
☑ read:packages
☑ admin:org (nếu dùng Organization)
```

### Bước 3: Generate và Save Token

```
1. Click "Generate token"
2. Copy token (chỉ hiển thị 1 lần!)
3. Lưu vào password manager hoặc file bảo mật
```

**⚠️ Security Note:**
- Không commit token vào Git
- Không share token cho người khác
- Revoke token khi hết dùng

---

## 2. Tạo Milestones

### Cách 1: Tạo thủ công trên GitHub UI

```
1. Repo → Issues → Milestones
2. Click "New milestone"
3. Điền thông tin: 

Milestone 1:
- Title:  Tuần 1-2: Setup & Preparation
- Due date: [2 tuần từ ngày bắt đầu]
- Description: Cài đặt hạ tầng, chuẩn bị môi trường phát triển

4. Click "Create milestone"
5. Repeat cho 6 milestones còn lại
```

### Cách 2: Tạo tự động bằng script

**File: `scripts/create_milestones.py`**

```python
import requests
from datetime import datetime, timedelta

REPO_OWNER = "droid2015"
REPO_NAME = "gis-geoserver-solution"
GITHUB_TOKEN = "your_token_here"

API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

start_date = datetime. now()

milestones = [
    ("Tuần 1-2: Setup & Preparation", "Infrastructure setup", 2),
    ("Tuần 3-4: Database & Backend Core", "Backend API", 4),
    ("Tuần 5-6: GeoServer & Map Services", "Map services", 6),
    ("Tuần 7-8: Frontend Development", "UI development", 8),
    ("Tuần 9-10: Integration & Features", "Integration", 10),
    ("Tuần 11: Testing & Bug Fixes", "Testing", 11),
    ("Tuần 12: Deployment & Training", "Go-live", 12)
]

for title, desc, weeks in milestones:
    due_date = (start_date + timedelta(weeks=weeks)).isoformat() + "Z"
    data = {"title": title, "description": desc, "due_on": due_date}
    
    response = requests.post(f"{API_BASE}/milestones", headers=HEADERS, json=data)
    if response.status_code == 201:
        print(f"✅ Created:  {title}")
    else:
        print(f"❌ Failed: {title}")
```

**Chạy:**
```bash
pip install requests
python scripts/create_milestones.py
```

---

## 3. Tạo Issues tự động

### Chạy script tạo issues

**File đã có:** `create_all_issues_complete.py`

```bash
# 1. Update GitHub token trong file (dòng 23)
notepad create_all_issues_complete.py

# 2. Chạy script
python create_all_issues_complete.py
```

Script sẽ tạo: 
- ✅ ~30 issues cho 12 tuần
- ✅ Tự động assign vào milestones
- ✅ Thêm labels phù hợp
- ✅ Link dependencies

**Verify:**
```
Repo → Issues → Should see all issues created
```

---

## 4. Tạo Project Board

### Bước 1: Tạo Project

```
1. Repo → Projects tab
2. Click "New project"
3. Template:  Chọn "Team backlog" hoặc "Table"
4. Project name: "GIS System - 12 Week Sprint"
5. Description: "Project management for GIS Power Grid System"
6. Click "Create project"
```

### Bước 2: Customize Views

**Table View (Default):**
```
Columns:
- Title
- Assignees
- Status
- Priority
- Milestone
- Labels
```

**Board View:**
```
1. Click "+ New view" → Board
2. Name: "Sprint Board"
3. Group by: Status
4. Columns:
   - 📋 Backlog
   - 📝 To Do
   - 🔄 In Progress
   - 👀 In Review
   - ✅ Done
```

### Bước 3: Add Issues vào Project

```
1. Click "Add items" (bottom của project)
2. Search:  `repo: droid2015/gis-geoserver-solution`
3. Select all issues hoặc filter theo milestone
4. Click "Add selected items"
```

### Bước 4: Configure Automation (Optional)

```
Settings → Workflows: 

Auto-add items: 
☑ When: Issue opened
☑ Then: Add to project with status "Backlog"

Auto-move to Done:
☑ When: Issue closed
☑ Then: Move to "Done"

Auto-move to In Progress: 
☑ When: Pull request opened
☑ Then:  Move linked issue to "In Progress"
```

---

## 5. Setup Labels

### Tạo Labels thủ công

```
Repo → Issues → Labels → New label

Labels cần tạo: 

Category Labels:
- backend (#0052CC) - Backend tasks
- frontend (#00FF00) - Frontend tasks
- gis (#FF6B00) - GIS tasks
- database (#8B00FF) - Database tasks
- devops (#FFD700) - DevOps tasks
- documentation (#CCCCCC) - Documentation

Priority Labels:
- priority: critical (#FF0000) - Critical priority
- priority: high (#FF6B00) - High priority
- priority: medium (#FFD700) - Medium priority
- priority: low (#00FF00) - Low priority

Status Labels:
- blocked (#FF0000) - Blocked
- needs review (#FFD700) - Needs review
- in progress (#0052CC) - In progress

Type Labels:
- bug (#FF0000) - Bug report
- feature (#00FF00) - Feature request
- enhancement (#0052CC) - Enhancement
```

### Script tự động tạo labels

**File: `scripts/create_labels.py`**

```python
import requests

REPO_OWNER = "droid2015"
REPO_NAME = "gis-geoserver-solution"
GITHUB_TOKEN = "your_token_here"

API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

labels = [
    ("backend", "0052CC", "Backend tasks"),
    ("frontend", "00FF00", "Frontend tasks"),
    ("gis", "FF6B00", "GIS tasks"),
    ("database", "8B00FF", "Database tasks"),
    ("priority: high", "FF0000", "High priority"),
    ("priority: medium", "FFD700", "Medium priority"),
    ("priority: low", "00FF00", "Low priority"),
    # ... thêm labels khác
]

for name, color, desc in labels: 
    data = {"name": name, "color": color, "description":  desc}
    response = requests. post(f"{API_BASE}/labels", headers=HEADERS, json=data)
    if response.status_code == 201:
        print(f"✅ Created label: {name}")
    else:
        print(f"⚠️  Label exists or error: {name}")
```

---

## 6. Setup Branch Protection

### Main Branch Protection

```
Repo → Settings → Branches → Add rule

Branch name pattern: main

Protect matching branches:
☑ Require a pull request before merging
  ☑ Require approvals:  1
  ☑ Dismiss stale pull request approvals when new commits are pushed
☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
☑ Require conversation resolution before merging
☑ Include administrators (optional)

Click "Create" hoặc "Save changes"
```

### Develop Branch Protection

```
Branch name pattern: develop

Protect matching branches:
☑ Require a pull request before merging
  ☑ Require approvals:  1
☑ Require status checks to pass before merging

Click "Create"
```

---

## 7. Setup Issue Templates

### Tạo templates folder

```bash
mkdir -p . github/ISSUE_TEMPLATE
```

### Task Template

**File: `.github/ISSUE_TEMPLATE/task.md`**

```markdown
---
name: 📋 Task
about: Standard task for team members
title: '[NV X] '
labels: ''
assignees: ''
---

## 🎯 Mục tiêu
<!-- Mô tả rõ ràng mục tiêu của task -->

## ✅ Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## 📦 Deliverables
- ✅ Item 1
- ✅ Item 2

## ⏱️ Time estimate
X hours (Y ngày)

## 🔗 Dependencies
- Depends on: #
- Blocks: #

## 📚 Resources
- [Link to documentation]

## 📝 Notes
<!-- Additional notes -->
```

### Bug Template

**File: `.github/ISSUE_TEMPLATE/bug. md`**

```markdown
---
name: 🐛 Bug Report
about: Report a bug
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 Description
<!-- Clear description of the bug -->

## 📋 Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## ✅ Expected behavior
<!-- What should happen -->

## ❌ Actual behavior
<!-- What actually happens -->

## 🖼️ Screenshots
<!-- If applicable -->

## 🌐 Environment
- Browser: [e.g.  Chrome 120]
- OS: [e.g. Windows 11]
- Version: [e. g. 1.0.0]

## 📝 Additional context
<!-- Any other information -->
```

### Feature Request Template

**File: `.github/ISSUE_TEMPLATE/feature_request.md`**

```markdown
---
name: 💡 Feature Request
about:  Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 💡 Feature Description
<!-- Clear description of the feature -->

## 🎯 Problem it solves
<!-- What problem does this solve?  -->

## ✅ Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## 📸 Mockups/Examples
<!-- If applicable -->

## 🔗 Related Issues
- Related to: #

## 📝 Additional context
<!-- Any other information -->
```

---

## 8. Setup Pull Request Template

**File: `.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## 📝 Description
<!-- Describe your changes -->

Closes #[issue number]

## 🔧 Type of change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📚 Documentation update
- [ ] 🎨 Code style update
- [ ] ♻️ Refactoring
- [ ] ⚡ Performance improvement

## ✅ Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No console errors

## 🖼️ Screenshots (if applicable)
<!-- Add screenshots here -->

## 🧪 Testing
<!-- Describe how you tested -->

## 📝 Additional Notes
<!-- Any additional information -->
```

---

## 9. Setup GitHub Actions (CI/CD)

### Backend CI

**File: `.github/workflows/backend-ci.yml`**

```yaml
name: Backend CI

on:
  push:
    branches: [develop, staging, main]
    paths: 
      - 'backend/**'
  pull_request:
    branches:  [develop, main]
    paths:
      - 'backend/**'

jobs: 
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name:  Setup Python
        uses: actions/setup-python@v4
        with:
          python-version:  '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Check code quality
        run: |
          cd backend
          flake8 app/ --max-line-length=120
```

### Frontend CI

**File: `.github/workflows/frontend-ci.yml`**

```yaml
name: Frontend CI

on: 
  push:
    branches: [develop, staging, main]
    paths:
      - 'frontend/**'
  pull_request: 
    branches: [develop, main]
    paths:
      - 'frontend/**'

jobs: 
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses:  actions/checkout@v3
      
      - name: Setup Node. js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage
      
      - name: Build
        run: |
          cd frontend
          npm run build
```

---

## 10. Verify Setup

### Checklist

- [ ] ✅ GitHub Token created và tested
- [ ] ✅ 7 Milestones created
- [ ] ✅ ~30 Issues created
- [ ] ✅ Project Board created
- [ ] ✅ All issues added to Project Board
- [ ] ✅ Labels created
- [ ] ✅ Branch protection rules set
- [ ] ✅ Issue templates created
- [ ] ✅ PR template created
- [ ] ✅ GitHub Actions CI/CD setup

### Test Commands

```bash
# Test API access
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/droid2015/gis-geoserver-solution

# Test milestones
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/droid2015/gis-geoserver-solution/milestones

# Test issues
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/droid2015/gis-geoserver-solution/issues
```

---

## 🔗 Next Steps

After setup complete: 
1. ✅ Read [02-daily-workflow.md](02-daily-workflow.md)
2. ✅ Organize [Kickoff Meeting](02-daily-workflow.md#kickoff-meeting)
3. ✅ [Assign issues](03-issue-management.md#assign-issues) to team members
4. ✅ Start Sprint 1 (Tuần 1-2)

---

## 🆘 Troubleshooting

**Issue:  Token không work**
```
- Check token chưa expire
- Check scopes đúng (repo)
- Try regenerate token
```

**Issue: Cannot create milestones**
```
- Check permissions (admin role required)
- Check API rate limit:  curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit
```

**Issue: Project board không hiển thị issues**
```
- Check issues đã được add vào project chưa
- Refresh browser
- Clear cache
```

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
