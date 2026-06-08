import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store/authStore";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";

function PrivateRoute({ children }: { children: React.ReactNode }) {
    const token = useAuthStore((s) => s.token);
    return token ? <>{children}</> : <Navigate to="/login" replace />;
}

function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <main>{children}</main>
        </div>
    );
}

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route
                    path="/profile"
                    element={
                        <PrivateRoute>
                            <Layout><ProfilePage /></Layout>
                        </PrivateRoute>
                    }
                />
                <Route
                    path="/menu"
                    element={
                        <PrivateRoute>
                            <Layout>
                                <div className="max-w-2xl mx-auto py-8 px-4">
                                    <h1 className="text-2xl font-bold mb-2">Генератор меню</h1>
                                    <p className="text-gray-500">Модуль генерації меню в розробці.</p>
                                </div>
                            </Layout>
                        </PrivateRoute>
                    }
                />
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        </BrowserRouter>
    );
}
