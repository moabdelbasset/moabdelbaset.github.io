+++
title = 'AI Engineering Reading Notes — Chapter 1: Foundation Models'
date = 2026-09-13T12:00:00+03:00
draft = false
description = 'My notes on language models, tokens, self-supervision, and adapting foundation models from Chapter 1 of AI Engineering by Chip Huyen.'
summary = 'Reading Chapter 1 of AI Engineering: how language models learn, what makes a foundation model useful, and why adapting an existing model is a practical starting point.'
tags = ['Reading Notes', 'AI Engineering', 'Foundation Models']
+++

I started reading *AI Engineering: Building Applications with Foundation Models* by Chip Huyen, published by O'Reilly. I am writing down what I understand as I go, starting with Chapter 1: **Introduction to Building AI Applications with Foundation Models**.

These are my personal reading notes, organized around the ideas that stood out to me. The book and its [companion resources](https://github.com/chiphuyen/aie-book) are the source for this reading series.

## Language models learn patterns in language

A language model encodes statistical information about one or more languages. It learns patterns that help it estimate how likely a piece of text is in a particular context.

For example, given:

> My favourite colour is ____.

A model that has learned English would generally assign a higher probability to **blue** than to **car** in that context.

These predictions are based on probabilities. A likely continuation is not guaranteed to be factually correct.

## Tokens and tokenization

The basic unit a language model works with is a **token**. A token can represent a character, a whole word, or part of a word. Tokens can also represent punctuation and other pieces of text.

The process of turning text into tokens is called **tokenization**. Different models can use different tokenizers, although some models share the same tokenizer. This means the same sentence can be split differently depending on the model.

## Masked and autoregressive language models

Two important approaches to language modeling are masked language modeling and autoregressive language modeling.

| Approach | Training task | Context used |
|---|---|---|
| Masked language modeling | Predict hidden tokens in a sequence | Context before and after the hidden tokens |
| Autoregressive language modeling | Predict the next token in a sequence | The preceding tokens |

A masked language model might receive:

> My favourite [MASK] is blue.

Its task is to predict the missing token using the surrounding text.

An autoregressive language model might receive:

> My favourite colour is

Its task is to predict the next token. Repeating this process allows it to generate longer text, with each new token becoming part of the context for the next prediction.

## Why self-supervision matters

In **supervised learning**, a model learns from examples paired with target labels. One example would be 10,000 photos that people have labeled as either “cat” or “dog.” Creating those labels manually can take a lot of time and money.

With **self-supervised learning**, the training targets come from the data itself. For language modeling, a sentence already contains the tokens the model needs to learn to predict.

For example, we can give the model the beginning of a sentence and use the next token in the original text as the target. We can also hide tokens and use their original values as the targets.

This reduces the need for humans to label each training example and makes it possible to learn from large amounts of text. People still work on collecting, filtering, and preparing that data, and other training stages may use human feedback.

## From language models to foundation models

A **multimodal model** works with more than one type of data, such as text and images. Large models with multimodal capabilities are often called **large multimodal models**, or **LMMs**. Being multimodal and generative does not, by itself, specify a model's size.

A **foundation model** is trained on broad data and can be adapted to many different tasks. What makes it a foundation is the range of applications that can be built on top of it; size alone does not define it.

Foundation models can already perform many tasks out of the box. However, getting useful general behavior is different from getting behavior that fits a particular application.

## Adapting a model to an application

Imagine using a model to write product descriptions for an online store. The descriptions are accurate, but they sound generic and do not match the brand's style.

Three approaches can help adapt the model, each addressing a different need:

| Approach | What changes | Product-description example |
|---|---|---|
| Prompt engineering | The instructions and examples given to the model | Describe the brand's tone and provide sample descriptions |
| Retrieval-augmented generation (RAG) | The relevant information supplied as context | Retrieve product details, brand guidelines, or customer reviews and include them in the input |
| Fine-tuning | The model's parameters through additional training | Train further on examples of descriptions in the desired style |

RAG involves retrieving relevant information and giving it to the model; simply connecting a database is not enough. For the style problem, clearer instructions and examples are a useful starting point. Retrieval helps when the model needs additional information, while fine-tuning can help it learn recurring patterns of behavior. These approaches can also be combined.

One of my biggest takeaways is to **start by adapting an existing model**. A small experiment may need only a few examples and a short amount of time, while training a foundation model from scratch requires substantially more data, compute, and effort. The actual requirements depend on the task and the quality needed.

## What AI engineering involves

In the context of this book, **AI engineering** is the process of building applications on top of foundation models.

The AI stack can be viewed as three layers:

1. **Application development:** using models to build features and applications that solve a user's problem.
2. **Model development:** training, adapting, and evaluating models, supported by development tools.
3. **Infrastructure:** the compute, data systems, serving infrastructure, and monitoring that support the work.

Building the application is one part of a larger system. The model still needs data, infrastructure, and a way to evaluate whether its outputs are useful.

## AI engineering and traditional ML engineering

Three differences stood out in my notes:

- **The starting point:** traditional ML engineering often includes training a model for a specific task. With foundation models, application developers can start with a model someone else has already trained. Reusing pretrained models also exists in traditional ML, so this is a difference in emphasis.
- **Scale and compute:** foundation models are often much larger than models built for narrow tasks. Their resource requirements matter even when another company hosts the model behind an API.
- **Open-ended outputs:** many foundation-model applications generate text or other content with multiple acceptable answers. Evaluating a product description is less straightforward than checking whether a photo was correctly classified as a cat or dog.

The practical idea I want to carry into the next chapters is that choosing a capable model is only the beginning. I also need to understand how to adapt it to the application and judge whether its outputs meet the intended need.
