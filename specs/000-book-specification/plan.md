# Implementation Plan: Physical AI and Humanoid Robotics Book

**Branch**: `001-book-core-spec` | **Date**: 2025-12-30 | **Spec**: [specs/000-book-specification/spec.md](spec.md)
**Input**: Feature specification from `/specs/000-book-specification/spec.md`

---

## Summary

Build a comprehensive, 260+ page robotics and AI educational book delivered via Docusaurus with hands-on code examples, interactive components, and video tutorials. The book spans 4 progressive modules (ROS 2, Gazebo/Physics, NVIDIA Isaac/SLAM, Vision-Language-Action) plus a capstone project, enabling learners to progress from understanding distributed middleware to building voice-commanded autonomous humanoids. The development will span 16 weeks with 3 team members, leveraging reusable MDX components, Docker for reproducibility, and GitHub-based CI/CD for continuous validation.

---

## Technical Context

**Language/Version**: TypeScript (Docusaurus), Python 3.10+, C++ (ROS 2 examples), YAML (configs)

**Primary Dependencies**:
- Docusaurus 3.x (documentation framework)
- React (for interactive components)
- Monaco Editor (code playgrounds)
- Three.js / babylon.js (3D visualization)
- ROS 2 Iron/Jazzy (middleware examples)
- Gazebo Garden (physics simulation)
- NVIDIA Isaac Sim 2025.1+ (advanced sim)
- Docker (reproducibility)
- GitHub Actions (CI/CD)
- Vercel/Netlify (hosting)

**Storage**: N/A (static site, but datasets hosted on GitHub Releases or external CDN)

**Testing**:
- Python pytest (code example validation)
- Docusaurus build tests (markdown linting, broken links)
- Accessibility tests (WAVE, Axe)
- Screenshot/visual regression tests (Playwright)
- Docker container build/run validation

**Target Platform**: Web (Docusaurus site), cross-platform code examples (Windows WSL2, macOS, Linux)

**Project Type**: Documentation site + educational code repository (monorepo structure)

**Performance Goals**:
- Docusaurus page load: <3 seconds (LCP, FID, CLS)
- Code example setup: <30 minutes (end-to-end with Docker)
- Video load: <2 seconds (YouTube embed)
- Search indexing: <5 seconds for full site

**Constraints**:
- Zero hardware requirement (simulation-first)
- Code reproducibility on 3 platforms (Windows WSL2, macOS Intel/M1, Linux Ubuntu 22.04)
- Offline-capable: Whisper + LLM examples support local models
- Accessibility: WCAG AA compliance (captions, alt text, MathJax)
- Cost-aware: Free-tier services where possible (GitHub, Vercel, NVIDIA Isaac free tier)

**Scale/Scope**:
- 260+ pages of content
- 12 lessons (3 per module × 4 modules)
- 24+ code examples (2+ per lesson)
- 15+ video tutorials
- 40+ exercises with solutions
- 40 quiz questions (10 per module)
- 50+ architecture diagrams

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Alignment

**I. Hands-On Learning First** ✅
- Every lesson includes working, tested code examples
- Docusaurus site will embed Monaco Editor for live code playgrounds
- Docker ensures reproducibility across platforms
- Decision: Use interactive code components (Monaco) + Docker examples

**II. Progressive Complexity** ✅
- 4 modules ordered sequentially: ROS 2 → Simulation → AI → VLA → Capstone
- Each module independently meaningful (e.g., learner can stop after Module 1 and build basic node)
- Capstone integrates all 4 modules
- Decision: Enforce module dependencies in plan; capstone assumes all 4 modules

**III. Code Quality and Reproducibility** ✅
- All code tested on 3 platforms (Windows WSL2, macOS, Linux)
- Dockerfiles provided for all modules
- Professional standards: error handling, logging, version-pinned deps
- Decision: CI/CD pipeline validates every code example on 3 platforms weekly

**IV. Simulation-First, Hardware-Optional** ✅
- Gazebo and Isaac Sim are primary environments
- No hardware required to learn
- Hardware transfer guide provided (appendix)
- Decision: All examples use simulation; hardware optional extension

**V. Multi-Modal Perception and Action** ✅
- Module 4 covers voice (Whisper), LLM reasoning, vision grounding (CLIP, Grounding DINO)
- Capstone demonstrates integrated system
- Decision: Module 4 heavily weighted (80 pages, 15 hours); VLA pipeline is capstone focus

**VI. Architectural Clarity** ✅
- Each module includes layered architecture diagrams
- Separation: perception → state estimation → planning → control → cognition
- Decision: Require 4+ SVG diagrams per module; architecture explanation in every lesson intro

**VII. Accessibility for Diverse Learning Styles** ✅
- Content provided as: written explanations, diagrams, code, videos, quizzes
- Jargon explained on first use; glossary provided
- Decision: Docusaurus site supports dark mode, MathJax, captions, alt text

### Scope Alignment

**In Scope** ✅
- ROS 2 Iron/Jazzy LTS
- Gazebo Garden
- NVIDIA Isaac Sim free tier
- Whisper, LLaMA/Mistral
- Docusaurus, Docker
- All listed (3 platforms × 4 modules × 3 lessons)

**Out of Scope** ✅
- Hardware assembly tutorials (link to OEM docs)
- Real-time optimization (focus: stability)
- Formal verification
- Non-ROS comparisons
- Commercial licensing

### Non-Negotiable Constraints Alignment

**Reproducibility** ✅
- CI/CD pipeline enforces <30 min setup per module
- Docker standardizes all examples
- Platform testing: WSL2, macOS, Linux

**Open Source** ✅
- No paywalls; NVIDIA Isaac free for learning
- MIT license for code
- Creative Commons for content (with attribution)

**Safety** ✅
- Simulation-first eliminates physical risk
- Hardware section (future): safety standards required

**Accessibility** ✅
- All videos: captions + transcripts
- Images: alt text
- Math: MathJax (not images)
- WCAG AA: contrast ratios, semantic HTML

### **GATE RESULT: ✅ PASS** — No violations. Plan proceeds to Phase 0.

---

## Project Structure

### Documentation (this feature)

```text
specs/000-book-specification/
├── spec.md                          # Feature specification
├── plan.md                          # This file (implementation plan)
├── research.md                      # Phase 0 output (tech decisions)
├── data-model.md                    # Phase 1 output (content entities)
├── quickstart.md                    # Phase 1 output (dev setup)
├── contracts/                       # Phase 1 output
│   ├── docusaurus-config.schema.md
│   ├── mdx-components.schema.md
│   └── cicd-pipeline.schema.md
└── tasks.md                         # Phase 2 output (/sp.tasks command)
```

### Source Code Repository

```text
.
├── website/                         # Docusaurus site
│   ├── docusaurus.config.js
│   ├── sidebars.js
│   ├── package.json
│   ├── docs/
│   │   ├── intro.md
│   │   ├── module-1-ros2/
│   │   │   ├── lesson-1-1.mdx
│   │   │   ├── lesson-1-2.mdx
│   │   │   ├── lesson-1-3.mdx
│   │   │   ├── exercises.mdx
│   │   │   └── quiz.mdx
│   │   ├── module-2-gazebo/
│   │   ├── module-3-isaac/
│   │   ├── module-4-vla/
│   │   ├── capstone/
│   │   └── appendix/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeSandbox.tsx       # Interactive code editor
│   │   │   ├── URDFViewer.tsx        # 3D URDF viewer
│   │   │   ├── Quiz.tsx              # Interactive quiz
│   │   │   ├── VideoEmbed.tsx        # YouTube/Vimeo embed
│   │   │   └── AudioPlayer.tsx       # Audio playback
│   │   ├── css/
│   │   │   ├── custom.css            # Dark mode, custom styles
│   │   │   └── accessibility.css
│   │   └── theme/
│   │       └── custom-theme/
│   ├── static/
│   │   ├── images/
│   │   │   ├── module-1/
│   │   │   ├── module-2/
│   │   │   ├── module-3/
│   │   │   └── module-4/
│   │   ├── videos/                  # Video transcripts, slides
│   │   └── datasets/                # Links to external datasets
│   └── versioning/                  # (optional) for multi-version support

├── examples/                        # Code examples (tested, runnable)
│   ├── module-1-ros2/
│   │   ├── lesson-1-1/
│   │   │   ├── publisher.py
│   │   │   ├── subscriber.py
│   │   │   ├── Dockerfile
│   │   │   ├── docker-compose.yml
│   │   │   └── requirements.txt
│   │   ├── lesson-1-2/
│   │   └── lesson-1-3/
│   ├── module-2-gazebo/
│   ├── module-3-isaac/
│   ├── module-4-vla/
│   └── capstone/

├── tests/                           # CI/CD tests
│   ├── code-examples/
│   │   ├── test_module_1.py
│   │   ├── test_module_2.py
│   │   ├── test_module_3.py
│   │   └── test_module_4.py
│   ├── docusaurus/
│   │   ├── test_build.js
│   │   ├── test_links.js
│   │   └── test_accessibility.js
│   └── integration/
│       └── test_capstone.py

├── docker/                          # Docker setup
│   ├── Dockerfile.module-1
│   ├── Dockerfile.module-2
│   ├── Dockerfile.module-3
│   ├── Dockerfile.module-4
│   ├── Dockerfile.capstone
│   └── docker-compose.yml

├── .github/
│   ├── workflows/
│   │   ├── test-code-examples.yml   # Weekly validation
│   │   ├── build-docusaurus.yml     # On PR/push to main
│   │   ├── accessibility-audit.yml  # Monthly
│   │   └── deploy.yml               # On merge to main
│   └── ISSUE_TEMPLATE/
│       ├── bug-report.md
│       └── broken-example.md

├── docs/
│   ├── CONTRIBUTING.md              # Developer guide
│   ├── SETUP.md                     # Local dev environment
│   ├── VIDEO-GUIDE.md               # Video creation standards
│   └── CODE-STANDARDS.md            # Code style guide

├── datasets/                        # (External) Links + manifests
│   ├── README.md
│   ├── module-1-models.md
│   ├── module-2-worlds.md
│   ├── module-3-sensor-data.md
│   └── module-4-training-data.md

├── README.md
├── LICENSE (MIT)
└── package.json (monorepo root)
```

**Structure Decision**: Monorepo with `/website` (Docusaurus), `/examples` (tested code), `/tests` (CI/CD), `/docker` (container setup). Separation ensures clear ownership: content team works in `/website/docs`, code team in `/examples`, automation team in `.github/workflows`.

---

## Complexity Tracking

No Constitution violations or complexity tradeoffs required. Plan adheres to all 7 principles and constraints without exception.

| Decision | Rationale | Justification |
|----------|-----------|---------------|
| Monorepo structure | Unified versioning, easier cross-team collaboration | Single GitHub repo simplifies contribution workflow; sub-teams have clear directories |
| Docusaurus 3.x (not custom build) | Established framework, ecosystem, time-to-market | Custom Next.js solution would add 4–6 weeks dev time; Docusaurus has MDX support + plugins out-of-box |
| 16-week timeline | Aggressive but achievable with parallel work | Modules 1–4 can be written in parallel (weeks 3–14); setup (weeks 1–2) and polish (weeks 15–16) are sequential |

---

## Phase 0: Research & Technology Decisions

**Duration**: Parallel to Week 1–2 (setup phase)

### Research Tasks

1. **Docusaurus Configuration Patterns**
   - Task: Identify best practices for Docusaurus 3.x sidebar organization, theme customization, plugin setup
   - Output: research.md section on Docusaurus decisions
   - Owner: Tech Lead
   - Duration: 2 days

2. **MDX Component Implementation**
   - Task: Research Monaco Editor integration for code playgrounds, Three.js for URDF visualization, accessibility best practices
   - Output: research.md section on component architecture
   - Owner: Tech Lead
   - Duration: 3 days

3. **CI/CD Pipeline Design**
   - Task: Best practices for testing code examples in Docker, GitHub Actions caching, artifact storage
   - Output: research.md section on CI/CD architecture
   - Owner: DevOps Engineer (or Tech Lead)
   - Duration: 2 days

4. **Code Example Reproducibility**
   - Task: Validate Docker setup for ROS 2, Gazebo, Isaac Sim; identify platform-specific workarounds (WSL2, Apple Silicon)
   - Output: research.md section on platform testing strategy
   - Owner: Code Review Lead
   - Duration: 5 days (hands-on testing)

5. **Video Production Standards**
   - Task: Research video hosting (YouTube vs. Vimeo), captioning workflow, hosting costs
   - Output: research.md section on video delivery strategy
   - Owner: Video Producer
   - Duration: 2 days

6. **Dataset Hosting & Licensing**
   - Task: Identify suitable CDN for synthetic data, document licensing (CC-BY, CC0)
   - Output: research.md section on data distribution
   - Owner: Content Lead
   - Duration: 1 day

### Research Output

**File**: `specs/000-book-specification/research.md` (to be created in Phase 0)

**Contents**:
- **Docusaurus Setup**: Version choice (3.x), sidebar structure, plugins (image optimization, PWA, search), theme customization
- **MDX Components**: Monaco Editor (code sandbox), Three.js URDF viewer, Quiz component (localStorage state), VideoEmbed (YouTube)
- **CI/CD Pipeline**: GitHub Actions workflow (test-on-PR, build-on-push, deploy-on-merge), Docker caching, artifact storage
- **Platform Testing**: Windows WSL2 specific: Docker Desktop, networking; macOS: Docker Desktop + Docker Mac networking; Linux: native Docker
- **Video Strategy**: YouTube hosting (SEO, analytics), local transcription (Rev.com or community), embedded transcripts in MDX
- **Dataset Distribution**: GitHub Releases (small files), external CDN (large point clouds), manifest files for versioning

---

## Phase 1: Design & Data Model

**Duration**: Weeks 1–2 (parallel with Research, overlapping with Week 3 Module 1 work)

### 1.1 Data Model

**File**: `specs/000-book-specification/data-model.md`

**Key Entities**:

#### Module
- **id**: string (e.g., "module-1-ros2")
- **title**: string
- **description**: string
- **duration_hours**: number
- **page_count**: number
- **prerequisites**: string[] (e.g., ["intro"])
- **lessons**: Lesson[]
- **quiz**: Quiz

#### Lesson
- **id**: string (e.g., "lesson-1-1-intro")
- **title**: string
- **duration_minutes**: number
- **sections**: Section[] (intro, theory, practical, exercises)
- **learning_objectives**: string[]
- **code_examples**: CodeExample[]
- **exercises**: Exercise[]
- **videos**: Video[]

#### CodeExample
- **id**: string
- **title**: string
- **description**: string
- **language**: "python" | "cpp" | "yaml" | "bash"
- **code**: string (full, tested code)
- **explanation**: string
- **dockerfile**: string (for reproducibility)
- **execution_time_seconds**: number
- **platforms**: ("windows-wsl2" | "macos" | "linux")[]
- **related_exercise**: string (optional)

#### Exercise
- **id**: string
- **title**: string
- **problem_statement**: string
- **constraints**: string[]
- **starter_code**: string (optional)
- **solution**: string
- **solution_explanation**: string
- **difficulty**: "beginner" | "intermediate" | "advanced"

#### Video
- **id**: string
- **title**: string
- **duration_seconds**: number
- **youtube_id**: string
- **transcript**: string
- **topics**: string[]
- **lesson_references**: string[]

#### Quiz
- **id**: string
- **title**: string
- **questions**: QuizQuestion[]
- **passing_score**: number (percentage)

#### QuizQuestion
- **id**: string
- **type**: "multiple-choice" | "short-answer"
- **question_text**: string
- **options**: string[] (for multiple-choice)
- **correct_answer**: string | number
- **explanation**: string
- **lesson_reference**: string (link back to lesson for remediation)

### 1.2 API Contracts (Content Model)

**File**: `specs/000-book-specification/contracts/content-model.schema.md`

```yaml
# Docusaurus Sidebar Contract
sidebar:
  - label: string
    items:
      - id: string (doc path)
        label: string
        className?: string

# Module Structure
module:
  metadata:
    id: string
    title: string
    description: string
    duration_hours: number
    page_count: number
    prerequisites: string[]
  lessons: Lesson[]
  quiz: Quiz

# Lesson Structure
lesson:
  metadata:
    id: string
    title: string
    duration_minutes: number
    learning_objectives: string[]
  sections:
    - type: "introduction" | "theory" | "practical" | "exercises"
      content: string (markdown/MDX)
  code_examples: CodeExample[]
  videos: Video[]
  exercises: Exercise[]

# Code Example Contract
code_example:
  id: string
  title: string
  language: "python" | "cpp" | "yaml" | "bash" | "xml"
  code: string
  explanation: string
  dockerfile: string
  expected_output: string (for CI validation)
  platforms: string[]
  execution_instructions: string
```

**File**: `specs/000-book-specification/contracts/docusaurus-config.schema.md`

```javascript
// Docusaurus config structure
{
  title: "Physical AI and Humanoid Robotics",
  tagline: "Build autonomous humanoids from theory to practice",
  url: "https://physai-robotics.com",
  baseUrl: "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",

  i18n: {
    defaultLocale: "en",
    locales: ["en"]
  },

  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/physai/book/edit/main/website/",
          remarkPlugins: [require("mdx-mermaid")],
          rehypePlugins: []
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css")
        }
      }
    ]
  ],

  plugins: [
    require.resolve("@docusaurus/plugin-ideal-image"),
    require.resolve("@docusaurus/plugin-pwa"),
    [
      require.resolve("@docusaurus/plugin-search-local"),
      {
        indexDocs: true,
        indexBlog: false,
        language: ["en"],
        hashing: true,
        highlightSearchTermsOnTargetPage: true
      }
    ]
  ],

  themeConfig: {
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true
    },
    navbar: {
      title: "PhysAI Robotics",
      logo: { alt: "Logo", src: "img/logo.svg" },
      items: [
        { to: "/docs/intro", label: "Book", position: "left" },
        { href: "https://github.com/physai/book", label: "GitHub", position: "right" }
      ]
    },
    footer: {
      style: "dark",
      links: [
        { title: "Docs", items: [{ label: "Introduction", to: "/docs/intro" }] },
        { title: "Community", items: [{ label: "GitHub Discussions", href: "#" }] },
        { title: "Legal", items: [{ label: "License", href: "#" }] }
      ]
    }
  }
}
```

**File**: `specs/000-book-specification/contracts/mdx-components.schema.md`

```typescript
// Custom React components for Docusaurus

// CodeSandbox: Interactive Python editor
<CodeSandbox
  language="python"
  title="ROS 2 Publisher Example"
  code={`import rclpy\nfrom std_msgs.msg import String\n...`}
  hideOutput={false}
  timeout={30}
/>

// URDFViewer: 3D URDF model visualization
<URDFViewer
  urdfUrl="/static/models/humanoid.urdf"
  highlightJoints={["hip_roll", "knee"]}
  showAxes={true}
  allowRotation={true}
/>

// Quiz: Interactive quiz questions
<Quiz
  questions={[
    {
      type: "multiple-choice",
      question: "What is ROS 2?",
      options: ["Middleware", "OS", "Framework"],
      correct: 0,
      explanation: "ROS 2 is a middleware framework..."
    }
  ]}
  onPass={() => console.log("Quiz passed!")}
/>

// VideoEmbed: Embedded YouTube with transcript
<VideoEmbed
  videoId="abc123"
  title="ROS 2 Setup Tutorial"
  transcriptUrl="/static/transcripts/lesson-1-1.txt"
  startTime={60}
/>

// AudioPlayer: Audio playback (for Whisper examples)
<AudioPlayer src="/static/audio/voice-command.wav" controls />
```

### 1.3 Quick Start Guide

**File**: `specs/000-book-specification/quickstart.md`

**Contents**:
1. Local development environment setup (Node.js, npm, Docker)
2. Cloning the repo and installing dependencies
3. Running Docusaurus locally (`npm start`)
4. Building code examples (`docker build`)
5. Running tests locally (`npm test`)
6. Submitting PRs (branching, commit message format)

---

## Phase 1 Output Summary

- ✅ `data-model.md`: Entity definitions (Module, Lesson, CodeExample, Exercise, Video, Quiz)
- ✅ `contracts/content-model.schema.md`: Content structure contract
- ✅ `contracts/docusaurus-config.schema.md`: Docusaurus configuration
- ✅ `contracts/mdx-components.schema.md`: React component schemas
- ✅ `quickstart.md`: Developer onboarding guide

---

## Phase 2: Weekly Breakdown & Deliverables

**Total Duration**: 16 weeks
**Team**: 1 Lead Author (40 hrs/week) + 1 Technical Editor (20 hrs/week) + 1 Video Producer (10 hrs/week) + 10 Beta Testers (async)

### Weeks 1–2: Setup & Infrastructure

**Focus**: Docusaurus project initialization, component library, CI/CD, repository setup

**Deliverables**:

| Task | Owner | Hours | Completion Date |
|------|-------|-------|-----------------|
| Initialize Docusaurus 3.x project, configure sidebar, install plugins | Tech Lead | 16 | Jan 6 |
| Set up Docker for all modules (Dockerfile.module-1 through -4, docker-compose) | Tech Lead | 12 | Jan 6 |
| Create MDX components: CodeSandbox, URDFViewer, Quiz, VideoEmbed, AudioPlayer | Tech Lead | 24 | Jan 10 |
| Configure GitHub repo: branch protection, issue templates, CONTRIBUTING guide | Tech Lead | 8 | Jan 3 |
| Set up GitHub Actions: code-example tests, Docusaurus build, accessibility audits | Tech Lead/DevOps | 20 | Jan 10 |
| Deploy preview site to Vercel (staging environment) | Tech Lead | 8 | Jan 10 |
| Create SETUP.md, CODE-STANDARDS.md, VIDEO-GUIDE.md | Tech Lead / Content Lead | 12 | Jan 10 |

**Checkpoint**: Docusaurus site running locally, sample components working, CI/CD pipeline functional, team can merge PRs.

---

### Weeks 3–5: Module 1 (ROS 2 Nervous System)

**Focus**: Write 60 pages, create 8 code examples, produce 4 videos, design 6 diagrams, craft 8 exercises

**Content Assignments**:
- **Lead Author** (40 hrs/week): Write lesson content, review code examples
- **Code Reviewer**: Validate code examples on 3 platforms, test Docker builds
- **Video Producer** (10 hrs/week): 4 videos × 4 hours planning/production/editing = 2 weeks intensive

**Deliverables**:

| Lesson | Content | Code Examples | Videos | Exercises | Diagrams |
|--------|---------|---------------|--------|-----------|----------|
| 1.1 Middleware | 20 pages | Publisher, Subscriber, rclpy basics | 1 (4 min) | 2 | 2 |
| 1.2 Topics/Services/Actions | 20 pages | Service client/server, Action client/server | 2 (3 min each) | 3 | 2 |
| 1.3 URDF & Humanoid | 20 pages | URDF parser, Xacro parametric model, joint state pub | 1 (5 min) | 3 | 2 |
| **Module 1 Quiz** | 5 pages | N/A | N/A | 10 questions | N/A |

**Code Examples to Complete**:
1. `/examples/module-1-ros2/lesson-1-1/` - Publisher/Subscriber (Python)
2. `/examples/module-1-ros2/lesson-1-1/` - rclpy node lifecycle
3. `/examples/module-1-ros2/lesson-1-2/` - Service definition + client/server
4. `/examples/module-1-ros2/lesson-1-2/` - Action definition + client/server
5. `/examples/module-1-ros2/lesson-1-3/` - URDF parser (Python)
6. `/examples/module-1-ros2/lesson-1-3/` - Xacro with macros
7. `/examples/module-1-ros2/lesson-1-3/` - JointState publisher
8. Module 1 Capstone: Multi-node integration (pub + sub + service)

**Testing**: Each example tested on Windows WSL2, macOS, Linux; Dockerfile provided; output validated.

**Video Production Schedule**:
- Week 3: Script + record (4 videos)
- Week 4: Edit, add captions, generate transcripts
- Week 5: Review + upload to YouTube

**Checkpoint**: Module 1 content 100% complete, all examples tested, 4 videos published, quiz ready. Beta testers begin reviewing.

---

### Weeks 6–8: Module 2 (Digital Twin - Gazebo & Physics)

**Focus**: 50 pages, 7 code examples, 3 videos, 4 diagrams, 6 exercises

**Content Assignments**:
- **Lead Author**: Lesson writing, physics explanations
- **Code Reviewer**: Gazebo + physics validation
- **Video Producer**: 3 videos (intensive week 6)

**Deliverables**:

| Lesson | Content | Code Examples | Videos | Exercises | Diagrams |
|--------|---------|---------------|--------|-----------|----------|
| 2.1 Physics Sim | 17 pages | Gazebo world, physics params, force application | 1 (4 min) | 2 | 2 |
| 2.2 Sensor Sim | 17 pages | Camera plugin, LiDAR plugin, IMU, noise models | 1 (5 min) | 2 | 2 |
| 2.3 Collision & Control | 16 pages | PID controller, collision detection, control validation | 1 (4 min) | 2 | 2 |
| **Module 2 Quiz** | 5 pages | N/A | N/A | 10 questions | N/A |

**Code Examples to Complete**:
1. Gazebo world file (SDF) with humanoid + obstacles
2. Camera plugin + ROS 2 bridge
3. LiDAR plugin + point cloud streaming
4. IMU plugin with noise models
5. PID controller (Python node)
6. Collision detection listener
7. Module 2 Capstone: Full control loop with feedback

**Checkpoint**: Module 2 100% complete, Gazebo examples validated, 3 videos published. Cumulative progress: 110 pages.

---

### Weeks 9–11: Module 3 (AI-Robot Brain - NVIDIA Isaac & Nav2)

**Focus**: 70 pages, 9 code examples, 3 videos, 5 diagrams, 9 exercises

**Content Assignments**:
- **Lead Author**: Isaac Sim, SLAM, Nav2 deep dives
- **Code Reviewer**: Isaac Sim setup, SLAM validation
- **Video Producer**: 3 videos

**Deliverables**:

| Lesson | Content | Code Examples | Videos | Exercises | Diagrams |
|--------|---------|---------------|--------|-----------|----------|
| 3.1 Isaac Sim | 23 pages | Isaac setup, domain randomization, data export | 1 (6 min) | 3 | 2 |
| 3.2 SLAM & Localization | 24 pages | Isaac ROS SLAM node, map generation, loop closure | 1 (5 min) | 3 | 2 |
| 3.3 Nav2 & Motion Planning | 23 pages | Nav2 config, costmaps, path planning, bipedal controller | 1 (4.5 min) | 3 | 2 |
| **Module 3 Quiz** | 5 pages | N/A | N/A | 10 questions | N/A |

**Code Examples to Complete**:
1. Isaac Sim environment setup (USD scene)
2. Domain randomization script (lighting, object poses)
3. Synthetic data generation + export
4. Isaac ROS SLAM launch file
5. Map visualization + loop closure detection
6. Nav2 costmap configuration
7. Nav2 BehaviorTree navigation
8. Bipedal motion controller (trajectory interpolation)
9. Module 3 Capstone: SLAM + Nav2 integration

**Checkpoint**: Module 3 100% complete, Isaac Sim validated, SLAM + Nav2 working end-to-end. Cumulative progress: 180 pages.

---

### Weeks 12–14: Module 4 (Vision-Language-Action)

**Focus**: 80 pages, 10 code examples, 4 videos, 5 diagrams, 9 exercises

**Content Assignments**:
- **Lead Author**: Whisper, LLM, multimodal perception
- **Code Reviewer**: Voice integration, LLM API handling
- **Video Producer**: 4 videos (intensive module)

**Deliverables**:

| Lesson | Content | Code Examples | Videos | Exercises | Diagrams |
|--------|---------|---------------|--------|-----------|----------|
| 4.1 Whisper & LLM | 26 pages | Whisper transcription, LLM prompting, task planning | 1 (4 min) | 3 | 2 |
| 4.2 Multimodal Perception | 27 pages | CLIP zero-shot, Grounding DINO, 3D grounding | 1 (3.5 min) | 3 | 2 |
| 4.3 End-to-End VLA | 27 pages | State machine, error recovery, feedback loop, UI | 2 (5 + 8 min demo) | 3 | 2 |
| **Module 4 Quiz** | 5 pages | N/A | N/A | 10 questions | N/A |

**Code Examples to Complete**:
1. Whisper local installation + transcription
2. OpenAI GPT-4 API integration (with fallback to Mistral)
3. Task planning (prompt template + JSON parsing)
4. CLIP inference + zero-shot classification
5. Grounding DINO object detection
6. 3D pose estimation from 2D detections
7. State machine (VLA execution orchestration)
8. Error recovery (retry logic, fallback behaviors)
9. Simple web UI (Flask/React) for voice input
10. Module 4 Capstone: Full VLA pipeline (voice → humanoid action)

**Checkpoint**: Module 4 100% complete, voice-to-action pipeline functional. Cumulative progress: 260 pages. Capstone project ready for learner submission.

---

### Week 15: Polish, Testing & Peer Review

**Focus**: Final QA, accessibility audit, peer review, content refinement

**Deliverables**:

| Task | Owner | Hours | Details |
|------|-------|-------|---------|
| Run full accessibility audit (WAVE, Axe) | Tech Lead | 8 | Fix contrast, alt text, ARIA labels |
| Test all code examples on 3 platforms | Code Reviewer | 20 | Windows WSL2, macOS Intel/M1, Linux |
| Broken link audit + fix | Content Lead | 4 | `npm run build` + link checker |
| Peer review: 1-2 beta testers complete each module | Beta Testers | 40 (async) | Feedback on clarity, code errors, pacing |
| Address peer feedback | Lead Author | 16 | Rewrite unclear sections, fix bugs |
| Final content review (spelling, grammar) | Technical Editor | 12 | Proofread all 260 pages |
| Performance optimization (Core Web Vitals) | Tech Lead | 12 | Image optimization, lazy loading, code splitting |
| Update CHANGELOG + VERSION | Tech Lead | 2 | Prepare for v1.0.0 release |

**Checkpoint**: Site ready for public launch. All code examples passing CI/CD. Accessibility audit clean. No broken links.

---

### Week 16: Launch & Deployment

**Focus**: Production deployment, monitoring, community launch

**Deliverables**:

| Task | Owner | Hours | Details |
|------|-------|-------|---------|
| Deploy to production domain (physai-robotics.com) | Tech Lead | 4 | Configure DNS, SSL, Vercel settings |
| Activate analytics (Plausible or similar) | Tech Lead | 2 | Track page views, session duration, module completion |
| GitHub Releases: v1.0.0 | Tech Lead | 2 | Tag commit, generate release notes |
| Social media + ROS 2 community announcement | Community Manager | 4 | Twitter, LinkedIn, ROS 2 forum, r/robotics |
| Set up community support (GitHub Discussions, Discord) | Community Manager | 4 | Welcome message, pinned resources |
| Create post-launch survey (Typeform) | Content Lead | 2 | Collect learner feedback for v1.1 roadmap |
| Monitor site stability (first 48 hours) | Tech Lead | 8 | On-call support for critical issues |

**Checkpoint**: Site live, community engaged, initial feedback collected.

---

## Resource Allocation & Timeline

### Team Structure

| Role | Person | Hours/Week | Responsibility |
|------|--------|-----------|---|
| **Lead Author** | TBD | 40 | Content writing, lesson flow, code example curation |
| **Technical Editor** | TBD | 20 | Code quality, reproducibility, documentation |
| **Video Producer** | TBD | 10 | Video scripting, recording, editing, captions |
| **Tech Lead** | TBD | 40 | Docusaurus setup, CI/CD, component development, deployment |
| **Community Manager** | TBD | 5–10 (part-time) | GitHub management, issue response, community engagement |

### Beta Testers

- **10 volunteers** from ROS 2 / robotics communities
- **Commitment**: 4–5 hours per person (weeks 5, 8, 11, 15)
- **Contribution**: Review 1–2 modules, provide feedback on clarity/errors
- **Incentive**: Credit in CONTRIBUTORS.md, early access, free merch (optional)

### Weekly Burn Down

```
Week 1-2:  Setup 20% (infrastructure)
Week 3-5:  Module 1 + Setup 60% (content begins)
Week 6-8:  Module 2 100% (content ramping)
Week 9-11: Module 3 100% (content peak)
Week 12-14: Module 4 100% (content peak)
Week 15: Polish/Review 80% (tapering)
Week 16: Launch 100% (final push)
```

---

## Technical Milestones & Acceptance Criteria

### Milestone 1: Infrastructure (Week 2)

- ✅ Docusaurus project initialized with custom theme
- ✅ Sidebar structure matches `contracts/content-model.schema.md`
- ✅ CodeSandbox, URDFViewer, Quiz, VideoEmbed, AudioPlayer components working
- ✅ GitHub repo: branch protection enabled, CONTRIBUTING guide published
- ✅ CI/CD: test-on-PR, build-on-push, deploy-on-merge workflows active
- ✅ Vercel preview: site accessible at `https://[staging-url].vercel.app`

### Milestone 2: Module 1 Complete (Week 5)

- ✅ 60 pages of content (3 lessons + quiz)
- ✅ 8 code examples: all tested on 3 platforms, Dockerfiles provided
- ✅ 4 videos: published on YouTube with captions + transcripts
- ✅ 6 architecture diagrams: SVG format, high-contrast dark mode
- ✅ 8 exercises: starter code + solutions + explanations
- ✅ Module 1 Quiz: 10 questions, immediate feedback, lesson links
- ✅ All accessibility checks pass (alt text, semantic HTML, captions)

### Milestone 3: Module 2 Complete (Week 8)

- ✅ All Milestone 2 criteria for Module 2
- ✅ Cumulative: 110 pages, 15 code examples, 8 videos, 12 diagrams

### Milestone 4: Module 3 Complete (Week 11)

- ✅ All Milestone 2 criteria for Module 3
- ✅ Cumulative: 180 pages, 24 code examples, 11 videos, 17 diagrams

### Milestone 5: Module 4 + Capstone Complete (Week 14)

- ✅ All Milestone 2 criteria for Module 4
- ✅ Capstone project: architecture guide, code templates, demo video, submission guide
- ✅ Cumulative: 260+ pages, 34 code examples, 15 videos, 22 diagrams
- ✅ 40 quiz questions across all modules
- ✅ 40+ exercises with solutions

### Milestone 6: QA & Launch Ready (Week 16)

- ✅ All code examples pass CI/CD on 3 platforms
- ✅ Accessibility audit: ≤5 errors per page type (WAVE, Axe)
- ✅ Broken link audit: 0 broken internal links, external links spot-checked
- ✅ Performance: LCP <3s, FID <100ms, CLS <0.1
- ✅ Search functionality: full-text working, module filtering active
- ✅ Dark mode: WCAG AA contrast ratios met
- ✅ Peer review feedback addressed (≥80% of issues resolved)
- ✅ Production domain: DNS configured, SSL active, Vercel deployed
- ✅ Analytics: Plausible/GA active, baseline metrics captured
- ✅ Community: GitHub Discussions open, Discord server created, v1.0.0 released

---

## Dependencies & Critical Path

### Blocking Dependencies

```
Week 1-2: Infrastructure Setup
    ↓
Week 3-5: Module 1 (can start writing independently)
    ↓
Week 6-8: Module 2 (uses Module 1 code + concepts)
    ↓
Week 9-11: Module 3 (depends on Modules 1 & 2)
    ↓
Week 12-14: Module 4 (depends on Modules 1-3)
    ↓
Week 15: Polish (all content complete)
    ↓
Week 16: Launch
```

**Note**: Content writing (Modules 1–4) can happen in parallel if team is staffed. Code examples require sequential testing (earlier modules first) but writing can overlap.

### Resource Constraints

- **Only 1 Tech Lead**: Docusaurus setup (weeks 1–2) is critical path. Video producer can't start until week 3 when content is available.
- **Code validation bottleneck**: Technical Editor can validate at most 3 examples/day on 3 platforms. Plan: 2 validation sprints per module (week 3 & 4 for Module 1, etc.).
- **Video production**: 4 videos × 8 hours each (scripting, recording, editing, captions) = 32 hours/week in weeks 3-4. Video producer at 10 hrs/week needs 3-4 weeks for Module 1 videos.

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Dependency breakage (ROS 2 API changes) | Medium | High | Weekly CI/CD validation; dependency pinning; rapid patch releases |
| Code example reproducibility issues (platform variance) | Medium | High | Extensive platform testing (weeks 1–2); Docker standardization; troubleshooting guides |
| Video production delays | Medium | Medium | Pre-script all videos; batch recording; outsource captions (Rev.com) if needed |
| Peer review feedback requiring major rewrites | Low | Medium | Start peer review early (week 5); iterative feedback loop, not all-at-end |
| Team member turnover mid-project | Low | High | Document everything in CONTRIBUTING.md; onboard backups early |
| Low learner engagement post-launch | Low | Medium | Community management plan; regular feedback surveys; roadmap transparency |

---

## Success Metrics & KPIs

### Milestone Metrics (Quantitative)

| Milestone | Target | Actual | Status |
|-----------|--------|--------|--------|
| Week 2: Infrastructure complete | 7/7 components working | TBD | 🟡 Pending |
| Week 5: Module 1 complete | 60 pages, 8 examples, 4 videos | TBD | 🟡 Pending |
| Week 8: Module 2 complete | 50 pages, 7 examples, 3 videos | TBD | 🟡 Pending |
| Week 11: Module 3 complete | 70 pages, 9 examples, 3 videos | TBD | 🟡 Pending |
| Week 14: Module 4 + Capstone complete | 80 pages, 10 examples, 4 videos | TBD | 🟡 Pending |
| Week 15: QA complete | 0 accessibility errors, 0 broken links | TBD | 🟡 Pending |
| Week 16: Launch ready | Site live, analytics active, community channels open | TBD | 🟡 Pending |

### Quality Metrics (Week 16 Baseline)

- **Code reproducibility**: ≤5% failure rate across 3 platforms
- **Accessibility**: ≤5 WAVE/Axe errors per page type
- **Performance**: LCP <3s, FID <100ms, CLS <0.1
- **Content clarity**: ≥80% of peer reviewers rate as "clear" or "very clear"
- **Module completion time**: Average ≤10 hours per module

### Post-Launch KPIs (1st 6 months)

- **Engagement**: ≥60% of visitors complete ≥1 full lesson
- **Learning**: Quiz pass rate ≥75% per module
- **Adoption**: ≥100 GitHub stars, ≥10 capstone projects submitted
- **Community**: <7 day average response time to first-time issues
- **Code stability**: ≤5% of examples break due to upstream changes

---

## Docusaurus Configuration Summary

### Key Plugins

| Plugin | Purpose | Config |
|--------|---------|--------|
| `@docusaurus/plugin-ideal-image` | Image optimization (WebP, srcset) | Auto-enabled |
| `@docusaurus/plugin-pwa` | Offline support, service worker | `offlineModeActivationStrategies: ["appInstalled", "queryString"]` |
| `@docusaurus/plugin-search-local` | Full-text search | `language: ["en"]`, `hashing: true` |
| `docusaurus-plugin-image-zoom` | Image zoom on hover | Enabled for lesson images |

### Theme Customization

- **Dark Mode**: CSS variables for theme colors, dark-friendly code blocks
- **Sidebar**: Hierarchical (Modules → Lessons), collapsible
- **Navbar**: Logo, "Book" link, GitHub link
- **Footer**: Links to docs, community, legal

### MDX Extensions

- Mermaid diagrams (architecture flowcharts)
- Code blocks with line highlighting
- Admonitions (note, warning, tip)
- Tabs (for multi-language code)
- Katex/MathJax for equations

---

## Docusaurus Build & Deploy

### Local Development

```bash
cd website
npm install
npm start  # Runs on http://localhost:3000
```

### Production Build

```bash
npm run build  # Generates static files in build/
# Vercel auto-deploys on push to main
```

### GitHub Actions Workflow

```yaml
name: Build & Deploy
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install
      - run: npm run build
      - run: npm run accessibility-audit
      - uses: actions/upload-artifact@v3
        with:
          name: build
          path: build/

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: vercel/action@v4
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

---

## Summary & Next Steps

This plan provides a comprehensive, week-by-week roadmap for building the Physical AI and Humanoid Robotics book in Docusaurus over 16 weeks with 3 core team members and 10 beta testers.

**Key Highlights**:
- ✅ Constitution fully aligned (all 7 principles supported)
- ✅ Monorepo structure with clear team ownership
- ✅ Aggressive but achievable timeline (Module 1 complete by week 5)
- ✅ Reproducibility baked in (CI/CD from day 1)
- ✅ Accessibility prioritized (WCAG AA, captions, alt text)
- ✅ Clear success metrics and milestones

**Proceeding to Phase 2**: Task generation (`/sp.tasks` command) will break down each week's deliverables into specific, actionable tasks with dependencies and time estimates.

---

**Plan Version**: 1.0.0
**Created**: 2025-12-30
**Status**: Draft (awaiting user approval before proceeding to Phase 2: Tasks)
