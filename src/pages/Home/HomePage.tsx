
import React from 'react';
import { useCodePosts } from '@/contexts/CodePostsContext';
import CodeCard from '@/components/Code/CodeCard';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';

const HomePage: React.FC = () => {
  const { posts } = useCodePosts();
  const { isAuthenticated } = useAuth();
  
  // Получаем последние 6 постов для отображения на главной
  const latestPosts = [...posts]
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
    .slice(0, 6);

  return (
    <div className="space-y-10">
      <section className="py-12 bg-muted rounded-lg text-center">
        <h1 className="text-4xl font-bold mb-4">
          Добро пожаловать в Code Vault
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
          Ваша платформа для хранения, обмена и поиска кода и программ
        </p>
        <div className="flex gap-4 justify-center">
          {isAuthenticated ? (
            <Link to="/create">
              <Button size="lg">Поделиться кодом</Button>
            </Link>
          ) : (
            <>
              <Link to="/register">
                <Button size="lg">Начать бесплатно</Button>
              </Link>
              <Link to="/browse">
                <Button variant="outline" size="lg">Смотреть код</Button>
              </Link>
            </>
          )}
        </div>
      </section>

      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold">Последние публикации</h2>
          <Link to="/browse">
            <Button variant="link">Смотреть все</Button>
          </Link>
        </div>
        
        {latestPosts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {latestPosts.map((post) => (
              <CodeCard key={post.id} post={post} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground mb-4">
              Пока нет публикаций. Будьте первым, кто поделится кодом!
            </p>
            {isAuthenticated && (
              <Link to="/create">
                <Button>Создать публикацию</Button>
              </Link>
            )}
          </div>
        )}
      </section>

      <section className="bg-muted rounded-lg p-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-semibold mb-4">Преимущества Code Vault</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="p-4">
              <h3 className="text-lg font-medium mb-2">Делитесь кодом</h3>
              <p className="text-muted-foreground">Публикуйте свой код для других разработчиков</p>
            </div>
            <div className="p-4">
              <h3 className="text-lg font-medium mb-2">Находите решения</h3>
              <p className="text-muted-foreground">Ищите и используйте готовые решения для своих проектов</p>
            </div>
            <div className="p-4">
              <h3 className="text-lg font-medium mb-2">Обратная связь</h3>
              <p className="text-muted-foreground">Получайте обратную связь от сообщества</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
