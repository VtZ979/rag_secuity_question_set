
export default function OriginalQuestion({ question }) {
    return (
        <div tabIndex={0} className="collapse collapse-open bg-white border-gray-300 border rounded-lg shadow-sm">
            <div className="collapse-title font-semibold text-gray-900 bg-gray-50">Original Question:</div>
            <div className="collapse-content text-sm text-gray-800 leading-relaxed p-4">
                <div className="whitespace-pre-wrap break-words">
                    {question}
                </div>
            </div>
        </div>
    )
}