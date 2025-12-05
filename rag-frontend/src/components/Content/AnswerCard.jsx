/**
 * Answer Card Component - Main answer display
 */
import { BookOpenIcon } from '@heroicons/react/20/solid';

export default function AnswerCard({ data, onViewPost }) {
  if (!data?.answer) return null;

  const {
    user_question,
    llm_answer,
    challenges,
    skills,
    category
  } = data.answer;

  const related_posts = data.related_post || [];

  return (
    <div className="answer-card">
      <div className="px-4 sm:px-0">
        <h3 className="text-base/7 font-semibold text-gray-900">
          Knowledge Base Answer
        </h3>
      </div>
      
      <div className="mt-6 border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <InfoRow label="Category" value={category} />
          <InfoRow label="Challenges" value={challenges} multiline />
          <InfoRow label="Skills" value={skills} multiline />
          <InfoRow label="LLM Answer" value={llm_answer} />
          
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">
              Related Stack Overflow Questions
            </dt>
            <dd className="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              {related_posts.length > 0 ? (
                <ul
                  role="list"
                  className="divide-y divide-gray-100 rounded-md border border-gray-200"
                >
                  {related_posts.map((item, index) => (
                    <li
                      key={item.post_id || index}
                      className="flex items-center justify-between py-4 pr-5 pl-4 text-sm/6"
                    >
                      <div className="flex w-0 flex-1 items-center">
                        <BookOpenIcon
                          aria-hidden="true"
                          className="size-5 shrink-0 text-gray-400"
                        />
                        <div className="ml-4 flex min-w-0 flex-1 gap-2">
                          <span className="truncate font-medium">
                            {item.title}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4 shrink-0">
                        <button
                          className="font-medium text-indigo-600 hover:text-indigo-500"
                          onClick={() => onViewPost(item)}
                        >
                          View
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No related posts found.</p>
              )}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}

/**
 * Info Row Component - Reusable row for displaying key-value pairs
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

