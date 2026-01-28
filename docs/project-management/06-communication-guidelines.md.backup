# QUY TẮC COMMUNICATION

## 📱 Communication Channels

### Channel Hierarchy

```
1️⃣ GitHub Issues/PRs (PRIMARY)
   - Task discussions
   - Code reviews
   - Progress updates
   - Technical questions

2️⃣ Slack/Teams (REAL-TIME)
   - Urgent matters
   - Quick questions
   - Daily standup coordination
   - Team announcements

3️⃣ Email (FORMAL)
   - Weekly reports
   - Stakeholder communication
   - Official documentation

4️⃣ Video Calls (MEETINGS)
   - Daily standup
   - Sprint planning/review
   - Pair programming
   - Complex discussions
```

### When to Use Each Channel

| Situation | Channel | Response Time |
|-----------|---------|---------------|
| Task clarification | GitHub issue comment | < 2 hours |
| Code review | GitHub PR review | < 4 hours |
| Blocker | GitHub issue + Slack mention | < 1 hour |
| Quick question | Slack DM | < 30 min |
| Urgent issue | Slack + Phone call | Immediate |
| Weekly update | Email | N/A |
| Sprint planning | Video call | Scheduled |

---

## 💬 GitHub Communication

### Issue Comments

#### Structure

```markdown
## [Purpose] - [Date]

**[Emoji] Key point:**
Details

**[Emoji] Another point:**
More details

[Optional:   @mention if need attention]
```

#### Examples

**Progress Update:**
```markdown
## Progress Update - 2025-12-30

✅ **Completed:**
- Installed PostgreSQL 15
- Created database `gisdb`
- Configured performance settings

🔄 **In Progress:**
- Testing connection from app server (70% done)
- Writing connection documentation

⏭️ **Next:**
- Deploy to staging
- Update README with connection steps

⏱️ **Time spent:** 6 hours / 8 estimated

🚫 **Blockers:** None
```

**Asking for Help:**
```markdown
@droid2015 **Question:**

I'm getting this error when connecting to PostgreSQL: 
```
psycopg2.OperationalError: could not connect to server: Connection refused
```

**What I tried:**
- Checked PostgreSQL is running:   `systemctl status postgresql` ✅
- Checked port is open: `netstat -tlnp | grep 5432` ✅
- Checked pg_hba.conf: Looks correct ✅

**Need help with:**
Firewall configuration between app server and DB server

**Impact:**
Blocking Issue #2 completion
```

**Reporting Blocker:**
```markdown
@droid2015 **🚫 BLOCKER**

**Issue:** Cannot access production database credentials

**Tried:**
- Checked . env file: Not present
- Asked IT:  No response for 2 days
- Checked documentation: Credentials not documented

**Need:**
- Production DB credentials
- Or temporary staging DB access

**Impact:**
- Blocking Issue #10 (Authentication API)
- Blocking entire Week 3-4 sprint

**Urgency:** Critical - need by EOD today

**Workaround:**
Can use local PostgreSQL for development, but cannot test against real data
```

**Review Comment:**
```markdown
**🔴 Required change:**

Please add input validation for the `email` field.

Current code:
\```python
user = User(email=data['email'])
\```

Issue:  No validation for email format.   Can accept invalid emails like "abc" or "test@". 

Suggested fix:
\```python
from pydantic import EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # Pydantic validates email format
\```

Or use regex validation if not using Pydantic. 
```

### PR Communication

#### Responding to Review Comments

**Accept suggestion:**
```markdown
✅ **Done**

Fixed in commit `abc1234`.  Added email validation using Pydantic `EmailStr`.

Test added in `test_user. py` line 45.
```

**Disagree respectfully:**
```markdown
💭 **Discussion**

I understand your concern about performance. However, I chose this approach because: 

1. Readability:   More maintainable for future developers
2. Performance:   Profiled with 10K records, only 50ms difference
3. Scalability:  Easier to extend for future requirements

Happy to discuss in standup or video call if you'd like to explore alternatives. 

What do you think?
```

**Need clarification:**
```markdown
❓ **Clarification needed**

Can you elaborate on "add error handling here"?

Do you mean:
- A.  Try-catch for database connection errors? 
- B.  Validation for user input errors?
- C. Something else? 

Want to make sure I understand correctly before implementing. 
```

**Alternative solution:**
```markdown
💡 **Alternative approach**

Good catch on the potential bug! 

Instead of your suggested fix, what if we:
\```python
# Your suggestion: 
if user: 
    user.update(data)

# Alternative:
user = db.query(User).filter_by(id=user_id).first()
if not user:
    raise HTTPException(status_code=404, detail="User not found")

user.update(data)
\```

This way, we explicitly handle the 404 case with proper error message. 

Thoughts?
```

---

## 💬 Slack/Teams Communication

### Channel Structure

```
#general - Team announcements, general chat
#dev - Development discussions, technical questions
#standup - Daily standup notes
#pr-reviews - PR notifications (GitHub bot)
#deployments - Deployment notifications
#random - Non-work chat, memes 😄
```

### Message Guidelines

#### Good Messages ✅

**Quick question:**
```
Hey @teammate,  quick question about the PostGIS query in PR #45.

Did you consider using ST_DWithin instead of ST_Distance for performance? 

Not blocking, just curious.   Can discuss in standup if easier.
```

**Urgent blocker:**
```
@droid2015 🚨 URGENT

Production database down.   Users cannot login.

Error: "Connection timeout"

Started:  2:30 PM
Impact:   All users
GitHub issue:  #789

I'm investigating.  Need help from DevOps? 
```

**Announcement:**
```
@channel 📢 Announcement

Sprint review today at 4:00 PM. 

Agenda:
- Demo completed features
- Retrospective
- Plan Week 3-4

Meeting link: [Google Meet URL]

See you there!
```

#### Bad Messages ❌

**Too vague:**
```
❌ help
❌ anyone know about database?
❌ something is broken
```

**Should be in GitHub:**
```
❌ I think we should refactor the auth module (use GitHub issue)
❌ Here's my code for review (use GitHub PR)
❌ What's the status of Issue #5?  (check GitHub)
```

**Too chatty:**
```
❌ Hey
   Hey
   Are you there?
   Can I ask a question?
   It's about... 
   
✅ Hey @teammate, question about PostGIS query in PR #45...  (one message)
```

### Response Time Expectations

| Message Type | Response Time | Notification |
|--------------|---------------|--------------|
| @channel (all) | < 15 minutes | Push |
| @username (direct) | < 30 minutes | Push |
| General message | < 2 hours | None |
| After hours | Next working day | None |

### Status Updates

**Set Slack status:**

```
Working hours: 
🟢 Available
🔵 In meeting (9:00-9:15 AM - Standup)
🟡 Focused work (Do not disturb)
🔴 Lunch break

After hours: 
⚫ Away
```

**Custom status:**
```
🔧 Fixing production bug
💻 Deep work - Reply slower
📚 In training
🏠 Working from home
🌴 On vacation (Dec 25-31)
```

---

## 📧 Email Communication

### When to Use Email

```
✅ Use email for:
- Weekly progress reports to stakeholders
- Official documentation
- External communication (clients, vendors)
- Formal requests (budget, resources)
- Meeting invitations (calendar invites)

❌ Don't use email for:
- Daily task updates (use GitHub)
- Quick questions (use Slack)
- Code reviews (use GitHub PR)
- Urgent matters (use Slack + call)
```

### Email Templates

#### Weekly Report

```
Subject: GIS Project - Week [X] Progress Report

Hi [Manager Name],

Here's the progress report for GIS System Implementation - Week [X]: 

📊 OVERALL PROGRESS: 
- Milestone:   Tuần [X]-[Y] ([Milestone Name])
- Progress:  [X]% ([Y]/[Z] issues completed)
- Status:  🟢 On track / 🟡 At risk / 🔴 Delayed

✅ COMPLETED THIS WEEK:
- #1: [Issue title] ([Assignee]) ✅
- #2: [Issue title] ([Assignee]) ✅
- #3: [Issue title] ([Assignee]) ✅

🔄 IN PROGRESS: 
- #4: [Issue title] ([Assignee]) - [X]% done

⚠️ BLOCKERS/RISKS:
- [Blocker description] - [Action plan] - [ETA]
- None

📅 NEXT WEEK PLAN:
- Focus:   [Main objectives]
- [X] issues planned
- Key deliverable:  [What will be demo-able]

🎯 OVERALL PROJECT STATUS:  🟢 GREEN

Best regards,
[Your Name]
Project Manager
```

#### Stakeholder Update

```
Subject: GIS Project - Milestone [X] Completion

Dear [Stakeholder Name],

I'm pleased to inform you that we've completed Milestone [X]:  [Milestone Name].

KEY ACHIEVEMENTS: 
✅ [Achievement 1]
✅ [Achievement 2]
✅ [Achievement 3]

DEMO: 
You can view the working system at: [staging URL]
Demo video: [link]

NEXT STEPS: 
We're now starting Milestone [Y]:  [Milestone Name]
Expected completion:   [Date]

Please let me know if you have any questions or would like a demo.

Best regards,
[Your Name]
```

#### Meeting Invitation

```
Subject: Sprint Review - Week [X]

Meeting: GIS Project Sprint Review
Date: Friday, [Date]
Time: 4:00 PM - 5:00 PM (60 minutes)
Location: [Meeting room] / [Video link]

Agenda:
1. Demo completed features (30 min)
2. Retrospective (15 min)
3. Plan next sprint (15 min)

Attendees:
- @nhanvien_a
- @nhanvien_b
- @nhanvien_c
- [Stakeholders]

Please confirm attendance. 

Meeting materials:  [link to slides]
```

---

## 🎤 Meeting Communication

### Daily Standup (15 min)

**Format:**

```
Each person (max 3 min):

1. ✅ Yesterday: 
   "Completed Issue #2 - PostgreSQL setup.  
    Started Issue #3 - Git repo configuration."

2. 🔄 Today:
   "Continue Issue #3, expecting to complete by EOD. 
    Will also review PR #45 from @teammate."

3. 🚫 Blockers:
   "No blockers" 
   OR
   "Blocked on database access - need IT support"

PM notes action items. 
```

**Guidelines:**

```
✅ Do:
- Be concise (3 min max)
- Focus on work items (issues/PRs)
- Mention blockers clearly
- Stand up (if in-person, keeps it short)

❌ Don't:
- Get into detailed discussions (take offline)
- Problem-solve during standup
- Go over time
- Skip your turn
```

### Sprint Review (1 hour)

**Format:**

```
1.  Demos (30 min)
   - Each team member demos completed work
   - Show working software, not slides
   - Stakeholders ask questions

2. Retrospective (15 min)
   - What went well?
   - What didn't go well?
   - What to improve? 
   - Action items

3. Planning (15 min)
   - Review next sprint goals
   - Discuss priorities
   - Identify risks
```

**Demo Guidelines:**

```
✅ Prepare:
- Working demo environment
- Test demo flow beforehand
- Screenshot backup (if demo gods are cruel)
- List of what you'll show

During demo:
- Explain what you're showing
- Show user perspective (not code)
- Highlight challenges overcome
- Mention what's next

Example:
"This is the authentication API I built this week. 
Let me show you the login flow. 
First, I'll send a POST request with credentials... 
[Shows API call in Postman]
As you can see, it returns a JWT token.
This token is then used for all authenticated requests.
Next week, I'll integrate this with the frontend."
```

### Ad-hoc Meetings

**When to schedule:**

```
✅ Schedule meeting when:
- Discussion needs > 10 min
- Requires whiteboarding / screen share
- Multiple people need to align
- Decision needs group input

❌ Don't schedule meeting for:
- Can be answered in Slack/GitHub
- Only 1-2 people involved (DM instead)
- No clear agenda
- No decision needed
```

**Meeting invitation checklist:**

```
- [ ] Clear subject line
- [ ] Date & time (consider timezones)
- [ ] Duration (be realistic)
- [ ] Video link / location
- [ ] Agenda (bullet points)
- [ ] Required attendees (vs optional)
- [ ] Pre-read materials (if applicable)
- [ ] Clear outcome expected
```

---

## 📱 Notifications

### GitHub Notifications

**Configure:**

```
GitHub → Settings → Notifications

Participating: 
☑ Email:  ON
☑ Web: ON

Watching:
☑ Email: ON (for repos you care about)
☑ Web: ON

Custom routing:
gis-geoserver-solution → your@email.com
```

**Watch settings per repo:**

```
Repo → Watch button → Custom

☑ Issues
☑ Pull Requests
☑ Releases
☐ Discussions (if not needed)

This way, you're notified when:
- Someone @mentions you
- Issue assigned to you
- PR assigned to you
- Someone comments on your issue/PR
```

**Email filters:**

```
Gmail/Outlook filter: 

From: notifications@github.com
Subject: [droid2015/gis-geoserver-solution]
→ Label: "GIS Project"
→ Skip inbox (archive) for non-urgent
→ Mark important:  Subject contains "@yourusername"
```

### Slack Notifications

**Configure:**

```
Slack → Preferences → Notifications

Notify me about:
☑ Direct messages
☑ Mentions & keywords
☑ Threads I'm following

Keywords:  
- @yourusername
- "URGENT"
- "BLOCKER"
- "production"

Do Not Disturb: 
- Weekdays: 7:00 PM - 9:00 AM
- Weekends: All day
```

### Mobile Notifications

```
GitHub Mobile app: 
- Enable push notifications
- Mentions only (avoid spam)

Slack Mobile app:
- DMs:  ON
- Mentions: ON
- All messages: OFF (too noisy)
```

---

## 🤝 Communication Best Practices

### Be Respectful

```
✅ Good:
"I think there might be a better approach here. What if we tried X?"

❌ Bad:
"This code is terrible. You should rewrite it."

✅ Good:
"Can you help me understand the reasoning behind this decision?"

❌ Bad: 
"Why did you do it this way?  It doesn't make sense."
```

### Be Clear

```
✅ Good:
"The login API is returning 500 error when password is > 20 characters. 
Steps to reproduce:
1. POST /api/auth/login
2. Password: '12345678901234567890X'
3. Expected: 401 or validation error
4. Actual: 500 Internal Server Error"

❌ Bad:
"Login doesn't work"
```

### Be Timely

```
Response time expectations: 

GitHub: 
- Issue comment: < 2 hours (working hours)
- PR review: < 4 hours
- Blocker: < 1 hour

Slack:
- @mention: < 30 min
- DM: < 1 hour
- General message: < 2 hours

Email:
- Stakeholder: < 1 day
- Internal: < 2 days
```

### Be Async-Friendly

```
✅ Good async message:
"Hey @teammate, when you get a chance, can you review PR #45? 

No rush, but would appreciate feedback by EOD Friday for the sprint demo. 

Context: This implements the authentication API.  Main files to review:
- app/api/auth. py (new endpoint)
- tests/test_auth.py (test coverage)

Let me know if you have questions!"

[Provides context, sets expectations, doesn't block them]

❌ Bad: 
"Hey"
[waits for response]
"Are you there?"
[waits]
"Can you review my PR?"
[blocks their workflow]
```

### Assume Positive Intent

```
Scenario: PR got rejected with harsh-sounding comment

❌ React:
"Why are you blocking my PR?   I worked hard on this!"

✅ Respond:
"Thanks for the review. Can you help me understand the concern about [X]?  
I'm happy to make changes, just want to make sure I get it right."

[Assume they're trying to help, not attack]
```

---

## 🌍 Remote Work Communication

### Time Zone Considerations

```
Team across time zones:
- Person A:   UTC+7 (Vietnam)
- Person B: UTC-5 (US East Coast)
- Person C:  UTC+0 (UK)

Overlap hours:  9:00-11:00 AM Vietnam time

Meeting scheduling:
- Daily standup:   9:00 AM Vietnam time (everyone can join)
- Sprint review: Record for async viewing
- Use World Time Buddy:  https://www.worldtimebuddy.com/
```

### Async Communication

```
When timezones don't overlap: 

Use:
✅ GitHub issues (always available)
✅ Recorded video demos (Loom)
✅ Detailed written updates
✅ Clear documentation

Avoid:
❌ Synchronous back-and-forth
❌ "Are you available now?" messages
❌ Assuming immediate responses
❌ Scheduling meetings outside overlap hours
```

### Over-communicate

```
In office:  Can see if someone is working
Remote: Cannot see

Solution:  Over-communicate
- Start of day: "Good morning!  Starting work on Issue #5"
- Breaks: "Taking lunch break, back in 1 hour"
- EOD: "Heading out for the day.  Updated Issue #5 progress."
- Blockers: Report immediately, don't wait
```

---

## 🎯 Quick Reference

### Communication Decision Tree

```
Question to ask or update to share? 
│
├─ Urgent (< 1 hour)?
│  └─ Yes → Slack @mention + Call
│  └─ No → Continue
│
├─ Related to specific issue/PR?
│  └─ Yes → GitHub comment
│  └─ No → Continue
│
├─ Needs real-time discussion?
│  └─ Yes → Slack or schedule call
│  └─ No → Continue
│
├─ For stakeholders/formal? 
│  └─ Yes → Email
│  └─ No → Slack general message
```

### Response Time SLA

| Channel | Priority | Response Time |
|---------|----------|---------------|
| GitHub issue | Normal | < 2 hours |
| GitHub issue | Blocker | < 1 hour |
| GitHub PR review | Normal | < 4 hours |
| GitHub PR review | Urgent | < 2 hours |
| Slack @mention | Normal | < 30 min |
| Slack @channel | Urgent | < 15 min |
| Email | Normal | < 1 day |
| Phone call | Critical | Immediate |

### Communication Checklist

```
Before sending:
- [ ] Is this the right channel? 
- [ ] Have I provided enough context?
- [ ] Have I checked documentation first?
- [ ] Is my message clear and actionable?
- [ ] Have I @mentioned the right people?
- [ ] Is the tone respectful and professional?
- [ ] Can this wait, or is it truly urgent?
```

---

**Last updated:** 2025-12-30  
**Author:** @droid2015
