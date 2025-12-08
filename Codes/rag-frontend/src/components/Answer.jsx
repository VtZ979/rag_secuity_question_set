import { BookOpenIcon } from '@heroicons/react/20/solid'

export default function Answer({ data , onUpdateBreadcrumb , onShowPostOnly, onViewPost}) {

    if (!data?.answer) return null

    const handleExpand = (item) => {
        onUpdateBreadcrumb();
        onShowPostOnly();
        onViewPost(item)
    };

    const { 
      user_question,
      llm_answer,
      challenges,
      skills,
      category 
    } = data.answer
  
    const related_posts = data.related_post || []

  return (
    <div>
      <div className="px-4 sm:px-0">
        <h3 className="text-base/7 font-semibold text-gray-900">Knowledge Base Answer</h3>
      </div>
      <div className="mt-6 border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Category</dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0">{category}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Challenges</dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0 whitespace-pre-line">{challenges}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Skills</dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0 whitespace-pre-line">{skills}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">LLM Answer</dt>
            <dd className="mt-1 text-sm/6 text-gray-700 sm:col-span-2 sm:mt-0">{llm_answer}</dd>
          </div>

          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Related Stack Overflow Questions</dt>
            <dd className="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              <ul role="list" className="divide-y divide-gray-100 rounded-md border border-gray-200">
              { related_posts.map((item) => (
                <li key={item.post_id || item.id} className="flex items-center justify-between py-4 pr-5 pl-4 text-sm/6">
                    <div className="flex w-0 flex-1 items-center">
                        <BookOpenIcon aria-hidden="true" className="size-5 shrink-0 text-gray-400"/>
                        <div className="ml-4 flex min-w-0 flex-1 gap-2">
                            <span className="truncate font-medium">{item.title}</span>
                        </div>
                    </div>
                    <div className="ml-4 shrink-0">
                        <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500" onClick={() => handleExpand(item)} >
                            View
                        </a>
                    </div>
                </li>
             ))}
              </ul>
            </dd>
          </div>
        </dl>
      </div>
    </div>
  )
}