export default function Filter({ onTagClick }) {
    const tags = ['Java', 'PHP', 'XSS', 'SQL Injection', 'Access Control', 'Authentication'];
    return (
        <div className="popular-topics">
        <span className="topic-label">Popular Topics:</span>
        <div className="topics-list">
        {tags.map((tag) => (
            <span key={tag} onClick={() => onTagClick(tag)} className="topic">{tag}</span>
        ))}
        </div>
    </div>
    )
}


