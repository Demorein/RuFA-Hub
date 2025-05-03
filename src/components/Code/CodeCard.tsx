
import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Download, Heart, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';
import { CodePost } from '@/contexts/CodePostsContext';

interface CodeCardProps {
  post: CodePost;
}

const CodeCard: React.FC<CodeCardProps> = ({ post }) => {
  const formattedDate = new Date(post.createdAt).toLocaleDateString();
  
  // Ограничиваем описание для превью
  const truncateDescription = (text: string, maxLength: number = 100) => {
    if (text.length <= maxLength) return text;
    return `${text.substring(0, maxLength)}...`;
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-lg">
            <Link to={`/posts/${post.id}`} className="hover:underline hover:text-primary">
              {post.title}
            </Link>
          </CardTitle>
        </div>
        <div className="text-sm text-muted-foreground">
          Автор: {post.authorUsername} • {formattedDate}
        </div>
      </CardHeader>
      <CardContent className="flex-grow">
        <p className="mb-4 text-sm">{truncateDescription(post.description)}</p>
        <div className="flex flex-wrap gap-1">
          {post.tags.map((tag, index) => (
            <Badge key={index} variant="outline">{tag}</Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="flex justify-between items-center border-t pt-4">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1 text-sm">
            <Eye className="h-4 w-4" />
            <span>42</span>
          </span>
          <span className="flex items-center gap-1 text-sm">
            <Heart className="h-4 w-4" />
            <span>{post.likes}</span>
          </span>
          <span className="flex items-center gap-1 text-sm">
            <Download className="h-4 w-4" />
            <span>{post.downloads}</span>
          </span>
        </div>
        <Link to={`/posts/${post.id}`}>
          <Button variant="outline" size="sm">Подробнее</Button>
        </Link>
      </CardFooter>
    </Card>
  );
};

export default CodeCard;
