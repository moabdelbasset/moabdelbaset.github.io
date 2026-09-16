+++
title = 'AI Engineering Reading Notes — Chapter 2: Understanding Foundation Models'
date = 2026-09-15T10:00:00+03:00
draft = false
description = 'My Chapter 2 notes on training data, attention, model size, post-training, and sampling from AI Engineering by Chip Huyen.'
summary = 'Understanding what shapes a foundation model: the data it learns from, its architecture, how it is trained to answer, and how it selects output tokens.'
tags = ['Reading Notes', 'AI Engineering', 'Foundation Models']
+++

In [Chapter 1](/posts/ai-engineering-reading-notes-chapter-1/), my main takeaway was that building AI applications often starts with adapting an existing foundation model. Chapter 2 helped me understand more of what happens inside that model.

These are my personal notes from **Chapter 2: Understanding Foundation Models** of *AI Engineering: Building Applications with Foundation Models* by Chip Huyen, published by O'Reilly. I have organized my understanding below, with links to supporting sources where useful. The author's [companion repository](https://github.com/chiphuyen/aie-book) has additional material for the book.

## Training data shapes what a model can do

A model's capabilities depend heavily on the data it learns from. More data can help, but relevance, quality, and diversity matter too. Adding more low-quality text does not automatically produce a better model.

**Common Crawl** is an important source of web data, though individual models use different mixtures of sources. It is a nonprofit that maintains a large, open repository of crawled web content. Google's **C4**, short for *Colossal Clean Crawled Corpus*, was built by filtering Common Crawl data for the T5 project. See the [Common Crawl overview](https://commoncrawl.org/overview) and the [T5 paper](https://jmlr.org/papers/volume21/20-074/20-074.pdf).

The challenge is that the web contains spam, duplication, and incorrect information alongside useful content. Filtering is part of building a training dataset.

One example that stood out to me was GPT-2's WebText dataset. It used the content of outbound links from Reddit posts with at least three karma as a signal of quality. The training material was the linked web pages, rather than simply the Reddit posts themselves. This was a filtering heuristic, not a guarantee of correctness. [OpenAI's GPT-2 announcement](https://openai.com/index/better-language-models/) describes the approach.

### Language and domain coverage matter

English makes up a large share of Common Crawl. The exact percentages and language rankings vary between crawls, so I would treat figures such as “46% English” as a snapshot. [Common Crawl's language statistics](https://commoncrawl.github.io/cc-crawl-statistics/plots/languages) track that variation.

My practical takeaway is that strong performance in English does not establish equally strong performance in another language. The model's actual training mixture and the task both matter.

Specialized work can also require specialized datasets. Protein and DNA modeling, for example, needs suitable biological data. Some datasets have restricted access, but others are public: [GenBank](https://www.ncbi.nlm.nih.gov/genbank/) provides publicly available DNA sequences. Specialized does not necessarily mean private.

## From sequence-to-sequence models to attention

Around 2014, recurrent **sequence-to-sequence**, or **seq2seq**, models became an important approach to tasks such as machine translation. An **encoder** processed the input, and a **decoder** generated the output.

In early versions, the encoder had to compress the input into a fixed-length representation. That created a bottleneck, especially for longer sequences. Recurrent processing also limited how much work could happen in parallel.

**Attention** addressed the information bottleneck by letting the decoder use relevant parts of the encoded input while generating its output. I think of it as answering questions about a book while being able to look back at its pages, instead of depending entirely on a short summary. This idea is described in the [Bahdanau, Cho, and Bengio attention paper](https://arxiv.org/abs/1409.0473).

The **Transformer** later made attention central to an architecture without recurrence, allowing more parallel computation during training. Attention and transformers are related, but attention came first. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) introduces the Transformer architecture.

### Queries, keys, and values

The book analogy helps me remember the three kinds of vectors used in transformer attention:

| Vector | How I think about it |
|---|---|
| **Query (Q)** | What information am I looking for at this position? |
| **Key (K)** | What features make another position relevant to that query? |
| **Value (V)** | What information can that position contribute? |

Keys are learned representations, rather than literal page numbers. Attention compares a query with keys to calculate weights, then uses those weights to combine values. In a causal language model, the attention mask prevents a position from looking at future tokens.

### Prefill and decode

For ordinary autoregressive transformer inference, two phases are useful to distinguish:

- **Prefill:** process the input tokens, with computation across their positions parallelized within each layer, and prepare the cached information used during generation.
- **Decode:** generate a new token, then use it when predicting the next one. A key-value cache avoids recomputing the keys and values for previous tokens.

Prefill benefits from parallelism, but a long prompt can still take significant time. Decode is sequential across generated tokens in the basic generation loop. In both cases, the unit is a token, which may be only part of a word.

## Parameter count and memory

More parameters can increase a model's capacity to learn. However, a larger parameter count does not guarantee better results: data, training, architecture, and the task also matter.

Parameter count is still useful for estimating resource requirements. For example, if a model has **7 billion parameters**, stored at **2 bytes each**:

```text
7,000,000,000 parameters × 2 bytes
= 14,000,000,000 bytes
= 14 GB, or about 13 GiB
```

That is the storage needed for the **weights alone** at that precision. Running inference also needs memory for the KV cache, activations, and runtime overhead. Training requires additional memory, such as gradients and optimizer state. Quantization can reduce weight storage.

Sparsity adds another complication. **Weight sparsity** means many parameter values are zero. **Conditional computation**, such as a mixture-of-experts model, means only part of the model is active for a given token; its unused weights do not have to be zero. Total parameters, active parameters, and memory requirements therefore tell different parts of the story.

## Pretraining and post-training

An autoregressive base model is pretrained to predict tokens from preceding context. It can learn a great deal through that objective, but it is not necessarily a reliable conversational assistant. It may continue a question instead of answering it, and it can reproduce undesirable patterns from its training data.

**Post-training** helps shape those capabilities into useful behavior. Supervised fine-tuning and preference optimization are two common parts of that process, though they are not a mandatory two-step recipe and do not fix every problem.

### Supervised fine-tuning: examples of useful answers

**Supervised fine-tuning (SFT)** trains the model on examples of the behavior we want, such as a question paired with a good answer or a conversation with useful assistant responses.

Writing strong examples can require substantial time and expertise. Human-written examples are one source; datasets can also include synthetic or mixed-origin examples.

SFT can still use a token-level prediction loss. What changes is the training material: the model learns from demonstrations of desired responses rather than only broad pretraining text.

### Preference optimization: comparing answers

Preference data captures which response is preferred for a given prompt. Comparing answer A with answer B can be easier than assigning a consistent absolute score, although people can still disagree.

| Approach | What happens |
|---|---|
| **RLHF** | In a common pipeline, human comparisons train a reward model, then reinforcement learning updates the language model using that reward signal |
| **DPO** | Direct Preference Optimization trains on preferred and rejected responses without a separate reward-model training stage or an RL rollout loop |
| **RLAIF** | Reinforcement Learning from AI Feedback uses AI-generated feedback as a source of supervision |

The distinction between the first two approaches is explained in the [DPO paper](https://arxiv.org/abs/2305.18290).

**Best-of-N** is different: generate several candidate answers and use a scorer to select one. Selection alone does not update the language model's parameters, so it is not itself fine-tuning.

My takeaway is that pretraining develops broad predictive capabilities, while post-training shapes how those capabilities are used. Better preference scores do not guarantee factual accuracy.

## How probabilities become an answer

At each generation step, a typical language model produces **logits**: scores for the tokens in its vocabulary. **Softmax** converts scores into probabilities. A decoding strategy then selects the next token, and the process repeats.

The model produces scores; the generation process turns them into an answer. Two basic choices are **greedy decoding**, which always selects the highest-scoring token, and **sampling**, which selects randomly according to the probability distribution.

### Controls for token selection

| Control | Effect |
|---|---|
| **Temperature** | Rescales logits: lower positive values concentrate probability; higher values flatten it and increase randomness |
| **Top-k** | Keeps the k highest-scoring candidates and samples from their renormalized distribution |
| **Top-p (nucleus sampling)** | Keeps the smallest set of highest-probability tokens whose cumulative probability reaches or exceeds p, then renormalizes and samples |
| **Stopping conditions** | End generation at an output-token limit, an end-of-sequence token, or a configured stop sequence |

Temperature zero is commonly implemented as greedy decoding; it is not literal division by zero. Higher temperature adds randomness, which is not the same as useful creativity or correctness.

Top-k mainly restricts candidates. It does not generally avoid computing vocabulary-wide logits. Top-p adapts the candidate count to the distribution. [Hugging Face's decoding guide](https://huggingface.co/blog/how-to-generate) explains these strategies.

## What I am taking into the next chapter

I now have more questions to ask when looking at a model: what data did it learn from, what does its parameter count actually tell me, how was it post-trained, and how are its output tokens selected?

Those details help explain why two models—or two configurations of the same model—can behave differently. They also make it clearer why choosing a model requires more than comparing its size.

---

Previous: [Chapter 1 — Foundation Models](/posts/ai-engineering-reading-notes-chapter-1/)

Next: [Chapter 3 — Evaluation Methodologies](/posts/ai-engineering-reading-notes-chapter-3/)
