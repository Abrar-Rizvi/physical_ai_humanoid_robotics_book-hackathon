import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

interface FeatureCardProps {
  title: string;
  description: string;
  imgPath: string;
  imageAlt: string;
  icon?: React.ComponentType<React.SVGProps<SVGSVGElement>>;
}

// TODO: Replace placeholder image URLs with optimized images after running image optimization tasks
// See tasks.md T002-T004, T006-T008 for image preparation instructions
const FEATURE_LIST: FeatureCardProps[] = [
  {
    title: "Industry-Standard Tools",
    description: "Master ROS 2, Gazebo, and MoveIt—the same frameworks powering Boston Dynamics, Tesla, and leading robotics labs worldwide.",
    imgPath: "/img/industry.jpg",
    imageAlt: "Humanoid robot demonstrating bipedal locomotion and balance",
  },
  {
    title: "Real Hardware Integration",
    description: "Go beyond simulation with hands-on deployment to real robots. Learn sensor fusion, motor control, and safety-critical systems.",
    imgPath: "/img/row.jpg",
    imageAlt: "Industrial robotic arm performing precision manipulation tasks",
  },
  {
    title: "AI-Powered Intelligence",
    description: "Integrate LLMs, computer vision, and VLA models to create robots that perceive, reason, and act autonomously in dynamic environments.",
    imgPath: "/img/artificial-intelligence.jpg",
    imageAlt: "Neural network visualization representing AI-driven robot cognition",
  },
];

function FeatureCard({
  title,
  description,
  imgPath,
  imageAlt,
  icon: Icon,
}: FeatureCardProps) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureCardImage}>
        <img
            src={imgPath}
            alt={imageAlt}
            className={styles.cardImage}
            loading="lazy"
          />
      </div>
      <div className={styles.featureCardContent}>
        {Icon && <Icon className={styles.featureIcon} />}
        <Heading as="h3" className={styles.featureHeading}>
          {title}
        </Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.featuresContainer}>
      <div className={styles.featuresGrid}>
        {FEATURE_LIST.map((props, idx) => (
          <FeatureCard key={idx} {...props} />
        ))}
      </div>
    </section>
  );
}
