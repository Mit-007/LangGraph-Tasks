# State Machines & Memory Agent

A conversational AI chatbot built using a **State Machine architecture** that can:

- Answer user questions.
- Detect the user's mood from the current question.
- Maintain chat history across the conversation.
- Generate and update conversation summaries.
- Optimize memory by keeping only the most relevant context.

---

## Project Overview

This agent follows a state-machine workflow where each user message passes through multiple processing stages.

The agent:

1. Validates user input.
2. Maintains current conversation state.
3. Detects the user's current mood.
4. Generates responses using an LLM.
5. Periodically summarizes older conversations.
6. Optimizes memory usage by retaining only relevant information.

This allows the chatbot to handle longer conversations while keeping context size under control.

---

# How To Run

> Recommended: Read the root directory `README.md` first for environment setup instructions.

Open a terminal and navigate to the Task-1 directory:

```bash
cd Task-1
```

Run the application:

```bash
python -m app.main
```

---
# Exit Conversation

To end the current chat session, use either of the following methods:

### Option 1: Type `exit`

```text
👨 User: exit
```

### Option 2: Keyboard Interrupt

Press:

```text
Ctrl + C
```

This will immediately stop the running application and exit the chat session.

note : Once the End a current session the all messages history are removed. 
---

## ⚙️ `core/constant.py`

This file contains configurable constants used across the project.

- **`SUMMARY_COUNTER = 5`**
  - Defines the number of conversation turns after which a new chat summary is generated.
  - **Note:** This value should always be greater than `1`.

- **`MOOD_HISTORY_COUNTER = 10`**
  - Defines the number of conversation turns after which the stored mood history is cleared to optimize memory usage.

---
# State Schema

The entire conversation is managed using the following state object:

```python
class AgentState(TypedDict):
    messages: list[str]
    summary: str
    turn_count: int
    mood: list[Literal["positive", "neutral", "negative"]]
    summary_status : bool
```

## Field Explanation

### `messages`

```python
messages: list[str]
```

Stores the current conversation messages.

Example:

```python
[
    "Hello",
    "Hi! How can I help you?",
    "Who is the Prime Minister of India?"
]
```

---

### `summary`

```python
summary: str
```

Stores the compressed summary of previous conversations.

Instead of sending all old messages to the LLM every time, older messages are summarized and stored here.

Example:

```python
"The user asked about Indian politics, cricket, and world sports."
```

---

### `turn_count`

```python
turn_count: int
```

Tracks the number of valid user interactions.

Only valid user messages increase this count.

Invalid or empty inputs do **not** increment the counter.

Example:

```python
turn_count = 6
```

---

### `mood`

```python
mood: list[Literal["positive", "neutral", "negative"]]
```

Stores the detected mood of each user query.

Possible values:

- positive
- neutral
- negative

Example:

```python
[
    "neutral",
    "neutral",
    "positive",
    "negative"
]
```

---

### `summary_status`

```python
summary_status: bool
```

In summary turn If any reason Summary was not generated , then prevent the messages
If true then deleted messages , if False then summary is not generated that way avoid to delete messages

```python
True
```
---

# Node Explanation

---

## 1. `input_handler`

### Purpose

Validates the user's input before any processing occurs.

### Responsibilities

- Removes unnecessary spaces.
- Checks whether the message is empty.
- Increments the chat turn counter for valid messages.

### Logic

#### Invalid Input

If the user enters:

```text
""
```

or

```text
"     "
```

A `ValueError` is raised.

The conversation state remains unchanged:

- No response generated.
- No summary update.
- No turn count increment.

#### Valid Input

For valid user messages:

```text
"What is AI?"
```

The message is cleaned and:

```python
turn_count += 1
```

Then execution moves to the next node.

---

## 2. Conditional Edge

After `Responder`, the graph decides whether summarization is required.

### Condition

After Every 5(SUMMARY_COUNTER) valid chat turns the graph routes to:

```text
summarizer
```

Otherwise it directly routes to:

```text
responder
```

---

## 3. `summarizer`

### Purpose

Creates a compressed memory of previous conversations.

### Why?

Without summarization:

- Context grows continuously.
- Token usage increases.
- LLM costs increase.

### What It Does

Combines:

- Existing summary
- Recent conversation messages

into a new compact summary.

After summarization, execution moves to:

```text
responder
```

---

## 4. `responder`

### Purpose

Generates the AI response.

### Additional Feature

The node also classifies the user's mood into.

```text
positive
neutral
negative
```
---

## 5. `memory_updater`

### Purpose

Optimizes memory usage after the response is generated.

### Why?

Without cleanup:

- Message history keeps growing.
- Context becomes expensive.
- Performance decreases.

### Memory Optimization Strategy

#### After Every Summary

Old messages are removed because they already exist inside:

```python
state["summary"]
```

Only recent messages are retained.

---

#### Mood History Management

The agent stores mood history.

So Every 10(MOOD_HISTORY_COUNTER) turns:

- Old mood history is cleared.
- A fresh mood tracking cycle begins.

This prevents unlimited growth of mood data.

---

# Edge Flow Explanation

<img width="207" height="531" alt="image" src="https://github.com/user-attachments/assets/40e9899b-fbcd-441f-8b59-3b1bd0278bdc" />

### Flow Summary

#### Normal Turn

```text
START
→ input_handler
→ memory_updater
→ responder
→ END
```

#### Every 5th(SUMMARY_COUNTER) Turn

```text
START
→ input_handler
→ memory_updater
→ responder
→ summarizer
→ END
```

---

# Example Output

## First Turn

```text
👨 User : hii

🤖 AI : Hello there! How can I help you today?

Mood : neutral

Summary : ""

Turn Count : 1
```

---

## Sixth Turn

After five valid chats, a summary becomes available.

```text
👨 User :
i won the cricket match, now I want to post an Instagram story.

🤖 AI :
Cricket match victory!
Feeling on top of the world after that win!

#CricketFever #Victory #WinningMoment

Mood : positive

Summary :
The user asked about the Prime Minister of India,
the FIFA World Cup winner,
the Player of the Match in the final,
and the capital of India.

Turn Count : 6
```

---

## Tenth Turn

The agent now contains mood history.

```text
👨 User :
what is team size in cricket ?

🤖 AI :
A standard cricket team has 11 players.

Mood : neutral

Summary :
The user asked about the Prime Minister of India,
the winner of the FIFA World Cup 2022,
the Player of the Match in the final,
and the capital of India.

Turn Count : 10

Mood List :
[
    'neutral',
    'neutral',
    'neutral',
    'neutral',
    'neutral',
    'positive',
    'neutral',
    'negative',
    'neutral',
    'neutral'
]
```

---
