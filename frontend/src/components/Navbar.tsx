import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function Navbar() {
    const { user, logout } = useAuthStore();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <nav className="bg-primary shadow-md">
            <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
                <Link to="/menu" className="text-white font-bold text-xl tracking-tight">
                    SuperSportyk
                </Link>
                <div className="flex items-center gap-4">
                    <Link
                        to="/profile"
                        className={`text-sm font-medium px-2 py-1 rounded transition ${location.pathname === "/profile"
                            ? "bg-white text-primary"
                            : "text-white hover:bg-green-700"
                            }`}
                    >
                        Профіль
                    </Link>
                    {user && <span className="text-white text-sm">{user.username}</span>}
                    <button
                        onClick={handleLogout}
                        className="text-white border border-white text-sm px-3 py-1 rounded hover:bg-green-700 transition"
                    >
                        Вийти
                    </button>
                </div>
            </div>
        </nav>
    );
}
