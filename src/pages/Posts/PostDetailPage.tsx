
import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useCodePosts, CodePost } from '@/contexts/CodePostsContext';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Download, Heart, Edit, Trash } from 'lucide-react';
import CodeViewer from '@/components/Code/CodeViewer';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { toast } from 'sonner';

const PostDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getPostById, deletePost } = useCodePosts();
  const { user } = useAuth();
  const [post, setPost] = useState<CodePost | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (id) {
      const foundPost = getPostById(id);
      if (foundPost) {
        setPost(foundPost);
      }
      setIsLoading(false);
    }
  }, [id, getPostById]);

  const handleDownload = () => {
    if (!post) return;

    // Создаем текстовый файл с кодом
    const blob = new Blob([post.code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    // Создаем элемент для скачивания
    const a = document.createElement('a');
    a.href = url;
    a.download = `${post.title}.${getFileExtension(post.language)}`;
    document.body.appendChild(a);
    a.click();
    
    // Очищаем
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success('Код скачан!');
  };

  const getFileExtension = (language: string): string => {
    const extensions: Record<string, string> = {
      'JavaScript': 'js',
      'TypeScript': 'ts',
      'Python': 'py',
      'Java': 'java',
      'C#': 'cs',
      'C++': 'cpp',
      'C': 'c',
      'PHP': 'php',
      'Ruby': 'rb',
      'Go': 'go',
      'Rust': 'rs',
      'HTML': 'html',
      'CSS': 'css',
      'Kotlin': 'kt',
      'Swift': 'swift',
    };
    
    return extensions[language] || 'txt';
  };

  const handleDelete = async () => {
    if (!post || !id) return;
    
    try {
      await deletePost(id);
      toast.success('Публикация удалена');
      navigate('/browse');
    } catch (error) {
      toast.error('Ошибка при удалении публикации');
      console.error('Error deleting post:', error);
    }
  };

  const isAuthor = user && post && user.id === post.authorId;

  if (isLoading) {
    return <div className="text-center py-12">Загрузка публикации...</div>;
  }

  if (!post) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Публикация не найдена</h1>
        <Link to="/browse">
          <Button>Вернуться к обзору</Button>
        </Link>
      </div>
    );
  }

  const formattedDate = new Date(post.createdAt).toLocaleDateString();

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <Link to="/browse">
            <Button variant="link" className="px-0 mb-2">← Назад к обзору</Button>
          </Link>
          <h1 className="text-3xl font-bold">{post.title}</h1>
          <div className="text-muted-foreground mt-2">
            Опубликовано {post.authorUsername} • {formattedDate}
          </div>
        </div>
        
        {isAuthor && (
          <div className="flex gap-2">
            <Link to={`/edit/${post.id}`}>
              <Button variant="outline" size="sm">
                <Edit className="h-4 w-4 mr-1" />
                Редактировать
              </Button>
            </Link>
            
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive" size="sm">
                  <Trash className="h-4 w-4 mr-1" />
                  Удалить
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Вы уверены?</AlertDialogTitle>
                  <AlertDialogDescription>
                    Это действие нельзя отменить. Публикация будет удалена навсегда.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Отмена</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete}>
                    Удалить
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {post.tags.map((tag, index) => (
          <Badge key={index} variant="outline">{tag}</Badge>
        ))}
      </div>

      <div className="bg-muted p-4 rounded-lg">
        <h2 className="text-lg font-medium mb-2">Описание</h2>
        <p>{post.description}</p>
      </div>

      <div>
        <h2 className="text-lg font-medium mb-2">Код</h2>
        <CodeViewer code={post.code} language={post.language} />
      </div>

      <div className="flex items-center justify-between pt-4">
        <div className="flex gap-4 items-center">
          <Button variant="outline" size="sm">
            <Heart className="h-4 w-4 mr-1" />
            <span>Нравится ({post.likes})</span>
          </Button>
          
          <Button variant="outline" size="sm" onClick={handleDownload}>
            <Download className="h-4 w-4 mr-1" />
            <span>Скачать ({post.downloads})</span>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PostDetailPage;
