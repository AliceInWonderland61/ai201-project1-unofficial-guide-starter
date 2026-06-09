# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     The topic is Computer Science course difficulty ratings across different universities. As students, we are always providing feedback and discussing which courses are the hardest, when to take each course and which combination of courses to stay away from. We can't really find them through official channels because it's an opinion based statistic (word of mouth)instead of actual facts. So this system makes that student generated knowledge searchable and answerable in plain language 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/OMSCS difficulty rankings| Reddit Thread |https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/ |
| 2 |OMSCentral course reviews |Review platform |https://www.omscentral.com/ |
| 3 |r/csMajors hardest undergrad courses |Reddit Thread |https://www.reddit.com/r/csMajors/comments/13u8utd/hardest_individual_undergrad_cs_course_in_the_us/ |
| 4 |r/RPI CS course opinions |Reddit Thread |https://www.reddit.com/r/RPI/comments/sfoxhy/calling_all_cs_major_to_give_your_opinion_of_the/ |
| 5 |r/yorku CS course rankings |Reddit Thread |https://www.reddit.com/r/yorku/comments/i86cwl/computer_science_students_rank_your_undergrad/ |
| 6 |r/uml easiest to hardest |Reddit Thread |https://www.reddit.com/r/uml/comments/d9ct6d/cs_required_classes_easiest_to_hardest/ |
| 7 |r/WGU_CompSci difficulty ranking |Reddit Thread | https://www.reddit.com/r/WGU_CompSci/comments/13fovi2/class_difficulty_ranking/|
| 8 |r/uofu CS course planning | Reddit Thread| https://www.reddit.com/r/uofu/comments/vhi0bw/can_anyone_help_with_cs_course_planning_and_let/|
| 9 |r/csMajors hardest CS subjects | Reddit Thread|https://www.reddit.com/r/csMajors/comments/zrpwz4/in_your_own_opinion_what_is_the_hardest_subject/ |
| 10 |Rate My Professors — UTRGV CS | Review platform| https://www.ratemyprofessors.com/search/professors/1306?q=*&did=11|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
The chunk size is 1,200 characters which is about 300 tokens (4 characters per token as proxy)

**Overlap:**
The overlap was 200 charaters which is approximately 50 tokens

**Why these choices fit your documents:**
Most of my sources are Reddit threads so the best way (in my opinion) is to split them by comment since each comment contains information on a student's opinion and that's what we want to retrieve
Instead of cutting the text at every n characters, we split them by comment. Of course, there are a few that are quite large so if a comment was over 1,200 characters, then it got split again with a 200 character overlap so the two halves have enough information to share. 
Just like there's large comments, there's super short ones, so for those if there was a chunk that was under 80 characters, we disregard it since it was most likely just a fragment with no useful information. 

**Final chunk count:**
We had 179 chunks across 10 documents 

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
I used sentence-transformers/all-MiniLM-L6-v2. I chose this one because it runs completely on my own computer — no API key needed, no rate limits, and it's free (plus it was given to me). It's also fast enough to embed all 179 chunks in under a minute which was important for a project like this.

**Production tradeoff reflection:**
So if this were deployed for real useres I might contemplate on choosing another model becuase this model can only handle 256 tokens at a time, so longer reviews could potentially get cut off. This model was not trained on Computer Science course content specifically so it might not catch the difference between student expressions about courses. However, running it locally is great for personal projects so it has pretty good merits. 
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
I gave the model a set of rules it has to follow every time someone asks a question. The main ones are only answer using what's in the documents I provided, don't pull from general knowledge, and if the documents don't have enough to answer the question just say "I don't have enough information in my sources to answer that question." I also told it not to think out loud or explain its reasoning and to just give the answer directly. To make citations work, I formatted each chunk with its source name before the text (like [Source: r/uofu | University: University of Utah]) so the model always knows where each piece of information came from and can reference it by name instead of saying something vague like "Document 1 (which did show and I had to fix it)"

**How source attribution is surfaced in the response:**
There are two ways sources show up. First, the model is instructed to cite sources inline in its answer, for example "According to r/uofu..." or "A student on r/csMajors said...". Second, the pipeline collects the source names from all the retrieved chunks and displays them separately in a Sources box on the right side of the UI. That way even if the model forgets to mention a source in the answer, it still shows up in the Sources box.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What CS courses do students at multiple different universities all agree are difficult? |Should mention Operating Systems and/or Algorithms with evidence from different schools |Correctly identified Data Structures and Algorithms as universally hard, cited r/csMajors and r/RPI |Relevant |Accurate |

| 2 |What advice do students give about which CS courses NOT to take at the same time? |Should mention at least one specific pairing to avoid |Mentioned Comp Architecture + OS from r/csMajors and overloading warning from r/uofu|Relevant |Accurate |

| 3 |What factors besides course content make CS courses feel harder or easier? |Should mention professor choice, prior experience, working full time |Got professor dependency and personal interest right, missed prior experience and working while studying |Relevant |Partially Accurate |

| 4 |How do students describe the workload of hard CS courses in terms of time commitment? |Should include at least one specific hour estimate |Gave a ranked list from r/RPI and general workload mention from r/uofu but never surfaced the 80 hours/week estimatePartially relevant |Partially Relevant |Partially Accurate |

| 5 |What do students say about how their background or prior experience affects how hard they find CS courses? |Should mention prior programming experience, math background, or C/C++ familiarity |Only pulled from r/csMajors, answered about background in general terms but missed the specific C/C++ advice from r/uofu |Relevant |Partially Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"How do students describe the workload of hard CS courses in terms of time commitment?"
**What the system returned:**
It gave a ranked list of courses by time commitment from r/RPI and a vague mention from r/uofu that theory-heavy classes require a lot of homework and time. It never mentioned the specific 80 hours per week estimate that was in the r/uofu thread, which was the most useful and concrete answer for this question.
**Root cause (tied to a specific pipeline stage):**
I do believe it was a chunking problem The comment that contained the hours per week was kind of a long comment so it was split into two chunks due to the 1,200 character limit. The sentence with the actual hour estimate ended up in a different chunk than the course names it was referring to. So when the query came in asking about time commitment, the retrieval step found the chunk with the course names but not the one with the hour estimate and since niether half was specific enough on its own, then it was missed. 
**What you would change to fix it:**
I should probably try to keep sentences with specific numbers (like hours per week, GPA, percentages) attached to the surrounding context instead of just cutting at a character limit. That way the most imporant data points don't get split from the context that makes them meaningful.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Having the chunking strategy written out in planning.md before touching any code made the actual implementation way smoother. Since I decided that one comment equals one chunk, I didn't have to figure that out mid-coding and I just got to building exactly what the plan said. It also made it easy to check my work since I could look at the output and check if it was right or wrong

**One way your implementation diverged from the spec, and why:**
The spec said the chunk size would be 300-400 tokens but in the actual code I ended up using characters (1200 characters) instead of tokens. The reason is that counting tokens accurately would have required loading the embedding model during the chunking step which felt unnecessary and slow for something that just needs to split text. By using the characters as a proxy (about 4 characters per token) got me close enough to the same result. I updated planning.md to reflect this change so the spec and the code at least matched each other by the end.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave Claude my planning.md — specifically the Documents section with all 10 source URLs, the Chunking Strategy section (300-400 tokens, 50 token overlap, split by Reddit comment), and the ASCII pipeline diagram. I asked it to write ingest.py to fetch and save the documents and chunk.py to split them by comment boundary.

- *What it produced:*
Two complete Python scripts. ingest.py used the Reddit JSON API to fetch comments and save them as .txt files (didn't work but it produced it). chunk.py split on the --- separators between comments and applied a character-limit fallback for long comments.
- *What I changed or overrode:*
The chunk filter used startswith("[POST]") to remove post headers but that missed headers that started with === before the [POST] tag. I changed it to "[POST]" not in chunk_text to catch all of them. I also switched from token-based to character-based chunking because counting tokens would have required loading the embedding model during ingestion which was unnecessary.

**Instance 2**

- *What I gave the AI:*
I showed Claude the actual output from the system where the LLM was saying things like "According to Document 3..." and "Document 4 mentions..." instead of using real source names. I asked it to fix both the prompt and the context format so citations would use subreddit names instead.

- *What it produced:*
An updated generate.py where the context format changed from [Document {i+1} | Source: ...] to just [Source: ... | University: ...], removing the document number entirely. It also added a rule to the system prompt saying never say "Document 1" or "Document 2" and to use the source name instead.

- *What I changed or overrode:*
I noticed that just changing the context format wasn't enough on its own — the model would still invent document numbers sometimes. I kept both the format change and the explicit prompt rule together because only combining them actually fixed the problem consistently across all test queries.
