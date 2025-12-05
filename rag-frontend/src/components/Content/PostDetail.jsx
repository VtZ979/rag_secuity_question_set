/**
 * Post Detail Component - Detailed view of a Stack Overflow post
 */
import OriginalQuestion from './OriginalQuestion';

export default function PostDetail({ postData }) {
  if (!postData) return null;

  const {
    llmSolution,
    challenges,
    skills,
    category,
    similarity,
    sentimental,
    accepted_answers,
    ori_question,
    answer_similarity
  } = postData;

  return (
    <div className="post-detail">
      <OriginalQuestion question={ori_question} />

      <div className="mt-6 border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <InfoRow label="Category" value={category} />
          <InfoRow label="Similarity" value={similarity} />
          <InfoRow label="Answer Similarity" value={answer_similarity} />
          <InfoRow label="Sentiment" value={sentimental} />
          <InfoRow label="Challenges" value={challenges} multiline />
          <InfoRow label="Skills" value={skills} multiline />
          <InfoRow label="LLM Solution" value={llmSolution} />
          <InfoRow label="Accepted Answers" value={accepted_answers} multiline />
        </dl>
      </div>
    </div>
  );
}

/**
 * Info Row Component
 */
function InfoRow({ label, value, multiline = false }) {
  return (
    <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
      <dt className="text-sm/6 font-medium text-gray-900">{label}</dt>
      <dd
        className={`mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0 ${
          multiline ? 'whitespace-pre-line' : ''
        }`}
      >
        {value || 'N/A'}
      </dd>
    </div>
  );
}

