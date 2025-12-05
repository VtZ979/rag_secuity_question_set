/**
 * Topic Filter Component - Popular security topics
 */
export default function TopicFilter({ onTagClick }) {
  const topics = [
    'Java',
    'PHP',
    'XSS',
    'SQL Injection',
    'Access Control',
    'Authentication',
    'Encryption',
    'OAuth'
  ];

  return (
    <div className="popular-topics">
      <span className="topic-label">Popular Topics:</span>
      <div className="topics-list">
        {topics.map((topic) => (
          <span
            key={topic}
            onClick={() => onTagClick(topic)}
            className="topic"
            role="button"
            tabIndex={0}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                onTagClick(topic);
              }
            }}
          >
            {topic}
          </span>
        ))}
      </div>
    </div>
  );
}

