# AI 에이전트 하네스 엔지니어링 — 큐레이션 리서치 보고서

> **조사 기간** 2024-12 ~ 2026-04 발행물 위주
> **출처 수** 33건 (YouTube 8 · 엔지니어링 블로그 10 · LinkedIn 7 · Hacker News 8)
> **수집 방식** 4개 리서치 서브에이전트(소스 타입별) 병렬 수집 → 메인 세션 통합

---

## TL;DR

**"같은 LLM이라도 하네스(harness) 설계에 따라 동일 벤치마크에서 최대 6배 성능 차이가 난다."** 2025년 후반부터 AI 엔지니어링의 무게중심이 *모델* 자체에서 *모델을 둘러싼 오케스트레이션 레이어* — 즉 하네스 — 로 옮겨갔다. 본 보고서는 이 흐름을 만든 1차 자료(Anthropic·OpenAI·Cognition 엔지니어링 블로그, Boris Cherny·Mike Krieger·Barry Zhang·Walden Yan 등의 강연, Karpathy·Harrison Chase·Chip Huyen 등의 LinkedIn·HN 토론)를 큐레이션한다. 핵심 논쟁은 두 갈래다 — (1) 단일 에이전트 vs 멀티 에이전트, (2) 컨텍스트 엔지니어링의 정의와 한계. 합의된 원칙은 한 줄로 요약된다 — **루프는 단순하게, 컨텍스트는 작고 정교하게, 툴은 결정론↔비결정론 계약처럼 설계할 것.**

---

## 1. 핵심 개념 정리

### 1.1 하네스(harness)란?

**LLM 위에 얹어 에이전트로 동작시키는 모든 오케스트레이션 스캐폴딩.** 구체적으로는 다음을 포함한다 ([블로그 #1, #10], [영상 #3]).

- **Agent loop** — `plan → tool call → observe → repeat` 의 반복 루프
- **Tool registry** — 모델이 호출 가능한 도구 정의·라우팅·실행
- **Context/memory** — 시스템 프롬프트, 메시지 히스토리, 외부 메모리, 압축 전략
- **Sub-agent orchestration** — 자식 에이전트 호출과 결과 요약 인계
- **Sandboxing & permissions** — 실행 권한, 파일시스템 격리, 사용자 승인 흐름
- **Recovery / hooks** — 실패·재시도, 정책 강제, 가드레일

### 1.2 Framework / Runtime / Harness — 용어 구분

LangChain CEO Harrison Chase가 제시한 분류 ([LinkedIn #5]).

| 레이어 | 정의 | 비유 (웹) | 예시 |
|---|---|---|---|
| Framework | 기반 추상화 | Express | LangChain |
| Runtime | 실행 상태·내구성·흐름 제어 | Node.js | LangGraph |
| Harness | 특정 use case에 최적화된 opinionated 레이어 | Next.js | DeepAgents · Claude Code |

### 1.3 Inner harness vs Outer harness

Mario Zechner가 도입하고 HN에서 정착된 구분 ([HN #1]).

- **Inner harness** — 모델 제공자(Anthropic·OpenAI 등)가 책임지는 부분: 툴 콜 포맷, 추론 전략, 컨텍스트 관리 기본기
- **Outer harness** — 사용자가 엔지니어링하는 부분: 파일시스템 레이아웃, `CLAUDE.md`·`AGENTS.md`, 서브에이전트, 훅, MCP 서버 구성

> **시사점** — Inner harness는 모델 사이클에 따라 빠르게 흡수되지만, outer harness는 도메인 지식이 녹아 있어 사용자에게 남는 자산이 된다.

### 1.4 "에이전트는 무엇으로 이루어지는가" — 표준 분해

Barry Zhang(Anthropic) 정의 ([영상 #8]) · Erik Schluntz/Barry Zhang ([블로그 #10])

> **An agent is a model in a loop, with tools and memory.**
> 핵심 컴포넌트 3가지: **environment · tools · system prompt**

Chip Huyen은 메모리를 **core / episodic / semantic / procedural** 4 버킷으로 더 분해할 것을 제안 ([LinkedIn #7]).

---

## 2. 핵심 논쟁과 합의된 원칙

### 2.1 "모델보다 하네스" — 강한 명제

복수의 자료가 교차 검증한다.

- Stanford/MIT의 *Meta-Harness* 논문: **동일 LLM에 다른 하네스 → 최대 6× 성능 차이**, Terminal-Bench 2 pass@1 69.7% → 77.0% ([LinkedIn #1])
- Can.ac의 hashline 실험: **15개 LLM의 코딩 점수가 diff 포맷(하네스 일부)만 바꿔도 크게 출렁임** ([HN #3])
- Karpathy의 AutoResearch 리포지토리: **코드의 98.4%가 모델 가중치가 아닌 하네스** ([LinkedIn #3])
- Addy Osmani: *"A decent model with a great harness beats a great model with a bad harness."* ([블로그 #1])
- Mario Zechner (HN 1위 댓글): *"If the harness can make as much of a difference as the model itself, they have to be considered equally important."* ([HN #1])

### 2.2 단일 에이전트 vs 멀티 에이전트 — 정면 충돌

같은 시기(2025-06)에 두 입장이 정면으로 부딪쳤다.

| 입장 | 출처 | 핵심 주장 |
|---|---|---|
| **멀티 에이전트 추천** | Anthropic *"How we built our multi-agent research system"* ([블로그 #8]) | Opus 4 lead + Sonnet 4 sub-agents 구성이 단일 에이전트 대비 **+90%** 성능, 다만 **15× 토큰** 비용 |
| **멀티 에이전트 비추** | Cognition *"Don't Build Multi-Agents"* ([블로그 #9]) | 컨텍스트 분리 → 서브에이전트 간 implicit 결정 충돌 (Mario 배경 + 게임 외 자산 새 사례) |

**현장 합의** (HN #5, [LinkedIn #5]): **태스크의 본질에 따라 다르다.** 병렬 탐색이 가치 있는 리서치형 작업은 멀티가 유리, 일관된 코드 작성은 단일이 더 견고. Cognition도 Devin 2.0에서 결국 long-horizon 멀티 에이전트 오케스트레이션을 도입 ([영상 #6]). 이후 Cognition은 후속 글 *Multi-Agents: What's Actually Working* (<https://cognition.ai/blog/multi-agents-working>)에서 **"여러 에이전트가 지능을 기여하되 쓰기는 단일 스레드"** 패턴이 실전에서 작동한다고 입장을 정교화함.

### 2.3 컨텍스트 엔지니어링 — 새로운 1순위 스킬

Anthropic이 2025-09 공식적으로 정의 ([블로그 #4]).

> *"Context engineering is the art and science of curating what will go into the limited context window from a constantly evolving universe of possible information."*

Walden Yan(Cognition) — *"Context engineering is more durable than prompt engineering — assume the model gets smarter, and your job is to keep handing it the right context."* ([블로그 #6])

**4가지 기본 동작** ([HN #4] 합의):
1. **Offload** — 영구 정보를 컨텍스트 밖으로
2. **Retrieve dynamically** — 사전 적재 대신 필요 시 가져오기
3. **Isolate sub-tasks** — 서브에이전트로 격리
4. **Reduce history** — 신호는 보존하면서 압축

### 2.4 Long-horizon agents — 컨텍스트 윈도우를 넘기

Anthropic의 *Effective harnesses for long-running agents* ([블로그 #2])는 한 줄로 요약된다 — *"Each new session begins with no memory of what came before — the harness's job is to leave structured artifacts so the next agent starts already oriented."* 구체 패턴은 (1) **initializer agent + coding agent** 2단 구조, (2) `init.sh` · `claude-progress.txt` 같은 **외부 아티팩트로 상태 인계**, (3) **초기 git commit으로 작업 베이스 고정**.

OpenAI Frontier 팀(Ryan Lopopolo)은 같은 문제를 더 극단으로 밀어붙임 — **1M LOC 코드베이스를 일일 1B 토큰, 0% human code/review로 운영** ([영상 #5]). 병목은 모델 품질이 아니라 *harness reliability* 임을 강조.

### 2.5 Programmatic tool calling — 새 패러다임

Sonnet 4.6에서 도입된 **모델이 JSON 대신 코드를 작성해 도구를 호출**하는 방식이 하네스 설계의 다음 변곡점으로 지목됨 ([영상 #1]). 한 번의 모델 턴에서 여러 툴 호출과 변환 로직을 코드로 묶을 수 있어 *tool-loop overhead* 가 줄어든다.

---

## 3. 출처별 큐레이션 (newest-first)

### 3.1 YouTube 영상

- **Anthropic Just Killed Tool Calling (Programmatic Tool Calling on Sonnet 4.6)** — YouTube technical breakdown (2026-02)
  URL: <https://www.youtube.com/watch?v=8dVCSPXG6Mw>
  요약 — Sonnet 4.6의 programmatic tool calling을 분석하며, 에이전트가 JSON 대신 코드를 작성해 도구를 호출하는 방식이 하네스 설계와 컨텍스트 효율에 미치는 영향을 짚는다.
  핵심 — *"Letting the agent write code to invoke tools collapses the tool-loop overhead and reshapes how harnesses orchestrate observations."*

- **Inside Claude Code With Its Creator Boris Cherny** — Y Combinator / Lightcone Podcast (2026-02)
  URL: <https://www.youtube.com/watch?v=PQU9o_5rHC4>
  요약 — Claude Code 창시자 Boris Cherny가 터미널 기반 에이전트 하네스의 설계 철학, 단순한 agent loop 유지의 중요성, 그리고 sub-agent 활용 사례를 직접 풀어낸다.
  핵심 — *"Keep the harness dumb so the model can stay smart — resist the urge to over-scaffold the agent loop."*

- **Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic** — AI Engineer (2026-01)
  URL: <https://www.youtube.com/watch?v=TqC1qOfiVcQ>
  요약 — Claude Agent SDK(구 Claude Code SDK)로 agent loop, bash 도구, context engineering, sub-agent를 구성하는 2시간 실습 워크샵.
  핵심 — *"An agent is just a model in a loop with tools and memory — everything else is harness craftsmanship."*

- **Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI** — AI Engineer Europe Keynote (2026-01)
  URL: <https://www.youtube.com/watch?v=am_oeAoUhew>
  요약 — OpenAI Frontier 팀에서 100% 에이전트로 1M LOC 코드베이스를 운영한 경험을 바탕으로 autonomy scoping · context shaping · verification loop · tool access 등 하네스 설계 패턴 정리.
  핵심 — *"The engineering work is no longer writing the code — it's designing the harness that makes agents do the work safely and repeatedly."*

- **Extreme Harness Engineering for Token Billionaires: 1M LOC, 1B toks/day, 0% human code or review — Ryan Lopopolo, OpenAI** — Latent Space (2026-01)
  URL: <https://www.youtube.com/watch?v=CeOXx-XTYek>
  요약 — OpenAI의 Codex 기반 하네스가 일일 10억 토큰 규모로 100% 무인 작성·무인 리뷰 코드베이스를 운영하는 실전 사례. eval·feedback loop 구조를 깊이 다룸.
  핵심 — *"0% human code, 0% human review — the bottleneck is no longer model quality but harness reliability."*

- **Devin 2.0 and the Future of SWE — Scott Wu, Cognition** — AI Engineer World's Fair (2025-07)
  URL: <https://www.youtube.com/watch?v=MI83buT_23o>
  요약 — Cognition CEO가 Devin 2.0의 멀티 에이전트 오케스트레이션, 장기 실행 작업, planning·memory 구조 변화를 설명.
  핵심 — *"Long-horizon agents need a harness that treats planning, memory, and verification as first-class citizens, not afterthoughts."*

- **Claude Sonnet 4.5 and Anthropic's roadmap for Agents and Developers — Mike Krieger, Anthropic** — AI Engineer (2025-09)
  URL: <https://www.youtube.com/watch?v=aJxnel2_O7Q>
  요약 — Anthropic CPO Mike Krieger가 Sonnet 4.5와 함께 long-running agent · context management · tool-use 인프라 로드맵을 발표.
  핵심 — *"Models keep getting better at running longer — the harness must evolve to manage hours-long context and recovery, not just turns."*

- **How We Build Effective Agents — Barry Zhang, Anthropic** — AI Engineer Summit 2025 (2025-02)
  URL: <https://www.youtube.com/watch?v=D7_ipDqhtwk>
  요약 — Anthropic Applied AI 팀이 정리한 production agent harness 설계 원칙. agent vs workflow 분류, environment·tools·system prompt 3대 컴포넌트.
  핵심 — *"Don't build agents for everything, keep it simple, and think like your agents."*

### 3.2 엔지니어링 블로그·아티클

- **Agent Harness Engineering** — Addy Osmani (2026-04)
  URL: <https://addyosmani.com/blog/agent-harness-engineering/>
  요약 — 코딩 에이전트 = 모델 + 그를 둘러싼 모든 것이라는 관점에서, 프롬프트·툴·컨텍스트 정책·후크·샌드박스·서브에이전트·복구 경로를 하나의 하네스로 보고, 에이전트가 실수할 때마다 그 실수를 영원히 막도록 하네스를 단단히 조이는 엔지니어링 기법을 설명.
  핵심 — *"A decent model with a great harness beats a great model with a bad harness."*

- **Effective harnesses for long-running agents** — Anthropic Engineering (2025-11)
  URL: <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
  요약 — Claude Agent SDK를 여러 컨텍스트 윈도우에 걸쳐 구동하기 위한 initializer/coding 두 단계 구조와 `init.sh`, `claude-progress.txt`, 초기 git commit 같은 구조적 아티팩트 도입 사례 연구.
  핵심 — *"Each new session begins with no memory of what came before — the harness's job is to leave structured artifacts."*

- **Designing agentic loops** — Simon Willison (2025-09)
  URL: <https://simonwillison.net/2025/Sep/30/designing-agentic-loops/>
  요약 — 코딩 에이전트의 실력을 끌어올리는 새 스킬은 "명확한 목표 + 그 목표로 수렴하는 도구 집합"을 루프로 묶는 *agentic loop 설계*임을 주장.
  핵심 — *"If you can reduce your problem to a clear goal and a set of tools that can iterate towards that goal, a coding agent can often brute force its way to a solution."*

- **Effective context engineering for AI agents** — Anthropic Engineering (2025-09)
  URL: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
  요약 — 프롬프트 엔지니어링의 진화로서 *컨텍스트 엔지니어링*을 정의. 시스템 프롬프트·툴·MCP·메시지 히스토리 전체 상태를 멀티턴·장기 환경에서 큐레이션하는 방법.
  핵심 — *"Context engineering is the art and science of curating what will go into the limited context window from a constantly evolving universe of possible information."*

- **Writing effective tools for AI agents — with agents** — Anthropic Engineering (2025-09)
  URL: <https://www.anthropic.com/engineering/writing-tools-for-agents>
  요약 — 에이전트용 툴은 결정론적 시스템과 비결정론적 에이전트 사이의 계약이라는 관점에서, 평가 기반 반복 설계와 Claude를 활용한 툴 자동 최적화 방법.
  핵심 — *"Tools represent a contract between deterministic systems and non-deterministic agents — design them for agents, not for other developers."*

- **Why Cognition does not use multi-agent systems (notes from Walden Yan)** — Jason Liu / jxnl.co (2025-09)
  URL: <https://jxnl.co/writing/2025/09/11/why-cognition-does-not-use-multi-agent-systems/>
  요약 — Cognition CPO Walden Yan과의 대화를 정리. "프롬프트 엔지니어링 → 컨텍스트 엔지니어링" 패러다임 이동과, 코딩 도메인에서 단일 에이전트 + 강한 컨텍스트 관리가 멀티에이전트보다 우월한 이유.
  핵심 — *"Context engineering is more durable than prompt engineering — assume the model gets smarter, and your job is to keep handing it the right context."*

- **How we built our multi-agent research system** — Anthropic Engineering (2025-06)
  URL: <https://www.anthropic.com/engineering/multi-agent-research-system>
  요약 — Claude의 Research 기능을 만들면서 채택한 orchestrator-worker 패턴, LeadResearcher와 병렬 서브에이전트, CitationAgent 같은 구성 요소와 서브에이전트 폭주·과한 토큰 사용 같은 실패 사례 및 해결책.
  핵심 — *"Claude Opus 4 lead + Sonnet 4 subagents outperformed a single-agent setup by more than 90% — but multi-agent systems use ~15× more tokens."*

- **Don't Build Multi-Agents** — Walden Yan / Cognition AI (2025-06)
  URL: <https://cognition.ai/blog/dont-build-multi-agents>
  요약 — 컨텍스트가 분산된 멀티에이전트 시스템은 서로의 implicit 결정과 충돌해 fragile해진다는 주장과, "공유 컨텍스트", "행동은 암묵적 결정을 동반한다" 등 단일 스레드 에이전트 원칙.
  핵심 — *"Sub-agents that don't share full context will make conflicting implicit decisions — single-threaded linear agents get you surprisingly far in reliability."*

- **12-Factor Agents: Patterns of reliable LLM applications** — Dex Horthy / HumanLayer (2025-04)
  URL: <https://github.com/humanlayer/12-factor-agents>
  요약 — Heroku의 12-Factor App을 본떠 자연어→툴 호출 변환, 프롬프트 소유, 컨텍스트 윈도우 관리, 상태 통합, 인간 개입, 정적 reducer 패턴 등 프로덕션 LLM 앱 12원칙.
  핵심 — *"Most 'AI agents' that succeed in production aren't magical autonomous beings — they're well-engineered traditional software with LLM capabilities sprinkled in at key points."*

- **Building effective agents** — Erik Schluntz & Barry Zhang / Anthropic (2024-12)
  URL: <https://www.anthropic.com/research/building-effective-agents>
  요약 — 수십 팀과의 작업을 토대로 워크플로(미리 정해진 코드 경로)와 에이전트(LLM이 스스로 프로세스·툴 사용 통제)를 구분. 복잡한 프레임워크 대신 단순·합성 가능 패턴을 권장.
  핵심 — *"The most successful implementations weren't using complex frameworks — they were building with simple, composable patterns."*

### 3.3 LinkedIn 게시물

> 인증 벽으로 본문 전체 확인이 제한되어 검색 미리보기·외부 인용 기반 요약.

- **Agentic Harness Engineering // Pay attention to this one, AI engineers** — Elvis Saravia, Co-Founder DAIR.AI (2026-01)
  URL: <https://www.linkedin.com/posts/omarsar_agentic-harness-engineering-pay-attention-activity-7455257883274985473-bPWk>
  요약 — Stanford/MIT의 Meta-Harness 논문 소개. 동일 LLM이라도 하네스 설계에 따라 최대 6× 성능 차이. 구성요소를 revertible 파일로, 경험을 trajectory 토큰의 압축 증거로, 결정을 검증 가능한 예측으로 분리한 3-layer 프레임워크가 Terminal-Bench 2 pass@1을 69.7→77.0%로 견인.
  핵심 — *"Changing the harness around a fixed LLM can produce a 6x performance gap — what if we automated harness engineering itself?"*

- **What is an agent harness and why do you need one?** — Hugo Bowne-Anderson, Independent Data/AI Scientist (2025-12)
  URL: <https://www.linkedin.com/posts/hugo-bowne-anderson-045939a5_what-is-an-agent-harness-and-why-do-you-need-activity-7433212288045686785-0fsu>
  요약 — agent harness를 모델과 환경(도구·메모리·지시) 사이를 잇는 인프라 레이어로 정의. 문제 영역에 맞춰진 하네스가 효과적인 에이전트의 핵심 조건이라고 주장.
  핵심 — *"Effective agents are built on harnesses tailored to specific problem spaces — not on bigger models alone."*

- **Karpathy's AGENTS.md: Harness Engineering for AI** — Marc Oakes, Karpathy(ex-OpenAI/Tesla AI) 인용 (2025-12)
  URL: <https://www.linkedin.com/posts/marc-oakes-655979a_github-karpathyautoresearch-ai-agents-activity-7436368481740095488-rNFv>
  요약 — Karpathy의 AutoResearch 리포(AGENTS.md)를 분석해 코드의 98.4%가 모델 가중치가 아닌 하네스(권한·컨텍스트·툴 라우팅·observation 기록)임을 보임.
  핵심 — *"98.4% of the codebase is harness... It is everything between the model's output and a production action."*

- **Building Custom Agent Harnesses with LangChain Middleware** — Sydney Runkle, LangChain Engineer (2025-11)
  URL: <https://www.linkedin.com/posts/sydney-runkle_how-middleware-lets-you-customize-your-agent-activity-7443322676066029568-GzOK>
  요약 — LangChain agent middleware로 agent loop의 어느 단계든 hooking해 컨텍스트 주입·정책 강제·가드레일 추가로 커스텀 하네스 구축. tool-call limit, model fallback 등 미들웨어 시리즈 소개.
  핵심 — *"Middleware lets you hook into any step of the agent loop to inject context, enforce policies, or add guardrails."*

- **Agent Framework vs Runtime vs Harness** — Harrison Chase, LangChain Co-founder/CEO (2025-11)
  URL: <https://www.linkedin.com/posts/harrison-chase-961287118_agent-framework-vs-runtime-vs-harness-activity-7387885717261078529-_Mn_>
  요약 — 세 용어를 명확히 구분: framework(추상화) · runtime(실행 상태/durable flow) · harness(특정 use case 맞춤 opinionated 레이어). Node/Express/Next.js 비유로 직관 제공.
  핵심 — *"Node is the runtime, Express is the framework, Next.js is the harness — same pattern applies to agents."*

- **Effective context engineering for AI agents** — Anthropic 공식 페이지 (2025-09)
  URL: <https://www.linkedin.com/posts/anthropicresearch_new-on-the-anthropic-engineering-blog-most-activity-7378864157699244033-Y9U6>
  요약 — 컨텍스트 윈도우를 attention budget으로 보고 시스템 프롬프트·툴·메모리·서브에이전트가 협력해야 한다는 원칙을 발신.
  핵심 — *"What configuration of context is most likely to generate our model's desired behavior?"*

- **Agents (book excerpt)** — Chip Huyen, AI Researcher / *AI Engineering* 저자 (2025-01)
  URL: <https://www.linkedin.com/posts/chiphuyen_agents-activity-7282446481947598850-SyWh>
  요약 — 에이전트 설계의 이론 프레임 부재 속에서 도구 사용·지식 증강·계획·reflection·에러 정정·tool selection을 체계화. 메모리를 core·episodic·semantic·procedural 4 버킷으로 분해. Devin류의 "단일 에이전트 + tight feedback loop"를 단순 multi-agent보다 우선해야 한다고 주장.
  핵심 — *"Memory isn't just more vectors — unpack it into core, episodic, semantic, and procedural buckets, then design the loop around them."*

### 3.4 커뮤니티 토론 — Hacker News

> Reddit은 WebFetch 차단으로 검증 가능한 고-engagement 스레드 확보 실패. HN 8건으로 대체 (전부 100+ 댓글, 직접 토픽 일치).

- **Harnesses Explained: The Inner and Outer Workings of the Coding Agent Harness** — HN, ~150+ comments (2026-04)
  URL: <https://news.ycombinator.com/item?id=47885131>
  요약 — Mario Zechner(pi 하니스 제작자) 글에 대한 토론. *inner harness*(모델/툴 콜 형식) vs *outer harness*(파일시스템·CLAUDE.md·서브에이전트·훅) 분리 관점이 정착되는 계기.
  핵심 — *"If the harness can make as much of a difference as the model itself, they have to be considered equally important."*

- **Improving 15 LLMs at Coding in One Afternoon. Only the Harness Changed** — HN, 200+ comments (2026-02)
  URL: <https://news.ycombinator.com/item?id=46988596>
  요약 — Can.ac의 hashline diff 포맷 실험. 모델이 아니라 하네스(특히 코드 편집 포맷)만 바꿔도 15개 LLM 코딩 점수가 크게 출렁임. Aider 벤치 인용 다수.
  핵심 — *"The framing 'which model is best at coding' is increasingly misleading — in reality the bottleneck is the harness."*

- **Effective harnesses for long-running agents (Anthropic)** — HN, 100+ comments (2025-11)
  URL: <https://news.ycombinator.com/item?id=46081704>
  요약 — Anthropic 글에 대한 토론. initializer + coding 2단 구조와 `claude-progress.txt` 같은 외부 아티팩트로 상태 인계하는 패턴.
  핵심 — *"The remaining 30% of agent reliability is the killer — multi-agent judge setups can balloon to several hundred dollars per run."*

- **Effective context engineering for AI agents (Anthropic)** — HN, 200+ comments (2025-10)
  URL: <https://news.ycombinator.com/item?id=45418251>
  요약 — MCP 서버의 컨텍스트 비용 평가, 시스템 프롬프트 압축, 툴 디스크립션 다이어트, 동적 RAG vs 사전 적재 등 실전 트레이드오프.
  핵심 — *"Good context engineering = smallest set of high-signal tokens; the four moves are offload, retrieve dynamically, isolate sub-tasks, and reduce history."*

- **Don't Build Multi-Agents (Cognition)** — HN, 300+ comments (2025-09)
  URL: <https://news.ycombinator.com/item?id=45096962>
  요약 — Cognition 주장에 대한 격렬한 토론. Anthropic 멀티에이전트 글과 정면 충돌. 컨텍스트 공유 부재로 인한 서브에이전트 의사결정 충돌(Flappy Bird 사례)이 핵심 논점.
  핵심 — *"One builds a Mario background while another builds a non-game-asset bird — shared continuous context beats parallelism for almost every real product task."*

- **What makes Claude Code so damn good** — HN, 400+ comments (2025-08)
  URL: <https://news.ycombinator.com/item?id=44998295>
  요약 — Claude Code의 단일 마스터 루프(nO), 전용 Read/Edit/Grep/Glob 툴, TodoWrite, plan mode, 서브에이전트 위임 등 디자인 선택 분석. "하네스가 좋아서지 모델만의 마법 아니다"가 합의.
  핵심 — *"Claude Code's heart is a classic agent loop with disciplined tools — constraint, not cleverness, is what produces controllable autonomy."*

- **Claude Code: An Agentic Cleanroom Analysis** — HN, 200+ comments (2025-06)
  URL: <https://news.ycombinator.com/item?id=44153053>
  요약 — Claude Code 동작을 외부에서 역분석한 글. 시스템 프롬프트 길이, 툴 스키마 설계, 권한 모델, 단일 메시지 히스토리, 서브에이전트 결과 인계 방식 등 구체 구현에 대한 활발한 토론.
  핵심 — *"All the file reads, search results, and exploratory tool calls stay inside the child context and never pollute the main thread."*

- **The unreasonable effectiveness of an LLM agent loop with tool use** — HN, 300+ comments (2025-05)
  URL: <https://news.ycombinator.com/item?id=43998472>
  요약 — 단순 while-loop + tool calling만으로도 코딩·리서치·운영이 놀랍도록 잘 굴러간다는 주장. Claude Code · Cursor · Cline · Aider · Codex가 사실상 동일 루프 구조 공유. 마지막 10% 신뢰성을 짜내는 게 진짜 어려운 부분.
  핵심 — *"It's astonishing how well a loop with an LLM that can call tools works — that single pattern explains the entire current generation of coding agents."*

---

## 4. 종합 인사이트 — 행동 가능한 교훈

| # | 교훈 | 근거 |
|---|---|---|
| 1 | **하네스를 1차 자산으로 취급하라.** 모델은 6개월마다 바뀌지만 outer harness(도메인 지식)는 누적된다. | LinkedIn #1, #3 · HN #1, #3 · 블로그 #1 |
| 2 | **루프는 단순하게.** 복잡한 프레임워크보다 합성 가능한 단순 패턴이 프로덕션에서 이긴다. | 블로그 #10 · 영상 #2, #8 · HN #8 |
| 3 | **컨텍스트 엔지니어링 = 가장 ROI 높은 스킬.** "어떤 토큰 조합이 원하는 행동을 유도하는가?" 라는 질문을 1순위로. | 블로그 #4, #6 · LinkedIn #6 · HN #4 |
| 4 | **멀티 에이전트는 비용/가치를 계산하고 들어가라.** 15× 토큰 ↔ +90% 성능. 리서치형은 ✓, 일관성 필요 작업은 단일이 안전. | 블로그 #8 vs #9 · HN #5 · 영상 #6 |
| 5 | **Long-horizon은 외부 아티팩트로 푼다.** 컨텍스트 윈도우는 휘발성 — 파일·git commit·progress 노트로 상태를 인계. | 블로그 #2 · HN #3 · 영상 #5 |
| 6 | **툴은 결정론↔비결정론 계약처럼 설계.** 평가 기반 반복으로 툴 디스크립션·스키마를 다듬어라. | 블로그 #5 · LinkedIn #4 |
| 7 | **메모리를 4 버킷으로 분해.** core / episodic / semantic / procedural — 그 위에서 루프를 짠다. | LinkedIn #7 |
| 8 | **에이전트가 실수할 때마다 하네스를 조여라.** 사고가 곧 회귀 테스트, 하네스가 곧 가드레일. | 블로그 #1 |

---

## 5. 한계 및 추가 권장 리서치

- **Reddit 미커버** — WebFetch에서 403이 떨어져 검증 가능한 Reddit 스레드를 확보하지 못함. 필요 시 Reddit API / pushshift로 r/LocalLLaMA · r/ClaudeAI · r/cursor · r/MachineLearning을 시간 윈도우 + min-comments 필터로 별도 수집 권장.
- **LinkedIn 본문 부분 확인** — 인증 벽으로 본문 전체 확인은 제한적. 인용은 검색 미리보기 + 외부 인용 교차검증 기반.
- **학술 자료 미포함** — Stanford/MIT *Meta-Harness* 같은 핵심 논문은 LinkedIn 인용으로만 다룸. 후속 작업으로 arXiv·ACL Anthology 검색 추가 가능.
- **국문 자료 미포함** — 의도적으로 1차 영문 자료 위주 큐레이션. 국내 사례(Naver / Kakao / Upstage / 41 등)가 필요하면 별도 라운드 권장.

---

## 부록 · 전체 출처 빠른 참조

| # | 카테고리 | 제목 | 발행 |
|---|---|---|---|
| Y1 | YouTube | Anthropic Just Killed Tool Calling | 2026-02 |
| Y2 | YouTube | Inside Claude Code (Boris Cherny) | 2026-02 |
| Y3 | YouTube | Claude Agent SDK Workshop | 2026-01 |
| Y4 | YouTube | Harness Engineering (Ryan Lopopolo, OpenAI) | 2026-01 |
| Y5 | YouTube | Extreme Harness Engineering for Token Billionaires | 2026-01 |
| Y6 | YouTube | Devin 2.0 (Scott Wu) | 2025-07 |
| Y7 | YouTube | Sonnet 4.5 Roadmap (Mike Krieger) | 2025-09 |
| Y8 | YouTube | How We Build Effective Agents (Barry Zhang) | 2025-02 |
| B1 | Blog | Agent Harness Engineering — Addy Osmani | 2026-04 |
| B2 | Blog | Effective harnesses for long-running agents — Anthropic | 2025-11 |
| B3 | Blog | Designing agentic loops — Simon Willison | 2025-09 |
| B4 | Blog | Effective context engineering — Anthropic | 2025-09 |
| B5 | Blog | Writing effective tools — Anthropic | 2025-09 |
| B6 | Blog | Why Cognition does not use multi-agents — Jason Liu | 2025-09 |
| B7 | Blog | Multi-agent research system — Anthropic | 2025-06 |
| B8 | Blog | Don't Build Multi-Agents — Cognition | 2025-06 |
| B9 | Blog | 12-Factor Agents — Dex Horthy | 2025-04 |
| B10 | Blog | Building effective agents — Anthropic | 2024-12 |
| L1 | LinkedIn | Agentic Harness Engineering — Elvis Saravia | 2026-01 |
| L2 | LinkedIn | What is an agent harness — Hugo Bowne-Anderson | 2025-12 |
| L3 | LinkedIn | Karpathy's AGENTS.md — Marc Oakes | 2025-12 |
| L4 | LinkedIn | LangChain Middleware Harnesses — Sydney Runkle | 2025-11 |
| L5 | LinkedIn | Framework vs Runtime vs Harness — Harrison Chase | 2025-11 |
| L6 | LinkedIn | Anthropic Context Engineering announcement | 2025-09 |
| L7 | LinkedIn | Agents (book excerpt) — Chip Huyen | 2025-01 |
| H1 | HN | Harnesses Explained (Inner/Outer) | 2026-04 |
| H2 | HN | Improving 15 LLMs / Only the Harness Changed | 2026-02 |
| H3 | HN | Effective harnesses for long-running agents | 2025-11 |
| H4 | HN | Effective context engineering | 2025-10 |
| H5 | HN | Don't Build Multi-Agents | 2025-09 |
| H6 | HN | What makes Claude Code so damn good | 2025-08 |
| H7 | HN | Claude Code Cleanroom Analysis | 2025-06 |
| H8 | HN | Unreasonable effectiveness of LLM agent loop | 2025-05 |
