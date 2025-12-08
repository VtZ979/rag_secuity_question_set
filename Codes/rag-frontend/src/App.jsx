import { useState, useEffect } from 'react'
import { useRef } from 'react';

import Answer from './components/Answer.jsx'
import Footer from './components/Footer.jsx'
import Hero from './components/Hero.jsx'
import Header from './components/Header.jsx'
import Skeleton from './components/Skeleton.jsx'
import Filter from './components/Filter.jsx'
import PostContent from './components/PostContent.jsx'
import { searchKnowledge } from './services/searchService.js'


function App() {
  const [currentItem, setCurrentItem] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [isHome, setIsHome] = useState(true);
  const [showPostOnly, setShowPostOnly] = useState(false);
  const [postContentData, setPostContentData] = useState({});
  const inputRef = useRef(null);

  const handleTagClick = (tagValue) => {
    setSearchQuery(tagValue);
    if (inputRef.current) {
      inputRef.current.value = tagValue; 
    }
  };

  const handleSearch = async (e) => {
    // const query = e.target.value
    const query = inputRef.current?.value.trim(); 
    setSearchQuery(query)
    
    if (query.trim()) {
      setIsLoading(true)
      setHasSearched(true)
      try {
        const result = await searchKnowledge(query)
        setCurrentItem(result)
        setIsHome(true);
        setShowPostOnly(false);
      } catch (error) {
        setCurrentItem(null)
      } finally {
        setIsLoading(false)
      }
    } else {
      setHasSearched(false)
      setCurrentItem(null)
    }
  }

  const renderMainContent = () => {
    if (!hasSearched) {
      return <Hero />
    }
    if (isLoading) {
      return <Skeleton />
    }
    if (currentItem) {
      return <Answer data={currentItem} 
      onUpdateBreadcrumb={() => setIsHome(false)}  
      onShowPostOnly={() => setShowPostOnly(true)}
      onViewPost={handleViewPost}
      />
    }
    return <Hero />
  }

  const handleViewPost = (data) => {
    console.log('View Post clicked with data:', data);
    setPostContentData(data);     
    setShowPostOnly(true);        
    setIsHome(false);             
  };

  const handleBackToResults = () => {
    setShowPostOnly(false);
    setIsHome(true);
  };

  return (
    <div className="container">
      <Header />
      <div className="search-box flex flex-wrap items-center">
          <input 
            type="text" 
            ref={inputRef}
            placeholder="Search for security topics..." 
          />
          <button className="btn btn-ghost" onClick={handleSearch}>Search</button>
      </div>
      
      <Filter onTagClick={handleTagClick}/>
      <main>
        <div className="breadcrumbs text-base text-gray-500">
          <ul>
              <li>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="h-4 w-4 stroke-current">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                </svg>
                <a href="#" onClick={() => setIsHome(true)}>Home</a>
              </li>
              {!isHome && <li>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  className="h-4 w-4 stroke-current">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span className="text-gray-900 font-medium">Stack Overflow Question</span>
              </li>}
          </ul>
        </div>
        {isHome && renderMainContent()}
        {!isHome && showPostOnly && <PostContent postData={postContentData} onBack={handleBackToResults} />}
      </main>
      <Footer/>
    </div>
  )
}

export default App