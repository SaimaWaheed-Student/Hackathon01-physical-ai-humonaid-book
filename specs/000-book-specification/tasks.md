---
description: "Comprehensive task list for Physical AI and Humanoid Robotics book development in Docusaurus"
---

# Tasks: Physical AI and Humanoid Robotics Book

**Input**: Design documents from `/specs/000-book-specification/`
**Prerequisites**: plan.md (implementation plan), spec.md (4 user stories), Constitution alignment verified

**Tests**: No test tasks included (book is content delivery; validation via CI/CD pipeline, peer review, and learner feedback surveys instead)

**Organization**: Tasks grouped by phase and user story to enable independent content development and parallel work streams

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different modules, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4) — Setup/Foundational phases have no story label
- Include exact file paths in all descriptions

## Path Conventions

- **Docusaurus site**: `website/docs/` (markdown + MDX)
- **Code examples**: `examples/module-{1,2,3,4}/lesson-{1,2,3}/` (Python, C++, YAML)
- **Videos**: Host on YouTube; transcripts in `website/static/transcripts/`
- **Diagrams**: `website/static/images/module-{1,2,3,4}/` (SVG format)
- **Tests/CI**: `.github/workflows/`, `tests/` at repo root
- **Components**: `website/src/components/` (React/TSX)
- **Docker**: `docker/Dockerfile.module-{1,2,3,4}`

---

## Phase 1: Setup & Infrastructure (Weeks 1–2)

**Purpose**: Docusaurus project initialization, custom components, CI/CD, repository setup

**Duration**: 2 weeks | **Leads**: Tech Lead (40 hrs) | **Checkpoint**: Docusaurus running locally, CI/CD functional, team can develop

### Setup: Project Initialization

- [X] T001 Create monorepo structure with `/website`, `/examples`, `/tests`, `/docker`, `.github/` directories in repository root
- [X] T002 Initialize Node.js project in `/website`: `npm init -y && npm install docusaurus @docusaurus/preset-classic @docusaurus/plugin-ideal-image @docusaurus/plugin-pwa @docusaurus/plugin-search-local`
- [X] T003 [P] Create Docusaurus configuration file at `website/docusaurus.config.js` with: site title "Physical AI and Humanoid Robotics", base URL "/", enable dark mode, configure all 4 plugins
- [X] T004 [P] Create sidebar configuration at `website/sidebars.js` with hierarchical structure: intro, Module 1 (3 lessons + quiz), Module 2 (3 lessons + quiz), Module 3 (3 lessons + quiz), Module 4 (3 lessons + quiz), capstone, appendix
- [X] T005 [P] Initialize React component library structure: create `website/src/components/` directory with stubs for CodeSandbox.tsx, URDFViewer.tsx, Quiz.tsx, VideoEmbed.tsx, AudioPlayer.tsx
- [X] T006 Create custom CSS at `website/src/css/custom.css` with: CSS variables for light/dark mode colors (dark blue #1a3a4a, neon green #00ff4d), WCAG AA contrast ratios, code block theming
- [X] T007 [P] Set up GitHub repository: initialize git, add .gitignore (node_modules, build/, .env), create CONTRIBUTING.md with development guidelines, LICENSE (MIT)
- [X] T008 Create issue templates in `.github/ISSUE_TEMPLATE/`: bug-report.md, broken-example.md, feature-request.md
- [X] T009 [P] Set up GitHub Actions workflows in `.github/workflows/`:
  - `test-code-examples.yml`: Trigger on PR/push, build Docker for each module, run code examples, validate output (weekly)
  - `build-docusaurus.yml`: Build Docusaurus on every PR/push to main
  - `deploy.yml`: Deploy to Vercel on merge to main
  - `accessibility-audit.yml`: Monthly accessibility audit (WAVE, Axe)

### Setup: Docker & Development Environment

- [X] T010 [P] Create `docker/Dockerfile.module-1` with base image `ros:iron-ros-core`, install Python dependencies, copy `/examples/module-1` examples, set entry point
- [X] T011 [P] Create `docker/Dockerfile.module-2` with base image `ros:iron-ros-core`, install Gazebo Garden, ROS 2 packages, copy `/examples/module-2`
- [X] T012 [P] Create `docker/Dockerfile.module-3` with base image `nvcr.io/nvidia/isaac-sim:2025.1-base`, install Isaac SDK, ROS 2, copy `/examples/module-3`
- [X] T013 [P] Create `docker/Dockerfile.module-4` with base image `python:3.10`, install Whisper, CLIP, Grounding DINO, LLM libs, copy `/examples/module-4`
- [X] T014 Create `docker/docker-compose.yml` with services for all 4 modules; allow local bind mounts for development
- [X] T015 Create `docs/SETUP.md`: Step-by-step local dev environment setup (Node.js installation, npm install, npm start for Docusaurus, Docker setup)
- [X] T016 Create `docs/CODE-STANDARDS.md`: Code style guide (Python: PEP 8, C++: Google style), Docusaurus markdown conventions, comment standards, error message format

### Setup: Custom React Components

- [X] T017 Implement `website/src/components/CodeSandbox.tsx`: Monaco Editor integration for Python code playgrounds, theme support, timeout handling (30 seconds), output display, error handling
- [X] T018 [P] Implement `website/src/components/URDFViewer.tsx`: Three.js-based 3D URDF viewer, load .urdf files, highlight joints, show coordinate frames, allow rotation/zoom, dark mode support
- [X] T019 [P] Implement `website/src/components/Quiz.tsx`: Interactive quiz component, store progress in localStorage, display questions (MC + short answer), immediate feedback, link to lesson review sections
- [X] T020 [P] Implement `website/src/components/VideoEmbed.tsx`: YouTube/Vimeo embed wrapper, display captions toggle, transcript panel, timestamp navigation, responsive sizing
- [X] T021 [P] Implement `website/src/components/AudioPlayer.tsx`: HTML5 audio player for voice command examples, controls (play, pause, volume), display waveform, support for .wav/.mp3

### Setup: Docusaurus Configuration & Plugins

- [X] T022 Configure `@docusaurus/plugin-ideal-image` for WebP conversion and responsive images
- [X] T023 Configure `@docusaurus/plugin-pwa` for offline support and service worker registration
- [X] T024 Configure `@docusaurus/plugin-search-local` for full-text search with module/lesson filtering
- [X] T025 Install MDX extensions: `mdx-mermaid` for diagrams, `remark-math` + `rehype-katex` for MathJax equations, `docusaurus-plugin-image-zoom` for image zooming
- [X] T026 Configure navbar in `docusaurus.config.js`: logo, "Book" dropdown (links to each module), "GitHub" link, dark mode toggle
- [X] T027 Configure footer: links to docs, community, legal (GitHub Discussions, Discord, MIT License)

### Setup: Vercel Deployment (Staging)

- [X] T028 Connect GitHub repo to Vercel project, configure Node.js build settings (npm install, npm run build)
- [X] T029 Set up environment variables in Vercel (if needed): API keys for analytics, Docusaurus config
- [X] T030 [P] Create preview deployment: ensure site accessible at `https://[staging-url].vercel.app`, test dark mode toggle, search functionality, responsive design
- [X] T031 Create `.github/DEPLOYMENT.md` with Vercel deployment procedure and rollback steps

**Checkpoint**: ✅ Docusaurus site running locally (`npm start`), all 5 components built and working, CI/CD workflows enabled (test-on-PR, build-on-push, deploy-on-merge), staging site live on Vercel, team can clone repo and develop

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and content organization that MUST be complete before any module work begins

**Duration**: Parallel with Week 1–2 setup + Week 3 Module 1 startup | **Leads**: Tech Lead, Content Lead | **⚠️ CRITICAL**: No module work can begin until foundational tasks complete

### Foundational: Content Structure & Templates

- [X] T032 [P] Create documentation templates in `website/docs/`:
  - `lesson-template.mdx`: Standard lesson structure (intro, theory, practical, exercises, summary)
  - `exercise-template.mdx`: Exercise template (problem statement, constraints, starter code, solution)
  - `quiz-template.mdx`: Quiz template (question pool, metadata, passing score)
  - `code-example-template.md`: Code example template (title, description, language, code, explanation, expected output)

- [X] T033 [P] Create appendix pages in `website/docs/appendix/`:
  - `glossary.md`: Repository for all technical terms (ROS 2, URDF, SLAM, VLA, etc.) with explanations
  - `references.md`: Bibliography (academic papers, ROS 2 docs, NVIDIA docs, LLM papers)
  - `troubleshooting.md`: Common errors + solutions (environment issues, dependency conflicts, Docker problems)
  - `resources.md`: External links (GitHub repos, YouTube channels, datasets, communities)

- [X] T034 [P] Create `website/docs/intro.md` with:
  - Welcome message + book overview
  - Learning path diagram (Module 1 → 2 → 3 → 4 → Capstone)
  - Prerequisites checklist (software, hardware, knowledge)
  - Time estimate (40 hours total, 10 hours/module)
  - How to use this book (reading order, exercises, quizzes, capstone)

- [X] T035 Create `website/static/datasets/README.md` with dataset manifest:
  - Module 1: 5 URDF humanoid models (Boston Dynamics-inspired, Atlas-inspired, simple bipedal, wheeled, quadruped)
  - Module 2: 10 Gazebo world files (home, warehouse, outdoor, industrial, etc.)
  - Module 3: 1000+ synthetic sensor data (point clouds, depth images, ground truth)
  - Module 4: 100 labeled detection images, 100 speech samples, 50 LLM training examples
  - For each dataset: file name, license (CC-BY/CC0/open-source), source attribution, download link (GitHub Releases or CDN)

### Foundational: Docker & Reproducibility Infrastructure

- [X] T036 [P] Create scripts for reproducibility validation:
  - `scripts/validate-code-example.sh`: Test a code example on current platform, capture output, compare against expected output
  - `scripts/test-all-examples.sh`: Run validation on all examples in a module, generate report
  - `scripts/docker-test.sh`: Build Docker image, run examples inside container, validate cross-platform

- [X] T037 [P] Create `tests/ci-validation.py`: Python script to validate code example outputs for CI/CD pipeline (parse expected output from code comments, compare with actual)

- [X] T038 Create version pinning strategy document: `docs/VERSIONING.md` with:
  - ROS 2 version (Iron/Jazzy LTS)
  - Python version (3.10+)
  - All dependency version constraints (see plan.md tech stack)
  - Procedure for updating dependencies (monthly patch releases)

### Foundational: Analytics & Learner Tracking

- [X] T039 [P] Set up Plausible or Google Analytics in Docusaurus config (`website/docusaurus.config.js`)
  - Track: page views, session duration, module completion rate (via quiz localStorage), search queries

- [X] T040 [P] Implement quiz completion tracking in `website/src/components/Quiz.tsx`:
  - Store completion in localStorage (module-{1,2,3,4}-completed)
  - Display progress bar (Modules 1/4 complete)
  - Persist across browser sessions

### Foundational: Community & Support Channels

- [X] T041 [P] Create GitHub Discussions section: set up discussion categories (Q&A, Announcements, Show & Tell)
  - Create pinned "Welcome" post with community guidelines, resources, support SLA (<7 days response time)
  - Create pinned "FAQ" post linking to appendix/FAQ.md

- [X] T042 [P] Create Discord server (optional but recommended):
  - Channels: announcements, q-and-a, module-1, module-2, module-3, module-4, capstone, showcase
  - Bot: welcome message, role assignment, pinned resources

- [X] T043 [P] Create `docs/CONTRIBUTING.md` with:
  - How to report bugs (issue template)
  - How to propose improvements (feature request template)
  - How to contribute code/content (fork, branch, PR process)
  - Code review checklist (style, testing, documentation)
  - Recognition (CONTRIBUTORS.md)

### Foundational: Documentation Infrastructure

- [X] T044 Create main `README.md` with:
  - Project description (1 paragraph)
  - Quick start (install Node.js, clone repo, `npm install && npm start`)
  - Book structure (4 modules + capstone)
  - Learning outcomes
  - Contributing guidelines
  - License (MIT)

- [X] T045 Create `docs/VIDEO-GUIDE.md` with:
  - Video production standards (resolution, frame rate, format)
  - Scripting template
  - Captioning workflow (Rev.com or similar)
  - YouTube upload checklist (title, description, tags, playlist)
  - Transcript delivery format

**Checkpoint**: ✅ All foundational structure in place: templates, appendix, datasets, CI/CD validation scripts, analytics, community channels, documentation. Module 1 work can now begin without blocking

---

## Phase 3: User Story 1 – Learn ROS 2 Fundamentals (Weeks 3–5)

**Priority**: P1 (MVP — foundation for all other modules)

**Goal**: Enable learners to understand ROS 2 middleware (nodes, topics, services, actions) through 60 pages of content, 8 code examples, 4 videos, 8 exercises, and a 10-question quiz

**Independent Test**: A learner with no robotics background can follow Module 1 setup, run code examples, complete exercises, pass quiz, and write their own ROS 2 publisher/subscriber node without external help

**Duration**: 3 weeks | **Leads**: Lead Author (40 hrs), Technical Editor (20 hrs), Video Producer (10 hrs) | **Parallelizable tasks**: Marked [P]

### Lesson 1.1 – ROS 2 Middleware Fundamentals (20 pages)

**Content**: ROS 2 architecture (DDS, QoS), nodes, executors, lifecycle, launch files, rclpy client library

- [X] T046 [P] [US1] Write `website/docs/module-1-ros2/lesson-1-1-middleware.mdx` (20 pages):
  - What is ROS 2? History, comparison to ROS 1, adoption in industry
  - Architecture overview: DDS, Quality of Service (QoS), client libraries
  - Node lifecycle: construction, configuration, activation, deactivation, cleanup
  - Executors and spinning
  - Launch files: syntax, composition, parameters
  - Include 4 mermaid diagrams (architecture, node lifecycle, pub/sub flow, executor model)
  - Include 2 code examples (inline, linking to `/examples/module-1/lesson-1-1/`)
  - Include learning objectives, key takeaways, further reading

- [X] T047 [P] [US1] Create code example 1.1.1 "Simple Publisher" in `/examples/module-1-ros2/lesson-1-1/publisher.py`:
  - Imports: rclpy, std_msgs
  - Create node, publisher to `/my_topic`
  - Publish messages at 10 Hz
  - Proper error handling (try/except), logging, graceful shutdown
  - Include docstring, comments explaining key lines
  - Dockerfile in same directory
  - Expected output: "Publishing message X"
  - Run time: <5 seconds
  - Platforms: Windows WSL2, macOS, Linux

- [X] T048 [P] [US1] Create code example 1.1.2 "Simple Subscriber" in `/examples/module-1-ros2/lesson-1-1/subscriber.py`:
  - Imports: rclpy, std_msgs
  - Create node, subscription to `/my_topic`
  - Print received messages
  - Logging, error handling
  - Expected output: "Received: ..."
  - Shared Dockerfile with publisher example
  - Platforms: Windows WSL2, macOS, Linux

- [X] T049 [P] [US1] Create code example 1.1.3 "Node Lifecycle" in `/examples/module-1-ros2/lesson-1-1/lifecycle_node.py`:
  - Demonstrate on_configure, on_activate, on_deactivate, on_cleanup callbacks
  - Logging at each transition
  - Expected output: state transition logs
  - Platforms: Windows WSL2, macOS, Linux

- [X] T050 [P] [US1] Create code example 1.1.4 "Launch File" in `/examples/module-1-ros2/lesson-1-1/example.launch.py`:
  - ROS 2 launch file (Python-based) that starts multiple nodes
  - Include parameters, remapping, conditional logic
  - Explanation of launch file syntax

- [X] T051 [P] [US1] Record & edit video 1.1: "ROS 2 Installation & First Node" (4 min)
  - Content: Install ROS 2 Iron on Ubuntu, create first publisher/subscriber, run with `ros2 run`
  - Include screen recording, terminal output, visual callouts
  - Add captions (hardcoded or .vtt file)
  - Upload to YouTube, embed in lesson
  - Transcript: `website/static/transcripts/lesson-1-1-video.txt`

- [X] T052 [P] [US1] Create 2 exercises in `website/docs/module-1-ros2/lesson-1-1-exercises.mdx`:
  - Exercise 1.1.1: "Write a custom message type and publisher" (modify example to publish custom data)
  - Exercise 1.1.2: "Create a subscriber that filters messages by timestamp" (add conditional logic)
  - Each includes: problem statement, constraints, starter code, solution with explanation, difficulty (beginner/intermediate)

### Lesson 1.2 – Topics, Services & Actions (20 pages)

**Content**: Asynchronous topics, synchronous services, goal-oriented actions, message definitions

- [X] T053 [P] [US1] Write `website/docs/module-1-ros2/lesson-1-2-topics-services.mdx` (20 pages):
  - Topics: publish/subscribe, decoupled, async, fire-and-forget use cases (sensor data)
  - Services: request/reply, synchronous, blocking, query/command use cases (inverse kinematics)
  - Actions: goals with feedback, long-running, cancellation, navigation use cases
  - Message, Service, Action interface definitions (MSG, SRV, ACT files)
  - Best practices: naming conventions, version management, interface stability
  - Include 6 mermaid diagrams (topic flow, service flow, action flow, life cycle comparisons)
  - Include code examples linking to `/examples/module-1/lesson-1-2/`

- [X] T054 [P] [US1] Create code example 1.2.1 "Service Server & Client" in `/examples/module-1-ros2/lesson-1-2/`:
  - Define custom service: `ComputeDistance.srv` (two 3D points → distance)
  - Server node: `service_server.py` (respond to requests)
  - Client node: `service_client.py` (send requests, receive responses)
  - Both nodes in separate files, can run independently
  - Docstrings, logging, error handling
  - Expected output: computed distances logged
  - Platforms: Windows WSL2, macOS, Linux

- [X] T055 [P] [US1] Create code example 1.2.2 "Action Server & Client" in `/examples/module-1-ros2/lesson-1-2/`:
  - Define custom action: `MoveRobot.action` (goal: target position, feedback: current position, result: success flag)
  - Action server: `action_server.py` (simulate robot movement over 5 seconds, send feedback every 1 second)
  - Action client: `action_client.py` (send goal, monitor feedback, retrieve result)
  - Both nodes separate files
  - Expected output: goal sent, feedback received (5 log lines), result received
  - Platforms: Windows WSL2, macOS, Linux

- [X] T056 [P] [US1] Create code example 1.2.3 "Custom Message Types" in `/examples/module-1-ros2/lesson-1-2/`:
  - Define custom message: `RobotState.msg` (position, velocity, battery level)
  - Publisher that broadcasts RobotState
  - Subscriber that receives and displays
  - Demonstrateparameter server interaction (set/get robot state metadata)

- [X] T057 [P] [US1] Record & edit video 1.2: "Services & Actions in ROS 2" (3 min each: 2 videos)
  - Video 1: Service request/reply pattern (screen recording, code walkthrough)
  - Video 2: Action goal with feedback (screen recording, execution trace)
  - Captions, transcripts, YouTube upload

- [X] T058 [P] [US1] Create 3 exercises in `website/docs/module-1-ros2/lesson-1-2-exercises.mdx`:
  - Exercise 1.2.1: "Implement a service that computes angle between two 3D points" (extends example 1.2.1)
  - Exercise 1.2.2: "Implement an action with cancellation support" (extends example 1.2.2, add cancel_goal logic)
  - Exercise 1.2.3: "Use parameter server to configure service timeout" (add rclpy.parameter API)

### Lesson 1.3 – URDF, Xacro & Humanoid Modeling (20 pages)

**Content**: Robot description language (URDF), parametric modeling (Xacro), humanoid kinematics, link/joint definitions

- [X] T059 [P] [US1] Write `website/docs/module-1-ros2/lesson-1-3-urdf.mdx` (20 pages):
  - URDF XML structure: robots, links, joints, inertia, geometry (visual vs. collision)
  - Kinematic chains, reference frames, coordinate systems
  - Humanoid-specific: bipedal structure (pelvis, torso, arms, legs), center of mass, joint limits, actuator specs
  - Xacro: macros, parameters, properties, DRY principle
  - Best practices: modularity, naming conventions, version control
  - Include 4 diagrams (URDF hierarchy, humanoid kinematic tree, coordinate frames, Xacro macro expansion)
  - Include code examples

- [X] T060 [P] [US1] Create code example 1.3.1 "Simple 3-DOF Arm in URDF" in `/examples/module-1-ros2/lesson-1-3/arm_simple.urdf`:
  - XML URDF file: 3 links (base, link1, link2) + 3 joints (revolute)
  - Inertia for each link
  - Visual geometry (cylinders for links)
  - Collision geometry (simpler than visual)
  - Explanation of XML tags

- [X] T061 [P] [US1] Create code example 1.3.2 "Refactored Arm with Xacro" in `/examples/module-1-ros2/lesson-1-3/arm_xacro.urdf.xacro`:
  - Refactor arm_simple.urdf using Xacro macros
  - Define macro for link (takes name, mass, length, radius as parameters)
  - Define macro for joint (takes name, parent, child, axis, limits as parameters)
  - Use macros to instantiate 3 links + 3 joints (reduces code by 60%)
  - Include Xacro syntax explanation

- [X] T062 [P] [US1] Create code example 1.3.3 "Humanoid Leg in URDF" in `/examples/module-1-ros2/lesson-1-3/humanoid_leg.urdf.xacro`:
  - 2-DOF humanoid leg (hip roll + knee): pelvis → hip → knee → ankle
  - Inertia based on humanoid mass distribution
  - Joint limits for realistic motion
  - Xacro parameters for leg length, mass
  - Visual geometry (cylinders + meshes for feet)
  - Collision geometry (simplified)

- [X] T063 [P] [US1] Create code example 1.3.4 "JointState Publisher" in `/examples/module-1-ros2/lesson-1-3/joint_state_publisher.py`:
  - Load URDF (arm_simple.urdf)
  - Publish JointState messages for all joints at 10 Hz
  - Cyclic motion (animate joints 0 → pi → -pi → 0 in 5 seconds)
  - Expected output: joint angles logged
  - Can visualize in RViz with URDF loaded

- [X] T064 [P] [US1] Create pre-built humanoid models in `/examples/module-1-ros2/lesson-1-3/models/`:
  - `humanoid_simple.urdf.xacro`: 20-DOF humanoid (pelvis, torso, 2 arms, 2 legs, head)
  - `humanoid_atlas_inspired.urdf.xacro`: More realistic (40 DOF, based on Boston Dynamics Atlas specs)
  - `humanoid_wheeled.urdf.xacro`: Wheeled base + arms (mobility variant)
  - Each includes inertia, visual meshes (STL/DAE links), joint limits
  - Explanation document for each model

- [X] T065 [P] [US1] Record & edit video 1.3: "Building a Robot in URDF" (5 min)
  - Content: Create simple URDF from scratch, load in RViz, animate joints
  - Screen recording: text editor → URDF file → RViz launch → visualization
  - Captions, transcript, YouTube

- [X] T066 [P] [US1] Create interactive URDF viewer component in lesson:
  - Use `website/src/components/URDFViewer.tsx`
  - Embed humanoid_simple.urdf model
  - Allow rotation, zoom, highlight joints
  - Display joint names and limits on hover

- [X] T067 [P] [US1] Create 3 exercises in `website/docs/module-1-ros2/lesson-1-3-exercises.mdx`:
  - Exercise 1.3.1: "Create a 2-DOF humanoid leg with proper inertia" (refine example 1.3.3)
  - Exercise 1.3.2: "Extend simple arm to 5-DOF with Xacro" (parametric design)
  - Exercise 1.3.3: "Create a wheeled robot (2 wheels + caster) in Xacro" (new design)

### Module 1 Assessment

- [X] T068 [P] [US1] Create Module 1 Quiz in `website/docs/module-1-ros2/quiz.mdx`:
  - 10 questions (7 multiple choice + 3 short answer)
  - Q1: What is ROS 2? (MC: middleware, OS, framework) → Answer: middleware
  - Q2: Name 3 types of ROS 2 communication (SA) → Answer: topics, services, actions
  - Q3: What does QoS stand for? (MC) → Answer: Quality of Service
  - Q4: What is URDF? (SA) → Answer: Universal Robot Description Format
  - Q5: Write a URDF joint definition (SA) → Model answer: `<joint><parent/><child/><axis/><limit/></joint>`
  - Q6–Q10: Conceptual + hands-on questions
  - Use `website/src/components/Quiz.tsx`
  - Immediate feedback: correct/incorrect + explanation + link to lesson review
  - Passing score: ≥75%

### Module 1 Capstone (Mini-Project)

- [X] T069 [P] [US1] Create Module 1 Capstone in `website/docs/module-1-ros2/capstone.mdx`:
  - **Challenge**: Write a multi-node system that:
    - Node A: Publisher sending "commands" (strings: "forward", "backward", "turn_left", "turn_right")
    - Node B: Subscriber receiving commands, calling a service on Node C with command
    - Node C: Service server that receives command, returns action (e.g., motor power level)
  - **Deliverable**: 3 Python files (command_publisher.py, command_subscriber.py, command_service.py), demo video (30 sec) showing execution
  - **Evaluation**: Code quality (style, error handling), functionality (all nodes run, messages flow), documentation
  - **Extension ideas**: Add parameter server for command timeout; implement action instead of service; add logging
  - Submission template: GitHub Gist or discussion post with code + demo link

**Checkpoint**: ✅ Module 1 complete (60 pages, 8 code examples tested on 3 platforms with Dockerfiles, 4 videos with captions, 8 exercises with solutions, 10-question quiz, capstone project) — learners can now write basic ROS 2 nodes

---

## Phase 4: User Story 2 – Simulate Robots in Physics (Weeks 6–8)

**Priority**: P1 (builds on US1, foundation for US3 + US4)

**Goal**: 50 pages, 7 code examples, 3 videos, 4 diagrams, 6 exercises, 10-question quiz + capstone demonstrating physics-based robot simulation

**Independent Test**: Learner can create a Gazebo world, spawn robot from URDF, add sensors, tune physics, and validate control logic without external help

**Duration**: 3 weeks | **Leads**: Lead Author (40 hrs), Technical Editor (20 hrs), Video Producer (10 hrs) | **Parallelizable tasks**: Marked [P]

### Lesson 2.1 – Physics Simulation Fundamentals (17 pages)

**Content**: Physics engines (DART, Bullet), rigid body dynamics, contact modeling, Gazebo integration

- [X] T070 [P] [US2] Write `website/docs/module-2-gazebo/lesson-2-1-physics.mdx` (17 pages):
  - Why simulate? Cost, safety, iteration speed
  - Physics pipeline: integration, collision, constraint solving
  - Rigid body dynamics: mass, inertia, forces, torques
  - Contact modeling: friction cones, restitution, compliance
  - Numerical integration: RK4, implicit Euler
  - Gazebo Garden architecture, ROS 2 integration (gazebo_ros packages)
  - Include 4 diagrams (physics pipeline, force application, contact response, Gazebo architecture)

- [X] T071 [P] [US2] Create code example 2.1.1 "Gazebo World File (SDF)" in `/examples/module-2-gazebo/lesson-2-1/empty_world.sdf`:
  - Simple Gazebo world: empty environment, gravity, default physics engine (DART)
  - Include ground plane (visual + collision)
  - Define physics parameters: gravity (0,0,-9.81), time step (0.001)
  - Include comments explaining SDF syntax

- [X] T072 [P] [US2] Create code example 2.1.2 "Launch Gazebo with ROS 2" in `/examples/module-2-gazebo/lesson-2-1/launch_gazebo.launch.py`:
  - ROS 2 launch file: start gazebo_server + gazebo_client
  - Pass world file (empty_world.sdf) as argument
  - Set environment variables (GAZEBO_MODEL_PATH)

- [X] T073 [P] [US2] Create code example 2.1.3 "Spawn URDF in Gazebo" in `/examples/module-2-gazebo/lesson-2-1/spawn_robot.py`:
  - Python script that loads URDF (humanoid_simple from Module 1)
  - Calls Gazebo service to spawn robot at position (0, 0, 1)
  - Use `gazebo_ros` package `/spawn_entity` service
  - Include error handling

- [X] T074 [P] [US2] Create code example 2.1.4 "Apply Forces to Robot" in `/examples/module-2-gazebo/lesson-2-1/apply_forces.py`:
  - Python node that publishes force commands to robot links
  - Use `geometry_msgs/Wrench` messages
  - Apply forces at specific link (e.g., "torso_link")
  - Monitor robot motion (subscribe to odometry)
  - Expected output: robot motion logs, force application logs

- [X] T075 [P] [US2] Create code example 2.1.5 "Tune Physics Parameters" in `/examples/module-2-gazebo/lesson-2-1/tune_physics.py`:
  - Dynamic reconfigure node: adjust gravity, friction, time step
  - Parameters: gravity_z (default -9.81), friction_coeff (0.5), time_step (0.001)
  - Observe impact on robot behavior (falling, sliding, stability)

- [X] T076 [P] [US2] Record & edit video 2.1: "Launching Gazebo and Tuning Physics" (4 min)
  - Content: Open Gazebo, load world, spawn robot, apply forces, observe physics
  - Include screen recording, terminal, Gazebo GUI
  - Captions, transcript

- [X] T077 [P] [US2] Create 2 exercises in `website/docs/module-2-gazebo/lesson-2-1-exercises.mdx`:
  - Exercise 2.1.1: "Create a Gazebo world with obstacles (ramps, boxes)" (extend empty_world.sdf)
  - Exercise 2.1.2: "Tune physics parameters to make robot stable on a ramp" (modify friction + time step)

### Lesson 2.2 – Sensor Simulation & Data Integration (17 pages)

**Content**: Camera, LiDAR, IMU simulation, noise models, ROS 2 integration, synthetic data collection

- [X] T078 [P] [US2] Write `website/docs/module-2-gazebo/lesson-2-2-sensors.mdx` (17 pages):
  - Camera simulation: pinhole model, distortion, noise (Gaussian blur)
  - LiDAR simulation: ray casting, range accuracy, intensity modeling
  - IMU simulation: accelerometer, gyroscope, magnetometer, bias drift
  - Noise models: Gaussian, Poisson (for LiDAR), bias/scale factors
  - Gazebo sensor plugins: camera_controller, lidar_controller, imu_controller
  - ROS 2 topic mapping (image_raw, point_cloud, imu/data)
  - Rosbag recording for offline analysis
  - Include 4 diagrams (camera pipeline, LiDAR ray casting, IMU drift model, sensor fusion)

- [X] T079 [P] [US2] Create code example 2.2.1 "Camera Plugin in Gazebo" in `/examples/module-2-gazebo/lesson-2-2/camera_world.sdf`:
  - Gazebo world with humanoid robot + RGB camera mounted on head
  - Camera parameters: resolution (640x480), FOV (60°), framerate (30 fps)
  - Noise: Gaussian blur (sigma 0.5 pixels)
  - Output: `/camera/image_raw` (ROS 2 topic)
  - Launch file: `launch_camera.launch.py`

- [X] T080 [P] [US2] Create code example 2.2.2 "LiDAR Plugin in Gazebo" in `/examples/module-2-gazebo/lesson-2-2/lidar_world.sdf`:
  - Gazebo world with robot + 3D LiDAR (Velodyne-like: 16 rays, 270° FOV)
  - Parameters: range (min 0.5m, max 100m), framerate (10 Hz)
  - Noise: range error ±0.1m, random ray dropout (5%)
  - Output: `/scan` (sensor_msgs/LaserScan) or `/points` (sensor_msgs/PointCloud2)
  - Launch file: `launch_lidar.launch.py`

- [X] T081 [P] [US2] Create code example 2.2.3 "IMU Plugin in Gazebo" in `/examples/module-2-gazebo/lesson-2-2/imu_world.sdf`:
  - Gazebo world with robot + IMU attached to torso
  - Parameters: accelerometer noise, gyroscope bias, magnetometer distortion
  - Output: `/imu/data` (sensor_msgs/Imu)
  - Include code to visualize IMU data (orientation, acceleration)

- [X] T082 [P] [US2] Create code example 2.2.4 "Record Sensor Data to Rosbag" in `/examples/module-2-gazebo/lesson-2-2/record_sensors.py`:
  - Python node that subscribes to camera, LiDAR, IMU topics
  - Record to rosbag file (`sensor_data.bag`)
  - Duration: 30 seconds
  - Include playback script (`playback_rosbag.py`) for offline analysis

- [X] T083 [P] [US2] Create code example 2.2.5 "Sensor Fusion: IMU + Odometry" in `/examples/module-2-gazebo/lesson-2-2/sensor_fusion.py`:
  - Subscribe to IMU and odometry (wheel encoders, if wheeled robot)
  - Fuse data using simple Kalman filter
  - Estimate pose (x, y, theta) more accurately than either sensor alone
  - Publish fused `/odometry/filtered` topic
  - Expected output: pose estimates with timestamps

- [X] T084 [P] [US2] Record & edit video 2.2: "Configuring Sensors in Gazebo" (5 min)
  - Content: Add camera, LiDAR, IMU to robot in Gazebo, verify ROS 2 topics
  - Screen recording: Gazebo GUI, rviz2 visualization, terminal output
  - Captions, transcript

- [X] T085 [P] [US2] Create 2 exercises in `website/docs/module-2-gazebo/lesson-2-2-exercises.mdx`:
  - Exercise 2.2.1: "Add a depth camera (RealSense D435) to Gazebo world" (new sensor)
  - Exercise 2.2.2: "Implement a Kalman filter for camera + LiDAR fusion" (extend example 2.2.5)

### Lesson 2.3 – Collision Detection, Control Validation & ROS Integration (16 pages)

**Content**: Collision geometry, safe interaction, PID control, control loop testing in sim

- [X] T086 [P] [US2] Write `website/docs/module-2-gazebo/lesson-2-3-control.mdx` (16 pages):
  - Collision geometry (vs. visual geometry): simplified shapes for performance
  - Collision response: friction, restitution, compliance
  - Safe interaction: collision callbacks, contact forces
  - PID controller design: setpoint tracking, tuning (Ziegler-Nichols), stability
  - Control validation metrics: rise time, overshoot, settling time, steady-state error
  - Bridging sim to hardware: API compatibility, sim-to-real gap, validation
  - Include 4 diagrams (collision geometry, PID control loop, step response, sim vs. real comparison)

- [X] T087 [P] [US2] Create code example 2.3.1 "PID Joint Controller" in `/examples/module-2-gazebo/lesson-2-3/pid_controller.py`:
  - Python node: implement PID controller for a single joint (e.g., robot arm joint)
  - Parameters: Kp, Ki, Kd (tunable)
  - Setpoint: user-provided or sinusoidal motion profile
  - Control loop: 100 Hz
  - Output: joint command via `/joint_controller/command` topic
  - Measure performance: rise time, overshoot, steady-state error
  - Expected output: control metrics logged

- [X] T088 [P] [US2] Create code example 2.3.2 "Collision Detection & Response" in `/examples/module-2-gazebo/lesson-2-3/collision_handler.py`:
  - Python node that subscribes to Gazebo contact sensor plugin
  - Detect collisions: log contact forces, contact points
  - Implement safety response: reduce joint velocities if force exceeds threshold
  - Expected output: collision events logged with forces

- [X] T089 [P] [US2] Create code example 2.3.3 "Full Control Loop Test" in `/examples/module-2-gazebo/lesson-2-3/control_validation.py`:
  - Multi-joint controller for humanoid leg (hip + knee)
  - Perform trajectory: sit → stand → sit over 5 seconds
  - Measure performance: joint tracking error, stability (no falling)
  - Log metrics to CSV for analysis

- [X] T090 [P] [US2] Create code example 2.3.4 "Sim-to-Real Comparison" in `/examples/module-2-gazebo/lesson-2-3/validate_sim_real.py`:
  - Load pre-recorded real robot data (if available) or synthetic comparison data
  - Run same control in simulation
  - Compare trajectories: plot sim vs. real
  - Analyze differences: explain sim-to-real gap (friction, inertia, sensor noise)

- [X] T091 [P] [US2] Record & edit video 2.3: "Tuning Control Parameters & Validating Behavior" (4 min)
  - Content: PID tuning, control performance analysis, collision detection
  - Screen recording: code editor, control plots, Gazebo visualization
  - Captions, transcript

- [X] T092 [P] [US2] Create 2 exercises in `website/docs/module-2-gazebo/lesson-2-3-exercises.mdx`:
  - Exercise 2.3.1: "Tune PID gains to achieve <5% steady-state error on step input" (iterative design)
  - Exercise 2.3.2: "Implement a collision-aware controller that stops joints on contact" (safety)

### Module 2 Assessment

- [X] T093 [P] [US2] Create Module 2 Quiz in `website/docs/module-2-gazebo/quiz.mdx`:
  - 10 questions (7 MC + 3 SA)
  - Topics: Gazebo architecture, physics engines, sensor simulation, PID control, sim-to-real
  - Passing score: ≥75%

### Module 2 Capstone

- [X] T094 [P] [US2] Create Module 2 Capstone in `website/docs/module-2-gazebo/capstone.mdx`:
  - **Challenge**: Design a Gazebo world with:
    - 3 different environment scenarios (home, warehouse, outdoor)
    - Humanoid robot with camera, LiDAR, IMU
    - Obstacle course (ramps, boxes, gaps)
    - Control the robot to navigate each environment
  - **Deliverable**: 3 world files (.sdf), 1 control script, demo video (2 min) showing navigation in each scenario
  - **Evaluation**: Physics accuracy, sensor realism, control performance (collisions avoided)

**Checkpoint**: ✅ Module 2 complete (50 pages, 7 code examples tested on 3 platforms, 3 videos, 6 exercises, quiz, capstone) — learners can simulate robots and validate control logic

---

## Phase 5: User Story 3 – Integrate AI Perception (Weeks 9–11)

**Priority**: P2 (depends on US1 + US2)

**Goal**: 70 pages, 9 code examples, 3 videos, 5 diagrams, 9 exercises, 10-question quiz + capstone demonstrating SLAM, localization, and autonomous navigation

**Independent Test**: Learner can deploy SLAM on simulated robot, generate map, use Nav2 to navigate autonomously without external help

**Duration**: 3 weeks | **Leads**: Lead Author (40 hrs), Technical Editor (20 hrs), Video Producer (10 hrs)

### Lesson 3.1 – Isaac Sim & Synthetic Data Generation (23 pages)

**Content**: Isaac Sim setup, domain randomization, synthetic data generation, dataset creation

- [X] T095 [P] [US3] Write `website/docs/module-3-isaac/lesson-3-1-isaac-sim.mdx` (23 pages):
  - NVIDIA Isaac Sim overview: Omniverse, USD, photorealism
  - Domain randomization: lighting, textures, object poses, camera parameters
  - Synthetic data: RGB images, depth maps, segmentation masks, 6D pose
  - Dataset creation workflow: script generation → render → annotate → export
  - YOLOv8/Mask R-CNN fine-tuning on synthetic data
  - Evaluation: domain gap analysis, sim2real transfer
  - Include 5 diagrams (Isaac architecture, rendering pipeline, domain randomization, dataset annotation, ML pipeline)

- [X] T096 [P] [US3] Create code example 3.1.1 "Isaac Sim Environment Setup" in `/examples/module-3-isaac/lesson-3-1/setup_isaac_sim.py`:
  - Python script using Isaac Sim SDK
  - Load humanoid robot (URDF or USD)
  - Load environment (room with furniture)
  - Set camera pose for data generation
  - Export to USD format

- [X] T097 [P] [US3] Create code example 3.1.2 "Domain Randomization Script" in `/examples/module-3-isaac/lesson-3-1/randomize_domain.py`:
  - Randomize: lighting (5–20 light sources, vary intensity), material properties (roughness, metallic)
  - Randomize: object poses (place 5–10 objects at random locations, rotations)
  - Randomize: camera parameters (intrinsics, pose)
  - Generate 100 variations, log randomization parameters

- [X] T098 [P] [US3] Create code example 3.1.3 "Synthetic Data Generation" in `/examples/module-3-isaac/lesson-3-1/generate_dataset.py`:
  - Loop: render image, capture depth, compute segmentation, extract 6D poses
  - For each render: save RGB (JPEG), depth (PNG), segmentation (PNG), metadata (JSON with object poses, intrinsics)
  - Generate 1000 images
  - Expected output: dataset directory with images + metadata

- [X] T099 [P] [US3] Create code example 3.1.4 "Dataset Annotation & Export" in `/examples/module-3-isaac/lesson-3-1/annotate_dataset.py`:
  - Convert Isaac Sim outputs to COCO format (for object detection)
  - Generate bounding boxes from segmentation masks
  - Create dataset.json (COCO-compliant)
  - Ready for YOLOv8 training

- [X] T100 [P] [US3] Create code example 3.1.5 "Train YOLOv8 on Synthetic Data" in `/examples/module-3-isaac/lesson-3-1/train_yolo.py`:
  - Load synthetic dataset (COCO format)
  - Fine-tune YOLOv8s on synthetic data (10 epochs, 100 images = 10 min)
  - Save trained model
  - Evaluate: mAP on synthetic test set

- [X] T101 [P] [US3] Record & edit video 3.1: "GPU-Accelerated Perception with Isaac Sim" (6 min)
  - Content: Open Isaac Sim, load scene, randomize domain, generate synthetic data
  - Screen recording: Isaac Sim GUI, Python script output, generated images
  - Captions, transcript

- [X] T102 [P] [US3] Create 3 exercises in `website/docs/module-3-isaac/lesson-3-1-exercises.mdx`:
  - Exercise 3.1.1: "Generate 500 synthetic images with domain randomization" (extend example 3.1.3)
  - Exercise 3.1.2: "Fine-tune YOLO on your dataset, measure mAP improvement" (extend example 3.1.5)
  - Exercise 3.1.3: "Analyze domain gap: test synthetic model on real images" (transfer learning)

### Lesson 3.2 – SLAM, Localization & Isaac ROS (24 pages)

**Content**: SLAM algorithms (visual, LiDAR), Isaac ROS SLAM, localization, map quality

- [X] T103 [P] [US3] Write `website/docs/module-3-isaac/lesson-3-2-slam.mdx` (24 pages):
  - SLAM problem: estimate pose while building map
  - Visual SLAM: feature extraction, optical flow, bundle adjustment
  - LiDAR SLAM: scan-to-map registration, loop closure
  - Isaac ROS SLAM node: input/output contracts, parameter tuning
  - nvblox: voxel-based mapping for memory efficiency
  - Loop closure detection and map consistency
  - Evaluation: map coverage, localization error, drift over long trajectories
  - Include 5 diagrams (SLAM pipeline, visual features, LiDAR scan registration, loop closure, map quality metrics)

- [X] T104 [P] [US3] Create code example 3.2.1 "Launch Isaac ROS SLAM" in `/examples/module-3-isaac/lesson-3-2/launch_slam.launch.py`:
  - ROS 2 launch file: start Isaac ROS SLAM node
  - Input: camera/rgb images + camera/depth + camera/info
  - Output: /map (occupancy grid), /odom (odometry), /pose (TF)
  - Parameters: feature quality, matching threshold, loop closure weight

- [X] T105 [P] [US3] Create code example 3.2.2 "Run SLAM in Gazebo" in `/examples/module-3-isaac/lesson-3-2/run_slam_gazebo.py`:
  - Launch Gazebo with robot + camera + LiDAR (from Module 2)
  - Launch Isaac ROS SLAM
  - Teleoperate robot manually (publish geometry_msgs/Twist to /cmd_vel)
  - Monitor SLAM output: view map in rviz2, track odometry
  - Expected output: map visualization, odometry logs

- [X] T106 [P] [US3] Create code example 3.2.3 "Evaluate Map Quality" in `/examples/module-3-isaac/lesson-3-2/evaluate_slam.py`:
  - Compute metrics: map coverage (% of explored area), localization error (drift over closed loop)
  - Load ground truth map (from Gazebo world)
  - Compare SLAM map to ground truth: compute alignment error
  - Log metrics: coverage %, drift (m), alignment error (m)

- [X] T107 [P] [US3] Create code example 3.2.4 "Loop Closure Detection" in `/examples/module-3-isaac/lesson-3-2/detect_loop_closure.py`:
  - Subscribe to SLAM output
  - Detect loop closure events (map consistency improvement)
  - Log: loop closure confirmed, pose correction magnitude
  - Visualize: before/after map in rviz2

- [X] T108 [P] [US3] Create code example 3.2.5 "Long Trajectory SLAM" in `/examples/module-3-isaac/lesson-3-2/long_trajectory_slam.py`:
  - Simulate long robot trajectory in Gazebo (100+ meters)
  - Run SLAM, monitor drift accumulation
  - Include loop closure to correct drift
  - Measure: drift with vs. without loop closure

- [X] T109 [P] [US3] Record & edit video 3.2: "SLAM & Map Generation" (5 min)
  - Content: Run SLAM in Gazebo, watch map grow, trigger loop closure
  - Screen recording: rviz2 map visualization, terminal output, trajectory trace
  - Captions, transcript

- [X] T110 [P] [US3] Create 3 exercises in `website/docs/module-3-isaac/lesson-3-2-exercises.mdx`:
  - Exercise 3.2.1: "Run SLAM in a complex Gazebo world (warehouse) and measure coverage" (extend example 3.2.2)
  - Exercise 3.2.2: "Tune SLAM parameters (feature quality, loop closure weight) to improve map" (tuning)
  - Exercise 3.2.3: "Detect and fix map inconsistencies manually" (debugging)

### Lesson 3.3 – Navigation Stack (Nav2) & Bipedal Motion Planning (23 pages)

**Content**: Nav2 stack, costmaps, path planning, bipedal constraints, motion controllers

- [X] T111 [P] [US3] Write `website/docs/module-3-isaac/lesson-3-3-nav2.mdx` (23 pages):
  - Nav2 architecture: planner, controller, behavior tree
  - Costmaps: static (from map), dynamic (from sensors), inflated obstacles
  - Path planning: Dijkstra, A*, RRT*, comparison
  - Local planning: Dynamic Window Approach (DWA), Time Elastic Band (TEB)
  - Bipedal motion: COM stability, stepping frequency, footprint
  - Motion controllers: velocity -> joint commands for bipedal gait
  - Recovery behaviors: stuck detection, rotation, backing up
  - Include 5 diagrams (Nav2 stack, costmap inflation, path planning algorithms, DWA, bipedal footprint)

- [X] T112 [P] [US3] Create code example 3.3.1 "Nav2 Configuration" in `/examples/module-3-isaac/lesson-3-3/nav2_config.yaml`:
  - YAML file: costmap configuration (robot_radius, inflation_radius, max_obstacle_height)
  - Planner config: A* (standard)
  - Controller config: DWA (robot_base_frame, max_vel_x, max_vel_theta)
  - Behavior tree: standard navigation BT

- [X] T113 [P] [US3] Create code example 3.3.2 "Launch Nav2" in `/examples/module-3-isaac/lesson-3-3/launch_nav2.launch.py`:
  - Launch file: start Nav2 nodes (planner, controller, behavior tree, costmap)
  - Dependencies: localization (from SLAM), map, odometry
  - RViz2 config: display map, costmaps, plan, goal

- [X] T114 [P] [US3] Create code example 3.3.3 "Send Navigation Goals" in `/examples/module-3-isaac/lesson-3-3/send_goal.py`:
  - Python script: send geometry_msgs/PoseStamped goal to Nav2
  - Monitor: plan progress (path visualization in rviz2)
  - Handle: goal succeeded, goal failed, interrupted
  - Expected output: goal achieved, path executed

- [X] T115 [P] [US3] Create code example 3.3.4 "Bipedal Motion Controller" in `/examples/module-3-isaac/lesson-3-3/bipedal_controller.py`:
  - Convert velocity commands (vx, vy, vtheta) to joint commands for bipedal humanoid
  - Inverse kinematics: compute leg joint angles to achieve COM motion
  - Stability: check COM within support polygon
  - Output: joint trajectory for legs
  - Expected output: humanoid walking motion in Gazebo

- [X] T116 [P] [US3] Create code example 3.3.5 "Autonomous Navigation with Humanoid" in `/examples/module-3-isaac/lesson-3-3/autonomous_nav_humanoid.py`:
  - Combine: Nav2 (path planning) + bipedal controller (execution)
  - Send goal to Nav2
  - Receive velocity commands from Nav2 controller
  - Convert to bipedal leg commands
  - Execute in Gazebo
  - Expected output: humanoid walking autonomously to goal

- [X] T117 [P] [US3] Record & edit video 3.3: "Path Planning with Nav2" (4.5 min)
  - Content: Configure Nav2, set goal, observe path planning and execution
  - Screen recording: rviz2 costmap + plan + robot motion, terminal output
  - Captions, transcript

- [X] T118 [P] [US3] Create 3 exercises in `website/docs/module-3-isaac/lesson-3-3-exercises.mdx`:
  - Exercise 3.3.1: "Configure Nav2 for a cluttered warehouse environment" (tuning)
  - Exercise 3.3.2: "Implement a custom bipedal motion controller with gait optimization" (advanced)
  - Exercise 3.3.3: "Navigate complex obstacle course autonomously" (integration)

### Module 3 Assessment

- [X] T119 [P] [US3] Create Module 3 Quiz in `website/docs/module-3-isaac/quiz.mdx`:
  - 10 questions (7 MC + 3 SA)
  - Topics: Isaac Sim, synthetic data, SLAM, localization, Nav2, bipedal motion
  - Passing score: ≥75%

### Module 3 Capstone

- [X] T120 [P] [US3] Create Module 3 Capstone in `website/docs/module-3-isaac/capstone.mdx`:
  - **Challenge**: Deploy complete autonomous system:
    - SLAM to map environment
    - Nav2 to navigate to 5 waypoints (avoid obstacles)
    - Bipedal motion to execute trajectory
  - **Deliverable**: launch file, config files, motion controller, demo video (3 min)
  - **Evaluation**: map quality, path efficiency, obstacle avoidance success rate

**Checkpoint**: ✅ Module 3 complete (70 pages, 9 code examples, 3 videos, 9 exercises, quiz, capstone) — learners can deploy AI perception and autonomous navigation

---

## Phase 6: User Story 4 – Command Humanoid with Voice & Language (Weeks 12–14)

**Priority**: P2 (depends on US1 + US2 + US3, capstone of all 4 modules)

**Goal**: 80 pages, 10 code examples, 4 videos, 5 diagrams, 9 exercises, 10-question quiz + capstone enabling voice-commanded autonomous humanoid

**Independent Test**: Learner can issue voice commands ("walk to the table"), system transcribes, plans actions, and executes on simulated humanoid without external help

**Duration**: 3 weeks | **Leads**: Lead Author (40 hrs), Technical Editor (20 hrs), Video Producer (10 hrs intensive)

### Lesson 4.1 – Whisper Voice Interface & LLM Integration (26 pages)

**Content**: Speech-to-text (Whisper), LLM task planning (GPT-4, Mistral), task decomposition

- [X] T121 [P] [US4] Write `website/docs/module-4-vla/lesson-4-1-whisper-llm.mdx` (26 pages):
  - Whisper: multilingual, robust, local execution
  - LLM task planning: prompting strategies, few-shot learning, chain-of-thought
  - Task decomposition: high-level goal → low-level actions (move, grasp, release)
  - Safety: action grounding (commands must map to real robot capabilities)
  - Offline models: Mistral-7B, LLaMA as fallback to GPT-4
  - Context window, token limits, cost-aware inference
  - Error recovery: ambiguous commands, unsupported actions
  - Include 5 diagrams (Whisper architecture, LLM prompt structure, task decomposition tree, state machine, error recovery flow)

- [X] T122 [P] [US4] Create code example 4.1.1 "Whisper Speech-to-Text" in `/examples/module-4-vla/lesson-4-1/whisper_transcriber.py`:
  - Python node: record audio from microphone (or load from file)
  - Call Whisper model (local: openai/whisper-base, or API)
  - Transcribe to text
  - Output: publish transcribed text to ROS 2 topic `/speech_input`
  - Expected output: transcript logged

- [X] T123 [P] [US4] Create code example 4.1.2 "LLM Task Planning with GPT-4" in `/examples/module-4-vla/lesson-4-1/llm_planner_openai.py`:
  - Subscribe to `/speech_input` (transcribed command)
  - Create prompt: "Available actions: [walk, grasp, release, look]. Command: '{transcription}'. Plan: [JSON with step-by-step actions]"
  - Call GPT-4 API (use openai package)
  - Parse JSON response: list of actions
  - Publish plan to `/task_plan` (String or custom message)
  - Expected output: action plan logged

- [X] T124 [P] [US4] Create code example 4.1.3 "LLM with Local Model (Mistral)" in `/examples/module-4-vla/lesson-4-1/llm_planner_local.py`:
  - Same as 4.1.2 but using local Mistral-7B (4-bit quantized for memory efficiency)
  - Use `transformers` + `accelerate` library
  - Compare: latency (local ≈1s vs. API ≈2s), cost (free vs. $0.01 per call)
  - Expected output: action plan from local model

- [X] T125 [P] [US4] Create code example 4.1.4 "Prompt Engineering for Task Planning" in `/examples/module-4-vla/lesson-4-1/prompt_templates.py`:
  - Define reusable prompt templates (Python strings with placeholders)
  - Template 1: Simple instruction → action
  - Template 2: Complex multi-step (e.g., "pick up the red cup and place on table")
  - Template 3: Ambiguous command with clarification (use vision to disambiguate)
  - Evaluate: plan correctness on 20 diverse commands

- [X] T126 [P] [US4] Create code example 4.1.5 "Error Recovery & Fallback" in `/examples/module-4-vla/lesson-4-1/robust_planner.py`:
  - Detect invalid LLM output (malformed JSON, unsupported action)
  - Fallback: ask user for clarification via text
  - Implement: retry logic, timeout handling, graceful degradation
  - Expected output: invalid plan detected, user prompted

- [X] T127 [P] [US4] Record & edit video 4.1: "Voice Commands & LLM Task Planning" (4 min)
  - Content: Speak command, Whisper transcribes, LLM plans actions, display plan
  - Screen recording: terminal output, real-time transcription, LLM response
  - Captions, transcript

- [X] T128 [P] [US4] Create 3 exercises in `website/docs/module-4-vla/lesson-4-1-exercises.mdx`:
  - Exercise 4.1.1: "Fine-tune LLM prompt to handle 5 new command types" (prompt engineering)
  - Exercise 4.1.2: "Implement multi-turn conversation (user → command → plan → feedback → next command)" (conversation state machine)
  - Exercise 4.1.3: "Compare GPT-4 vs. local Mistral: speed, cost, accuracy" (benchmark)

### Lesson 4.2 – Multimodal Perception (CLIP & Grounding DINO) (27 pages)

**Content**: Vision-language grounding, zero-shot object detection, 3D spatial reasoning

- [X] T129 [P] [US4] Write `website/docs/module-4-vla/lesson-4-2-perception.mdx` (27 pages):
  - CLIP: vision-language model, zero-shot classification, embeddings
  - Grounding DINO: language-guided object detection (no per-object training)
  - 3D grounding: 2D detection → 3D position (depth camera)
  - Spatial reasoning: object relationships (above, left, near)
  - Scene graphs: entities + relationships + affordances
  - Failure modes: out-of-distribution images, ambiguous objects, occlusion
  - Evaluation: detection mAP, 3D localization accuracy
  - Include 5 diagrams (CLIP embeddings, Grounding DINO architecture, 2D→3D projection, scene graph, spatial relationships)

- [X] T130 [P] [US4] Create code example 4.2.1 "CLIP Zero-Shot Classification" in `/examples/module-4-vla/lesson-4-2/clip_classifier.py`:
  - Load CLIP model (openai/clip-vit-base-patch32)
  - Subscribe to camera images (`/camera/image_raw`)
  - For each frame: classify "Is this a cup? Is this a table?" using CLIP
  - Output: confidence scores for each class
  - Expected output: classification logs

- [X] T131 [P] [US4] Create code example 4.2.2 "Grounding DINO Detection" in `/examples/module-4-vla/lesson-4-2/grounding_dino_detector.py`:
  - Load Grounding DINO model
  - Query: "cup table chair" (multiple objects)
  - Run inference on camera image
  - Output: bounding boxes + confidence + class names
  - Publish detections to ROS 2 topic `/detections`
  - Expected output: detected objects with bboxes

- [X] T132 [P] [US4] Create code example 4.2.3 "3D Spatial Grounding" in `/examples/module-4-vla/lesson-4-2/spatial_grounding.py`:
  - Combine: Grounding DINO (2D detection) + depth camera (3D position)
  - For each detected object:
    - Get bounding box (2D)
    - Look up depth at box center
    - Compute 3D position (x, y, z)
    - Transform to robot frame (TF)
  - Output: 3D object positions in robot frame
  - Expected output: object pose logs

- [X] T133 [P] [US4] Create code example 4.2.4 "Scene Graph Construction" in `/examples/module-4-vla/lesson-4-2/scene_graph.py`:
  - Build scene graph: entities (detected objects) + relationships (spatial: left_of, above) + affordances (graspable, drinkable)
  - Query scene: "Where is the cup?" → retrieve 3D position + affordances
  - Extend: dynamic updates (as new objects detected)
  - Expected output: scene graph structure (nodes + edges)

- [X] T134 [P] [US4] Create code example 4.2.5 "Segment Anything (SAM) Integration" in `/examples/module-4-vla/lesson-4-2/sam_segmentation.py`:
  - Use Grounding DINO detection to initialize SAM (Segment Anything Model)
  - For each detected object: generate pixel-accurate segmentation mask
  - Output: instance masks for all objects
  - Expected output: segmentation visualization

- [X] T135 [P] [US4] Record & edit video 4.2: "Multimodal Perception: Vision + Language Grounding" (3.5 min)
  - Content: Run object detection, show 3D positions, construct scene graph
  - Screen recording: camera feed, detected objects + labels, RViz 3D visualization
  - Captions, transcript

- [X] T136 [P] [US4] Create 3 exercises in `website/docs/module-4-vla/lesson-4-2-exercises.mdx`:
  - Exercise 4.2.1: "Extend detector to recognize 10+ object types using Grounding DINO" (zero-shot)
  - Exercise 4.2.2: "Implement spatial reasoning: answer 'Is the cup on the table?'" (scene graph queries)
  - Exercise 4.2.3: "Fine-tune CLIP on custom objects for higher accuracy" (adaptation)

### Lesson 4.3 – End-to-End VLA Pipeline & Capstone Integration (27 pages)

**Content**: Full integration, state machine, error recovery, capstone walkthrough

- [X] T137 [P] [US4] Write `website/docs/module-4-vla/lesson-4-3-vla-integration.mdx` (27 pages):
  - VLA architecture: perception → cognition → action → feedback
  - State machine: idle → listening → planning → executing → done
  - Feedback loop: action outcome (success/failure) → replanning if needed
  - Multi-modal fusion: text (transcription) + vision (scene) + proprioception (joint states)
  - Execution engine: map abstract actions to ROS 2 services/topics
  - Evaluation: task success rate, time to completion, user satisfaction
  - Include 5 diagrams (VLA state machine, information flow, feedback loop, execution graph, error recovery)

- [X] T138 [P] [US4] Create code example 4.3.1 "State Machine for VLA" in `/examples/module-4-vla/lesson-4-3/vla_state_machine.py`:
  - Implement state machine using `transitions` library or custom class
  - States: IDLE (waiting for command), LISTENING (recording audio), PLANNING (calling LLM), EXECUTING (running actions), DONE
  - Transitions: on_command_received, on_plan_generated, on_execution_complete, on_error
  - Expected output: state transition logs

- [X] T139 [P] [US4] Create code example 4.3.2 "Action Executor" in `/examples/module-4-vla/lesson-4-3/action_executor.py`:
  - Subscribe to `/task_plan` (from LLM planner)
  - Map abstract actions to ROS 2 services (walk, grasp, release, look)
  - Execute sequentially or in parallel
  - Handle failures: timeout, service error → fallback
  - Output: `/action_feedback` topic with success/failure
  - Expected output: execution logs

- [X] T140 [P] [US4] Create code example 4.3.3 "Feedback & Replanning" in `/examples/module-4-vla/lesson-4-3/feedback_loop.py`:
  - Subscribe to action outcome
  - If failed: extract failure reason (e.g., "object not found")
  - Call LLM again with failure context: "Action 'grasp cup' failed because object not found. Replan."
  - Generate new plan
  - Execute new plan
  - Track: plan attempts, success on retry

- [X] T141 [P] [US4] Create code example 4.3.4 "End-to-End VLA System" in `/examples/module-4-vla/lesson-4-3/vla_system.py`:
  - Integrate all components:
    - Audio input → Whisper → transcription
    - Transcription + perception → LLM → plan
    - Plan → action executor → motion commands
    - Feedback → replanning if needed
  - Single Python node with state machine
  - Expected output: complete task execution logs

- [X] T142 [P] [US4] Create code example 4.3.5 "Web UI for VLA" in `/examples/module-4-vla/lesson-4-3/web_ui.py` (optional Flask/React frontend):
  - Simple Flask app: text input for commands (bypass Whisper for testing)
  - Display: current plan, execution status, action feedback
  - Real-time updates via WebSocket
  - Expected output: interactive web interface

- [X] T143 [P] [US4] Record & edit videos 4.3a & 4.3b:
  - Video 4.3a: "Full VLA Pipeline Demo" (5 min)
    - Content: Issue voice command, system processes end-to-end, humanoid executes task
    - Screen recording: system state, plan visualization, robot motion in Gazebo
    - Captions, transcript
  - Video 4.3b: "Humanoid Capstone Demonstration" (8 min, also serves as capstone demo video)
    - Content: 5 diverse voice commands (walk, pick up, navigate, etc.), successful execution
    - Professional edit: smooth cuts, clear narration, captions

- [X] T144 [P] [US4] Create 3 exercises in `website/docs/module-4-vla/lesson-4-3-exercises.mdx`:
  - Exercise 4.3.1: "Implement error recovery for 3 failure scenarios" (robustness)
  - Exercise 4.3.2: "Add constraints: 'Only grasp red objects'" (safety + perception)" (grounding)
  - Exercise 4.3.3: "Create custom domain for your use case" (extension)

### Module 4 Assessment

- [X] T145 [P] [US4] Create Module 4 Quiz in `website/docs/module-4-vla/quiz.mdx`:
  - 10 questions (7 MC + 3 SA)
  - Topics: Whisper, LLM planning, CLIP, Grounding DINO, state machines, feedback loops
  - Passing score: ≥75%

### Module 4 Capstone

- [X] T146 [P] [US4] Create Module 4 & Overall Capstone Project in `website/docs/capstone/capstone-project.mdx`:
  - **Challenge**: Build voice-commanded humanoid that executes complex task sequence
    - Example: "Pick up the red cup from the table and place it on the shelf"
    - System must: hear command → transcribe → understand → plan steps → execute → handle failures → provide feedback
  - **Deliverables**:
    - Source code: all 4 modules integrated (ROS 2 nodes, Gazebo sim, Isaac perception, VLA pipeline)
    - Architecture diagram: full system dataflow
    - Setup guide: reproducible on clean system in <30 min with Docker
    - Demo video: 3–5 min showing 5+ diverse commands
    - Project report: approach, challenges, lessons learned, future improvements (optional)
  - **Evaluation**: Code quality, functionality (task success rate >80%), creativity (custom tasks), documentation
  - **Extension ideas**: Multi-humanoid coordination, hardware transfer, domain-specific fine-tuning, custom LLM training

---

## Phase 7: Polish, Testing & Peer Review (Week 15)

**Purpose**: Final QA, accessibility audit, peer review feedback incorporation, performance optimization

**Duration**: 1 week | **Leads**: Tech Lead, Technical Editor, Lead Author, 10 Beta Testers | **Critical**: No new content development, only refinement

### Polish & QA Tasks

- [X] T147 Run full accessibility audit using WAVE + Axe (automated):
  - Scan all pages in `website/docs/`
  - Target: ≤5 errors per page type
  - Fix: missing alt text (images), low contrast (dark mode), ARIA labels (interactive components)
  - Verify: MathJax equations render correctly, captions on all videos

- [X] T148 [P] Validate all code examples on 3 platforms:
  - Windows WSL2: Docker Desktop, ROS 2, Gazebo
  - macOS (M1): Docker Desktop, Apple Silicon compatibility
  - Linux (Ubuntu 22.04): native Docker
  - For each example: build Docker, run, capture output, compare with expected output
  - Fix: environment variables, path issues, missing dependencies

- [X] T149 [P] Run Docusaurus build + link validator:
  - `npm run build` in `/website`
  - Check for broken internal links (0 broken)
  - Spot-check external links (GitHub, arXiv, etc.)
  - Fix: broken links, update outdated docs

- [X] T150 [P] Peer review feedback collection & incorporation:
  - Collect feedback from 10 beta testers (1–2 testers per module)
  - Feedback form: clarity (1–5), code errors (yes/no), engagement (1–5), time spent, suggestions
  - Prioritize: critical issues (broken code, confusing explanations), moderate (missing details), cosmetic (spelling)
  - Re-assign: critical issues to Lead Author for revision, cosmetic to Content Lead for proofreading

- [X] T151 [P] Proof-reading & grammar review:
  - Technical Editor reviews all 260+ pages
  - Fix: spelling, grammar, consistency (terminology, capitalization, code formatting)
  - Verify: learning objectives match content, no orphaned sections, cross-references correct

- [X] T152 [P] Performance optimization (Core Web Vitals):
  - Analyze: LCP (Largest Contentful Paint), FID (First Input Delay), CLS (Cumulative Layout Shift)
  - Optimize: image size/format (WebP), code splitting, lazy loading, CSS minification
  - Target: LCP <3s, FID <100ms, CLS <0.1
  - Tools: Lighthouse, WebPageTest

- [X] T153 [P] Search functionality validation:
  - Verify: full-text search works, returns relevant results
  - Test: module/lesson filtering, typo tolerance
  - Example queries: "ROS 2", "URDF", "SLAM", "Whisper"

- [X] T154 [P] Dark mode validation:
  - Test on all pages: contrast ratios (WCAG AA), readability
  - Verify: code blocks, images, diagrams render correctly
  - Fix: color variables, light/dark theme inconsistencies

- [X] T155 [P] Video transcripts & captions quality:
  - Review: all 15 videos have captions (auto or manual)
  - Verify: transcripts are accurate, downloadable
  - Fix: timing issues, missing captions, inaccurate transcription

- [X] T156 Create changelog & version bump:
  - Document all changes in `CHANGELOG.md` (v1.0.0)
  - Update version in `package.json`, `docusaurus.config.js`
  - Create release notes for GitHub

**Checkpoint**: ✅ All accessibility checks pass, code validates on 3 platforms, peer feedback addressed, documentation complete, site ready for production

---

## Phase 8: Launch & Deployment (Week 16)

**Purpose**: Production deployment, community launch, monitoring

**Duration**: 1 week | **Leads**: Tech Lead, Community Manager

### Deployment Tasks

- [X] T157 Deploy to production domain (physai-robotics.com):
  - Configure DNS: CNAME to Vercel
  - Enable SSL/HTTPS (automatic via Vercel)
  - Test: site accessible, responsive, dark mode working
  - Verify: analytics loaded (Plausible/GA)

- [X] T158 [P] Create GitHub Release v1.0.0:
  - Tag commit on `main` branch
  - Generate release notes (highlights, known issues, future roadmap)
  - Upload: release notes, link to deployed site

- [X] T159 [P] Launch community support channels:
  - GitHub Discussions: enable, create categories, post welcome message
  - Discord server: create channels, invite community, post introduction
  - Email newsletter signup (optional): Mailchimp or similar

- [X] T160 [P] Social media & community announcements:
  - Twitter: announce v1.0.0 release, link to site, thank contributors
  - LinkedIn: professional announcement, learning path diagram
  - ROS 2 Discourse: post in tutorials category, link to book
  - r/robotics: share to Reddit community
  - Include: learning outcomes, free/open-source positioning, call-to-action (star on GitHub, complete module, share feedback)

- [X] T161 [P] Community engagement setup:
  - Prepare response templates for common questions (troubleshooting, module order, prerequisites)
  - Set support SLA: respond to first-time questions <7 days
  - Create FAQ document linking to GitHub Discussions
  - Assign Community Manager: monitor channels, respond, triage issues

- [X] T162 Create post-launch survey (Typeform/Google Forms):
  - Q1: How did you hear about this book?
  - Q2: Which modules did you complete?
  - Q3: Rate clarity, engagement, code quality (1–5)
  - Q4: What was missing or could improve?
  - Q5: Will you complete the capstone?
  - Results used for v1.1 roadmap

- [X] T163 [P] Monitor site stability (first 48 hours):
  - Check: uptime (>99.9%), response time (<1s), error logs
  - Be on-call for critical issues (5xx errors, service outages)
  - Fix: deployment issues, broken links, missing dependencies
  - Document: incident reports, resolution time

- [X] T164 [P] Analytics baseline capture:
  - Record initial metrics: page views, unique users, module completion rate
  - Set up dashboards: weekly metrics review
  - Define success: ≥100 unique visitors/week, ≥10% module 1 completion

---

## Phase 9: Polish & Cross-Cutting Concerns (Final Phase)

**Purpose**: Documentation refinement, knowledge base, community assets

**Duration**: Ongoing (no time limit, quality improvements)

### Documentation Tasks

- [X] T165 Create comprehensive `docs/QUICKSTART.md`:
  - 5-minute setup: clone repo, `npm install`, `npm start`
  - Test: run 1 code example in Docker
  - Verify: Docusaurus running locally

- [X] T166 [P] Create `docs/DEPLOYMENT.md`:
  - How to deploy to Vercel
  - Custom domain setup (DNS, SSL)
  - Environment variables, secrets management
  - Rollback procedure

- [X] T167 [P] Create `docs/CONTRIBUTING.md` (enhance existing):
  - Code style guide: Python (PEP 8), YAML, markdown
  - How to submit PRs: fork, branch naming, commit message format
  - Testing expectations: all code examples must run on 3 platforms
  - Review process: CI/CD checks, peer review, merge

- [X] T168 [P] Create `docs/EXTENDING.md`:
  - How to add new modules (5th module: advanced capstone, hardware, etc.)
  - Template: spec, plan, tasks generation
  - Code review checklist for new content

- [X] T169 Create `CONTRIBUTORS.md`:
  - Recognition: list contributors (authors, reviewers, beta testers, translators)
  - Roles: content authors, code reviewers, video producers, community managers
  - How to get added: make first contribution via PR

- [X] T170 [P] Create video index in `website/static/video-index.md`:
  - Central catalog: all 15+ videos with links, duration, transcript links
  - Organized by module
  - Searchable

- [X] T171 [P] Create `docs/FAQ.md` (knowledge base):
  - Common installation issues (ROS 2, Gazebo, Docker) + solutions
  - Code example errors + fixes
  - Best practices for learning (module order, time commitment, prerequisites)
  - Hardware requirements (CPU, GPU, RAM recommendations)
  - Offline learning options

- [X] T172 [P] Create `docs/ROADMAP.md`:
  - v1.0.0: current release
  - v1.1 (3 months): community feedback improvements, bug fixes
  - v1.2 (6 months): new module (hardware transfer), advanced capstone
  - v2.0 (TBD): major revision (new tech, updated frameworks)

---

## Dependencies & Execution Order

### Critical Path

```
Phase 1 (Weeks 1-2): Setup & Infrastructure
  ↓ (blocking all content)
Phase 2: Foundational (Weeks 1-3): Content templates, Docker, CI/CD
  ↓ (blocking all module work)
Phase 3 (Weeks 3-5): Module 1 (ROS 2) — P1
  ↓ (Module 2 depends on Module 1 concepts)
Phase 4 (Weeks 6-8): Module 2 (Gazebo) — P1
  ↓ (Module 3 depends on Modules 1 & 2)
Phase 5 (Weeks 9-11): Module 3 (Isaac) — P2
  ↓ (Module 4 depends on Modules 1-3)
Phase 6 (Weeks 12-14): Module 4 (VLA) — P2
  ↓
Phase 7 (Week 15): Polish & QA
  ↓
Phase 8 (Week 16): Launch
```

### Parallelizable Opportunities (within Phase)

**Phase 1 Setup** (can run in parallel):
- T001–T007: Project structure, Docusaurus config, GitHub setup
- T010–T014: Docker files for all 4 modules
- T017–T021: All 5 React components

**Phase 2 Foundational** (can run in parallel):
- T032–T035: All documentation templates
- T036–T037: Validation scripts
- T039–T043: Analytics, community channels

**Phase 3 Module 1** (can run in parallel):
- Content writing: Lesson 1.1, 1.2, 1.3 (3 writers)
- Code examples: 4 examples per lesson (4 tasks in parallel per writer)
- Videos: script, record, edit in parallel (separate video producer)

**Phase 3+ All Modules**:
- Writing + coding: Different modules can proceed in parallel if team capacity allows
- Video production: Can lag content by 1 week (script in advance)

---

## Task Summary & Metrics

### Total Task Count
- **Phase 1 (Setup)**: 31 tasks (T001–T031)
- **Phase 2 (Foundational)**: 12 tasks (T032–T043)
- **Phase 3 (Module 1)**: 23 tasks (T046–T068)
- **Phase 4 (Module 2)**: 24 tasks (T070–T094)
- **Phase 5 (Module 3)**: 25 tasks (T095–T120)
- **Phase 6 (Module 4)**: 28 tasks (T121–T146)
- **Phase 7 (Polish)**: 10 tasks (T147–T156)
- **Phase 8 (Launch)**: 8 tasks (T157–T164)
- **Phase 9 (Cross-cutting)**: 8 tasks (T165–T172)

**Total: 169 tasks**

### Tasks per User Story
- **US1 (Module 1)**: 46 tasks (setup + Module 1 content + quiz + capstone)
- **US2 (Module 2)**: 44 tasks (Module 2 content + quiz + capstone)
- **US3 (Module 3)**: 44 tasks (Module 3 content + quiz + capstone)
- **US4 (Module 4)**: 44 tasks (Module 4 content + quiz + capstone)
- **Cross-cutting (Setup, Polish, Launch)**: 49 tasks (foundational + QA + deployment)

### Deliverables Summary
| Item | Count | Notes |
|------|-------|-------|
| **Pages of Content** | 260+ | 60 (M1) + 50 (M2) + 70 (M3) + 80 (M4) + 20 (capstone/appendix) |
| **Code Examples** | 34 | 8 (M1) + 7 (M2) + 9 (M3) + 10 (M4) |
| **Videos** | 15+ | 4 (M1) + 3 (M2) + 3 (M3) + 4 (M4) + 1 (capstone demo) |
| **Diagrams** | 22+ | 4–5 per module |
| **Exercises** | 40+ | 8 (M1) + 6 (M2) + 9 (M3) + 9 (M4) + capstone |
| **Quiz Questions** | 40 | 10 per module |
| **Interactive Components** | 5 | CodeSandbox, URDFViewer, Quiz, VideoEmbed, AudioPlayer |
| **Dockerfiles** | 6 | 1 per module + compose file |
| **Datasets** | Multiple | URDF models, Gazebo worlds, sensor data, training data |

---

## MVP Scope (Minimal Viable Product)

To launch quickly, focus on **Module 1 (ROS 2) only**:

**Deliverables**:
- 60 pages of Module 1 content (3 lessons + quiz)
- 8 code examples (tested on 3 platforms)
- 4 videos (YouTube)
- 8 exercises with solutions
- 1 capstone (multi-node ROS 2 system)
- Docusaurus site with Module 1 visible, Modules 2–4 placeholders
- GitHub repo with CI/CD working
- Live on staging Vercel site

**Timeline**: 5 weeks (Weeks 1–5)

**Team**: Lead Author (40 hrs), Tech Lead (40 hrs), Video Producer (10 hrs), Technical Editor (20 hrs)

**Success Metric**: ≥50 users complete Module 1, ≥80% pass quiz, capstone projects submitted

**Then increment**: Add Module 2 (Weeks 6–8), Module 3 (Weeks 9–11), Module 4 (Weeks 12–14)

---

## Parallel Execution Example

**Scenario**: Full team (4 people) working Weeks 3–5 (Module 1)

```
Week 3:
  Tech Lead: [P] T017–T021 (React components) — 40 hrs
  Lead Author: [P] T046, T053, T059 (lesson writing) — 40 hrs
  Video Producer: [P] Script videos 1.1, 1.2, 1.3, 1.4
  Tech Editor: Code review T047, T048, T049, T050 (4 examples)

Week 4:
  Tech Lead: T051 (video 1.1 integration)
  Lead Author: [P] T052, T058, T067 (exercises)
  Video Producer: Record & edit all 4 videos — 40 hrs
  Tech Editor: [P] Validate all 8 examples on 3 platforms — 40 hrs

Week 5:
  Tech Lead: [P] T068 (Module 1 quiz)
  Lead Author: [P] T069 (capstone)
  Video Producer: [P] Upload, caption, create transcripts
  Tech Editor: Peer review feedback incorporation
```

**Result**: Module 1 complete, all tasks in parallel, no bottlenecks

---

## Format Validation Checklist

Every task MUST follow format: `- [ ] [ID] [P?] [Story?] Description with file path`

✅ **Valid examples**:
- `- [X] T001 Create monorepo structure...`
- `- [X] T010 [P] Create `docker/Dockerfile.module-1`...`
- `- [X] T046 [P] [US1] Write `website/docs/module-1-ros2/lesson-1-1.mdx`...`
- `- [X] T147 Run full accessibility audit...`

❌ **Invalid** (missing components):
- `- [ ] Create project structure` (missing ID)
- `T001 Create project structure` (missing checkbox)
- `- [X] T046 [US1] Write lesson` (missing file path)

---

**Task Generation Version**: 1.0.0
**Total Tasks**: 169
**Created**: 2025-12-30
**Status**: ✅ Complete and ready for execution
