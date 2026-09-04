# Information request — what I need to know to keep building useful tools

**From:** Tim Stranske
**To:** the AI assistant available in this environment, working with me
**Purpose:** The nine tools described in this bundle were built outside this environment on public and synthetic material only. To decide what to build next, and to make what exists work here, I need an accurate picture of what this environment permits and what shape our document collection takes. Please answer the numbered questions below in a single returned document.

---

## Do not include any of the following in your answer

This answer will be read outside this environment. It must contain **no confidential or identifying material of any kind**. Specifically, do not include:

- Manager, fund, firm, client, consultant, vendor or counterparty **names**, or anything that identifies them indirectly.
- Any **content** from a document: no excerpts, quotations, figures, terms, holdings, valuations, fees, positions, or performance numbers.
- **Personal data** about any employee, retiree, member or beneficiary.
- Internal **server names, hostnames, URLs, IP addresses, network shares, database names, user names or account identifiers**.
- Any **credential**: password, key, token, connection string.
- Internal **file paths that reveal system or entity names**. Describe the shape instead, for example "one folder per manager, then a folder per document category".
- Anything covered by a **non-disclosure agreement, confidentiality provision, or legal privilege**.

What I am asking for is the **shape and the limits**: counts as ranges, file formats, yes or no, and field names without values. If a question cannot be answered without crossing the line above, answer it at the level of "yes", "no" or "partly" and describe the constraint generically. **"Unknown" is a perfectly good answer.** Please mark any answer that reflects a policy rather than a technical limit, because policies can be discussed.

---

## A. What can actually run on this computer

1. Which of these can run here: static web pages saved locally, including ones that use WebAssembly; Excel with macros; Word; Office add-ins that show a task pane; Power Query; Power Automate; a Python interpreter of any kind, whether installed, portable or embedded; PowerShell scripts; a downloaded executable or a portable zip; containers or a Linux subsystem.
2. Are there restrictions on downloading a finished tool from a public code-hosting site: file size, file type, or the source itself?
3. When a locally saved web page links to a local document, does the link open the document, or is local-file linking blocked?
4. Is there a way to link directly to a single document in the document system, such that clicking the link opens that document? If yes, describe the shape of the link generically, without a real example.

## B. AI assistance available here

5. Which AI assistants are available, and for each: can it read files, write files, and run code? Are there daily or monthly usage limits I should design around?
6. Is there guidance on which categories of document may be given to an AI assistant? A yes, no or partly per category is enough.

## C. The document collection, described only by shape

7. Roughly how many documents exist in each category, as a range only, choosing from fewer than one hundred, one hundred to one thousand, one thousand to ten thousand, or more than ten thousand: call notes; manager letters and newsletters; data and performance packets; legal documents; consultant reports; research articles; marketing material; regulatory filings and audited statements; questionnaires; internal annual diligence reports and presentations.
8. For each category, which file formats dominate: scanned image PDF, text PDF, Word, Excel, PowerPoint, or email?
9. Does each document carry a stable identifier that stays the same over time, so a tool can record it and later reopen the original? Is there a version or supersession concept when a document is reissued?
10. Is a mirror of these documents on a local drive or a document library permitted? If one exists, is it organized by manager, by category, by date, or some combination? Describe the folder shape without real names.
11. What is known about planned programmatic access to the document system: expected timing, whether it would allow listing and bulk retrieval or only one document at a time, and any rate limits?

## D. The three tools I already built here, described structurally only

12. For the consultant-report comparison tool, the legal-document lineage tool, and the communication synthesis tool: what is each built in, where does it run, and what are its inputs and outputs in shape terms, for example "two documents in, one comparison page and one table of changed sections out"?
13. For each, list the **field names and data types only** of the variables it extracts, with no values. I want to reuse the same names in the tools built outside, so the two sides stay compatible.
14. Which parts of those three are fragile or manual today: rerunning them, updating them when a new version arrives, or sharing the result with a colleague?

## E. Getting results to colleagues

15. How do colleagues receive output today, and are there constraints on interactive web pages in that channel?
16. Is keeping tool source code under version control permitted on this side, and if so where?

## F. Your own read

17. Of the nine tools in this bundle, which do you judge could work here with the least change, and what would block each of the others? Ground your answer in the state column of the cover memo and say which constraint above drives each judgment.

---

**Return format:** one document, numbered answers, no confidential material. If you are unsure whether something crosses the line in the do-not-include list, leave it out and say that you did.
