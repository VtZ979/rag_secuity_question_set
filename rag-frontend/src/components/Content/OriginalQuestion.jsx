/**
 * Original Question Component - Displays the original Stack Overflow question
 */
export default function OriginalQuestion({ question }) {
  if (!question) return null;

  return (
    <div
      tabIndex={0}
      className="collapse collapse-open bg-base-100 border-base-300 border"
    >
      <div className="collapse-title font-semibold">Original Question:</div>
      <div className="collapse-content text-sm">{question}</div>
    </div>
  );
}

