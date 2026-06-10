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

My domain is going to be things to do around UC San Diego. This knowlegde is valuable because new students will want to know where to go and explore. They want to be able to experience San Diego. There is too much information, so having it in one place will be helpful for students. This can also help students that are still deciding if they would like to go to UC San Diego. They can ask about activities and resturants around UC San Diego.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Ultimate Guide to UC San Diego | Gives areas to go to around UC San Diego | https://prked.com/post/your-ultimate-guide-to-an-unforgettable-time-around-uc-san-diego |
| 2 | 26 things to do in San Diego | List of things to do around SD | https://californiathroughmylens.com/things-to-do-in-san-diego/ |
| 3 | Top 10 Eats Near UCSD | 10 food places near UC San Diego | https://ucsdguardian.org/2024/01/29/top-10-eats-near-ucsd/ |
| 4 | Reddit San Diego | Favorite beach in San Diego | https://www.reddit.com/r/sandiego/comments/osxcqd/whats_your_favorite_beach_in_san_diego/ |
| 5 | Study spots | 10 best stpots to study on campus | https://today.ucsd.edu/story/10-best-spots-to-study-on-campus |
| 6 | Reddit Food San Diego | Best boba places in San Diego | https://www.reddit.com/r/FoodSanDiego/comments/1ior4sy/best_boba_places_in_san_diego/ |
| 7 | Sunset spots | 5 Best spots to watch the sunset in San Diego | https://soulsummittravel.com/2024/04/30/sunset-spots-san-diego/|
| 8 | Running trails in SD| Best places to run in San Diego| https://www.chelseyexplores.com/best-places-to-run-in-san-diego/ |
| 9 | Food places at UC San Diego| Places to Eat at UCSD | https://blink.ucsd.edu/facilities/services/general/personal/dining.html |
| 10 | Activities at UC San Diego | 15 Ideas for your UC San Diego Bucket List| https://today.ucsd.edu/story/15-ideas-for-your-uc-san-diego-bucket-list |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

The chunk size that I opted to use was 1000 characters. I used both a recursive chunker and semantic chunker depending on the document. For text dense documents, I used the recursive chunker with 1000 characters to capture the paragraph of text without losing the information.

**Overlap:**

The overlap size I chose was 150 characters. I used 150 characters because there is a chance that the chunker can cut out the beginning sentence which includes the key data (name of place) so by having the overlap big enough to recover the lost info

**Why these choices fit your documents:**

I chose to use both a recursive chunker and semantic chunker because some documents were more dense and others were very sparse with many one liners. When testing just the recursive chunker, on the sparse document it returns only one line. So I used both to account for some documents.

**Final chunk count:**

The final chunk count across all documents was 251.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

The embedding model that I used was the all-MiniLM-L6-v2 via sentence-transformers model. This model is lightweight and local. It is free and requires no api calls. So I can keep testing my chunking and embedding anytime I want and tweak the functions.

**Production tradeoff reflection:**

If cost wasn't an issue I would choos e a better model such as gemini embedding 2 becasue it has a higher context window than the one i chose. This allows for better embedding of the data which leads to better accuracy of similarity. The tradeoff would be latency since the all-MiniLM-L6-v2 via sentence-transformers model runs locally so it is fast, but that is a tradeoff I would take for better accuracy.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

My system enforces grounding in my system prompt in my generate response function. In the system prompt, I strictly told it to
use only information from the provided documents without retrieving outside sources. I then added another prompt to embed inline source citations into the response directly. I also told it to respond with not enough information if the context from the retrieval doesn't fully answer the question. 

**How source attribution is surfaced in the response:**

Source attribution is surfaced in the response through inline citations. It embeds the citation within the response from the system prompt. 


---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which floor of Geisel Library is the silent study floor?| The 8th floor of Geisel is considered the silent study floor| The silent study floor of Geisel Library is located on the 8th floor [Source: 10 Best Spots To Study On Campus].| Relevant | Accurate|
| 2 | What is a good dirt trail to run?| Tecolote| According to the "Best Places To Run In Sd" document, Tecolote Canyon Trails offer dirt trails for running, with options for easy dirt paths and hillier paths, and distances ranging from 0.3 to 3.8 miles [Source: Best Places To Run In Sd]| Relevant | Accurate |
| 3 | Are there any museums or aquariums I can visit near campus?  | Birch Aquarium or Museum of Contemporary Art | You can visit the Timken Museum of Art, which has the only Rembrandt on public display in San Diego, and it's always free [Source: Ultimate Guide To Ucsd]. Additionally, you can visit the Birch Aquarium at Scripps Institution of Oceanography, which features various marine life, including sea dragons, corals, and a Giant Pacific Octopus [Source: 15 Ideas For Your Ucsd Bucket List].| Partially relevant| Partially Accurate |
| 4 | What is a good place to nap on campus? | Hammock Swings| Campus hammocks, located on the lawns of the Price Center and the Main Gym, as well as near Revelle and Marshall Colleges, can be a great spot to take a nap [Source: 10 Best Spots To Study On Campus]. | Relevant| Accurate |
| 5 | Which beaches near campus have fire pits? |  La Jolla Shores or Mission Beach| La Jolla Shores has fire pits, where you can see bonfires dotting the shoreline on a warm evening, but it's recommended to get there early to snag a fire pit [Source: Ultimate Guide To Ucsd]. | Relevant | Partially Accurate |

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

I asked the question "What is a good boba spot in convoy?"

**What the system returned:**

The system returned with "There is a boba spot in Convoy [Source: Best Boba In Sd]. It has "the biggest emptiest parking lot you will find on Convoy" [Source: Best Boba In Sd]."

**Root cause (tied to a specific pipeline stage):**

This response shows how the chunking failed. The info in this chunk only says boba spot in Convoy. It doesn't mention a name of the shop. This means that the name is in a different chunk. It matched the keyword boba and convoy, but failed to give the name of the actual place. 

**What you would change to fix it:**

To fix this failure case, I would edit my chunker to account for the document structure. I think this document structure is sparse, so I would have to use a different method to capture all relevant information instead of just boba and convoy.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
One way the spec helped me during implementation was planning out the questions to test the RAG with. This helped because when I was looking through the chunks this gave me a rough idea of there was enough information in each chunk or not. This helped me tweak the chunk size to 1000 and overlap to 150.

**One way your implementation diverged from the spec, and why:**

One way my implementation diverged from the spec is my chunk size and overlap. Originally I had the chunk set to 650 and overlap set to 80. This was way to small because it started cutting off alot of data for each chunk. So the name would be in one chunk and the description would be in another.

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

- *What I gave the AI:* I gave Claude the Chunking Strategy from planning.md and the example code of recursive chunking from the class demo. I asked it to implement the chunk_text with my given chunk count and overlap.
- *What it produced:* It produced a modified version of the function with my given chunk size and my overlap.
- *What I changed or overrode:* I changed the chunk_size and overlap after testing out the code. I noticed that the chunks were too small and didnt have enough information.

**Instance 2**

- *What I gave the AI:* I prompted Claude to help me with the generate_response function when calling the groq api. I provided the specs for what I wanted for this function and what I wanted it to return.
- *What it produced:* It produced the generate_response function with a very simple system prompt and the return value was only one combined output.
- *What I changed or overrode:* I changed the system prompt to be more specific about embedding the sources into the output itself. I also changed the function to work with the existing gradio code snippet provided. I did this by returning both the llm_answer and source_list separately instead of one combined return. This solved the gradio error.
