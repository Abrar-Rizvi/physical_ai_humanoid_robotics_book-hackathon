import React from 'react';
import styles from './styles.module.css';

// TypeScript interfaces
interface ContentCardProps {
  title: string;
  content: string[];
  iconType?: 'check' | 'nike';
  className?: string;
}

interface HomepageContentSectionProps {
  className?: string;
  heading?: string;
}

// ContentCard sub-component
const ContentCard: React.FC<ContentCardProps> = ({
  title,
  content,
  iconType = 'check',
  className = ''
}) => {
  return (
    <div className={`${styles.card} ${className}`}>
      <h3 className={styles.cardTitle}>{title}</h3>
      <div className={styles.cardContent}>
        <ul className={styles.bulletList}>
          {content.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const HomepageContentSection: React.FC<HomepageContentSectionProps> = ({
  className = '',
  heading = 'A New Chapter in Robotics: Beyond Automation'
}) => {
  // Placeholder content for the cards
  const leftCardContent = {
    title: "Traditional Robotics",
    content: [
      "Predetermined behaviors",
      "Rule-based systems",
      "Limited adaptability"
    ]
  };

  const rightCardContent = {
    title: "Physical AI Evolution",
    content: [
      "Learning from environment",
      "Adaptive behaviors",
      "Real-world interaction"
    ]
  };

  return (
    <section className={`${styles.contentSection} ${className}`}>
      <h2 className={styles.sectionHeading}>
        {heading}
      </h2>
      <div className={styles.gridContainer}>
        <ContentCard
          title={leftCardContent.title}
          content={leftCardContent.content}
        />
        <ContentCard
          title={rightCardContent.title}
          content={rightCardContent.content}
        />
      </div>
    </section>
  );
};

export default HomepageContentSection;