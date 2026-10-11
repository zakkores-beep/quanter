# Goldman Sachs Engineering OA: Format (research summary, Oct 2026)

**What's confirmed:** your invitation email and Goldman's official HackerRank guide.
**What isn't:** question counts and difficulty. Those come from candidate reports and prep sites, which are thin and sometimes disagree. Where they conflict, the default chosen for this trainer is in **bold**.

## 1. Software Fundamentals: 30 min, DSA, any language
- **Official:** all candidates take this section. It tests data structures and algorithms in the language of your choice. No question count is given. ([GS guide][gs])
- **Reports:**
  - 2 coding questions in 30 min, rated "higher" difficulty ([PrepInsta][prepinsta])
  - 2 LeetCode-medium DS&A problems ([Glassdoor][gd2], older)
  - "Medium DSA, DP and graph questions more" ([Glassdoor 2025][gd1])
  - arrays, strings and complexity ([LeetCode Discuss 2025][lc1])
  - Older or other-track reports describe 120-min tests with 3-4 problems. Those don't match the current 30-min format.
- **Default: 2 problems in 30 min (1 easy, 1 medium).** The topic mix leans toward arrays and hashing, strings, DP and graphs. Expect HackerRank-style I/O: you implement a function, and hidden tests include large inputs.

## 2. Software Diagnostics: 45 min, fix a bug in an existing app
- **Official:** engineering applicants work inside an existing Django, Node.js or Spring Boot app to diagnose and fix issues. A built-in AI assistant helps with UI navigation, syntax and problem clarity, but won't give the full solution. GS advises using it "as you would on the job" while validating the fix yourself. ([GS guide][gs], via search summaries)
- **Prep sites:** reading an unfamiliar repo, debugging, tests and targeted fixes ([PracHub][ph1], [PracHub][ph2]).
- **Thin:** I found no first-hand description of an actual Diagnostics bug.
- **Default:** each exercise is a small Django project with a ticket-style bug report and a failing test. You find and fix a single realistic logic bug, then run the test suite to confirm. Bug types:
  - ORM filters
  - off-by-one pagination
  - timezones
  - auth and permissions
  - aggregation
  - validation
  - N+1 queries
  - transactions

## 3. Math: 22 min, multiple choice
- **Official:** multiple-choice questions on probability, statistics, calculus and linear algebra. The guide lists this section for Quantitative Strategist candidates, but your invitation includes it, so prepare for it. ([GS guide][gs])
- **Question count:** not published. A 2021 report says the math section had **10 MCQs** ([LeetCode Discuss 2021][lc2], old). The 2023 MCQ topics match the four above ([Naukri 2023][nk1]).
- **Subtopics** from a prep guide ([PracHub][ph1]):
  - conditional probability, independence, expectation and variance
  - discrete distributions and counting
  - matrix rank, determinants, inverses and eigenvalues
- **Default: 10 questions in 22 min (~2 min each).** Weighting: about 50% probability and statistics, 20% calculus, 20% linear algebra and 10% counting.
- No calculator is assumed, so numbers are kept hand-computable.

## Proctoring
Camera on, no outside help, timer can't be paused. Practice under the same conditions: no notes, no LLM, one sitting.

## Disagreements and caveats
- Some 2024-2026 reports describe SHL aptitude tests, HireVue interviews, or 2-hour combined tests. Those are other regions or tracks. Your invitation is the authority.
- Question counts for Fundamentals and Math are inferred from a few anecdotal reports. The trainers make them configurable.
- I could not open goldmansachs.com or prachub.com directly from this environment (network policy). The citations above are based on search-engine extracts of those pages.

## Sources
- [gs]: https://www.goldmansachs.com/careers/blog/guide-to-hackerrank (official)
- [ph1]: https://prachub.com/resources/goldman-sachs-hackerrank-assessment-guide-coding-math-and-what-comes-next
- [ph2]: https://prachub.com/resources/goldman-sachs-core-quantitative-strats-oa-2027-software-diagnostics-math-and-the-97-minute-format
- [prepinsta]: https://prepinsta.com/goldman-sachs/technical-test/coding-questions/
- [gd1]: https://www.glassdoor.it/Colloquio/Goldman-Sachs-Colloquio-E2800-RVW35994958.htm
- [gd2]: https://www.glassdoor.com/Interview/HackerRank-with-math-and-coding-questions-Normal-data-structures-algorithms-dp-probability-calculus-linear-algebra-an-QTN_5573509.htm
- [lc1]: https://leetcode.com/discuss/interview-experience/7289995
- [lc2]: https://leetcode.com/discuss/interview-question/910999/goldman-sachs-engineering-internship-hackerrank-challenge-2021/
- [nk1]: https://www.naukri.com/code360/interview-experiences/goldman-sachs/goldman-sachs-interview-experience-on-campus-jul-2023
- Also seen, low weight: [linkjob.ai](https://www.linkjob.ai/interview-questions/goldman-sachs-hackerrank-test/), [interviewfox.ai](https://interviewfox.ai/interview-questions/goldman-sachs-hackerrank-guide/), [placementpapers.app](https://placementpapers.app/goldman-sachs/interview-experience/)

[gs]: https://www.goldmansachs.com/careers/blog/guide-to-hackerrank
[ph1]: https://prachub.com/resources/goldman-sachs-hackerrank-assessment-guide-coding-math-and-what-comes-next
[ph2]: https://prachub.com/resources/goldman-sachs-core-quantitative-strats-oa-2027-software-diagnostics-math-and-the-97-minute-format
[prepinsta]: https://prepinsta.com/goldman-sachs/technical-test/coding-questions/
[gd1]: https://www.glassdoor.it/Colloquio/Goldman-Sachs-Colloquio-E2800-RVW35994958.htm
[gd2]: https://www.glassdoor.com/Interview/HackerRank-with-math-and-coding-questions-Normal-data-structures-algorithms-dp-probability-calculus-linear-algebra-an-QTN_5573509.htm
[lc1]: https://leetcode.com/discuss/interview-experience/7289995
[lc2]: https://leetcode.com/discuss/interview-question/910999/goldman-sachs-engineering-internship-hackerrank-challenge-2021/
[nk1]: https://www.naukri.com/code360/interview-experiences/goldman-sachs/goldman-sachs-interview-experience-on-campus-jul-2023
