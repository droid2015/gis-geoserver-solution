# XỬ LÝ TÌNH HUỐNG

## 🆘 Tổng quan

Hướng dẫn xử lý các tình huống thường gặp trong quản lý dự án và giải pháp khuyến nghị.

---

## 🚧 TÌNH HUỐNG 1: Nhân viên bị Block

### Dấu hiệu nhận biết

```
- Nhân viên report blocker trong issue
- Issue stuck ở "In Progress" > 2 ngày
- Không có update trong 24 giờ
- Nhân viên silent trong standup
```

### Ví dụ

```markdown
Issue #5:  Data Collection

@droid2015 **🚫 BLOCKER**

Cannot access company's old database server.
Emailed IT 2 days ago, no response. 

Impact: Cannot collect historical data
Blocking: Week 2 sprint completion
```

### Giải pháp PM

#### Bước 1: Assess Urgency (5 phút)

```markdown
Questions to ask:
- Does this block sprint completion?  (YES → Critical)
- Can we work around it? (NO → High priority)
- When do we need this resolved? (EOD → Urgent)

Decision: This is CRITICAL
```

#### Bước 2: Take Immediate Action (30 phút)

```
1. Reply in issue (within 15 minutes):
   ```
   @nhanvien_b Thanks for flagging.  I'll handle this NOW.
   ```

2. Escalate: 
   - Email IT manager (not just ticket)
   - CC your manager if needed
   - Phone call if no response in 1 hour

3. Find workaround:
   - Can use sample data temporarily? 
   - Can work on other tasks meanwhile? 

4. Assign alternative work:
   ```
   @nhanvien_b While waiting, can you start Issue #6 (Database schema)?
   ```
```

#### Bước 3: Follow Up (Every 2 hours)

```
10:00 AM - Initial escalation
12:00 PM - Check status, escalate higher if needed
2:00 PM - Update team in standup channel
4:00 PM - Resolve or set EOD deadline

Keep team informed: 
"Update:  Still waiting for IT.  @nhanvien_b is working on Issue #6 meanwhile."
```

#### Bước 4: Resolve & Document

```markdown
After resolution: 

1. Update issue: 
   ```
   ✅ RESOLVED
   
   IT provided database access at 3:00 PM. 
   Resolution time: 4 hours from escalation. 
   
   Root cause: IT email went to spam folder.
   Prevention: Add IT email to contacts, use ticketing system.
   ```

2. Update risk register:
   - Risk: External dependencies (IT, vendors)
   - Mitigation: Contact 1 week in advance, escalate early
   - Owner: PM

3. Thank everyone:
   ```
   Thanks @nhanvien_b for clear blocker report.
   Thanks IT team for quick resolution.
   ```
```

### Prevention

```markdown
Proactive measures: 

1. Weekly dependency check: 
   - "What external dependencies do you need next week?"
   - Contact them NOW, not when needed

2. Buffer time:
   - Add 1-2 day buffer for external dependencies

3. Backup plans:
   - Always have Plan B (sample data, mock services, etc.)

4. Escalation path:
   - Document:  Who to contact, when to escalate, phone numbers
```

---

## ⏰ TÌNH HUỐNG 2: Issue Quá Deadline

### Dấu hiệu nhận biết

```
- Issue due date passed
- Estimate exceeded (actual > estimate)
- Progress stalled at X% for 2+ days
- Nhân viên keeps saying "almost done"
```

### Ví dụ

```
Issue #10: Authentication API
Estimate: 16 hours (2 days)
Actual: Already 24 hours, only 60% done
Due: Yesterday
```

### Root Cause Analysis

#### PM Investigation (15 phút)

```markdown
Ask these questions: 

1. **Scope creep? **
   "Is the scope larger than initially planned?"
   Example: "Originally just login, now includes 2FA, OAuth"
   
2. **Technical complexity underestimated?**
   "Was the task more complex than expected?"
   Example: "JWT implementation harder than thought"

3. **Skill gap?**
   "Does developer need help/training?"
   Example: "Never worked with JWT before"

4. **Distractions?**
   "Was developer pulled into other work?"
   Example: "Had to fix production bug"

5. **Personal issues?**
   "Is there something affecting focus?"
   Example: "Family emergency, internet issues"
```

#### Common Root Causes

| Root Cause | Frequency | Solution |
|------------|-----------|----------|
| Scope creep | 40% | Re-scope, split issue |
| Poor estimation | 30% | Re-estimate with team |
| Technical complexity | 20% | Pair programming, research time |
| Distractions | 10% | Protect focus time |

### Giải pháp

#### Option 1: Re-scope

```markdown
If scope grew beyond original plan: 

1. Comment in issue:
   ```
   Original scope: Login with username/password
   Current scope: Login + 2FA + OAuth + Password reset
   
   Let's split this: 
   - Keep:  Login with username/password (original)
   - New issues: #11 (2FA), #12 (OAuth), #13 (Password reset)
   ```

2. Create new issues for additional scope

3. Close original issue with reduced scope

4. Update sprint plan
```

#### Option 2: Extend Timeline

```markdown
If legitimately needs more time:

1. Re-estimate remaining work:
   ```
   Original estimate: 16 hours
   Actual spent: 24 hours
   Progress: 60%
   Remaining: (40% / 60%) * 24h = 16h
   New total: 24h + 16h = 40 hours
   ```

2. Adjust sprint: 
   ```
   Impact: Will delay sprint completion by 3 days
   Mitigation:  Can other team members help?
   Decision: Extend deadline to Friday
   ```

3. Communicate to stakeholders:
   ```
   Update: Issue #10 taking longer than expected due to JWT complexity. 
   New ETA: Friday (was Wednesday).
   Sprint completion: 90% instead of 100%.
   ```
```

#### Option 3: Pair Programming

```markdown
If skill gap or stuck:

1. Assign helper:
   ```
   @nhanvien_a can you pair with @nhanvien_c on Issue #10?
   Target: Complete by EOD tomorrow
   
   Session 1: Today 2-4 PM (JWT implementation)
   Session 2: Tomorrow 10-12 PM (Testing)
   ```

2. Knowledge transfer:
   - Experienced dev drives, mentors
   - Less experienced dev learns
   - Both benefit

3. Document learnings:
   - Add notes to issue
   - Create wiki article
   - Share in team meeting
```

#### Option 4: Reduce Scope (MVP)

```markdown
If deadline is HARD: 

1. Define MVP:
   ```
   Full scope: 
   - Login with username/password ✅
   - Remember me checkbox ❌ (nice-to-have)
   - Password strength indicator ❌ (nice-to-have)
   - Login history ❌ (future sprint)
   
   MVP: Just basic login
   Defer others to next sprint
   ```

2. Deliver MVP on time

3. Create follow-up issues for deferred items
```

### Prevention

```markdown
Better estimation:

1. **Planning poker:**
   - Team estimates together
   - Discuss differences
   - More accurate than individual estimates

2. **Add buffers:**
   - Multiply estimates by 1.5x for new tech
   - Add 20% contingency for unknowns

3. **Break down large tasks:**
   - Issues > 16 hours → Split into smaller issues
   - Easier to estimate, track progress

4. **Track actuals:**
   - Log:  Estimate vs Actual
   - Learn from differences
   - Improve future estimates
```

---

## 👻 TÌNH HUỐNG 3: Nhân viên "Silent" (Không Update)

### Dấu hiệu nhận biết

```
- No comments in issue for 2+ days
- No PR activity
- No commits
- Misses standup or says "nothing to report"
- No response to @mentions
```

### Ví dụ

```
Issue #15: GeoServer Configuration
Assigned:  @nhanvien_b
Last update: 3 days ago
Status: "In Progress" (but no visible progress)
Standup: "Still working on it"
```

### Giải pháp

#### Step 1: Private Check-in (Không public shame)

```markdown
Slack DM (không trong issue public):

"Hey @nhanvien_b, noticed Issue #15 hasn't had updates in a few days.
Everything okay? Any blockers I can help with? 

Just checking in - no pressure, just want to make sure you're not stuck. 

Can we do a quick call (15 min) to discuss?  I'm free now or this afternoon."
```

**Don't:**
- ❌ Call out publicly in issue:  "Why no updates?"
- ❌ Assume laziness
- ❌ Threaten consequences

**Do:**
- ✅ Assume positive intent (maybe stuck, stressed, personal issue)
- ✅ Offer help, not blame
- ✅ Private first, escalate if needed

#### Step 2: Diagnose Issue (Call/Meeting)

```markdown
Questions to ask (empathetically):

1. "How's the task going?"
   → Listen for:  Stuck, confused, scope unclear

2. "What have you tried so far?"
   → Listen for:  Lack of direction, wrong approach

3. "What's blocking you?"
   → Listen for:  Technical, personal, overwhelmed

4. "How can I help?"
   → Listen for: Specific needs (training, pair programming, clearer requirements)

5. "Is there something else going on?"
   → Listen for:  Personal issues, burnout, team dynamics
```

#### Step 3: Action Plan

**If technically stuck:**
```markdown
Solution:  Pair programming

"Let's pair for 1 hour this afternoon. 
I'll help you get unstuck on GeoServer config.
Then you can continue independently."

Schedule: 2-3 PM today
Goal: Get past blocker
```

**If scope unclear:**
```markdown
Solution: Clarify requirements

"Let me clarify what's needed:
1. Install GeoServer (Docker)
2. Create workspace 'power_grid'
3. Publish 3 layers (substations, lines, poles)
4. Apply SLD styles

Is this clear?  Any questions? 

Expected deliverable: URL to view WMS layers"
```

**If overwhelmed:**
```markdown
Solution: Break down task

"This issue is large. Let's break it down:

#15.1: Install GeoServer (4h) - You
#15.2: Create workspace (1h) - You
#15.3: Publish layers (2h) - I'll pair with you
#15.4: Apply styles (3h) - You

Complete #15.1 today, we'll tackle #15.2 together tomorrow."
```

**If personal issues:**
```markdown
Solution: Adjust workload

"I understand you have some personal matters. 

Let's adjust: 
- Issue #15: Extend deadline by 2 days (no pressure)
- I'll reassign Issue #16 to @nhanvien_c
- Focus on #15 only

Take care of yourself first.  Let me know if you need more time."
```

#### Step 4: Set Clear Expectations

```markdown
After call:

"Thanks for the chat. Here's what we agreed:

1. You'll complete #15.1 (GeoServer install) by EOD today
2. We'll pair on #15.3 (publish layers) tomorrow 2 PM
3. You'll update issue with progress daily (even just 1 line)
4. If stuck > 2 hours, ping me immediately

Sound good? 

You've got this!  💪"
```

### Prevention

```markdown
Create culture of transparency:

1. **Daily updates expected:**
   - Add to Definition of Done:  "Comment progress daily"
   - Lead by example:  PM updates issues daily

2. **No shame in asking for help:**
   - Celebrate questions:  "Great question!"
   - Pair programming as default, not last resort

3. **Psychological safety:**
   - "It's okay to be stuck"
   - "It's okay to say you don't know"
   - "What's NOT okay is staying silent"

4. **Check-ins proactive:**
   - PM: Check issues daily, reach out BEFORE 2 days of silence
   - "Hey, saw you're working on X. How's it going?"
```

---

## 🔥 TÌNH HUỐNG 4: Production Bug / Hotfix Needed

### Dấu hiệu nhận biết

```
- Users cannot access system
- Data loss or corruption
- Security vulnerability
- Critical feature broken in production
```

### Ví dụ

```
Friday 3:00 PM - User report: 
"Cannot login. Error 500.  Tried multiple times."

Impact: ALL users blocked
Urgency:  CRITICAL
```

### Immediate Response (< 15 minutes)

#### Step 1: Assess Severity

```markdown
Severity levels: 

🔴 **P0 - Critical:**
- System down
- Data loss
- Security breach
→ Drop everything, fix NOW

🟠 **P1 - High:**
- Major feature broken
- Many users affected
→ Fix within 2 hours

🟡 **P2 - Medium:**
- Minor feature broken
- Some users affected
→ Fix within 1 day

🟢 **P3 - Low:**
- Cosmetic issue
- Few users affected
→ Fix in next sprint
```

#### Step 2: All-Hands Response (P0/P1)

```markdown
1. Alert team (Slack @channel):
   ```
   @channel 🚨 PRODUCTION DOWN
   
   Issue: Login returning 500 error
   Impact: All users cannot login
   Priority: P0 - CRITICAL
   
   ALL HANDS: 
   - @nhanvien_a:  Investigate backend logs
   - @nhanvien_b: Check database
   - @nhanvien_c: Test frontend
   
   War room: https://meet.google.com/xxx
   Join NOW. 
   ```

2. Create incident issue:
   ```
   Title: [P0] Production down - Login 500 error
   Labels: bug, production, p0-critical
   Assignees: All
   ```

3. Stakeholder notification:
   ```
   Email to: [manager, stakeholders]
   Subject:  URGENT - Production Issue
   
   We are aware of login issues.  Team is investigating.
   ETA for fix: [Best guess based on initial assessment]
   
   Will update every 30 minutes. 
   ```
```

#### Step 3: War Room (Video Call)

```markdown
Team on call, screen sharing:

1. **Investigate (parallel):**
   - NV A: Check backend logs
     ```
     tail -f /var/log/app/error.log
     # Look for stack traces
     ```
   
   - NV B: Check database
     ```
     SELECT * FROM users WHERE last_login > NOW() - INTERVAL '1 hour';
     # Check if DB is accessible
     ```
   
   - NV C: Test frontend
     ```
     Browser console → Check API calls
     Network tab → Look for failed requests
     ```

2. **Share findings:**
   Each person reports what they found in call

3. **Identify root cause:**
   Example: "Database connection pool exhausted"

4. **Implement fix:**
   Most experienced dev implements
   Others review/test in parallel
```

#### Step 4: Deploy Hotfix

```markdown
Hotfix process (bypass normal review for P0):

1. Create hotfix branch from main:
   ```bash
   git checkout main
   git pull
   git checkout -b hotfix/login-500-error
   ```

2. Fix bug:
   ```bash
   # Make changes
   git add .
   git commit -m "hotfix: Fix database connection pool exhaustion"
   ```

3. Test locally:
   ```bash
   # Verify fix works
   ```

4. Deploy to production:
   ```bash
   git push origin hotfix/login-500-error
   # Deploy via CI/CD or manual
   ```

5.  Verify fix in production:
   ```
   Test login → Success ✅
   ```

6.  Merge hotfix:
   ```bash
   git checkout main
   git merge hotfix/login-500-error
   git push origin main
   
   git checkout develop
   git merge hotfix/login-500-error
   git push origin develop
   ```
```

#### Step 5: Communication

```markdown
After fix deployed:

1. Test extensively:
   - PM tests login ✅
   - NV C tests multiple browsers ✅
   - Ask internal users to test ✅

2. Announce resolution (30 min after fix):
   ```
   @channel ✅ RESOLVED
   
   Login issue fixed at 4:15 PM.
   Root cause: Database connection pool exhausted
   Fix:  Increased pool size from 10 to 50
   
   All users can now login.
   Monitoring closely for next 2 hours.
   
   Apologies for the disruption.
   ```

3. Email stakeholders:
   ```
   Subject: RESOLVED - Production Issue
   
   Issue resolved at 4:15 PM (duration: 75 minutes).
   All users can now access the system.
   
   Root cause: [Brief explanation]
   Permanent fix: [Long-term solution]
   
   Post-mortem: Will conduct tomorrow. 
   ```
```

### Post-Mortem (Next Day)

```markdown
## Post-Mortem Template

**Incident:** Production login failure
**Date:** [Date]
**Duration:** 75 minutes (3:00 PM - 4:15 PM)
**Severity:** P0 - Critical
**Impact:** 100% of users unable to login

---

### Timeline

| Time | Event |
|------|-------|
| 3:00 PM | First user report received |
| 3:05 PM | Team alerted, war room started |
| 3:15 PM | Root cause identified (DB pool exhaustion) |
| 3:30 PM | Fix implemented |
| 3:45 PM | Deployed to production |
| 4:00 PM | Verified working |
| 4:15 PM | Announced resolution |

---

### Root Cause

**What happened:**
Database connection pool set to 10 connections (default).
Traffic spike from 500 to 2000 concurrent users exhausted pool.
New login requests failed with 500 error.

**Why it happened:**
- Did not configure connection pool for production load
- No monitoring/alerting on connection pool usage
- Load testing did not simulate production traffic

---

### Resolution

**Immediate fix (hotfix):**
Increased connection pool size from 10 to 50 connections.

**Permanent fix (implemented):**
1. Set pool size to 100
2. Add monitoring on pool usage (alert at 80%)
3. Implement connection pool auto-scaling

---

### Impact

**Users affected:** 100% (all users)
**Duration:** 75 minutes
**Data loss:** None
**Revenue impact:** None (internal system)

---

### What Went Well ✅

1. Fast detection (5 minutes from first report to alert)
2. Quick team response (all joined war room within 5 min)
3. Efficient investigation (root cause found in 10 min)
4. Fast deployment (hotfix in 30 min)
5. Good communication (stakeholders updated every 30 min)

---

### What Didn't Go Well ❌

1. No production load testing before launch
2. No monitoring on critical resources (DB pool)
3. No auto-scaling configured
4. Alerting not set up (relied on user report)

---

### Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| Configure DB pool auto-scaling | NV A | Tomorrow | P0 |
| Add monitoring dashboards | NV A | This week | P0 |
| Set up alerting (PagerDuty) | PM | This week | P0 |
| Conduct load testing | Team | Next sprint | P1 |
| Document incident response | PM | This week | P1 |
| Review all resource limits | NV A | Next week | P2 |

---

### Lessons Learned

1. **Load test before production** - Will add to DoD
2. **Monitor all critical resources** - DB pool, memory, CPU, disk
3. **Auto-scale critical resources** - Don't rely on fixed limits
4. **Fast war room response works** - Keep doing this

---

**Post-mortem meeting:** [Date, attendees]
**Report by:** @droid2015
```

---

## 🤝 TÌNH HUỐNG 5: Team Conflict

### Dấu hiệu nhận biết

```
- Passive-aggressive comments in PR reviews
- Decreased collaboration
- Blaming in issue comments
- Silent treatment
- Side conversations excluding someone
```

### Ví dụ

```
PR #45 review: 

NV A (reviewer): "This code is terrible.  Did you even test it?"
NV C (author): "Well maybe if you wrote better APIs I wouldn't have to hack around"

[Tension escalating]
```

### Giải pháp

#### Step 1: De-escalate Immediately

```markdown
PM comments in PR (within 15 minutes):

"@nhanvien_a @nhanvien_c Let's take this offline. 

I'll set up a call for this afternoon to discuss.

In the meantime, let's keep PR comments constructive and professional. 

Thanks for understanding."
```

**Then:**
- Delete or hide inflammatory comments (if possible)
- Or at least stop the thread

#### Step 2: Private 1-on-1s (Before Group)

```markdown
Talk to each person individually first:

Call with NV A (20 min):

PM: "Hey, noticed some tension in PR #45. What's going on from your perspective?"

[Listen without judgment]

PM: "I understand your frustration with code quality. Let's talk about constructive ways to give feedback. 

Instead of 'This is terrible', try: 
'I have concerns about [specific issue].  Can we discuss approach?'

Okay?"

---

Call with NV C (20 min):

PM: "Hey, want to hear your side on PR #45 situation."

[Listen]

PM: "I get that defensive feeling.  NV A's comment was harsh. 

But let's also look at:  Were there test failures? Code review checklist?

How can we improve code quality so reviews go smoother?"
```

#### Step 3: Mediated Discussion (3-person call)

```markdown
PM facilitates (30 min):

1. **Set ground rules:**
   "We're here to solve the problem, not assign blame.
   - Listen respectfully
   - No interrupting
   - Focus on issues, not personalities
   - Assume positive intent"

2. **Each person shares perspective:**
   PM: "@nhanvien_a, can you share your concern?"
   NV A: "I'm frustrated because I see basic bugs in code reviews.  It feels like testing is not happening."
   
   PM: "@nhanvien_c, your perspective?"
   NV C: "I'm doing my best, but the API documentation is unclear. I have to guess how things work."

3. **Find common ground:**
   PM: "Okay, so both want: 
   - Higher code quality ✅
   - Clear documentation ✅
   - Less rework ✅
   
   Agree?"

4. **Action plan:**
   ```
   Agreements:
   - NV C: Will run full test suite before PR (add to checklist)
   - NV A: Will improve API documentation (create this week)
   - Both: Will use constructive feedback template
   - PM: Will add PR review guidelines
   
   Sound fair? 
   ```

5. **Follow-up:**
   "Let's try this for 1 week. I'll check in with both of you on Friday. 
   
   Thanks for working this out.  Appreciate you both."
```

### Prevention

```markdown
Create healthy team culture:

1. **Clear communication guidelines:**
   - Document:  docs/project-management/06-communication-guidelines.md
   - Review in kickoff meeting
   - Reinforce when violated

2. **PR review guidelines:**
   ```
   ✅ Do:
   - Be constructive:  "Consider using X for better performance"
   - Ask questions: "Can you explain the approach here?"
   - Praise good code: "Nice error handling!"
   
   ❌ Don't: 
   - Personal attacks:  "You're a bad developer"
   - Dismissive:  "This is wrong"
   - Sarcasm: "Great job breaking prod"
   ```

3. **Regular team retrospectives:**
   - Safe space to raise concerns
   - Action items to improve
   - Celebrate what's working

4. **PM models behavior:**
   - Give constructive feedback yourself
   - Acknowledge mistakes:  "My bad, I should have..."
   - Praise publicly, criticize privately
```

---

## 🎯 Quick Reference:  Tình Huống & Giải Pháp

| Tình Huống | Severity | Response Time | First Action |
|------------|----------|---------------|--------------|
| **Blocker** | High | < 1 hour | Escalate, find workaround |
| **Late Issue** | Medium | Same day | Assess root cause, re-scope or extend |
| **Silent Developer** | Medium | 2 days | Private check-in, offer help |
| **Production Bug** | Critical | < 15 min | All-hands, war room, hotfix |
| **Team Conflict** | High | < 1 hour | De-escalate, mediate, action plan |
| **Scope Creep** | Medium | During planning | Document change, stakeholder approval |
| **Resource Shortage** | High | < 1 day | Prioritize, defer low-priority items |
| **Technical Debt** | Low | Next sprint | Create backlog items, schedule refactor |

---

## 📞 Escalation Matrix

### When to Escalate

```
Level 1 - Team (handle internally):
- Minor technical issues
- Small delays (< 1 day)
- Process questions
→ Resolve:  PM + team

Level 2 - Manager (escalate up):
- Blockers > 1 day
- Resource shortages
- Budget overruns
→ Escalate: PM → Manager

Level 3 - Executive (critical):
- Project at risk of failure
- Major budget/timeline issues
- Legal/compliance concerns
→ Escalate: Manager → Executive

Level 4 - External (outside org):
- Vendor issues
- Client escalations
- Legal matters
→ Escalate: Executive → Legal/Vendor Management
```

### Escalation Template

```markdown
Email to: [Manager]
Subject: Escalation Required - [Brief Description]

**Issue:**
[Clear description of problem]

**Impact:**
- Timeline:  [Days delayed]
- Budget: [Cost overrun]
- Scope: [Features at risk]

**What We've Tried:**
1. [Action 1] - Result: [Failed/Partial]
2. [Action 2] - Result: [Failed/Partial]

**Need From You:**
[Specific ask - resources, decision, stakeholder intervention]

**Urgency:**
[Timeline - When do we need resolution?]

**Impact if Not Resolved:**
[Consequence - project delay, cost increase, etc.]

---
PM: @droid2015
Date: [Date]
```

---

## 💡 General Troubleshooting Principles

### 1. Stay Calm

```
😰 Panic → Bad decisions
😌 Calm → Clear thinking

Even in P0 incidents: 
- Take 30 seconds to breathe
- Assess situation clearly
- Then act decisively
```

### 2. Gather Information First

```
Before reacting, ask:
- What exactly is the problem?
- What's the impact?
- What's the urgency?
- What have we tried? 

Don't: 
- Jump to solutions
- Blame people
- Make assumptions
```

### 3. Communicate Proactively

```
Over-communicate during incidents:
- Update team every 30-60 min
- Update stakeholders every 1-2 hours
- Log everything in issue/doc

Silence = Panic
Updates = Confidence
```

### 4. Document Everything

```
During incident:
- Keep timeline of events
- Log all actions taken
- Screenshot errors
- Save logs

After resolution:
- Write post-mortem
- Extract lessons
- Create action items
- Share with team
```

### 5. Learn & Improve

```
Every problem is opportunity:
- What can we do better?
- What can we automate?
- What can we prevent? 

Update: 
- Processes
- Documentation
- Tools
- Training
```

---

## 🆘 Emergency Contacts

### Internal

| Role | Name | Phone | Email | Availability |
|------|------|-------|-------|--------------|
| Project Manager | @droid2015 | [phone] | [email] | 24/7 |
| Tech Lead | NV A | [phone] | [email] | Working hours |
| Manager | [Name] | [phone] | [email] | Working hours |
| IT Support | [Name] | [phone] | [email] | 8 AM - 6 PM |

### External

| Service | Contact | Phone | Website |
|---------|---------|-------|---------|
| Hosting Provider | [Provider] | [phone] | [support URL] |
| Database Support | [Vendor] | [phone] | [support URL] |
| Internet Provider | [ISP] | [phone] | [support URL] |

### On-Call Rotation

```
Week 1: NV A (primary), NV B (backup)
Week 2: NV B (primary), NV C (backup)
Week 3: NV C (primary), NV A (backup)

On-call responsibilities:
- Respond to P0/P1 alerts within 15 min
- Available for emergency calls
- Compensation:  Overtime pay or comp time
```

---

## 🎯 Prevention Checklist

```markdown
To minimize incidents:

Infrastructure:
- [ ] Monitoring on all critical resources
- [ ] Alerting configured (PagerDuty, etc.)
- [ ] Auto-scaling for traffic spikes
- [ ] Regular backups (daily + tested restores)
- [ ] Disaster recovery plan documented

Process:
- [ ] Code review mandatory
- [ ] CI/CD tests passing before merge
- [ ] Staging environment for testing
- [ ] Load testing before production
- [ ] Rollback plan for deployments

Communication:
- [ ] Clear escalation paths
- [ ] Contact information up-to-date
- [ ] Incident response runbook
- [ ] Regular fire drills (simulate incidents)

Team:
- [ ] Cross-training (no single point of failure)
- [ ] Documentation up-to-date
- [ ] Knowledge sharing sessions
- [ ] On-call rotation fair
```

---

**Last updated:** 2025-12-30  
**Author:** @droid2015

**Remember:** Every problem is solvable. Stay calm, communicate clearly, and work together.  You've got this!  💪
