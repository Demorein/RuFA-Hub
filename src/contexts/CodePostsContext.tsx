
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from './AuthContext';
import { toast } from 'sonner';

export type CodePost = {
  id: string;
  title: string;
  description: string;
  code: string;
  language: string;
  authorId: string;
  authorUsername: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
  likes: number;
  downloads: number;
};

type CodePostsContextType = {
  posts: CodePost[];
  isLoading: boolean;
  createPost: (post: Omit<CodePost, 'id' | 'authorId' | 'authorUsername' | 'createdAt' | 'updatedAt' | 'likes' | 'downloads'>) => Promise<CodePost>;
  updatePost: (id: string, updatedData: Partial<Omit<CodePost, 'id' | 'authorId' | 'authorUsername' | 'createdAt' | 'updatedAt'>>) => Promise<CodePost>;
  deletePost: (id: string) => Promise<void>;
  getPostById: (id: string) => CodePost | undefined;
  getUserPosts: () => CodePost[];
  searchPosts: (query: string) => CodePost[];
};

const POSTS_STORAGE_KEY = 'code_vault_posts';

const CodePostsContext = createContext<CodePostsContextType | undefined>(undefined);

export const CodePostsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [posts, setPosts] = useState<CodePost[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();

  // Загружаем посты при инициализации
  useEffect(() => {
    const storedPosts = localStorage.getItem(POSTS_STORAGE_KEY);
    if (storedPosts) {
      try {
        setPosts(JSON.parse(storedPosts));
      } catch (error) {
        console.error('Failed to parse stored posts', error);
      }
    }
    setIsLoading(false);
  }, []);

  // Сохраняем посты при изменении
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem(POSTS_STORAGE_KEY, JSON.stringify(posts));
    }
  }, [posts, isLoading]);

  const createPost = async (postData: Omit<CodePost, 'id' | 'authorId' | 'authorUsername' | 'createdAt' | 'updatedAt' | 'likes' | 'downloads'>): Promise<CodePost> => {
    if (!user) throw new Error('Необходимо авторизоваться для создания публикации');

    const now = new Date().toISOString();
    const newPost: CodePost = {
      id: `post-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      ...postData,
      authorId: user.id,
      authorUsername: user.username,
      createdAt: now,
      updatedAt: now,
      likes: 0,
      downloads: 0,
    };

    setPosts(prevPosts => [...prevPosts, newPost]);
    toast.success('Публикация успешно создана!');
    return newPost;
  };

  const updatePost = async (id: string, updatedData: Partial<Omit<CodePost, 'id' | 'authorId' | 'authorUsername' | 'createdAt' | 'updatedAt'>>): Promise<CodePost> => {
    if (!user) throw new Error('Необходимо авторизоваться для обновления публикации');

    const postIndex = posts.findIndex(post => post.id === id);
    if (postIndex === -1) throw new Error('Публикация не найдена');

    const post = posts[postIndex];
    if (post.authorId !== user.id) throw new Error('Вы можете редактировать только свои публикации');

    const updatedPost: CodePost = {
      ...post,
      ...updatedData,
      updatedAt: new Date().toISOString(),
    };

    const newPosts = [...posts];
    newPosts[postIndex] = updatedPost;
    setPosts(newPosts);

    toast.success('Публикация обновлена!');
    return updatedPost;
  };

  const deletePost = async (id: string): Promise<void> => {
    if (!user) throw new Error('Необходимо авторизоваться для удаления публикации');

    const post = posts.find(post => post.id === id);
    if (!post) throw new Error('Публикация не найдена');
    if (post.authorId !== user.id) throw new Error('Вы можете удалять только свои публикации');

    setPosts(prevPosts => prevPosts.filter(post => post.id !== id));
    toast.success('Публикация удалена!');
  };

  const getPostById = (id: string): CodePost | undefined => {
    return posts.find(post => post.id === id);
  };

  const getUserPosts = (): CodePost[] => {
    if (!user) return [];
    return posts.filter(post => post.authorId === user.id);
  };

  const searchPosts = (query: string): CodePost[] => {
    if (!query) return posts;
    
    const lowerCaseQuery = query.toLowerCase();
    return posts.filter(post => 
      post.title.toLowerCase().includes(lowerCaseQuery) ||
      post.description.toLowerCase().includes(lowerCaseQuery) ||
      post.tags.some(tag => tag.toLowerCase().includes(lowerCaseQuery))
    );
  };

  return (
    <CodePostsContext.Provider 
      value={{
        posts,
        isLoading,
        createPost,
        updatePost,
        deletePost,
        getPostById,
        getUserPosts,
        searchPosts,
      }}
    >
      {children}
    </CodePostsContext.Provider>
  );
};

export const useCodePosts = (): CodePostsContextType => {
  const context = useContext(CodePostsContext);
  if (context === undefined) {
    throw new Error('useCodePosts должен использоваться внутри CodePostsProvider');
  }
  return context;
};
