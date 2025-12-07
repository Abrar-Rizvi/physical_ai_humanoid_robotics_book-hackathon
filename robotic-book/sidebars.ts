import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundation',
      items: [
        'foundation/chapter1-physical-ai-fundamentals',
        'foundation/chapter2-embodied-intelligence',
      ],
    },
    {
      type: 'category',
      label: 'Analysis',
      items: [
        'analysis/chapter3-ros2-nervous-system',
        'analysis/chapter4-ros2-communication-patterns',
        'analysis/chapter5-gazebo-unity-digital-twin',
        'analysis/chapter6-nvidia-isaac-sim-ecosystem',
      ],
    },
    {
      type: 'category',
      label: 'Synthesis',
      items: [
        'synthesis/chapter7-vision-language-action-pipelines',
        'synthesis/chapter8-capstone-autonomous-humanoid',
      ],
    },
  ],
};

export default sidebars;
