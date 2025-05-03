
import React, { useEffect, useState } from 'react';
import { useCodePosts, CodePost } from '@/contexts/CodePostsContext';
import CodeCard from '@/components/Code/CodeCard';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Filter } from 'lucide-react';
import { useLocation } from 'react-router-dom';

const BrowsePage: React.FC = () => {
  const location = useLocation();
  const { posts } = useCodePosts();
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredPosts, setFilteredPosts] = useState<CodePost[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');
  
  // Парсим query параметры из URL
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const searchParam = queryParams.get('search');
    if (searchParam) {
      setSearchQuery(searchParam);
    }
  }, [location.search]);

  // Получаем уникальные языки из постов
  const languages = Array.from(new Set(posts.map(post => post.language)));

  // Фильтрация постов на основе поиска и языка
  useEffect(() => {
    let result = posts;
    
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(post => 
        post.title.toLowerCase().includes(query) || 
        post.description.toLowerCase().includes(query) ||
        post.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }
    
    if (selectedLanguage) {
      result = result.filter(post => post.language === selectedLanguage);
    }
    
    // Сортируем по дате от новых к старым
    result = [...result].sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
    
    setFilteredPosts(result);
  }, [posts, searchQuery, selectedLanguage]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Фильтрация уже происходит в useEffect
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-stretch md:items-center gap-4">
        <h1 className="text-3xl font-bold">Обзор публикаций</h1>
        
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-grow">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Поиск по названию, описанию или тегам"
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button type="submit">Найти</Button>
        </form>
      </div>

      <div className="flex flex-wrap gap-2 items-center">
        <Filter className="h-4 w-4" />
        <span className="font-medium mr-2">Фильтр по языку:</span>
        <Button 
          variant={selectedLanguage === '' ? "secondary" : "outline"}
          size="sm"
          className="rounded-full"
          onClick={() => setSelectedLanguage('')}
        >
          Все
        </Button>
        {languages.map(lang => (
          <Button
            key={lang}
            variant={selectedLanguage === lang ? "secondary" : "outline"}
            size="sm"
            className="rounded-full"
            onClick={() => setSelectedLanguage(lang)}
          >
            {lang}
          </Button>
        ))}
      </div>

      {filteredPosts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPosts.map((post) => (
            <CodeCard key={post.id} post={post} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-xl mb-2">Публикации не найдены</p>
          <p className="text-muted-foreground">
            Попробуйте изменить поисковый запрос или фильтры
          </p>
        </div>
      )}
    </div>
  );
};

export default BrowsePage;
