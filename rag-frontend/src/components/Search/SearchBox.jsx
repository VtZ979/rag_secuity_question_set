/**
 * Search Box Component
 */
import { useRef, forwardRef, useImperativeHandle } from 'react';

const SearchBox = forwardRef(({ onSearch, placeholder = "Search for security topics..." }, ref) => {
  const inputRef = useRef(null);

  // Expose input ref to parent component
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    setValue: (value) => {
      if (inputRef.current) {
        inputRef.current.value = value;
      }
    },
    getValue: () => inputRef.current?.value || ''
  }));

  const handleSearch = () => {
    const query = inputRef.current?.value.trim();
    if (query) {
      onSearch(query);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-box flex flex-wrap items-center">
      <input
        type="text"
        ref={inputRef}
        placeholder={placeholder}
        onKeyPress={handleKeyPress}
        className="search-input"
      />
      <button 
        className="btn btn-ghost" 
        onClick={handleSearch}
        aria-label="Search"
      >
        Search
      </button>
    </div>
  );
});

SearchBox.displayName = 'SearchBox';

export default SearchBox;

