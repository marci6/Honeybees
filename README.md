# How Bees Can Survive When Disoriented

**MSc AI & Adaptive Systems — University of Sussex, 2020**

> An agent-based model of collective decision-making in honeybee swarms under disorientation — and why a little noise can actually improve group decisions.

---

## The question

When a honeybee colony needs a new home, hundreds of scout bees search independently and recruit others through the **waggle dance** — a behaviour that encodes the direction and quality of a candidate site. But what happens when part of the colony is disoriented and can't dance correctly?

This research introduces a new parameter `β` (proportion of correctly oriented bees) into an established agent-based model of nest-site selection, and tests how robustly the swarm reaches the *best* decision across a range of disorientation scenarios.

---

## Key results

| Finding | Detail |
|---------|--------|
| Decision-making is robust | Colonies reached correct consensus across most disorientation levels |
| Best performance ≠ full orientation | Peak correct choices occurred at β = 0.6 (λ=0.8) and β = 0.2 (λ=0.2) — not at full orientation |
| Low disorientation can help | A partial disorientation shifts consensus toward the best site, improving average outcomes |
| High interdependence amplifies everything | At λ=0.8, correct choices peaked at **97%** (β=0.6); at λ=0.2 the effect was weaker |
| Total disorientation is fatal | At β=0, the colony never reached quorum for the best site |

The most counterintuitive finding: **the best collective decisions were made when part of the colony was disoriented**. The noise introduced by disoriented bees appears to help the swarm sample a wider range of information, avoiding premature convergence on a suboptimal site.

---

## Model design

Built on the agent-based model by List, Elsholtz & Seeley (2009), with one new parameter.

Each bee `i` at time `t` has state vector `x(i,t) = (s, d, o)`:
- `s` — site the bee is currently dancing for (0 = not dancing)
- `d` — remaining dance duration
- `o` — orientation flag (1 = correctly oriented, 0 = disoriented)

Probability of a bee finding nest `j`:

```
p(j,t) = (1 − λ) · π(j) + λ · f(j,t)
```

- `π(j)` — prior probability of finding nest j independently
- `f(j,t)` — proportion of bees *correctly* dancing for j (depends on β)
- `λ` — interdependence weight (how much bees follow each other vs. act independently)

**Quorum definition (conservative):**
1. Nest j has more than twice the support of any other nest
2. Fewer than 80% of bees are inactive

---

## Simulations

- **N = 100** bees, **k = 5** candidate nests, **tmax = 300** time steps
- Nest qualities: 0, 1, 3, 4, 6, 8 — best site is quality 8
- β swept across `{0, 0.2, 0.4, 0.6, 0.8, 1.0}`, each repeated **100 times**
- Two scenarios: high interdependence (λ=0.8) and low interdependence (λ=0.2)

---

## Why this matters beyond bees

The honeybee nest-site problem is a clean model for **decentralised consensus under noisy communication** — and the core finding maps onto many real systems:

**Product & UX** — the quorum mechanism mirrors how social proof drives user decisions. The disorientation result is analogous to how a small amount of friction or randomness can redirect users toward better choices by preventing herd behaviour.

**System design** — distributed systems where all nodes send clean, identical signals can converge on local optima. Controlled noise can improve global outcomes — a principle used in simulated annealing, dropout in neural networks, and epsilon-greedy exploration in RL.

**Organisational behaviour** — teams with partial information and some independent thinkers ("disoriented" from the group view) often outperform fully aligned teams on hard problems. This research gives a formal model for why.

---

## Implementation

- Language: **Python**
- Approach: discrete-time agent-based simulation
- Methodology: parameter sweep + repeated Monte Carlo runs with mean/variance recording

---

## Read the paper

The full paper is included in this repository: [`HOW_BEES_CAN_SURVIVE_WHEN_DISORIENTED.pdf`](./HOW_BEES_CAN_SURVIVE_WHEN_DISORIENTED.pdf)

---

## Context

This project was completed as part of the **MSc in AI and Adaptive Systems** at the University of Sussex (2020). Skills demonstrated:

- Agent-based modelling and simulation design
- Emergent behaviour and collective intelligence
- Parameter sweep experimental design
- Statistical analysis (mean, variance, Monte Carlo)
- Scientific writing and literature synthesis

---

*Marcello Chiesa — [LinkedIn](https://linkedin.com/in/marcellochies) · [GitHub](https://github.com/marci6)*
