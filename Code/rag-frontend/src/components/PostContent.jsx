import { BookOpenIcon, ArrowLeftIcon } from '@heroicons/react/20/solid'
import OriginalQuestion from './OriginalQuestion.jsx'

export default function PostContent({ postData, onBack }) {
      console.log("PostContent----");
      console.log(postData);
    
      const {
        challenges,
        skills,
        category,
        similarity,
        sentimental,
        accepted_answers,
        ori_question
      } = postData;
  

  return (
    <div>
      {/* Back Button */}
      <div className="mb-4">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
        >
          <ArrowLeftIcon className="h-4 w-4" />
          Back to Results
        </button>
      </div>
      {/* <div className="px-4 sm:px-0">
        <h3 className="text-base/7 font-semibold text-gray-900">Stack Overflow Post Content</h3>
      </div> */}
      <OriginalQuestion question={ori_question}/>

      <div className="mt-6 border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Category</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0">{category}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Similarity</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0">{similarity}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Sentiment</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0">{sentimental}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Challenges</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0 whitespace-pre-wrap break-words leading-relaxed">{challenges}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Skills</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0 whitespace-pre-wrap break-words leading-relaxed">{skills}</dd>
          </div>
          <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
            <dt className="text-sm/6 font-medium text-gray-900">Accepted Answers</dt>
            <dd className="mt-1 text-sm/6 text-gray-800 sm:col-span-2 sm:mt-0 whitespace-pre-wrap break-words leading-relaxed">
              {accepted_answers}
            </dd>
          </div>

        </dl>
      </div>
    </div>
  )
}