/**
 * Main App Component
 */
import { useState, useRef } from 'react';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Breadcrumb from './components/Layout/Breadcrumb';
import SearchBox from './components/Search/SearchBox';
import TopicFilter from './components/Search/TopicFilter';
import Hero from './components/Content/Hero';
import LoadingSkeleton from './components/Content/LoadingSkeleton';
import AnswerCard from './components/Content/AnswerCard';
import PostDetail from './components/Content/PostDetail';
import { searchKnowledge } from './services/api';

function App() {
  // State management
  const [currentItem, setCurrentItem] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [isHome, setIsHome] = useState(true);
  const [showPostOnly, setShowPostOnly] = useState(false);
  const [postContentData, setPostContentData] = useState({});
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  /**
   * Handle search action
   */
  const handleSearch = async (query) => {
    if (!query?.trim()) {
      setHasSearched(false);
      setCurrentItem(null);
      setError(null);
      return;
    }

    setSearchQuery(query);
    setIsLoading(true);
    setHasSearched(true);
    setError(null);
    setIsHome(true);
    setShowPostOnly(false);

    try {
      const result = await searchKnowledge(query);
      setCurrentItem(result);
    } catch (err) {
      setError(err.message || 'An error occurred while searching.');
      setCurrentItem(null);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle topic tag click
   */
  const handleTagClick = (tagValue) => {
    setSearchQuery(tagValue);
    if (inputRef.current) {
      inputRef.current.setValue(tagValue);
    }
    handleSearch(tagValue);
  };

  /**
   * Handle viewing a post detail
   */
  const handleViewPost = (data) => {
    setPostContentData(data);
    setShowPostOnly(true);
    setIsHome(false);
  };

  /**
   * Handle returning to home
   */
  const handleHomeClick = () => {
    setIsHome(true);
    setShowPostOnly(false);
  };

  /**
   * Render main content based on current state
   */
  const renderMainContent = () => {
    if (!hasSearched) {
      return <Hero />;
    }

    if (isLoading) {
      return <LoadingSkeleton />;
    }

    if (error) {
      return (
        <div className="alert alert-error">
          <span>{error}</span>
        </div>
      );
    }

    if (currentItem) {
      return (
        <AnswerCard data={currentItem} onViewPost={handleViewPost} />
      );
    }

    return <Hero />;
  };

  return (
    <div className="container">
      <Header />
      
      <SearchBox ref={inputRef} onSearch={handleSearch} />
      
      <TopicFilter onTagClick={handleTagClick} />
      
      <main>
        <Breadcrumb isHome={isHome} onHomeClick={handleHomeClick} />
        
        {isHome && renderMainContent()}
        
        {!isHome && showPostOnly && (
          <PostDetail postData={postContentData} />
        )}
      </main>
      
      <Footer />
    </div>
  );
}

export default App;

