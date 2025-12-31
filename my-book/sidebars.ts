import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Physical AI and Humanoid Robotics Book - Sidebar Configuration
 * Hierarchical structure: Intro → 4 Modules (3 lessons each) → Capstone → Appendix
 */
const sidebars: SidebarsConfig = {
  bookSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '📖 Introduction',
    },
    {
      type: 'category',
      label: '🤖 Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/lesson-1-1-middleware',
        'module-1-ros2/lesson-1-2-topics-services',
        'module-1-ros2/lesson-1-3-urdf',
        'module-1-ros2/exercises-1',
        'module-1-ros2/quiz-1',
        'module-1-ros2/capstone-1',
      ],
    },
    {
      type: 'category',
      label: '🌍 Module 2: The Digital Twin (Gazebo & Physics)',
      items: [
        'module-2-gazebo/lesson-2-1-physics',
        'module-2-gazebo/lesson-2-2-sensors',
        'module-2-gazebo/lesson-2-3-control',
        'module-2-gazebo/exercises-2',
        'module-2-gazebo/quiz-2',
        'module-2-gazebo/capstone-2',
      ],
    },
    {
      type: 'category',
      label: '🧠 Module 3: The AI-Robot Brain (NVIDIA Isaac & Nav2)',
      items: [
        'module-3-isaac/lesson-3-1-isaac-sim',
        'module-3-isaac/lesson-3-2-slam',
        'module-3-isaac/lesson-3-3-nav2',
        'module-3-isaac/exercises-3',
        'module-3-isaac/quiz-3',
        'module-3-isaac/capstone-3',
      ],
    },
    {
      type: 'category',
      label: '🎤 Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vla/lesson-4-1-whisper-llm',
        'module-4-vla/lesson-4-2-perception',
        'module-4-vla/lesson-4-3-vla-integration',
        'module-4-vla/exercises-4',
        'module-4-vla/quiz-4',
        'module-4-vla/capstone-4',
      ],
    },
    {
      type: 'category',
      label: '🎯 Capstone Project',
      items: [
        'capstone/overview',
        'capstone/submission-guide',
      ],
    },
    {
      type: 'category',
      label: '📚 Appendix',
      items: [
        'appendix/glossary',
        'appendix/troubleshooting',
        'appendix/references',
        'appendix/resources',
      ],
    },
  ],
};

export default sidebars;
