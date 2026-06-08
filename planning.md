# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? --> I chose Computer Science Course Difficulty Rankings, there isn't an official page where Universities and Colleges rank their courses in terms of difficulty so relying on student experiences will be helpful

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Reddit |A list which combines the last three years of grades and reviews data to sort all courses by average difficulty |https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/|
| 2 |OMS Reviews |Community Rankings of all Online Master of Science in Computer Science from Georgia Tech's Program  |https://www.omscentral.com/ |
| 3 |Reddit |Hardest Undergraduate courses for CS |https://www.reddit.com/r/csMajors/comments/13u8utd/hardest_individual_undergrad_cs_course_in_the_us/ |
| 4 |Reddit |Rensselaer Polytechnic Institute students rating and describing their specific CS courses |https://www.reddit.com/r/RPI/comments/sfoxhy/calling_all_cs_major_to_give_your_opinion_of_the/ |
| 5 |Reddit |York University student ratings for their CS courses |https://www.reddit.com/r/yorku/comments/i86cwl/computer_science_students_rank_your_undergrad/ |
| 6 |Reddit |UMass Lowell University student ratings for their CS courses |https://www.reddit.com/r/uml/comments/d9ct6d/cs_required_classes_easiest_to_hardest/ |
| 7 |Reddit |WGU CS students ranking the CS courses |https://www.reddit.com/r/WGU_CompSci/comments/13fovi2/class_difficulty_ranking/ |
| 8 |Reddit |University of Utah students discussing the order of when to take classes based on order and difficuly |https://www.reddit.com/r/uofu/comments/vhi0bw/can_anyone_help_with_cs_course_planning_and_let/ |
| 9 |Reddit |Discussion of the Hardest courses in Computer Science |https://www.reddit.com/r/csMajors/comments/zrpwz4/in_your_own_opinion_what_is_the_hardest_subject/ |
| 10 |Rate My Professors |There's a difficulty level for each course in Computer Science across different universities  |https://www.ratemyprofessors.com/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
 So each webpage (majority are Reddit) does have comments some are large and others are small so i'm thinking of averaging 200-400 tokens per chunk 
 I want to have one comment per chunk (hopefuly)

**Overlap:**
Probably a 50 token overalp 
**Reasoning:**
Some of the reddit comments contain a lot of classes and rankings so i need to make sure each chunk has the most amount of data 
A 50 token overlap will allow a smooth transition from one chunk to the other without having too much info lost (or included)

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
The embedding model will be the sentence-transformers(all-MiniLM-L6-v2)

**Top-k:**
Probably 6? I think that should be a good number so that it gets a solid conclusion. Can't be less than 4 since we could miss the overall decision 

**Production tradeoff reflection:**
So the all-MiniLM-L6-v2 has a 256 max token input length which should hopefully be alright due to the nature of the posts. Other models allow for more tokens, but for now this shiuld be enough 

This model doesn't train on the content so we might not get the most accurate output but it is fast so we'll give it props for that 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What CS courses do students at multiple different universities all agree are difficult? |Should mention Operating Systems and/or Theory of Computation/Algorithms with evidence from different schools |
| 2 |What advice do students give about which CS courses NOT to take at the same time?   |Should mention at least one specific pairing to avoid |
| 3 |What factors besides course content make CS courses feel harder or easier? |Should mention things like professor choice, prior experience, whether you're working or just focusing on school etc |
| 4 | How do students describe the workload of hard CS courses in terms of time commitment? | Should include at least one specific hour estimate, such as hours per week spent on assignments or total time per semester|
| 5 | What do students say about how their background or prior experience affects how hard they find CS courses? | Should mention that prior programming experience, math background, or familiarity with languages like C or C++ makes specific courses easier or harder |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Probably inconsistent answers for some of the questions since everyone's experience is different and there's different opinions on hard classes in terms of ranking

2. I noticed that Reddit cannot be directly scrapped and we'll need a workaround since it blocks automted requests

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Document Ingestion: ------------------------>   Chunking: --------------------------------------> Embedding and Vector Storage
          -> Python Requests                            -> 200 - 400 tokens                               -> use the all-MiniLM-L6-v2 (sentence-transformers) with ChromaDB
          -> Reddit JSON                                -> 50 token overalp
          -> .txt for the threads                       -> We split by the Reddit comment



After Embedding and Vector Storage---> Retrieval: ---------------------> Genertion: Groq API llama-3.3-70b
                                          ->ChromaDB Search                
                                          -> topk is 6 chunks
 

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     I'm planning on using Claude

     - What you'll give it as input (which sections of this planning.md, which requirements)
     I'll be giving the source table from planning.md plus the 10 URLS (need to note that scrapping cannot be done directly; need additional tools)
     - What you expect it to produce
     It shouls produce ingest.py which will save the raw text as text files

     - How you'll verify the output matches your spec
     I can sort of compare the output words with what the webpages have and ensure that each text file has words 

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


     Document Ingestion:
     Which AI:
     Input: 
     What it'll Produce: 
     Verfy Output:

     Chunking:
     Which AI:
     Input: 
     What it'll Produce: 
     Verfy Output:

     Embedding and Vector Storage:
     Which AI:
     Input: 
     What it'll Produce: 
     Verfy Output:

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
