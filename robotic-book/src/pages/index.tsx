import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';



// Hero Content Constants
const HERO_CONTENT = {
  headline: "Master Physical AI & Build Real Humanoid Robots",
  subheadline: "The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware",
  // paragraph: "Learn to design, simulate, and deploy autonomous humanoid robots from scratch. This comprehensive course combines cutting-edge AI models with industry-standard robotics frameworks, giving you the skills to build the future of physical intelligence.",
  ctaText: "Start Learning Free 🚀",
  ctaLink: "/docs/intro",
};

// Hero Image Constants
// TODO: Replace placeholder URLs with optimized images after running image optimization tasks
// See tasks.md T001-T012 for image preparation instructions
const HERO_IMAGE = {
  imgPath: "/img/ai-robot.png", // Using PNG as a placeholder, as per user example format.
  alt: "Futuristic humanoid robot showcasing advanced Physical AI capabilities",
};

function HomepageHeader() {
  return (
    <header className={styles.heroContainer}>
      <div className={styles.heroVideoSection}>
        <div className={styles.heroVideoContainer}>
          <video
            autoPlay
            muted
            loop
            playsInline
            poster="/img/hero-robot.jpg"
            className={styles.heroVideo}
          >
            <source src="/video/hero-book.mp4" type="video/mp4" />
          </video>
        </div>
      </div>

      <div className={styles.heroTextSection}>
        <Heading as="h1" className={styles.heroHeadline}>
          {HERO_CONTENT.headline}
        </Heading>
        <Heading as="h2" className={styles.heroSubheadline}>
          {HERO_CONTENT.subheadline}
        </Heading>
        {/* <p className={styles.heroParagraph}>
          {HERO_CONTENT.paragraph}
        </p> */}
        <Link className={styles.heroCTA} to={HERO_CONTENT.ctaLink}>
          {HERO_CONTENT.ctaText}
        </Link>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Learn Physical AI & Humanoid Robotics`}
      description="Master ROS 2, Gazebo, MoveIt, LLMs and real robot hardware with hands-on projects">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      
      
      </main>
    </Layout>
  );
}
