# Speaker Split - 5 People

**Total Presentation Time:** 15 minutes  
**Per Person:** ~3 minutes each

---

## Assignment Strategy

Divide slides by **expertise area**, not strictly by slide count.

---

## Option A: By Technical Domain

### Person 1: Introduction & Dataset (3 min)

**Slides:**
- Slide 1: Title & Team
- Slide 2: Project Overview
- Slide 7: Dataset Overview
- Slide 8: ETL Pipeline

**Responsibilities:**
- Introduce project
- Explain dataset source and size
- Describe ETL process

**Why:**
- Sets context for entire presentation
- Non-technical audience can follow
- Explains "where data comes from"

---

### Person 2: Database Design - ER & Mapping (3 min)

**Slides:**
- Slide 3: ER Diagram (High-Level)
- Slide 4: ER to Relational Mapping
- Slide 6: Schema Summary

**Responsibilities:**
- Present ER diagram (entities, relationships, cardinality)
- Explain ER → Relational mapping rules
- Summarize final schema (9 tables)

**Why:**
- Core database theory (rubric requirement)
- Visual (ER diagram)
- Shows design process

---

### Person 3: Normalization & Schema Design (3 min)

**Slides:**
- Slide 5: Normalization

**Responsibilities:**
- Explain normalization process (denormalized → 3NF)
- Show before/after example
- Describe functional dependencies

**Why:**
- Deep dive into one complex topic
- Academic focus (normalization proof)
- Less time needed (1 slide but detailed)

---

### Person 4: Features & Complex Queries (3 min)

**Slides:**
- Slide 9: Application Features
- Slide 10: Complex Query 1 - Revenue by Category
- Slide 11: Complex Query 2 - Review vs Delivery
- Slide 13: SQL Concepts Demonstrated

**Responsibilities:**
- Demo dashboard (live or screenshots)
- Walk through 2 complex SQL queries
- Highlight SQL techniques (JOIN, TIMESTAMPDIFF, HAVING)

**Why:**
- Most "showy" section (live demo)
- Technical depth (SQL code)
- Showcases project's complexity

---

### Person 5: Performance, Testing & Conclusion (3 min)

**Slides:**
- Slide 12: Query Optimization (Performance)
- Slide 14: Testing & CI/CD
- Slide 15: Conclusion & Q&A

**Responsibilities:**
- Explain index design and performance gains
- Describe testing strategy (pytest + CI/CD)
- Wrap up and open Q&A

**Why:**
- Technical highlights (10-21x speedup)
- Quality assurance (testing)
- Owns Q&A moderation

---

## Option B: Sequential Split (Equal Slides)

If team prefers equal slide distribution:

### Person 1: Slides 1-3 (3 slides)
- Introduction
- Overview
- ER Diagram

### Person 2: Slides 4-6 (3 slides)
- ER Mapping
- Normalization
- Schema Summary

### Person 3: Slides 7-9 (3 slides)
- Dataset
- ETL
- Features

### Person 4: Slides 10-12 (3 slides)
- Complex Query 1
- Complex Query 2
- Performance

### Person 5: Slides 13-15 (3 slides)
- SQL Concepts
- Testing
- Conclusion

---

## Option C: Expertise-Based (Recommended)

Assign based on who wrote/understands each part best:

### Person 1: Project Lead
- Introduction (Slides 1-2)
- Conclusion (Slide 15)
- Q&A moderation

### Person 2: Database Designer
- ER Diagram (Slide 3)
- ER Mapping (Slide 4)
- Schema Summary (Slide 6)

### Person 3: Theory Expert
- Normalization (Slide 5)
- SQL Concepts (Slide 13)

### Person 4: Developer (Backend)
- Features (Slide 9)
- Complex Queries (Slides 10-11)
- Performance (Slide 12)

### Person 5: Developer (Testing/DevOps)
- Dataset & ETL (Slides 7-8)
- Testing & CI/CD (Slide 14)

---

## Transition Script

**Use these phrases to transition between speakers:**

### Person 1 → Person 2:
> "Now that you understand the dataset, let me hand it over to [Person 2] to explain how we designed the database schema from scratch."

### Person 2 → Person 3:
> "With the ER diagram in place, [Person 3] will walk you through our normalization process to eliminate redundancy."

### Person 3 → Person 4:
> "Now that we have a clean schema, [Person 4] will demonstrate the application features and complex queries we built on top of it."

### Person 4 → Person 5:
> "Those queries were optimized for performance, and [Person 5] will explain how we achieved 10-21x speedup, plus our testing strategy."

### Person 5 → Conclusion:
> "And that concludes our technical presentation. We're now open for questions."

---

## Rehearsal Plan

### Practice Sessions

**Session 1 (2 days before):**
- Each person practices their slides solo
- Time yourself (aim for 2:30-3:00 per person)
- Refine slide content if too long

**Session 2 (1 day before):**
- Full run-through with transitions
- Time entire presentation (should be 14-16 minutes)
- Practice Q&A responses

**Session 3 (Morning of demo):**
- Quick run-through (no slides, just talking points)
- Verify equipment (projector, laptop, demo setup)
- Confirm backup plan (screenshots ready)

---

## Demo Day Roles

### Technical Roles

**Demo Driver:**
- Person 4 (runs live demo during Slide 9)
- Has laptop connected to projector
- Runs `start-demo.ps1` before presentation

**Backup Demo:**
- Person 5 (has screenshots ready)
- Takes over if live demo fails

**Q&A Lead:**
- Person 1 (moderates questions)
- Can delegate technical questions to relevant person

---

## Backup Plan (If Someone Missing)

**If 1 person absent:**
- Person 1 covers Slides 1-2, 15
- Person 2 covers Slides 3-6
- Person 3 covers Slides 7-9
- Person 4 covers Slides 10-14

**If 2 people absent:**
- Merge slides (skip backup slides)
- 3 people × 5 minutes = 15 minutes

---

## Equipment Checklist (Team Responsibility)

Before presentation:

- [ ] Laptop with demo loaded
- [ ] Projector connection tested
- [ ] MySQL service running
- [ ] Demo backend started
- [ ] Frontend loaded in browser
- [ ] Backup screenshots in folder
- [ ] Slide deck loaded
- [ ] Timer/stopwatch ready
- [ ] Water bottles (hydration!)

---

## Post-Presentation

**Debrief:**
- What went well?
- What could improve?
- Any surprising questions?

**Documentation:**
- Add Q&A notes to repo (if interesting questions)
- Update README with presentation feedback

---

## Contact During Prep

**Coordinate via:**
- WhatsApp/Slack: Quick questions
- GitHub Issues: Technical blockers
- Google Docs: Slide edits

---

**For slide content, see [SLIDE_OUTLINE.md](SLIDE_OUTLINE.md)**  
**For screenshot targets, see [SHOTLIST.md](SHOTLIST.md)**
