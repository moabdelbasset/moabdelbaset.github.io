+++
title = 'AI Engineering Reading Notes — Chapter 3: Evaluation Methodologies'
date = 2026-09-16T00:00:00+03:00
draft = false
description = 'My Chapter 3 notes on evaluation metrics, functional correctness, reference answers, AI judges, and model rankings from AI Engineering by Chip Huyen.'
summary = 'How do we know an AI application is good enough? Notes on measuring predictions, testing outcomes, comparing answers, and evaluating the judges themselves.'
tags = ['Reading Notes', 'AI Engineering', 'Foundation Models']
+++

[Chapter 2](/posts/ai-engineering-reading-notes-chapter-2/) helped me understand what shapes a foundation model's behavior. Chapter 3 raises the next question: **how do we know whether that behavior is good enough?**

These are my personal reading notes from **Chapter 3: Evaluation Methodologies** of *AI Engineering: Building Applications with Foundation Models* by Chip Huyen, published by O'Reilly. I have organized the ideas that stood out to me and added clarifications and supporting references. The author's [companion repository](https://github.com/chiphuyen/aie-book) provides additional reading material.

## Why evaluation is difficult

AI failures have real consequences, so evaluation is part of building an application. A convincing demonstration does not establish that the system will work reliably across the situations users bring to it.

Several challenges stood out in my notes:

- **More capable models can be harder to judge.** Checking a complex answer may require specialist knowledge and considerable time.
- **Outputs are open-ended.** There are many acceptable ways to write an essay or answer a question.
- **Access can be limited.** A hosted model may expose its outputs without revealing its training data, weights, or full token probabilities.
- **Benchmarks need maintenance.** They can become saturated, contaminated by training data, or less representative of the tasks we care about.
- **The scope keeps growing.** An application may need checks for correctness, reliability, cost, latency, and other requirements.

Evaluation can become a substantial part of development. Automating some judgments with AI can help, but then the quality of the judge becomes another thing to evaluate.

## Metrics for predicting text

Four related measures in my notes are **cross-entropy**, **perplexity**, **bits per character (BPC)**, and **bits per byte (BPB)**. These measure predictive performance on text; they are not a complete set of application-quality metrics.

**Entropy** describes average uncertainty or information under a distribution. **Cross-entropy** measures how well a model's predicted distribution fits the observed data. A confidently wrong prediction can have low predictive entropy and high cross-entropy, so the two should not be confused.

For the same evaluated text, let `L` be its total negative log-likelihood in bits, and let `N`, `C`, and `B` be the evaluated token, character, and byte counts:

| Metric | Relationship |
|---|---|
| Cross-entropy in bits per token | `L / N` |
| Perplexity | `2^(L / N)` |
| Bits per character | `L / C` |
| Bits per byte | `L / B` |

These conversions require consistent text, scoring conventions, log units, and counts. One reported number alone is not enough to recover all the others.

Lower cross-entropy or perplexity means better prediction of the evaluation text under comparable conditions. It does not establish factual accuracy or application usefulness. Tokenization also affects comparisons. [Hugging Face's perplexity guide](https://huggingface.co/docs/transformers/perplexity) explains the cross-entropy relationship and tokenization caveat.

## Objective and subjective judgments

Some tasks have a clearly specified correct result. A multiple-choice question with an agreed answer key can be graded automatically. Other tasks involve judgment: two people may grade the same essay differently because they value different qualities.

A rubric helps make subjective criteria explicit. For example, an essay might be judged separately on factual accuracy, clarity, and organization. That is more useful than leaving “good” undefined.

Objective grading and exact string matching are also different ideas. A program can have many valid implementations, all of which pass the same tests.

## Functional correctness: did it do the job?

This is the evaluation question I find easiest to connect to an application:

- Did the website implement the requested behavior?
- Was the reservation actually created with the right details?
- Did the energy-management system achieve the intended savings under the required conditions?

The check should target the outcome. A response saying “your reservation is confirmed” is not proof that a reservation exists.

### Understanding pass@k

For tasks with pass/fail tests, **pass@k** measures the chance that at least one of `k` generated candidates passes, averaged across problems. In a simple experiment, if 5 out of 10 problems have a passing candidate among three attempts each, the observed success rate at three attempts is 50%.

Under the same sampling setup, increasing the attempt budget cannot reduce the probability of at least one success. The relationship is non-strict: `pass@1 ≤ pass@3 ≤ pass@10`; scores can remain equal.

Benchmark implementations often estimate pass@k from a larger pool of samples. It also assumes a way to recognize a passing candidate: generating one somewhere in a batch does not mean the application will select it. The [HumanEval paper](https://arxiv.org/abs/2107.03374) describes this evaluation approach.

Passing tests only establishes success against those tests. Missing requirements or weak test coverage can still hide failures.

## Comparing outputs with reference answers

When a reference answer is available, we can compare the model's output with it in several ways:

| Method | What it checks | Main limitation |
|---|---|---|
| **Exact match** | Whether the output equals the reference, possibly after specified normalization | Can reject valid alternative wording |
| **Lexical similarity** | How much the texts overlap in words or phrases | Similar wording can conceal a different meaning |
| **Semantic similarity** | How closely their meanings align according to a representation or model | Similarity does not prove correctness |

For example, “the reservation was canceled” and “the reservation was not canceled” share nearly all their words while reporting opposite outcomes.

### Where embeddings fit

An **embedding** is a vector—a list of numbers—that represents features of data. Its dimensionality depends on the embedding model. For semantic text embeddings, the aim is to make useful relationships in meaning measurable through distances or similarities between vectors.

“The cat is on the mat” and “a cat is sitting on a mat” would ideally be close under a model intended for paraphrase similarity. A sentence about AI research would generally be less similar. The exact result depends on the model and its training objective.

An embedding score is a useful signal, but details such as negation, numbers, and names may need separate checks.

## Using AI as a judge

An AI judge can evaluate an answer alone, compare it with a reference, or choose between two candidate answers. Pairwise comparisons are also a format used for preference data: human judgments can support RLHF, while AI judgments provide AI feedback.

AI judging can reduce manual effort, but its suitability depends on the task and rubric. It has costs and latency, can be inconsistent, and may favor its own outputs, a particular answer position, or greater verbosity. These issues are documented in [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685).

I would use explicit criteria, compare judgments with human-reviewed examples, and test whether swapping answer order changes the result. Where a reliable functional check exists, it should remain part of the evaluation. An AI judge is a tool to validate for the use case, rather than a universally preferred replacement for other checks.

## Ranking models: pointwise and comparative

**Pointwise evaluation** scores each model's responses independently using a shared rubric, then aggregates those scores. I think of this as giving each dancer a score for their individual performance.

**Comparative evaluation** asks which of two responses is better and combines the results into a ranking. This is like watching dancers side by side. Judges can be people or AI models. Rating methods such as Elo or Bradley–Terry models can turn pairwise outcomes into relative ratings. [The Chatbot Arena paper](https://arxiv.org/abs/2403.04132) describes an approach based on human preferences.

Comparative evaluation can make a decision easier than assigning an absolute score, but it still needs representative prompts and dependable judgments. Gathering enough comparisons becomes more expensive as the model pool grows, and rankings can inherit voters' preferences and biases.

Fresh comparisons can help keep an evaluation relevant, but they do not make it immune to manipulation or guarantee that it will never become stale.

The distinction I want to remember is that **ranking higher does not establish that a model meets my application's requirements**. Both candidates could fail a critical requirement even if one is consistently preferred.

## What I am taking into the next chapter

My main takeaway is to define success before choosing a metric. Predicting text well, passing functional tests, resembling a reference, and winning a preference comparison answer different questions.

For an application, I would start with observable requirements, use direct checks where possible, and add human or AI judgments for qualities that need interpretation. The evaluation should tell me whether the application meets its purpose, as well as how it compares with alternatives.

---

Previous: [Chapter 2 — Understanding Foundation Models](/posts/ai-engineering-reading-notes-chapter-2/)
