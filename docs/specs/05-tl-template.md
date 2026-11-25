# Spec 05: TL interview template

The first template. Roadmap step 9 turns this into `templates/tl-interview.json`, validated against [spec 01](01-template-schema.md). Items marked placeholder or TBD are still open.

## Formats and scale

- Formats: 75 and 90 minutes.
- Scale: 1 to 3.
- 7 criteria, so totals range from 7 to 21.

## Sections

| Section | Type | 75 / 90 min | Criteria |
|---|---|---|---|
| Intro | questions | 3 / 5 | none |
| Part 1: PR review | checklist | 15 / 20 | code_review |
| Part 2: Unfamiliar territory (scope, then design) | whiteboard | 20 / 25 | scoping, architecture |
| Part 3: Project walkthrough | questions | 17 / 22 | walkthrough_depth |
| Part 4: Behavioral | questions | 15 / 15 | member_ownership, pressure_communication |
| Candidate questions | questions | 5 / 3 | none |

Overall criterion scored once after the interview: coachability.

## Criteria

| Criterion | 1 Not yet | 2 Meets | 3 Strong |
|---|---|---|---|
| code_review | Style nits only, misses the main bug, or feedback is vague or harsh | Finds the obvious bug and one logic or validation gap, with specific and polite feedback | Finds them all, ranks by impact, catches a subtle issue, and the feedback explains why and teaches |
| scoping | Starts building, asks no questions | Asks relevant questions, defines a first version | Questions change the scope, first version fits a small student team, names what is cut |
| architecture | Can't place data or services | Clear pieces, data flow and storage | Also names the API, a failure point, and a data or user concern (privacy, bad inputs) |
| walkthrough_depth | Can't explain their own code | Traces one data flow end to end | Explains tradeoffs, hardest bug, and what they would change |
| member_ownership | Hands out tasks, or vague "make them feel valued" | Concrete steps, such as owning a piece end to end or real input on decisions | Tailors to each person, builds real autonomy and growth, supports less experienced members |
| pressure_communication | Hides the problem or cuts randomly | Cuts by priority and tells the team | Cuts by client impact, tells the PL and client early, offers a plan |
| coachability | Bluffs or gets defensive | Says "not sure" at times, uses hints | Reasons from a hint, owns gaps, adjusts mid answer |

## Hints

Revealed in order.

- PR review:
  1. "What happens if this input is empty or unexpected?"
  2. "Does this match how the rest of the repo handles it?"
  3. "Which comment would you leave first for a newer member?"
- Part 2:
  1. "Who uses this and what do they do with it?"
  2. "Given your team and timeline, what ships first?"
  3. "Where does the data come from and where does it live?"
  4. "What happens if this step fails?"
  5. "Anything about this data or the users you would handle carefully?"
- Walkthrough:
  1. "Pick one request and trace it from start to finish."

## Prompts and items

- **Intro**: "This is live and there is no single right answer. We care about how you think. Ask us questions any time. If you're unsure, say so."
- **PR review**: "Walk us through what you notice in the code, and what feedback you would give the member." Checklist items are placeholders: obvious bug, logic or validation bug, design smell, subtle issue.
- **Part 2**: the feature is a placeholder (TBD).
- **Walkthrough follow ups**: one full data flow end to end, how services communicate, codebase organization, GitHub use (branching, reviews, CI), where the design breaks under scale, testing, tech stack choice, hardest bug, what they would change.
- **Behavioral**:
  1. Younger, less experienced members will produce less than senior members. How will you ensure they feel ownership over the project?
  2. A week before a deadline you realize the team won't finish everything. How do you decide what to cut, and who do you tell?
  3. (If time) A time you were wrong about a technical decision and someone else was right.

## Red flags

| Red flag | Section |
|---|---|
| Harsh or dismissive feedback to a member | PR review |
| Designs a full solution without asking a question | Part 2 |
| Can't explain their own code, or takes all the credit and names no mistakes | Walkthrough |
| Hides the problem or cuts without telling anyone | Behavioral |
| States something wrong as fact instead of saying "not sure" | Overall |
