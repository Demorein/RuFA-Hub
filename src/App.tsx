
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { CodePostsProvider } from "./contexts/CodePostsContext";
import Layout from "./components/Layout/Layout";
import HomePage from "./pages/Home/HomePage";
import BrowsePage from "./pages/Browse/BrowsePage";
import PostDetailPage from "./pages/Posts/PostDetailPage";
import CreatePostPage from "./pages/Posts/CreatePostPage";
import EditPostPage from "./pages/Posts/EditPostPage";
import LoginPage from "./pages/Auth/LoginPage";
import RegisterPage from "./pages/Auth/RegisterPage";
import ProfilePage from "./pages/Profile/ProfilePage";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <CodePostsProvider>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Layout><HomePage /></Layout>} />
              <Route path="/browse" element={<Layout><BrowsePage /></Layout>} />
              <Route path="/posts/:id" element={<Layout><PostDetailPage /></Layout>} />
              <Route path="/create" element={<Layout><CreatePostPage /></Layout>} />
              <Route path="/edit/:id" element={<Layout><EditPostPage /></Layout>} />
              <Route path="/login" element={<Layout><LoginPage /></Layout>} />
              <Route path="/register" element={<Layout><RegisterPage /></Layout>} />
              <Route path="/profile" element={<Layout><ProfilePage /></Layout>} />
              <Route path="*" element={<Layout><NotFound /></Layout>} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </CodePostsProvider>
    </AuthProvider>
  </QueryClientProvider>
);

export default App;
