
import React, { createContext, useState, useContext, useEffect } from 'react';
import { toast } from 'sonner';

type User = {
  id: string;
  username: string;
  email: string;
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Имитация базы данных пользователей для MVP
const USERS_STORAGE_KEY = 'code_vault_users';
const CURRENT_USER_KEY = 'code_vault_current_user';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Загружаем пользователя при инициализации
  useEffect(() => {
    const storedUser = localStorage.getItem(CURRENT_USER_KEY);
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
      } catch (error) {
        console.error('Failed to parse stored user', error);
        localStorage.removeItem(CURRENT_USER_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  // Функция для регистрации
  const register = async (username: string, email: string, password: string): Promise<void> => {
    setIsLoading(true);
    
    try {
      // Получаем существующих пользователей
      const existingUsersJson = localStorage.getItem(USERS_STORAGE_KEY);
      const existingUsers = existingUsersJson ? JSON.parse(existingUsersJson) : [];
      
      // Проверяем, существует ли уже пользователь с таким email
      if (existingUsers.some((u: User) => u.email === email)) {
        throw new Error('Пользователь с таким email уже существует');
      }
      
      // Создаем нового пользователя
      const newUser = {
        id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        username,
        email,
        password // В реальном приложении пароль хэшировался бы
      };
      
      // Добавляем пользователя в "базу данных"
      const updatedUsers = [...existingUsers, newUser];
      localStorage.setItem(USERS_STORAGE_KEY, JSON.stringify(updatedUsers));
      
      // Устанавливаем пользователя как текущего
      const { password: _, ...userWithoutPassword } = newUser;
      setUser(userWithoutPassword);
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(userWithoutPassword));
      
      toast.success('Регистрация успешна!');
    } catch (error) {
      console.error('Registration error:', error);
      toast.error(error instanceof Error ? error.message : 'Ошибка регистрации');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Функция для логина
  const login = async (email: string, password: string): Promise<void> => {
    setIsLoading(true);
    
    try {
      // Получаем пользователей
      const usersJson = localStorage.getItem(USERS_STORAGE_KEY);
      const users = usersJson ? JSON.parse(usersJson) : [];
      
      // Ищем пользователя
      const foundUser = users.find((u: any) => u.email === email && u.password === password);
      
      if (!foundUser) {
        throw new Error('Неверный email или пароль');
      }
      
      // Устанавливаем пользователя без пароля
      const { password: _, ...userWithoutPassword } = foundUser;
      setUser(userWithoutPassword);
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(userWithoutPassword));
      
      toast.success('Вход выполнен успешно!');
    } catch (error) {
      console.error('Login error:', error);
      toast.error(error instanceof Error ? error.message : 'Ошибка входа');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Функция для выхода
  const logout = (): void => {
    localStorage.removeItem(CURRENT_USER_KEY);
    setUser(null);
    toast.info('Вы вышли из системы');
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth должен использоваться внутри AuthProvider');
  }
  return context;
};
