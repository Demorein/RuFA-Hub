
import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useCodePosts } from '@/contexts/CodePostsContext';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import CodeCard from '@/components/Code/CodeCard';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const ProfilePage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const { getUserPosts } = useCodePosts();
  const navigate = useNavigate();
  
  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const userPosts = getUserPosts();

  if (!user) {
    return null; // Редирект уже должен был произойти
  }

  // Получаем инициалы пользователя для аватара
  const getInitials = (username: string) => {
    return username.substring(0, 2).toUpperCase();
  };

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>Профиль пользователя</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-6 items-center md:items-start">
            <Avatar className="h-24 w-24">
              <AvatarFallback className="text-2xl">
                {getInitials(user.username)}
              </AvatarFallback>
            </Avatar>
            
            <div className="space-y-2 text-center md:text-left">
              <h1 className="text-3xl font-bold">{user.username}</h1>
              <p className="text-muted-foreground">{user.email}</p>
              
              <div className="flex gap-4 mt-4 justify-center md:justify-start">
                <Button variant="outline">Изменить профиль</Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="posts">
        <TabsList>
          <TabsTrigger value="posts">Мои публикации ({userPosts.length})</TabsTrigger>
        </TabsList>
        
        <TabsContent value="posts" className="mt-6">
          {userPosts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {userPosts.map((post) => (
                <CodeCard key={post.id} post={post} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-muted rounded-lg">
              <p className="text-xl font-medium mb-2">У вас пока нет публикаций</p>
              <p className="text-muted-foreground mb-6">
                Поделитесь своим первым кодом с сообществом
              </p>
              <Button onClick={() => navigate('/create')}>
                Создать публикацию
              </Button>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProfilePage;
